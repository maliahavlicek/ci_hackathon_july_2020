from django import template
from datetime import datetime
from django.utils import timezone

register = template.Library()


@register.filter()
def format_date(date):
    """Function takes a datetime object and stringifies it down to MM/DD/YYYY format"""
    try:
        start_date = datetime.strftime(date, '%m/%d/%Y')
    except (TypeError, ValueError) as e:
        start_date = date
        pass
    return start_date


@register.filter(name='hours_ago')
def hours_ago(time, hours):
    if time < timezone.now() - timezone.timedelta(hours=hours):
        return False
    else:
        return True
