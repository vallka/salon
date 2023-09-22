from django.db import models

# Create your models here.
class Category(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True,default='',null=True)
    position = models.IntegerField(default=0)
    active = models.BooleanField(default=1)

    def show_groups(self):
        groups = Group.objects.filter(category=self).order_by('position')
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

    def show(self):
        view_pics = f'<a href="{self.photo_page}">photos »</a>' if self.photo_page else ''
        str = f'''<div class="fresha_name">{self.name}</div>
<div class="fresha_description">{self.description if self.description else ""} {view_pics}</div>
'''
        str += self.show_items()
        return str

    def show_items(self):
        str = ''
        items = Item.objects.filter(group=self).order_by('position')
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
        return str(self.name) + '-' + str(self.caption)
