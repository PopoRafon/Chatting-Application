from django import template

register = template.Library()


@register.filter
def add_class_attributes(field, attributes):
    field.field.widget.attrs['class'] = attributes
    return field
