from django.contrib.admin import widgets as admin_widgets
from django.utils.html import format_html


class MarkdownPreviewWidget(admin_widgets.AdminTextareaWidget):
    """Admin textarea with a live Markdown preview pane.

    The preview is rendered client-side by a small, dependency-free renderer
    (see portfolio/static/portfolio/admin/markdown_preview.js) that HTML-escapes
    all input first, so it cannot execute injected markup (XSS-safe).
    """

    class Media:
        css = {"all": ("portfolio/admin/markdown_preview.css",)}
        js = ("portfolio/admin/markdown_preview.js",)

    def render(self, name, value, attrs=None, renderer=None):
        attrs = attrs or {}
        attrs.setdefault("rows", 18)
        attrs.setdefault("class", "vLargeTextField markdown-input")
        textarea = super().render(name, value, attrs, renderer)
        target_id = attrs.get("id", f"id_{name}")
        preview = format_html(
            '<div class="markdown-preview" id="preview-{0}" data-target="{0}" '
            'aria-live="polite"><em>Preview…</em></div>',
            target_id,
        )
        return format_html('<div class="markdown-preview-widget">{0}{1}</div>', textarea, preview)
