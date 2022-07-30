from django.http import HttpResponseNotFound, Http404
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views import View

from news.forms import NewsForm, CommentForm
from news.models import Category, News, Profile, CommentNews


class NewsView(View):
    def post(self, request):
        form = NewsForm(request.POST)
        categories = Category.objects.all()
        if form.is_valid():
            form.save()
        news = News.objects.all().order_by('-id')
        context = {
            'news': news,
            'categories': categories,
            'post_form': NewsForm,
            'title': 'Home page',
            'categories_selected': 0,
        }
        return render(request, 'news/news_list.html', context=context)

    def get(self, request):
        news = News.objects.all().order_by('-id')
        categories = Category.objects.all()
        if request.method == "GET" and 'search' in request.GET:
            search = request.GET['search']
            news = news.filter(title__icontains=search)
        context = {
            'news': news,
            'categories': categories,
            'post_form': NewsForm,
            'title': 'Home page',
            'categories_selected': 0,
        }
        return render(request, 'news/news_list.html', context=context)


def news_detail(request, index):
    news = get_object_or_404(News, pk=index)
    comments = CommentNews.objects.filter(news=news)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.news = news
            comment.save()
    else:
        form = CommentForm()
    context = {
        'news': news,
        'rev_form': form,
        'comments': comments
    }
    return render(request, 'news/news_detail.html', context=context)


def user_info(request, user):
    user = get_object_or_404(Profile, pk=user)
    context = {'user': user}
    return render(request, 'news/profile.html', context=context)


def news_list_sorted(request, index):
    news = get_list_or_404(News, author=index)
    context = {'news': news}
    return render(request, 'news/news_list_sorted.html', context=context)


class AddNewsView(View):
    def post(self, request):
        form = NewsForm(request.POST)
        if form.is_valid():
            form.save()
            news = News.objects.all().order_by('-id')
        context = {'news': news, 'post_form': NewsForm}
        return render(request, 'news/add_news.html', context=context)

    def get(self, request):
        news = News.objects.all().order_by('-id')
        if request.method == "GET" and 'search' in request.GET:
            search = request.GET['search']
            news = news.filter(title__icontains=search)
        context = {'news': news, 'post_form': NewsForm}
        return render(request, 'news/add_news.html', context=context)


def view_category(request, category_id):
    news = News.objects.filter(category_id=category_id)
    categories = Category.objects.all()

    if len(news) == 0:
        raise Http404()

    context = {
        'news': news,
        'categories': categories,
        'categories_selected': category_id,
    }

    return render(request, 'news/news_list.html', context=context)


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Sorry. Page not found</h1>')