(() => {
  const DEBOUNCE_MS = 400;
  const REMOTE_URL_RE = /https?:\/\//i;

  const SHEET_CHROME = `
:host { display: block; }
.sheet {
  box-sizing: border-box;
  max-width: 210mm;
  min-height: 297mm;
  margin: 0 auto;
  padding: 20mm 18mm;
  background: #fff;
  box-shadow: 0 1px 3px rgba(15, 23, 42, 0.08);
  border-radius: 2px;
}
.preview-placeholder { color: #94a3b8; font-family: system-ui, sans-serif; }
`;

  const els = {
    workspace: document.getElementById("workspace"),
    panePdf: document.getElementById("pane-pdf"),
    paneSource: document.getElementById("pane-source"),
    paneDoc: document.getElementById("pane-doc"),
    pdfFrame: document.getElementById("pdf-frame"),
    pdfLabel: document.getElementById("pdf-label"),
    status: document.getElementById("status"),
    statusDot: document.getElementById("status-dot"),
    error: document.getElementById("error"),
    privacyHint: document.getElementById("privacy-hint"),
    importHint: document.getElementById("import-hint"),
    editor: document.getElementById("editor"),
    editorStats: document.getElementById("editor-stats"),
    previewHost: document.getElementById("preview-host"),
    mdViewHost: document.getElementById("md-view-host"),
    mdViewScroll: document.getElementById("md-view-scroll"),
    previewState: document.getElementById("preview-state"),
    fileInput: document.getElementById("file-input"),
    pdfInput: document.getElementById("pdf-input"),
    fileLabel: document.getElementById("file-label"),
    btnConvert: document.getElementById("btn-convert"),
    btnDownloadMd: document.getElementById("btn-download-md"),
    btnClear: document.getElementById("btn-clear"),
    btnModeEdit: document.getElementById("btn-mode-edit"),
    btnModeView: document.getElementById("btn-mode-view"),
    dropzone: document.getElementById("dropzone"),
    themeSelect: document.getElementById("theme-select"),
  };

  let sourceFilename = null;
  let pdfSourceName = null;
  let pdfObjectUrl = null;
  let layoutMode = "md"; // md | pdf
  let sourceView = "edit"; // edit | view
  let previewTimer = null;
  let converting = false;
  let importing = false;
  let themeCss = "";
  let highlightCss = "";
  let lastHtml = "";
  let previewShadow = null;
  let mdViewShadow = null;
  let healthOk = false;

  function currentTheme() {
    return els.themeSelect.value || "informe";
  }

  function ensureShadow(host, cacheKey) {
    if (cacheKey === "preview") {
      if (!previewShadow) previewShadow = host.attachShadow({ mode: "open" });
      return previewShadow;
    }
    if (!mdViewShadow) mdViewShadow = host.attachShadow({ mode: "open" });
    return mdViewShadow;
  }

  function setStatus(text, kind = "ok") {
    els.status.textContent = text;
    els.status.classList.toggle("is-error", kind === "error");
    els.statusDot.classList.remove("is-ok", "is-error", "is-busy");
    if (kind === "ok") els.statusDot.classList.add("is-ok");
    else if (kind === "error") els.statusDot.classList.add("is-error");
    else if (kind === "busy") els.statusDot.classList.add("is-busy");
  }

  function setError(message) {
    if (!message) {
      els.error.hidden = true;
      els.error.textContent = "";
      return;
    }
    els.error.hidden = false;
    els.error.textContent = message;
  }

  function updatePrivacyHint(markdown) {
    els.privacyHint.hidden = !REMOTE_URL_RE.test(markdown || "");
  }

  function setImportHint(message) {
    if (!message) {
      els.importHint.hidden = true;
      els.importHint.textContent = "";
      return;
    }
    els.importHint.hidden = false;
    els.importHint.textContent = message;
  }

  function updateStats() {
    const text = els.editor.value;
    const chars = text.length;
    const lines = text === "" ? 0 : text.split(/\r\n|\r|\n/).length;
    const words = text.trim() === "" ? 0 : text.trim().split(/\s+/).length;
    els.editorStats.textContent = `${words} palabras · ${chars} caracteres · ${lines} líneas`;
  }

  function syncButtons() {
    const hasText = els.editor.value.trim().length > 0;
    const busy = converting || importing;
    els.btnConvert.disabled = !hasText || busy;
    if (els.btnDownloadMd) els.btnDownloadMd.disabled = !hasText || busy;
    els.btnClear.disabled = (!hasText && !sourceFilename && !pdfSourceName) || busy;
    if (els.pdfInput) els.pdfInput.disabled = busy;
    if (els.fileInput) els.fileInput.disabled = busy;
  }

  function pdfName() {
    if (!sourceFilename) return "documento.pdf";
    const base = sourceFilename.replace(/\.[^.]+$/, "") || "documento";
    return `${base}.pdf`;
  }

  function mdName() {
    if (sourceFilename) {
      const lower = sourceFilename.toLowerCase();
      if (lower.endsWith(".md") || lower.endsWith(".markdown") || lower.endsWith(".txt")) {
        return sourceFilename.replace(/\.(markdown|txt)$/i, ".md");
      }
      const base = sourceFilename.replace(/\.[^.]+$/, "") || "documento";
      return `${base}.md`;
    }
    if (pdfSourceName) {
      const base = pdfSourceName.replace(/\.[^.]+$/, "") || "documento";
      return `${base}.md`;
    }
    return "documento.md";
  }

  function downloadMarkdown() {
    const text = els.editor.value;
    if (!text.trim()) return;
    const blob = new Blob([text], { type: "text/markdown;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = mdName();
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
    setStatus(`Markdown listo · ${mdName()}`, "ok");
  }

  function clearPdfPreview() {
    if (pdfObjectUrl) {
      URL.revokeObjectURL(pdfObjectUrl);
      pdfObjectUrl = null;
    }
    els.pdfFrame.removeAttribute("src");
    els.pdfLabel.textContent = "";
    pdfSourceName = null;
  }

  function showPdfPreview(file) {
    clearPdfPreview();
    pdfSourceName = file.name;
    pdfObjectUrl = URL.createObjectURL(file);
    els.pdfFrame.src = pdfObjectUrl;
    els.pdfLabel.textContent = file.name;
  }

  function setLayoutMode(mode) {
    layoutMode = mode === "pdf" ? "pdf" : "md";
    els.workspace.dataset.mode = layoutMode;
    els.panePdf.hidden = layoutMode !== "pdf";
    els.paneDoc.hidden = layoutMode !== "md";
  }

  function setSourceView(view) {
    sourceView = view === "view" ? "view" : "edit";
    const editing = sourceView === "edit";
    els.paneSource.classList.toggle("is-editing", editing);
    els.paneSource.classList.toggle("is-viewing", !editing);
    els.btnModeEdit.classList.toggle("is-active", editing);
    els.btnModeView.classList.toggle("is-active", !editing);
    els.btnModeEdit.setAttribute("aria-pressed", editing ? "true" : "false");
    els.btnModeView.setAttribute("aria-pressed", editing ? "false" : "true");
    els.mdViewScroll.hidden = editing;
    if (!editing) {
      paintHost(els.mdViewHost, "md", lastHtml);
    }
  }

  function paintHost(host, kind, html) {
    const root = ensureShadow(host, kind === "preview" ? "preview" : "md");
    const body =
      html ||
      '<p class="preview-placeholder">Escribí Markdown para ver el preview.</p>';
    root.innerHTML = `
      <style>
${themeCss}
${highlightCss}
${SHEET_CHROME}
      </style>
      <div class="sheet">
        <main class="document">${body}</main>
      </div>
    `;
  }

  function renderPreview(html) {
    lastHtml = html || "";
    if (layoutMode === "md") {
      paintHost(els.previewHost, "preview", lastHtml);
    }
    if (sourceView === "view") {
      paintHost(els.mdViewHost, "md", lastHtml);
    }
  }

  async function loadThemeCss() {
    const theme = currentTheme();
    try {
      const [themeRes, hlRes] = await Promise.all([
        fetch(`/theme/themes/${theme}.css`),
        fetch("/api/highlight.css"),
      ]);
      themeCss = themeRes.ok ? await themeRes.text() : "";
      highlightCss = hlRes.ok ? await hlRes.text() : "";
    } catch {
      themeCss = "";
      highlightCss = "";
    }
  }

  async function checkHealth() {
    try {
      const res = await fetch("/api/health");
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      if (data.playwright === "ready") {
        healthOk = true;
        setStatus("Listo · API y Playwright OK", "ok");
      } else {
        healthOk = false;
        setStatus(data.message || "API OK, Playwright no listo", "error");
      }
    } catch (err) {
      healthOk = false;
      setStatus(`Sin API: ${err.message}`, "error");
    }
  }

  async function refreshPreview() {
    const markdown = els.editor.value;
    updatePrivacyHint(markdown);
    updateStats();

    if (!markdown.trim()) {
      if (els.previewState) els.previewState.textContent = "vacío";
      renderPreview("");
      syncButtons();
      return;
    }

    if (els.previewState) els.previewState.textContent = "actualizando…";
    try {
      const res = await fetch("/api/preview", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ markdown, theme: currentTheme() }),
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || `HTTP ${res.status}`);
      }
      const data = await res.json();
      renderPreview(data.html || "");
      if (els.previewState) els.previewState.textContent = "al día";
      setError("");
    } catch (err) {
      if (els.previewState) els.previewState.textContent = "error";
      setError(`Preview: ${err.message}`);
    } finally {
      syncButtons();
    }
  }

  function schedulePreview() {
    syncButtons();
    updateStats();
    updatePrivacyHint(els.editor.value);
    clearTimeout(previewTimer);
    previewTimer = setTimeout(refreshPreview, DEBOUNCE_MS);
  }

  async function convertPdf() {
    const markdown = els.editor.value;
    if (!markdown.trim() || converting) return;

    converting = true;
    els.btnConvert.textContent = "Generando…";
    syncButtons();
    setError("");
    setStatus("Generando PDF…", "busy");

    try {
      const res = await fetch("/api/convert", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          markdown,
          filename: sourceFilename || "documento.md",
          theme: currentTheme(),
        }),
      });

      if (!res.ok) {
        let detail = `HTTP ${res.status}`;
        try {
          const err = await res.json();
          detail = err.detail || detail;
        } catch {
          /* body no JSON */
        }
        throw new Error(detail);
      }

      const saved = res.headers.get("X-Saved-Path");
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = pdfName();
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
      setStatus(
        saved ? `PDF listo · ${pdfName()} (copia en output/)` : `PDF listo · ${pdfName()}`,
        "ok"
      );
    } catch (err) {
      setError(`PDF: ${err.message}`);
      setStatus("Error al generar PDF", "error");
    } finally {
      converting = false;
      els.btnConvert.textContent = "Generar PDF";
      syncButtons();
    }
  }

  function loadText(text, filename, { importWarning, keepPdf } = {}) {
    els.editor.value = text;
    sourceFilename = filename || null;
    els.fileLabel.textContent = sourceFilename || "";
    setError("");
    if (importWarning) setImportHint(importWarning);
    else setImportHint("");
    if (!keepPdf) {
      clearPdfPreview();
      setLayoutMode("md");
    }
    setSourceView("edit");
    updatePrivacyHint(text);
    updateStats();
    syncButtons();
    refreshPreview();
  }

  async function importPdfFile(file) {
    if (!file || importing) return;
    importing = true;
    syncButtons();
    setError("");
    setStatus("Importando PDF…", "busy");

    try {
      showPdfPreview(file);
      setLayoutMode("pdf");
      setSourceView("edit");

      const form = new FormData();
      form.append("file", file, file.name);
      const res = await fetch("/api/import-pdf", { method: "POST", body: form });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) {
        throw new Error(data.detail || `HTTP ${res.status}`);
      }
      const md = data.markdown || "";
      const name = data.filename || file.name.replace(/\.pdf$/i, ".md");
      const warnings = Array.isArray(data.warnings) ? data.warnings : [];
      const pages = data.meta && data.meta.pages;
      const warn =
        warnings.join(" ") ||
        "Conversión con pérdida: revisá títulos, tablas e imágenes.";
      const withPages = pages ? `${warn} (${pages} pág.)` : warn;
      loadText(md, name, { importWarning: withPages, keepPdf: true });
      setStatus(`PDF importado · ${name}`, "ok");
    } catch (err) {
      setError(`Importar PDF: ${err.message}`);
      setStatus("Error al importar PDF", "error");
      clearPdfPreview();
      setLayoutMode("md");
    } finally {
      importing = false;
      syncButtons();
    }
  }

  function readMarkdownFile(file) {
    if (!file) return;
    const lower = file.name.toLowerCase();
    if (!(/\.(md|markdown|txt)$/.test(lower) || file.type.startsWith("text/"))) {
      setError("Solo archivos .md, .markdown, .txt o .pdf");
      return;
    }
    const reader = new FileReader();
    reader.onload = () => {
      clearPdfPreview();
      setLayoutMode("md");
      loadText(String(reader.result || ""), file.name);
    };
    reader.onerror = () => setError("No se pudo leer el archivo");
    reader.readAsText(file, "UTF-8");
  }

  function handleIncomingFile(file) {
    if (!file) return;
    const lower = file.name.toLowerCase();
    if (lower.endsWith(".pdf") || file.type === "application/pdf") {
      importPdfFile(file);
      return;
    }
    readMarkdownFile(file);
  }

  function clearAll() {
    els.editor.value = "";
    sourceFilename = null;
    els.fileLabel.textContent = "";
    els.fileInput.value = "";
    if (els.pdfInput) els.pdfInput.value = "";
    clearPdfPreview();
    setLayoutMode("md");
    setSourceView("edit");
    setError("");
    setImportHint("");
    updatePrivacyHint("");
    updateStats();
    if (els.previewState) els.previewState.textContent = "vacío";
    renderPreview("");
    setStatus(healthOk ? "Listo · API y Playwright OK" : "Listo", healthOk ? "ok" : "error");
    syncButtons();
  }

  els.editor.addEventListener("input", () => {
    setImportHint("");
    schedulePreview();
  });
  els.btnConvert.addEventListener("click", convertPdf);
  if (els.btnDownloadMd) {
    els.btnDownloadMd.addEventListener("click", downloadMarkdown);
  }
  els.btnClear.addEventListener("click", clearAll);
  els.btnModeEdit.addEventListener("click", () => setSourceView("edit"));
  els.btnModeView.addEventListener("click", () => setSourceView("view"));
  els.themeSelect.addEventListener("change", async () => {
    await loadThemeCss();
    await refreshPreview();
  });
  els.fileInput.addEventListener("change", () => {
    const file = els.fileInput.files && els.fileInput.files[0];
    readMarkdownFile(file);
  });
  els.pdfInput.addEventListener("change", () => {
    const file = els.pdfInput.files && els.pdfInput.files[0];
    importPdfFile(file);
  });

  // Drop silencioso (sin overlay): solo Abrir .md / Abrir PDF muestran UI de carga.
  ["dragenter", "dragover"].forEach((type) => {
    els.dropzone.addEventListener(type, (e) => {
      e.preventDefault();
    });
  });

  els.dropzone.addEventListener("drop", (e) => {
    e.preventDefault();
    const file = e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files[0];
    handleIncomingFile(file);
  });

  document.addEventListener("keydown", (e) => {
    const mod = e.ctrlKey || e.metaKey;
    if (mod && e.key === "Enter") {
      e.preventDefault();
      convertPdf();
    }
    if (mod && (e.key === "o" || e.key === "O")) {
      e.preventDefault();
      els.fileInput.click();
    }
  });

  setLayoutMode("md");
  setSourceView("edit");
  updateStats();
  loadThemeCss().then(() => {
    renderPreview("");
    syncButtons();
    checkHealth();
  });
})();
