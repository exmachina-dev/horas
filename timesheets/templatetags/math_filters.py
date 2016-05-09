from django import template
import math

register = template.Library()


@register.filter(is_safe=False)
def substract(value, arg):
    """Substracts the arg to the value."""
    try:
        return int(value) - int(arg)
    except (ValueError, TypeError):
        try:
            return value - arg
        except Exception:
            return ''


@register.filter(is_safe=False)
def multiply(value, arg):
    """Multiply the arg to the value."""
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        try:
            return value * arg
        except Exception:
            return ''


@register.filter(is_safe=False)
def fhours(value):
    """Formats float to hours representation."""
    try:
        h = int(math.floor(float(value)))
        m = int((float(value) - h) * 60)
        return '{:d}h{:02d}'.format(h, m)
    except (ValueError, TypeError):
        try:
            return '-'
        except Exception:
            return ''


@register.filter(name='range', is_safe=False)
def gen_range(value):
    """Generate a range from value."""
    try:
        r = range(int(value))
        return r
    except (ValueError, TypeError):
        try:
            return ()
        except Exception:
            return ''
