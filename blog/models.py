import re
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify


# Create your models here.
class Category(models.Model):
    class Meta:
        ordering = ['slug']

    category = models.CharField(_("Category"), blank=True, max_length=100, unique=True)
    slug = models.SlugField(_("Slug"), unique=True, max_length=100, blank=True, null=False)
    is_default = models.BooleanField(_("Default Category"),default=False)

    def __str__(self):
        return str(self.slug) + ' -- ' + str(self.category)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.category)
            
        super().save(*args, **kwargs)


class Post(models.Model):
    class Meta:
        ordering = ['-id']

    title = models.CharField(_("Title"), max_length=100, unique=False)
    slug = models.SlugField(_("Slug"), unique=True, max_length=100, blank=True, null=False)

    blog = models.BooleanField(_("Publish to blog"),default=False)
    blog_start_dt = models.DateTimeField(_("Published"), blank=True, null=True)
    email = models.BooleanField(_("Send as newsletter"),default=False)
    email_subject = models.CharField(_("Subject"), max_length=100, blank=True, null=False, default='')
    email_send_dt = models.DateTimeField(_("Sent"), blank=True, null=True)

    class EmailStatus(models.IntegerChoices):
        NONE = 0
        SENDING = 1
        SENT = 2

    email_status = models.IntegerField(default=EmailStatus.NONE,choices=EmailStatus.choices)

    class Domains(models.IntegerChoices):
        CO_UK = 1
        EU = 2

    domain = models.IntegerField(default=Domains.CO_UK,choices=Domains.choices)

    category = models.ManyToManyField(Category, )

    title_color = models.CharField(_("Title Color"),max_length=20, blank=True, null=False, default='#232323')
    title_bgcolor = models.CharField(_("Title Bg Color"),max_length=20, blank=True, null=False, default='#eeeeee')

    text = MarkdownxField(_("Text"), blank=True, null=False)

    created_dt = models.DateTimeField(_("Created Date/Time"), auto_now_add=True, null=True)
    updated_dt = models.DateTimeField(_("Updated Date/Time"), auto_now=True, null=True)

    description  = models.TextField(_("Meta Description"), blank=True, null=False, default='')
    keywords  = models.TextField(_("Meta Keywords"), blank=True, null=False, default='')
    json_ld  = models.TextField(_("script ld+json"), blank=True, null=False, default='')


    @property
    def formatted_markdown(self):
        text = re.sub('~~([^~]+)~~',r'<s>\1</s>',self.text) # not in standard extensions
        text = markdownify(text)
        text = text.replace('<img ','<img loading="lazy"')
        return text

    @property
    def plain_text(self):
        text = re.sub('~~([^~]+)~~',r'<s>\1</s>',self.text) # not in standard extensions
        md = markdownify(text)

        md = re.sub('<a[^>]+?>','',md)
        md = re.sub(r'</a>','',md)
        md = re.sub('<img[^>]+?>','',md)
        return md
        #return '<p>'.join(BeautifulSoup(md,features="html.parser").findAll(text=True))
        #return '<p>' + ''.join(BeautifulSoup(md,features="html.parser").findAll(text=True)) + '</p>'

    @property
    def first_image(self):
        img = re.search(r'\!\[\]\(([^)]+)\)',self.text)
        if img and img.group(1):
            return img.group(1)
        else:
            return None

    def __str__(self):
        return str(self.id) + ':'+ str(self.slug)

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.title)

            try:
                Post.objects.get(slug=slug)
                for i in range(1,1000):
                    try:
                        Post.objects.get(slug=slug+str(i))
                        continue
                    except Post.DoesNotExist:
                        slug = slug+str(i)
                        break

            except Post.DoesNotExist:
                None

            self.slug = slug

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return '/' + str(self.slug)        

class PostLang(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    lang_iso_code = models.CharField(_("Language ISO Code"), max_length=5)
    title = models.CharField(_("Title"), max_length=100, default='')
    email_subject = models.CharField(_("Subject"), max_length=100, blank=True, null=False, default='')
    text = models.TextField(_("Text"), blank=True, null=False, default='')
    description = models.TextField(_("Meta Description"), blank=True, null=False, default='')
    keywords  = models.TextField(_("Meta Keywords"), blank=True, null=False, default='')
    json_ld  = models.TextField(_("script ld+json"), blank=True, null=False, default='')
    class Meta:
        unique_together = ('post', 'lang_iso_code')



class AllLanguages:
    # needs to match table content: ps17_lang
    langs = ['','','pl','ro','uk','ru']

    @classmethod
    def getById(cls,id):
        return cls.langs[id]
