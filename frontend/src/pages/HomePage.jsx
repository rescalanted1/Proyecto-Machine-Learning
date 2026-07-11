import { useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import TopAppBar from "../components/TopAppBar.jsx";
import BottomNavBar from "../components/BottomNavBar.jsx";
import LoadingOverlay from "../components/LoadingOverlay.jsx";
import useAnalysis from "../hooks/useAnalysis.js";

export default function HomePage({ onResult }) {
  const navigate = useNavigate();
  const fileInputRef = useRef(null);
  const { status, error, analyze, reset } = useAnalysis();

  const [preview, setPreview] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);

  /* ---- File selection ---- */
  const handleFileChange = (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setSelectedFile(file);
    setPreview(URL.createObjectURL(file));
    reset();
  };

  const clearSelection = () => {
    setSelectedFile(null);
    setPreview(null);
    if (fileInputRef.current) fileInputRef.current.value = "";
    reset();
  };

  /* ---- Submit ---- */
  const handleAnalyze = async () => {
    if (!selectedFile) return;
    try {
      const result = await analyze(selectedFile);
      onResult(result);
      navigate("/results");
    } catch {
      // error is handled by useAnalysis hook → shown in UI
    }
  };

  return (
    <>
      <TopAppBar />
      {status === "loading" && <LoadingOverlay />}

      <main className="main-content page-container stagger">
        {/* Hero */}
        <section className="hero">
          <div className="hero__content">
            <h2 className="text-display-lg hero__title">
              Diagnóstico de Cultivos Instantáneo
            </h2>
            <p className="text-body-lg hero__subtitle">
              Analiza tus plantas con inteligencia artificial. Detecta
              enfermedades en tomate, papa y pimiento en segundos.
            </p>
          </div>
          <div className="hero__bg" aria-hidden="true">
            <div
              style={{
                width: "100%",
                height: "100%",
                background:
                  "linear-gradient(135deg, var(--secondary) 0%, var(--primary) 100%)",
                opacity: 0.3,
              }}
            />
          </div>
        </section>

        {/* Upload Action */}
        <section className="action-grid">
          <button
            className="action-card action-card--upload"
            onClick={() => fileInputRef.current?.click()}
            id="upload-button"
          >
            <div className="action-card__icon-wrap">
              <span className="material-symbols-outlined action-card__icon">
                upload_file
              </span>
            </div>
            <div>
              <span className="action-card__title">Subir Imagen</span>
              <br />
              <span className="action-card__desc">
                Selecciona una foto de una hoja desde tu dispositivo
              </span>
            </div>
          </button>
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            className="sr-only"
            onChange={handleFileChange}
            id="file-input"
          />
        </section>

        {/* Image Preview */}
        {preview && (
          <section className="preview-section animate-fade-in">
            <img src={preview} alt="Vista previa de la imagen seleccionada" />
            <p className="text-body-sm" style={{ color: "var(--on-surface-variant)" }}>
              {selectedFile?.name}
            </p>
            <div className="preview-actions">
              <button className="btn btn--primary" onClick={handleAnalyze}>
                <span className="material-symbols-outlined">biotech</span>
                Analizar Imagen
              </button>
              <button className="btn btn--outline" onClick={clearSelection}>
                <span className="material-symbols-outlined">close</span>
                Cancelar
              </button>
            </div>
          </section>
        )}

        {/* Error */}
        {status === "error" && (
          <div className="error-card animate-fade-in">
            <span className="material-symbols-outlined error-card__icon">
              error
            </span>
            <p className="error-card__title">Error en el análisis</p>
            <p className="error-card__message">{error}</p>
            <button className="btn btn--error-outline" onClick={reset}>
              Intentar de nuevo
            </button>
          </div>
        )}

        {/* Tips */}
        <section className="tips-section">
          <div className="tips-section__header">
            <span className="material-symbols-outlined">lightbulb</span>
            <h3 className="text-title-md">
              Consejos para un diagnóstico preciso
            </h3>
          </div>
          <div className="tips-grid">
            <div className="tip-item">
              <div className="tip-item__icon">
                <span className="material-symbols-outlined">wb_sunny</span>
              </div>
              <div>
                <p className="text-label-caps tip-item__label">Iluminación</p>
                <p className="text-body-sm tip-item__text">
                  Evita sombras fuertes o luz solar directa extrema sobre la
                  hoja.
                </p>
              </div>
            </div>
            <div className="tip-item">
              <div className="tip-item__icon">
                <span className="material-symbols-outlined">
                  center_focus_strong
                </span>
              </div>
              <div>
                <p className="text-label-caps tip-item__label">Enfoque</p>
                <p className="text-body-sm tip-item__text">
                  Mantén la cámara a unos 15-20cm y asegúrate de que la hoja
                  esté nítida.
                </p>
              </div>
            </div>
            <div className="tip-item">
              <div className="tip-item__icon">
                <span className="material-symbols-outlined">
                  filter_center_focus
                </span>
              </div>
              <div>
                <p className="text-label-caps tip-item__label">Aislamiento</p>
                <p className="text-body-sm tip-item__text">
                  Trata de que solo una hoja sea la protagonista de la imagen.
                </p>
              </div>
            </div>
          </div>
        </section>
      </main>

      <BottomNavBar />
    </>
  );
}
