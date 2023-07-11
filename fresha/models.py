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

class Group(models.Model):
    id = models.BigIntegerField(primary_key=True)
    category = models.ForeignKey(Category,on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True,default='',null=True)
    position = models.IntegerField(default=0)
    active = models.BooleanField(default=1)

    def show(self):
        str = f'<div class="fresha_name">{self.name}</div><div class="fresha_description">{self.description if self.description else ""}</div>'
        str += self.show_items()
        return str

    def show_items(self):
        str = ''
        items = Item.objects.filter(group=self).order_by('position')
        for i in items:
            str += i.show()
        return str

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
        str = f'''<div class="fresha_caption">{self.caption if self.caption else ""}</div>
<div class="fresha_duration">{self.duration_h}</div>
<div class="fresha_price">from £{self.price}</div>
<div class="fresha_book"><a href="{link}">BOOK NOW</a></div>
'''
        return str


