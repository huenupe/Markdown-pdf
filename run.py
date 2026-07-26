"""
Arranque recomendado de MD-PDF (evita problemas de --reload + Playwright en Windows).

Uso (con .venv activo):
  python run.py
  python run.py --port 9000
  python run.py --reload          # opcional; en Windows puede ser menos estable
"""

from __future__ import annotations

import argparse
import os
import sys


def main() -> None:
    parser = argparse.ArgumentParser(description="MD-PDF local server")
    parser.add_argument("--host", default=os.getenv("HOST", "127.0.0.1"))
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.getenv("PORT", "8765")),
        help="Puerto HTTP (default 8765; evita conflictos típicos con 8000 en Windows)",
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Auto-reload (en Windows preferí sin esto si Playwright falla)",
    )
    args = parser.parse_args()

    if sys.platform == "win32":
        import asyncio

        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    import uvicorn

    print(f"[md-pdf] http://{args.host}:{args.port}")
    uvicorn.run(
        "server.main:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        loop="asyncio",
    )


if __name__ == "__main__":
    main()
