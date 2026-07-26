"""Smoke test local: health, UI assets, preview, convert, frontmatter, import-pdf."""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PORT = os.getenv("PORT", "8765")
BASE = os.getenv("MD_PDF_BASE", f"http://127.0.0.1:{PORT}")


def get(path: str) -> tuple[int, bytes]:
    with urllib.request.urlopen(BASE + path) as resp:
        return resp.status, resp.read()


def post(path: str, payload: dict) -> tuple[int, dict, bytes]:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        BASE + path,
        data=data,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as resp:
        return resp.status, dict(resp.headers), resp.read()


def post_multipart(path: str, field: str, filename: str, content: bytes, content_type: str) -> tuple[int, bytes]:
    boundary = "----mdpdfsmoke7f3a9c"
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="{field}"; filename="{filename}"\r\n'
        f"Content-Type: {content_type}\r\n\r\n"
    ).encode("utf-8") + content + f"\r\n--{boundary}--\r\n".encode("utf-8")
    req = urllib.request.Request(
        BASE + path,
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        return resp.status, resp.read()


def main() -> int:
    checks: list[tuple[str, bool, object]] = []
    ok = True

    try:
        status, body = get("/api/health")
        health = json.loads(body)
        checks.append(
            (
                "health",
                status == 200 and health.get("ok") and health.get("playwright") == "ready",
                health,
            )
        )
    except Exception as exc:  # noqa: BLE001
        checks.append(("health", False, str(exc)))
        ok = False

    for path in (
        "/",
        "/static/app.js",
        "/theme/themes/informe.css",
        "/api/highlight.css",
        "/api/themes",
    ):
        try:
            status, _ = get(path)
            checks.append((path, status == 200, status))
        except Exception as exc:  # noqa: BLE001
            checks.append((path, False, str(exc)))
            ok = False

    simple = (ROOT / "fixtures" / "simple.md").read_text(encoding="utf-8")
    try:
        status, _, body = post("/api/preview", {"markdown": simple, "theme": "informe"})
        prev = json.loads(body)
        checks.append(("preview", status == 200 and "<h1>" in prev.get("html", ""), len(prev.get("html", ""))))
    except Exception as exc:  # noqa: BLE001
        checks.append(("preview", False, str(exc)))
        ok = False

    pdf_bytes = b""
    try:
        status, _, body = post(
            "/api/convert",
            {"markdown": simple, "filename": "smoke-simple.md", "theme": "informe"},
        )
        pdf_bytes = body
        checks.append(
            (
                "convert",
                status == 200 and body.startswith(b"%PDF"),
                f"{len(body)}b",
            )
        )
    except Exception as exc:  # noqa: BLE001
        checks.append(("convert", False, str(exc)))
        ok = False

    demo = (ROOT / "fixtures" / "frontmatter-demo.md").read_text(encoding="utf-8")
    try:
        status, _, body = post("/api/preview", {"markdown": demo})
        prev = json.loads(body)
        meta = prev.get("meta") or {}
        checks.append(
            (
                "frontmatter",
                "doc-title" in prev.get("html", "") and bool(meta.get("title")),
                meta,
            )
        )
    except Exception as exc:  # noqa: BLE001
        checks.append(("frontmatter", False, str(exc)))
        ok = False

    if pdf_bytes.startswith(b"%PDF"):
        try:
            status, body = post_multipart(
                "/api/import-pdf",
                "file",
                "smoke-simple.pdf",
                pdf_bytes,
                "application/pdf",
            )
            data = json.loads(body)
            md = data.get("markdown") or ""
            warnings = data.get("warnings") or []
            checks.append(
                (
                    "import-pdf",
                    status == 200 and len(md.strip()) > 20 and bool(warnings),
                    f"{len(md)} chars, pages={data.get('meta', {}).get('pages')}",
                )
            )
        except Exception as exc:  # noqa: BLE001
            checks.append(("import-pdf", False, str(exc)))
            ok = False
    else:
        checks.append(("import-pdf", False, "sin PDF de convert"))
        ok = False

    for name, passed, detail in checks:
        print(f"{'OK' if passed else 'FAIL'}  {name}: {detail}")
        if not passed:
            ok = False

    print("SMOKE", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except urllib.error.URLError as exc:
        print(f"FAIL  server: no responde en {BASE} ({exc})")
        print("SMOKE FAIL")
        raise SystemExit(1) from exc
