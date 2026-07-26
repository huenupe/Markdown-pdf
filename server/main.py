"""Entrypoint FastAPI: API + UI estática."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles

from server.config import CLIENT_DIR, SHARED_DIR
from server.routes.api import router as api_router
from server.services.pdf_service import pdf_service


@asynccontextmanager
async def lifespan(_app: FastAPI):
    try:
        await pdf_service.start_async()
    except Exception as exc:  # noqa: BLE001 — la API puede arrancar; convert reintenta
        print(f"[md-pdf] Aviso: no se pudo iniciar Playwright al arrancar: {exc}")
        print("[md-pdf] Se reintentará al generar el primer PDF.")
    yield
    await pdf_service.stop_async()


app = FastAPI(
    title="MD-PDF",
    description="Convertidor local Markdown ↔ PDF",
    version="1.1.0",
    lifespan=lifespan,
)

app.include_router(api_router)


@app.get("/")
def index() -> FileResponse:
    return FileResponse(CLIENT_DIR / "index.html")


@app.get("/favicon.ico", include_in_schema=False)
def no_favicon() -> Response:
    """Sin archivo favicon: 204 evita 404 si algún cliente aún pide /favicon.ico."""
    return Response(status_code=204)


app.mount("/static", StaticFiles(directory=CLIENT_DIR), name="static")
app.mount("/theme", StaticFiles(directory=SHARED_DIR), name="theme")
