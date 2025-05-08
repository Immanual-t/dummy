# ai_assistant/templatetags/ai_formatting.py
from django import template
from django.utils.safestring import mark_safe
from ..utils import ResponseFormatter

register = template.Library()


@register.filter
def format_ai_response(text):
    """
    Custom template filter to format AI responses with proper HTML formatting

    Usage: {{ ai_response|format_ai_response }}
    """
    return ResponseFormatter.format_for_html(text)


@register.filter
def format_insight(text):
    """
    Format AI insights with simpler styling for dashboard display

    Usage: {{ insight.insight_text|format_insight }}
    """
    if not text:
        return ""

    # For insights, we'll use a slightly simpler format
    formatted = text

    # Wrap in div with appropriate styling
    formatted = f'<div class="ai-insight-text">{formatted}</div>'

    return mark_safe(formatted)


@register.filter
def format_chat_message(text):
    """
    Format chat messages with simpler styling for the conversation interface

    Usage: {{ message.content|format_chat_message }}
    """
    return ResponseFormatter.format_for_chat(text)