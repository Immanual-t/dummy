# ai_assistant/templatetags/json_tags.py
import json
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def to_json(value):
    """
    Convert Python object to JSON string for JavaScript use

    Usage: {{ object|to_json }}
    """
    return mark_safe(json.dumps(value))

@register.filter
def json_script(value, element_id):
    """
    Output Python object as JSON in a script tag

    Usage: {{ object|json_script:"my-data" }}
    """
    json_str = json.dumps(value)
    return mark_safe(f'<script id="{element_id}" type="application/json">{json_str}</script>')

@register.filter
def parse_json(value):
    """
    Parse a JSON string into a Python object

    Usage: {{ json_string|parse_json }}
    """
    try:
        return json.loads(value)
    except (TypeError, json.JSONDecodeError):
        return None

@register.filter
def get_item(dictionary, key):
    """
    Get an item from a dictionary by key

    Usage: {{ dictionary|get_item:key }}
    """
    if dictionary is None:
        return None
    return dictionary.get(key)