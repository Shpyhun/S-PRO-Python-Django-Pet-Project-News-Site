from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView

from news.forms import AddNewsForm, CommentForm
from news.models import *
from .utils import *

menu = [{'title': 'Add news', 'url_name': 'add_news'},
        {'title': 'Weather', 'url_name': 'weather'}
        ]


class NewsView(View):
    def post(self, request):
        form = AddNewsForm(request.POST)
        if form.is_valid():
            form.save()
        news = News.objects.all().order_by('-id')
        context = {
            'menu': menu,
            'news': news,
            'post_form': AddNewsForm,
            'title': 'News',
            'categories_selected': 0,
        }
        return render(request, 'news/news_list.html', context=context)

    def get(self, request):
        news = News.objects.all().order_by('-id')
        if request.method == "GET" and 'qwerty' in request.GET:
            qwerty = request.GET['qwerty']
            news = news.filter(title__icontains=qwerty)
        context = {
            'menu': menu,
            'news': news,
            'post_form': AddNewsForm,
            'title': 'News',
            'categories_selected': 0,
        }
        return render(request, 'news/news_list.html', context=context)


def news_detail(request, news_slug):
    news = get_object_or_404(News, slug=news_slug)
    comments = Comment.objects.filter(news=news)
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
        'menu': menu,
        'news': news,
        'title': 'Add news',
        'comment_form': form,
        'comments': comments,
        'categories_selected': news.category_id,
    }
    return render(request, 'news/news_detail.html', context=context)


class AddNewsView(LoginRequiredMixin, View):
    def post(self, request):
        form = AddNewsForm(request.POST, request.FILES  )
        if form.is_valid():
            form.save()
            news = News.objects.all().order_by('-id')
        context = {
            'menu': menu,
            'news': news,
            'title': 'Add news',
            'post_form': AddNewsForm}
        return render(request, 'news/add_news.html', context=context)

    def get(self, request):
        news = News.objects.all().order_by('-id')
        if request.method == "GET" and 'qwerty' in request.GET:
            qwerty = request.GET['qwerty']
            news = news.filter(title__icontains=qwerty)
        context = {
            'menu': menu,
            'news': news,
            'title': 'Add news',
            'post_form': AddNewsForm}
        return render(request, 'news/add_news.html', context=context)


class ViewCategory(ListView):
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news'
    allow_empty = False

    def get_queryset(self):
        return News.objects.filter(category__slug=self.kwargs['category_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Category - ' + str(context['news'][0].category),
                                      category_selected=context['news'][0].category_id)
        return dict(list(context.items()) + list(c_def.items()))


def view_category(request, category_slug):
    news = News.objects.filter(slug=category_slug)
    categories = Category.objects.all()

    # if len(news) == 0:
    #     raise Http404()

    context = {
        'menu': menu,
        'title': 'View by topic',
        'categories': categories,
        'categories_selected': category_slug,
    }

    return render(request, 'news/news_list.html', context=context)


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Sorry. Page not found</h1>')