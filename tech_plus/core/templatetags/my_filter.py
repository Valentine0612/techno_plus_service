from django import template

register = template.Library()

@register.filter(name='times') 
def times(number):
    return range(number)

@register.filter
def filter(objects, name):
    return objects.filter(name=name)

@register.filter(name='lookup')
def lookup(value, arg):
    return value[arg]

@register.simple_tag
def url_replace(request, field, value):
    dict_ = request.GET.copy()
    dict_[field] = value
    return dict_.urlencode()