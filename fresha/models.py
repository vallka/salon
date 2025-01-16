import re
import requests

from django.db import models
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify


# Create your models here.
class Category(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True,default='',null=True)
    position = models.IntegerField(default=0)
    active = models.BooleanField(default=1)

    def show_groups(self):
        groups = Group.objects.filter(category=self,active=True).order_by('position')
        str = ''
        for g in groups:
            str += g.show()

        return str

    def __str__(self):
        return str(self.name)


class Group(models.Model):
    id = models.BigIntegerField(primary_key=True)
    category = models.ForeignKey(Category,on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True,default='',null=True)
    position = models.IntegerField(default=0)
    active = models.BooleanField(default=1)
    photo_page = models.CharField(max_length=255,blank=True,default='')
    extra_text = MarkdownxField(blank=True, null=False,default='')

    @property
    def first_image(self):
        img = re.search(r'\!\[\]\(([^)]+)\)',self.extra_text)
        if img and img.group(1):
            return img.group(1)
        else:
            return None
        
    @property
    def last_image(self):
        all_images = re.findall(r'\!\[\]\(([^)]+)\)', self.extra_text)
        if all_images:
            return all_images[-1]
        else:
            return '/static/images/nail-svg.png'

    def show(self):
        a_fresha_img = 'a_fresha_extra' if self.extra_text else ''
        extra_text = f'<div class="extra_text" style="display:none">{markdownify(self.extra_text)}</div>' if self.extra_text else ''
        view_pics = f'<a href="#" class="a_fresha_extra">photos »</a>' if self.extra_text else ''
        last_img = f'<div class="fresha_img {a_fresha_img}"><img src="{self.last_image}"></div>' if self.last_image else ''
        str = f'''<div class="fresha_name">{self.name}</div>
{last_img}
<div class="fresha_description">{self.description if self.description else ""}</div>
{view_pics}
{extra_text}
<div style="clear:both"></div>
'''
        str += self.show_items()
        return f'<div class="fresha_group">{str}</div><div style="clear:both"></div>'

    def show_items(self):
        str = ''
        items = Item.objects.filter(group=self,active=True).order_by('position')
        for i in items:
            str += i.show()
        return str

    def __str__(self):
        return str(self.name)
        
class Item(models.Model):
    str_id = models.CharField(max_length=25,default='sv',primary_key=True)
    group = models.ForeignKey(Group,on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True,default='',null=True)
    position = models.IntegerField(default=0)
    active = models.BooleanField(default=1)
    price = models.FloatField(default=0)
    duration = models.IntegerField(default=0)
    caption = models.CharField(max_length=255,blank=True,default='',null=True)

    @property
    def full_name(self):
        return re.sub(r'\s+', ' ', self.name + (' - ' + self.caption if self.caption else '')).strip()
    

    @property
    def duration_h(self):
        total_mins = self.duration // 60
        hrs = total_mins // 60
        mins = total_mins % 60

        if hrs and mins:
            return f"{hrs}h {mins}min"
        elif hrs:
            return f"{hrs}h"
        else:
            return f"{mins}min"

    def show(self):
        link = f'https://www.fresha.com/book-now/gellifique-nail-bar-wq7vlwkv/services?lid=805208&oiid={self.str_id}&pId=756682'
        str = f'''<div class="row fresha_item align-items-center"><div class="col-6">
<div class="fresha_caption">{self.caption if self.caption else ""}</div>
<div class="fresha_price">from £{self.price} - {self.duration_h}</div>
</div>
<div class="fresha_book col-6"><a href="{link}">BOOK NOW</a></div>
</div>
'''
        return str


    def __str__(self):
        return self.full_name

    @classmethod
    def populate_all(cls):
        print ('populate_all')

        r=requests.get('https://api.fresha.com/locations/805208/marketplace-offer?context=booking-flow')

        data=r.json()['data']
        included=r.json()['included']


        categories = []
        groups = []
        items = []

        #"""
        for i in included:
            if i['type']=='offer-item-categories':
                print(i['type'], i['id'], i['attributes']['name'],i['attributes']['position'])
                try:
                    category = Category.objects.get(id=i['id'])
                    category.name=i['attributes']['name']
                    category.description=i['attributes']['description']
                    category.position=i['attributes']['position']
                except Category.DoesNotExist:
                    category = Category(id=i['id'],name=i['attributes']['name'],description=i['attributes']['description'],position=i['attributes']['position'])

                categories.append(i['id'])
                category.save()    

            elif i['type']=='offer-item-groups':
                print(i['type'], i['id'], i['attributes']['name'],i['attributes']['position'],i['relationships']['category']['data']['id'])
                id = i['id'][2:]
                i['attributes']['name'] = i['attributes']['name'].replace('( ','(').replace(' )',')').replace('  ',' ')
                try:
                    group = Group.objects.get(id=id)
                    group.name=i['attributes']['name']
                    group.description=i['attributes']['description']
                    group.position=i['attributes']['position']
                    group.category_id=i['relationships']['category']['data']['id']
                except Group.DoesNotExist:
                    group = Group(
                        id=id,
                        name=i['attributes']['name'],
                        description=i['attributes']['description'],
                        position=i['attributes']['position'],
                        category_id=i['relationships']['category']['data']['id']
                    )

                groups.append(id)
                group.save()
        #"""

        for d in data:
            print(d['id'],d['attributes']['name'],d['attributes']['position'],d['relationships']['item-group']['data']['id'],d['attributes']['retail-price'],d['attributes']['duration-for-customer-in-seconds'])
            d['attributes']['name'] = d['attributes']['name'].replace('( ','(').replace(' )',')').replace('  ',' ')
            try:
                item = Item.objects.get(str_id=d['id'])
                item.caption=d['attributes']['caption']
                item.name=d['attributes']['name']
                item.description=d['attributes']['description']
                item.position=d['attributes']['position']
                item.group_id=d['relationships']['item-group']['data']['id'][2:]
                item.price = d['attributes']['retail-price']
                item.duration = d['attributes']['duration-for-customer-in-seconds']
            except Item.DoesNotExist:
                item = Item(
                    str_id=d['id'],
                    caption=d['attributes']['caption'],
                    name=d['attributes']['name'],
                    description=d['attributes']['description'],
                    position=d['attributes']['position'],
                    group_id=d['relationships']['item-group']['data']['id'][2:],
                    price = d['attributes']['retail-price'],
                    duration = d['attributes']['duration-for-customer-in-seconds']
                )
            item.save()
            items.append(d['id'])


        print(categories)
        print(groups)
        print(items)

        Category.objects.exclude(id__in=categories).update(active=False)
        Group.objects.exclude(id__in=groups).update(active=False)
        Item.objects.exclude(str_id__in=items).update(active=False)
