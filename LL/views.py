from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import *
from easy_thumbnails.files import get_thumbnailer


# Create your views here.

def landing(request):
    return render(request, 'base.html')


def works_list(request):
    works = Post.objects.all()
    return render(request, 'list_of_works.html', context={'posts': works})


def work_detail(request, slug):
    post = get_object_or_404(Post, slug__iexact=slug)

    return render(request, 'work_detail.html', context={'post': post})
