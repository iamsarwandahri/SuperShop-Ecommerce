from django import template

register = template.Library()

@register.filter
def multiply(value,multiplyby):
    return round(float(value*multiplyby),2)

@register.filter
def mod(value,dividedby):
    if value % dividedby == 0:
        return True
    else:
        return False

