from django.db.models import Count
from openid.yadis import services
from rest_framework.decorators import action
from rest_framework.response import Response

from news.models import Category

menu = [{'title': 'Add news', 'url_name': 'add_news'},
        {'title': 'Weather', 'url_name': 'weather'}
        ]


class DataMixin:
    paginate_by = 2

    def get_user_context(self, **kwargs):
        context = kwargs
        categories = Category.objects.annotate(Count('news'))
        context['menu'] = menu
        context['categories'] = categories
        if 'category_selected' not in context:
            context['category_selected'] = 0
        return context


class LikeMixin:

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        obj = self.get_object()
        services.add_like(obj, request.user)
        return Response()

    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        obj = self.get_object()
        services.remove_like(obj, request.user)
        return Response()
