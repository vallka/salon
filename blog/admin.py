# Register your models here.
from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from markdownx.models import MarkdownxField
from django.db import models
from django.forms.widgets import Textarea
from django.utils import timezone
from django.urls import reverse
from django.utils.html import format_html

from .models import *

# Register your models here.
#admin.site.register(Post, MarkdownxModelAdmin)
admin.site.register(Category)
@admin.register(PostLang)
class PostLangAdmin(MarkdownxModelAdmin):
    list_display = ['post','lang_iso_code','title']
    list_display_links = ['post','title',]
    list_filter = ['post']
    
class PostLangInline(admin.TabularInline):
    model = PostLang
    fields = ['lang_iso_code','title','email_subject','edit_link']
    readonly_fields = ['lang_iso_code','title','email_subject','edit_link',]
    extra = 0
    
    def edit_link(self, obj):
        url = reverse('admin:blog_postlang_change', args=[obj.pk])
        return format_html('<a href="{}" target="_blank">Edit</a>', url)

    edit_link.short_description = 'Edit'


@admin.register(Post)
class PostAdmin(MarkdownxModelAdmin):
    list_display = ['id','slug','title','domain','blogged','f_blog_start_dt','newsletter','f_email_send_dt','formatted_created_dt']
    list_display_links = ['id','slug','title',]
    search_fields = ['title', ]
    list_filter = ['blog','email','domain']
    inlines = [PostLangInline]

    def formatted_created_dt(self, obj):
        return obj.created_dt.strftime("%d-%m-%Y %H:%M")
    formatted_created_dt.admin_order_field = 'created_dt'
    formatted_created_dt.short_description = 'Created dt'

    def f_blog_start_dt(self, obj):
        return obj.blog_start_dt.strftime("%d-%m-%Y %H:%M") if obj.blog_start_dt else ""
    f_blog_start_dt.admin_order_field = 'blog_start_dt'
    f_blog_start_dt.short_description = 'Published'

    def f_email_send_dt(self, obj):
        return obj.email_send_dt.strftime("%d-%m-%Y %H:%M") if obj.email_send_dt else ""
    f_email_send_dt.admin_order_field = 'email_send_dt'
    f_email_send_dt.short_description = 'Sent'

    def blogged(self,instance):
        return True if instance.blog and instance.blog_start_dt and instance.blog_start_dt<=timezone.now() else False
    
    blogged.boolean = True      
    blogged.short_description = 'Blog'

    def newsletter(self,instance):
        return True if instance.email and instance.email_send_dt and instance.email_send_dt<=timezone.now() else False
    
    newsletter.boolean = True      
    newsletter.short_description = 'News'

