from django import template


register = template.Library()

@register.filter(name='split')
def split(str, key):
    return str.split(key)


@register.filter(name='remfl')
def remfl(str1, key):
	if str1 != '' and key != '':
		return str(str1)[int(key):-int(key)]


