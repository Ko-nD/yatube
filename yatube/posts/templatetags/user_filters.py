<<<<<<< HEAD
from django import template


register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})
=======
from django import template


register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})
>>>>>>> e00ceddaa1758d008aea9fd3ff70b76728ca2368
