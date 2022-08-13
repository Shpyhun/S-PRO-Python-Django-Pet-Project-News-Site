from django import template

from news.models import Category

register = template.Library()


@register.simple_tag()
def get_categories(filter=None):
    if not filter:
        return Category.objects.all()
    else:
        return Category.objects.all(pk=filter)


@register.inclusion_tag('news/list_categories.html')
def view_categories(sort=None, category_slug=0):

    if not sort:
        categories = Category.objects.all()
    else:
        categories = Category.objects.order_by(sort)
    return {'categories': categories, 'category_selected': category_slug}
