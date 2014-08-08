from django import template

register = template.Library()


@register.filter
def get_url(d):
	return d.images['standard_resolution'].url


@register.filter
def get_user(d):
	return d.user.username