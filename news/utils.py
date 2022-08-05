from django.db.models import Count

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
