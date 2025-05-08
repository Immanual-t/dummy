# ai_assistant/utils.py
import re
import html
from django.utils.safestring import mark_safe


class ResponseFormatter:
    """
    Utility class for formatting AI responses for display in the frontend
    """

    @staticmethod
    def format_for_html(response_text):
        """
        Format AI response for HTML display with proper formatting

        Args:
            response_text (str): The raw AI response text

        Returns:
            str: Formatted HTML-safe response with proper styling
        """
        # Handle empty responses
        if not response_text:
            return ""

        # Escape HTML to prevent injection
        escaped_text = html.escape(response_text)

        # Split into paragraphs
        paragraphs = escaped_text.split('\n\n')
        formatted_text = ""

        for paragraph in paragraphs:
            # Skip empty paragraphs
            if not paragraph.strip():
                continue

            # Handle lists
            if paragraph.strip().startswith(('* ', '- ', '• ')):
                lines = paragraph.split('\n')
                list_items = []

                for line in lines:
                    line = line.strip()
                    if line.startswith(('* ', '- ', '• ')):
                        item = line[2:].strip()
                        list_items.append(f"<li class='list-group-item border-0 py-1'>{item}</li>")

                if list_items:
                    formatted_text += f"<ul class='list-group list-group-flush mb-3'>{''.join(list_items)}</ul>"
            else:
                # Regular paragraph with possible line breaks
                formatted_paragraph = paragraph.replace('\n', '<br>')

                # Handle headings
                if formatted_paragraph.startswith('# '):
                    heading_text = formatted_paragraph[2:]
                    formatted_text += f"<h3 class='mt-4 mb-3'>{heading_text}</h3>"
                elif formatted_paragraph.startswith('## '):
                    heading_text = formatted_paragraph[3:]
                    formatted_text += f"<h4 class='mt-3 mb-2'>{heading_text}</h4>"
                elif formatted_paragraph.startswith('### '):
                    heading_text = formatted_paragraph[4:]
                    formatted_text += f"<h5 class='mt-3 mb-2'>{heading_text}</h5>"
                else:
                    formatted_text += f"<p class='mb-3'>{formatted_paragraph}</p>"

        # Format inline markdown elements
        formatted_text = re.sub(r'(\*\*|__)(.*?)(\*\*|__)', r'<strong>\2</strong>', formatted_text)
        formatted_text = re.sub(r'(\*|_)(.*?)(\*|_)', r'<em>\2</em>', formatted_text)
        formatted_text = re.sub(r'`(.*?)`', r'<code>\1</code>', formatted_text)

        # Add styling for blockquotes
        formatted_text = re.sub(r'&gt;\s*(.*?)(?=<br>|</p>)',
                                r'<blockquote class="border-start border-3 ps-3 text-muted">\1</blockquote>',
                                formatted_text)

        # Highlight key terms or phrases that might be important
        keywords = [
            'insurance', 'credit card', 'loan', 'investment', 'savings', 'demat',
            'premium', 'interest', 'commission', 'benefits', 'features', 'objection'
        ]

        for keyword in keywords:
            formatted_text = re.sub(
                rf'\b({keyword})\b',
                r'<span class="text-primary">\1</span>',
                formatted_text,
                flags=re.IGNORECASE
            )

        # Make it safe to include in a template
        return mark_safe(formatted_text)

    @staticmethod
    def format_for_chat(response_text):
        """
        Format AI response for chat bubbles with simpler styling

        Args:
            response_text (str): The raw AI response text

        Returns:
            str: Formatted HTML-safe response for chat interface
        """
        # Handle empty responses
        if not response_text:
            return ""

        # Escape HTML
        escaped_text = html.escape(response_text)

        # Simple paragraph formatting
        paragraphs = escaped_text.split('\n\n')
        formatted_text = ""

        for paragraph in paragraphs:
            if paragraph.strip():
                formatted_text += f"<p>{paragraph.replace('\n', '<br>')}</p>"

        # Format inline markdown elements
        formatted_text = re.sub(r'(\*\*|__)(.*?)(\*\*|__)', r'<strong>\2</strong>', formatted_text)
        formatted_text = re.sub(r'(\*|_)(.*?)(\*|_)', r'<em>\2</em>', formatted_text)

        # Make it safe to include in a template
        return mark_safe(formatted_text)

    @staticmethod
    def format_as_json(response_text):
        """
        Format AI response as JSON for API returns

        Args:
            response_text (str): The raw AI response text

        Returns:
            dict: Formatted response as dictionary
        """
        # Basic structure that can be expanded
        return {
            'response': response_text,
            'metadata': {
                'has_markdown': '**' in response_text or '*' in response_text or '#' in response_text,
                'has_lists': ('* ' in response_text or '- ' in response_text or '• ' in response_text),
                'word_count': len(response_text.split())
            }
        }