from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Blogs
from account.models import BloggerAccount
from django.http import HttpResponse, HttpResponseRedirect
# from datetime import date
import datetime
from .forms import add_blog

def getblogger(email):
    vendor = BloggerAccount.objects.get(email=email)
    return vendor

def getvendorbyBlogname(blogname):
    blogger = BloggerAccount.objects.get(blogname=blogname)
    return blogger

def blog(request,):
    blogs = Blogs.objects.all().order_by('-id')
    params = {'blogs': blogs}
    return render(request, "blog/blog.html", params)

def blogpost(request,id):
    blog = Blogs.objects.get(id=id)
    blogger = blog.blogger
    params = {'blog': blog, 'blogger': blogger}
    return render(request, "blog/post.html", params)

# ---------------------------------------------------------------------
# vendor related functions
# ---------------------------------------------------------------------

@login_required(login_url="../login")
def addblog(request):
    if request.user.is_Blogger:
        if request.method == 'POST':
            form = add_blog(request.POST, request.FILES)
            if form.is_valid():
                content = form.cleaned_data['content']
                image = form.cleaned_data['image']
                title = form.cleaned_data['title']
                blogger = getblogger(request.user.email)
                # pub_date = date.today()
                pub_date = datetime.datetime.now()
                cont = Blogs.objects.create(image=image, content=content, blogger=blogger, title=title, pub_date=pub_date)
                cont.save()
                msg="Blog Successfully Posted"
                return render(request, 'blog/addblog.html', {'form': form,"msg":msg})
        else:
            form = add_blog()
            msg=""
            return render(request, 'blog/addblog.html', {'form': form, "msg": msg})
    else:
        return render(request, "shop/unauthorized.html")

def viewblog(request,blogname):
    blogger = getvendorbyBlogname(blogname)
    template = blogger.template.split(",")
    style = template[1]
    template = "blog/theme/" + template[0] + "/bloggerindex.html"
    blogs = Blogs.objects.filter(blogger=blogger)
    params = {'blogs': blogs, 'blogger': blogger,"style":style}
    print(template)
    return render(request, template, params)

def bloggerblogpost(request,id):
    blog = Blogs.objects.get(id=id)
    blogger = blog.blogger
    style = blogger.template.split(",")[1]
    params = {'blog': blog, 'blogger': blogger, 'style':style}
    return render(request, "blog/theme/default/bloggerpost.html", params)


