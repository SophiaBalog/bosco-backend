from django import template

register = template.Library()

@register.filter(name='currency')
def currency(value):
    try:
        return f"{float(value):,.2f} грн"
    except (ValueError, TypeError):
        return value