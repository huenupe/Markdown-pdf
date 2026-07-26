"""Markdown → fragmento HTML (frontmatter + highlight)."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from html import escape

import frontmatter
import markdown

EXTENSIONS = [
    "fenced_code",
    "codehilite",
    "tables",
    "nl2br",
    "sane_lists",
]

EXTENSION_CONFIGS = {
    "codehilite": {
        "css_class": "highlight",
        "guess_lang": True,
        "linenums": False,
    }
}

_SCRIPTISH = re.compile(
    r"<(script|style|iframe|object|embed)[^>]*>.*?</\1>",
    re.IGNORECASE | re.DOTALL,
)
_ON_ATTR = re.compile(r"\son\w+\s*=\s*(['\"]).*?\1", re.IGNORECASE | re.DOTALL)
_JS_HREF = re.compile(r"""\shref\s*=\s*(['"])\s*javascript:[^'"]*\1""", re.IGNORECASE)


@dataclass
class RenderResult:
    html: str
    meta: dict = field(default_factory=dict)


def sanitize_html(html: str) -> str:
    html = _SCRIPTISH.sub("", html)
    html = _ON_ATTR.sub("", html)
    html = _JS_HREF.sub("", html)
    return html


def _meta_header(meta: dict) -> str:
    title = meta.get("title")
    author = meta.get("author")
    date = meta.get("date")
    if not any([title, author, date]):
        return ""

    parts = ['<header class="doc-meta">']
    if title:
        parts.append(f'<h1 class="doc-title">{escape(str(title))}</h1>')
    byline = " · ".join(
        escape(str(x)) for x in (author, date) if x is not None and str(x).strip()
    )
    if byline:
        parts.append(f'<p class="doc-byline">{byline}</p>')
    parts.append("</header>")
    return "\n".join(parts)


def _body_to_html(text: str) -> str:
    raw = markdown.markdown(
        text,
        extensions=EXTENSIONS,
        extension_configs=EXTENSION_CONFIGS,
        output_format="html5",
    )
    return sanitize_html(raw)


def render_markdown(text: str) -> RenderResult:
    """Parsea frontmatter + Markdown → HTML de documento."""
    post = frontmatter.loads(text)
    meta = {k: v for k, v in dict(post.metadata).items() if v is not None}
    # date puede ser datetime/date
    for key in ("date",):
        if key in meta and hasattr(meta[key], "isoformat"):
            meta[key] = meta[key].isoformat()

    body_html = _body_to_html(post.content or "")
    html = _meta_header(meta) + body_html
    return RenderResult(html=html, meta=meta)


def markdown_to_html(text: str) -> str:
    """Compat: solo el HTML."""
    return render_markdown(text).html
