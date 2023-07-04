from django.shortcuts import render
from django.views import generic
from django.utils import timezone
from django.shortcuts import get_object_or_404,redirect


from .models import *

# Create your views here.
class ListView(generic.ListView):
    model = Post
    paginate_by = 10
    
    def get_queryset(self):
        
        posts = Post.objects.filter(blog_start_dt__lte=timezone.now(),blog=True,)
        cat_slug = self.kwargs.get('slug')
        if cat_slug:
            cat = Category.objects.get(slug=cat_slug)
            print (cat)
            posts = posts.filter(category=cat)
        else:
            cat_ex = Category.objects.filter(category__startswith='_')
            posts = posts.exclude(category__in=cat_ex)

        self.request.session['category'] = cat_slug

        return posts.order_by('-blog_start_dt')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['post'] = context['post_list'] and context['post_list'][0]
        context['categories'] = Category.objects.all().order_by('id')

        page = int(self.request.GET.get('page',1))

        n = 0
        for p in context['post_list']:
            if n>0 or page>1:
                #print(p.text)
                pics = re.finditer(r'\!\[\]\(',p.text)

                pos = [pic.start() for pic in pics]

                print(p.slug,pos)

                if len(pos)>1 and pos[0]<100:
                    p.text = p.text[0:pos[1]]
                    p.read_more = True
                
                elif len(pos)>0 and pos[0]>=100:
                    p.text = p.text[0:pos[0]]
                    p.read_more = True

                else:
                    crs = re.finditer(r'\n',p.text)    
                    pos = [cr.start() for cr in crs]
                    if len(pos)>3:
                        p.text = p.text[0:pos[3]]
                        p.read_more = True

            n += 1

        if context['post']:
            context['breadcrumb'] = re.sub(r'[^\x00-\x7F]',' ', context['post'].title)
            context['page_title'] = context['breadcrumb']
        return context     

class HomeView(generic.ListView):
    model = Post
    paginate_by = 20
    template_name = "blog/post_home.html"

    
    def get_queryset(self):
        
        posts = Post.objects.filter(blog_start_dt__lte=timezone.now(),blog=True,).order_by('-blog_start_dt')
        cat_slug = self.kwargs.get('slug')
        self.request.session['category'] = cat_slug

        if cat_slug:
            self.home = False
            cat = Category.objects.get(slug=cat_slug)
            self.cat = cat
            posts = posts.filter(category=cat)
            return posts
        else:
            self.home = True
            self.cat = None
            cat_ex = Category.objects.filter(category__startswith='_')
            posts = posts.exclude(category__in=cat_ex).order_by('-blog_start_dt')[:4]

            self.shown = []
            for p in posts:
                print (p.id)
                self.shown.append(p.id)

            return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['post'] = context['post_list'] and context['post_list'][0]
        context['categories'] = Category.objects.all().order_by('id')

        page = int(self.request.GET.get('page',1))


        if self.home:
            context['breadcrumb'] = 'Home'
        else:
            context['breadcrumb'] = self.cat.category

        context['page_title'] = context['breadcrumb']

        return context                

class PostView(generic.DetailView):
    model = Post

    def get_object(self, queryset=None):
        post = get_object_or_404(Post, slug=self.kwargs['slug'])
        lang = self.kwargs.get('lang')

        if not lang or lang == 'en':
            post.lang = lang
            return post

        #post_lang = get_object_or_404(PostLang, post=post, lang_iso_code=lang)
        try:
            post_lang = PostLang.objects.get(post=post, lang_iso_code=lang)
        except PostLang.DoesNotExist:
            post.lang = lang
            return post

        if post_lang.title: post.title = post_lang.title
        if post_lang.email_subject: post.email_subject = post_lang.email_subject
        if post_lang.text: post.text = post_lang.text

        post.lang = lang

        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = re.sub(r'[^\x00-\x7F]',' ', context['post'].title)
        context['categories'] = Category.objects.all().order_by('id')

        this_dt = context['post'].blog_start_dt

        if this_dt:
            cat_slug = self.request.session.get('category')
            cat = None
            if cat_slug:
                cat = Category.objects.get(slug=cat_slug)
            
                next = Post.objects.filter(
                    blog_start_dt__lte=timezone.now(),blog=True,blog_start_dt__gt=this_dt,category=cat
                ).order_by('blog_start_dt')[:1]

                prev = Post.objects.filter(
                    blog_start_dt__lte=timezone.now(),blog=True,blog_start_dt__lt=this_dt,category=cat
                ).order_by('-blog_start_dt')[:1]

            else:
                next = Post.objects.filter(
                    blog_start_dt__lte=timezone.now(),blog=True,blog_start_dt__gt=this_dt,
                ).order_by('blog_start_dt')[:1]

                prev = Post.objects.filter(
                    blog_start_dt__lte=timezone.now(),blog=True,blog_start_dt__lt=this_dt,
                ).order_by('-blog_start_dt')[:1]

            if len(next): 
                context['next'] = next[0].slug
            if len(prev): 
                context['prev'] = prev[0].slug

        context['post'].text = context['post'].text.replace('<referral_url>','')
        context['post'].text = context['post'].text.replace('<firstname>','')
        context['post'].text = context['post'].text.replace('<!-- Hi Firstname -->','')

        return context        
