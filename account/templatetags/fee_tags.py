from django import template

register = template.Library()

@register.simple_tag
def get_fee(fee_base, hours):
    return "testing"

@register.simple_tag
def get_duration(start_time, end_time, *args, **kwargs):
    return end_time - start_time