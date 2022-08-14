from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, DetailView, ListView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import mixins, viewsets
from rest_framework.generics import RetrieveUpdateAPIView, RetrieveAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from accounts.models import User
from news.forms import AddNewsForm, CommentForm
from news.models import Comment, Category, News
from news.serializers import AddCommentSerializer, NewsSerializer, CategorySerializer, UserSerializer, \
    NewsDetailSerializer
from news.utils import DataMixin

menu = [{'title': 'Add news', 'url_name': 'add_news'},
        {'title': 'Weather', 'url_name': 'weather'},
        ]


class NewsView(View):
    template_name = 'news/news_list.html'
    context_object_name = 'news'

    def get(self, request):
        news = News.objects.all().filter(is_published=True).order_by('-id')
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
    context_object_name = 'news'

    def get(self, request, news_slug):
        news = get_object_or_404(News, slug=news_slug)
        comments = Comment.objects.filter(news=news)
        form = CommentForm()
        total_likes = news.likes.count()
        liked = news.likes.filter(id=self.request.user.id).exists()
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
        news = get_object_or_404(News, slug=news_slug)
        comments = Comment.objects.filter(news=news)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.news = news
            comment.save()
        form = CommentForm()

        total_likes = news.likes.count()
        liked = news.likes.filter(id=self.request.user.id).exists()
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
        context = {
            'menu': menu,
            'news': news,
            'title': 'View by topic',
            'categories': categories,
            'categories_selected': category_slug,
        }
        return render(request, 'news/news_list.html', context=context)

    def get_queryset(self):
        return News.objects.filter(category__slug=self.kwargs['category_slug'])


class LikeView(View):

    def post(self, request, pk):
        news = get_object_or_404(News, id=pk)
        if news.likes.filter(id=request.user.id).exists():
            news.likes.remove(request.user)
        else:
            news.likes.add(request.user)
        return HttpResponseRedirect(reverse('news_detail', args=[news.slug]))


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Sorry. Page not found</h1>')


class CreateCommentViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = AddCommentSerializer
    permission_classes = [IsAuthenticated]


class NewsViewSet(mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['user', 'category', 'time_update']
    search_fields = ['title']


class NewsDetailAPIView(RetrieveAPIView):
    queryset = News.objects.all()
    serializer_class = NewsDetailSerializer

    def get_object(self):
        """
        Returns the object the view is displaying.

        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
                'Expected view %s to be called with a URL keyword argument '
                'named "%s". Fix your URL conf, or set the `.lookup_field` '
                'attribute on the view correctly.' %
                (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    # def list(self, request):
    #     # Note the use of `get_queryset()` instead of `self.queryset`
    #     queryset = self.get_queryset()
    #     serializer = NewsDetailSerializer(queryset, many=True)
    #     return Response(serializer.data)
    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)

    # def get(self, request, *args, **kwargs):
    #     queryset = News.objects.get(id=self.request.news.id)
    #     serializer = NewsSerializer(queryset)
    #     return Response(serializer.data)

    # @action(methods=['post'], detail=True)  #permission_classes=[IsAuthenticated]
    # def get_mark_like(self, request, pk=None):
    #     news = self.get_object()
    #     if news.likes.filter(id=request.user.id).exists():
    #         news.likes.remove(request.user)
    #     else:
    #         news.likes.add(request.user)
    #     serializer = self.get_serializer(news)
    #     return Response(serializer.data)


# class TopNews(ListAPIView, ModelViewSet):
#     queryset = News.objects.all()
#     serializer_class = NewsSerializer
#
#     def get_queryset(self):
#         today = datetime.date.today()
#         week_ago = today - datetime.timedelta(days=2)
#         id_top_news = [i['news'] for i in
#                           list(Comment.objects.values('news').annotate(dcount=Count('news_id')))
#                           if i['dcount'] >= 10]
#         id_top_like = [i.id for i in News
#         queryset = News.objects.filter((Q(pk__in=id_top_news) | Q(pk__in=id_top_like) | Q(top_news=True)) &
#                                           Q(created_news__range=(week_ago, today)))
#
#         return queryset




class CategoryAPIView(mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class ProfileUpdate(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    def get_object(self):
        return self.get_queryset().get(id=self.request.user.id)

    #
    # def get_object(self, pk):
    #     try:
    #         return User.objects.get(pk=pk)
    #     except User.DoesNotExist:
    #         raise Http404

    # def get_profile(self, request, pk, format=None):
    #     snippet = self.get_object(pk)
    #     serializer = UserSerializer(snippet)
    #     return Response(serializer.data)

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     queryset = queryset.filter(user=self.request.user)
    #     return queryset





