"""HTML → PDF con Playwright sync (compatible con Windows / uvicorn)."""

from __future__ import annotations

import asyncio
import threading
from functools import lru_cache
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape
from playwright.sync_api import Browser, Playwright, sync_playwright
from pygments.formatters import HtmlFormatter

from server.config import (
    DEFAULT_THEME,
    OUTPUT_DIR,
    PDF_TIMEOUT_MS,
    TEMPLATES_DIR,
    THEMES_DIR,
    normalize_theme,
)

FOOTER_TEMPLATE = """
<div style="font-size:9px;width:100%;text-align:center;color:#555;font-family:Segoe UI,Helvetica Neue,Arial,sans-serif;padding:0 18mm;">
  <span class="pageNumber"></span> / <span class="totalPages"></span>
</div>
"""


@lru_cache(maxsize=1)
def highlight_css() -> str:
    return HtmlFormatter(style="default").get_style_defs(".highlight")


class PdfService:
    """Playwright sync + lock: evita NotImplementedError de asyncio en Windows."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._playwright: Playwright | None = None
        self._browser: Browser | None = None
        self._env = Environment(
            loader=FileSystemLoader(str(TEMPLATES_DIR)),
            autoescape=select_autoescape(["html", "xml"]),
        )
        self._last_error: str | None = None

    @property
    def ready(self) -> bool:
        with self._lock:
            return self._browser is not None and self._browser.is_connected()

    @property
    def last_error(self) -> str | None:
        return self._last_error

    def start(self) -> None:
        with self._lock:
            if self._browser is not None and self._browser.is_connected():
                return
            try:
                self._playwright = sync_playwright().start()
                self._browser = self._playwright.chromium.launch(headless=True)
                self._last_error = None
            except Exception as exc:  # noqa: BLE001
                self._last_error = str(exc)
                self._browser = None
                if self._playwright is not None:
                    try:
                        self._playwright.stop()
                    except Exception:  # noqa: BLE001
                        pass
                    self._playwright = None
                raise

    def stop(self) -> None:
        with self._lock:
            if self._browser is not None:
                try:
                    self._browser.close()
                except Exception:  # noqa: BLE001
                    pass
                self._browser = None
            if self._playwright is not None:
                try:
                    self._playwright.stop()
                except Exception:  # noqa: BLE001
                    pass
                self._playwright = None

    def theme_css(self, theme: str | None) -> str:
        name = normalize_theme(theme)
        path = THEMES_DIR / f"{name}.css"
        if not path.exists():
            path = THEMES_DIR / f"{DEFAULT_THEME}.css"
        return path.read_text(encoding="utf-8") if path.exists() else ""

    def build_document_html(self, html_fragment: str, theme: str | None = None) -> str:
        css = self.theme_css(theme) + "\n" + highlight_css()
        template = self._env.get_template("document.html")
        return template.render(css=css, content=html_fragment)

    def save_to_output(self, pdf_bytes: bytes, filename: str) -> Path:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        dest = OUTPUT_DIR / filename
        dest.write_bytes(pdf_bytes)
        return dest

    def html_to_pdf_sync(self, html_fragment: str, theme: str | None = None) -> bytes:
        with self._lock:
            if self._browser is None or not self._browser.is_connected():
                # reintento lazy (sin soltar el lock: start interno usa el mismo lock → deadlock)
                # Por eso arrancamos inline aquí:
                if self._playwright is None:
                    self._playwright = sync_playwright().start()
                self._browser = self._playwright.chromium.launch(headless=True)
                self._last_error = None

            assert self._browser is not None
            full_html = self.build_document_html(html_fragment, theme=theme)
            page = self._browser.new_page()
            try:
                page.set_content(
                    full_html, wait_until="networkidle", timeout=PDF_TIMEOUT_MS
                )
                return page.pdf(
                    format="A4",
                    print_background=True,
                    margin={
                        "top": "20mm",
                        "right": "18mm",
                        "bottom": "20mm",
                        "left": "18mm",
                    },
                    display_header_footer=True,
                    header_template="<div></div>",
                    footer_template=FOOTER_TEMPLATE,
                )
            finally:
                page.close()

    async def start_async(self) -> None:
        await asyncio.to_thread(self.start)

    async def stop_async(self) -> None:
        await asyncio.to_thread(self.stop)

    async def html_to_pdf(self, html_fragment: str, theme: str | None = None) -> bytes:
        try:
            return await asyncio.to_thread(self.html_to_pdf_sync, html_fragment, theme)
        except Exception as exc:  # noqa: BLE001
            self._last_error = str(exc)
            raise RuntimeError(
                "No se pudo generar el PDF con Playwright/Chromium. "
                "Con el .venv activo ejecutá: playwright install chromium. "
                f"Detalle: {exc}"
            ) from exc


pdf_service = PdfService()
