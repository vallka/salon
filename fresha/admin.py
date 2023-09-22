from django.contrib import admin
from fresha.models import Category,Group,Item

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'active', ]
    list_display_links = ['id', 'name', ]
    list_editable = ['active'] 

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'active', 'category']
    list_display_links = ['id', 'name', 'category']
    list_filter = ['active',  'category' ]
    list_editable = ['active'] 

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['str_id', 'name', 'active', 'group']
    list_display_links = ['str_id', 'name', 'group']
    list_filter = ['active',  'group' ]
    list_editable = ['active'] 
