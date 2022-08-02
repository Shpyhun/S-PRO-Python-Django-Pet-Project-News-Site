from news.models import Category

menu = [{'title': 'Add news', 'url_name': 'add_news'},
        {'title': 'Weather', 'url_name': 'add_news'}
        ]


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        categories = Category.objects.all
        context['menu'] = menu
        context['category'] = categories
        if 'category_selected' not in context:
            context['category_selected'] = 0
        return context
