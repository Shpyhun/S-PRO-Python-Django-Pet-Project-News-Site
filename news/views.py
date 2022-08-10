from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from news.forms import AddNewsForm, CommentForm
from news.models import News, Comment, Category
from news.utils import DataMixin

menu = [{'title': 'Add news', 'url_name': 'add_news'},
        {'title': 'Weather', 'url_name': 'weather'},
        ]


class NewsView(ListView):
    template_name = 'news/news_list.html'
    context_object_name = 'news'

    def get(self, request):
        news = News.objects.all().filter(is_published=True)
        paginator = Paginator(news, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        if search := request.GET.get('search'):
            page_obj = news.filter(title__icontains=search)
        context = {
            'menu': menu,
            'title': 'News',
            'news': page_obj,
            'categories_selected': 0,
        }
        return render(request, 'news/news_list.html', context=context)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="News")
        return dict(list(context.items()) + list(c_def.items()))


class NewsDetail(DetailView):
    slug_url_kwarg = 'news_slug'
    context_object_name = 'news'

    def get(self, request, news_slug):
        news = get_object_or_404(News, slug=news_slug)
        comments = Comment.objects.filter(news=news)
        form = CommentForm()
        total_likes = news.total_likes()
        liked = news.likes.filter(id=self.request.user.id).exists()
        # if news.likes.filter(id=self.request.user.id).exists():
        #     liked = True

        context = {
            'menu': menu,
            'news': news,
            'title': 'News',
            'total_likes': total_likes,
            'liked': liked,
            'comment_form': form,
            'comments': comments,
        }
        return render(request, 'news/news_detail.html', context=context)

    def post(self, request, news_slug):
        # news = News.objects.all().order_by('-id')
        news = get_object_or_404(News, slug=news_slug)
        comments = Comment.objects.filter(news=news)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.news = news
            comment.save()
        form = CommentForm()
        total_likes = news.total_likes()
        liked = False
        if news.likes.filter(id=self.request.user.id).exists():
            liked = True
        context = {
            'menu': menu,
            'news': news,
            'title': 'News',
            'total_likes': total_likes,
            'liked': liked,
            'comment_form': form,
            'comments': comments,
        }
        return render(request, 'news/news_detail.html', context=context)


# def news_detail(request, news_slug):
#     news = get_object_or_404(News, slug=news_slug)
#     comments = Comment.objects.filter(news=news)
#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.user = request.user
#             comment.news = news
#             comment.save()
#     else:
#         form = CommentForm()
#     context = {
#         'menu': menu,
#         'news': news,
#         'title': 'Add news',
#         'comment_form': form,
#         'comments': comments,
#         'categories_selected': news.category_id,
#     }
#     return render(request, 'news/news_detail.html', context=context)

class AddNewsView(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddNewsForm
    template_name = 'news/add_news.html'
    success_url = reverse_lazy('news_list')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Add news")
        return dict(list(context.items()) + list(c_def.items()))


class CategoryView(DataMixin, ListView):
    context_object_name = 'news'
    allow_empty = False

    def get(self, request, category_slug):
        news = News.objects.filter(category__slug=category_slug)
        categories = Category.objects.all()
        # if len(news) == 0:
        #     raise Http404()
        context = {
            'menu': menu,
            'news': news,
            'title': 'View by topic',
            'categories': categories,
            'categories_selected': category_slug,
        }
        return render(request, 'news/news_list.html', context=context)

    # def get_queryset(self):
    #     return News.objects.filter(category__slug=self.kwargs['category_slug'])

def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Sorry. Page not found</h1>')