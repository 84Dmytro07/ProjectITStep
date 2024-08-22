from django import template
from django.forms import BoundField

register = template.Library()

@register.filter(name='add_class')
def add_class(value, arg):
    if isinstance(value, BoundField):
        return value.as_widget(attrs={'class': arg})
    return value  # Возвращаем исходное значение, если оно не является полем формы


