from datetime import date
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Article
from . import forms
# from django.http import HttpResponse

from django.contrib.auth.decorators import login_required

# Create your views here.
def article_list(request):
    articles = Article.objects.all().order_by("date")
    return render(request, "articles/article_list.html", {'articles': articles})


def article_detail(request, slug):
    # return HttpResponse(slug)
    article = Article.objects.get(slug=slug)
    return render(request, "articles/article_detail.html", {'article':article})

#adding a decorator to allow only logged in users to access this page
@login_required(login_url="accounts:login")
def article_create(request):
    if request.method == 'POST':
        form = forms.CreateArticle(request.POST, request.FILES)
        if form.is_valid():
            #save article to db
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return redirect('articles:list')
    else:
        form = forms.CreateArticle()
    return render(request, "articles/article_create.html", {'form':form})