from django import template

register = template.Library()


@register.filter
def get_url(d):
	return d.images['standard_resolution'].url