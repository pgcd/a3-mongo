from utils import string_to_dict, string_to_list, get_query_string

__author__ = 'pgcd'
from django import template

register = template.Library()
@register.simple_tag(takes_context = True)
def query_string(context, add = None, remove = None, add_parameters = None):
    """
    Allows the addition and removal of query string parameters.

    Usage:
    http://www.url.com/{% query_string "param_to_add=value, param_to_add=value" "param_to_remove, params_to_remove" %}
    http://www.url.com/{% query_string "" "filter" %}filter={{new_filter}}
    http://www.url.com/{% query_string "sort=value" "sort" %}
    """
    # Written as an inclusion tag to simplify getting the context.
    if add_parameters:
        add = string_to_dict(add % tuple(string_to_list(add_parameters)))
    else:
        add = string_to_dict(add)
    remove = string_to_list(remove)
    params = dict(context['request'].GET.items())
    response = get_query_string(params, add, remove)
    return response