import { useState } from "react";
import { useNavigate } from "react-router-dom";
import TopAppBar from "../components/TopAppBar.jsx";
import BottomNavBar from "../components/BottomNavBar.jsx";

/* ---- Severity helpers ---- */
const SEVERITY_LABELS = {
  critical: "Estado Crítico: Se requiere intervención inmediata.",
  high: "Severidad Alta: Se recomienda tratamiento pronto.",
  moderate: "Severidad Moderada: Monitorear y tratar si progresa.",
  none: "Planta saludable. No se detectan anomalías.",
};

const SEVERITY_ICONS = {
  critical: "warning",
  high: "warning",
  moderate: "info",
  none: "check_circle",
};

function confidenceChipClass(confidence) {
  if (confidence >= 80) return "chip--success";
  if (confidence >= 60) return "chip--warning";
  return "chip--error";
}

export default function ResultsPage({ result, onReset }) {
  const navigate = useNavigate();
  const [lightbox, setLightbox] = useState(false);

  if (!result) {
    // Guard: if someone navigates here directly without a result
    return (
      <>
        <TopAppBar showBack />
        <main className="main-content page-container" style={{ textAlign: "center" }}>
          <div className="error-card animate-fade-in">
            <span className="material-symbols-outlined error-card__icon">
              image_not_supported
            </span>
            <p className="error-card__title">Sin resultados</p>
            <p className="error-card__message">
              Sube una imagen primero para obtener un diagnóstico.
            </p>
            <button
              className="btn btn--primary"
              onClick={() => navigate("/")}
            >
              Ir al inicio
            </button>
          </div>
        </main>
        <BottomNavBar />
      </>
    );
  }

  const {
    class_name_es,
    plant,
    confidence,
    is_healthy,
    description,
    severity,
    treatment,
    gradcam_image,
    top_predictions,
  } = result;

  const handleNewAnalysis = () => {
    onReset();
    navigate("/");
  };

  return (
    <>
      <TopAppBar showBack />

      {/* Lightbox */}
      {lightbox && (
        <div className="lightbox" onClick={() => setLightbox(false)}>
          <img
            src={`data:image/png;base64,${gradcam_image}`}
            alt="Mapa de calor Grad-CAM ampliado"
          />
        </div>
      )}

      <main className="main-content page-container stagger">
        {/* Header */}
        <div className="results-header">
          <div>
            <p className="text-label-caps" style={{ color: "var(--secondary)" }}>
              Análisis Completado
            </p>
            <h1 className="text-headline-lg">Resultados del Diagnóstico</h1>
          </div>
          <div className={`chip ${confidenceChipClass(confidence)}`}>
            <span className="material-symbols-outlined filled" style={{ fontSize: 18 }}>
              check_circle
            </span>
            {confidence.toFixed(1)}% de Confianza
          </div>
        </div>

        {/* Bento: Grad-CAM + Diagnosis */}
        <div className="bento-grid">
          {/* Grad-CAM Image */}
           <div className="gradcam-card">
            {gradcam_image ? (
              <img
                className="gradcam-card__image"
                src={`data:image/png;base64,${gradcam_image}`}
                alt="Imagen analizada"
              />
            ) : (
              <div
                className="gradcam-card__image"
                style={{
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  background: "var(--surface-container)",
                }}
              >
                <span
                  className="material-symbols-outlined"
                  style={{ fontSize: 48, color: "var(--outline)" }}
                >
                  image_not_supported
                </span>
              </div>
            )}
            <div className="gradcam-card__label">
              <div
                className={`gradcam-card__label-dot ${
                  is_healthy ? "gradcam-card__label-dot--healthy" : ""
                }`}
              />
              {is_healthy ? "Sin anomalías" : "Focos de Infección"}
            </div>
            <button
              className="gradcam-card__zoom"
              onClick={() => setLightbox(true)}
              aria-label="Ampliar imagen"
            >
              <span className="material-symbols-outlined">zoom_in</span>
            </button>
          </div>

          {/* Diagnosis Data */}
          <div className="diagnosis-card">
            <div>
              <p className="text-label-caps" style={{ color: "var(--on-surface-variant)" }}>
                Especie Detectada
              </p>
              <h3 className="text-title-md diagnosis-card__plant">{plant}</h3>
            </div>

            <hr className="diagnosis-card__divider" />

            <div>
              <p className="text-label-caps" style={{ color: "var(--on-surface-variant)" }}>
                Diagnóstico
              </p>
              <h2 className="text-headline-mobile diagnosis-card__disease">
                {class_name_es}
              </h2>
              <div style={{ marginTop: 8 }}>
                <span className={`severity-badge severity-badge--${severity}`}>
                  {is_healthy ? "Saludable" : severity === "critical" ? "Crítico" : severity === "high" ? "Alto" : "Moderado"}
                </span>
              </div>
            </div>

            <div className={`diagnosis-card__alert diagnosis-card__alert--${severity}`}>
              <span
                className={`material-symbols-outlined filled diagnosis-card__alert-icon diagnosis-card__alert-icon--${severity}`}
              >
                {SEVERITY_ICONS[severity]}
              </span>
              <p className="diagnosis-card__alert-text">
                {SEVERITY_LABELS[severity]}
              </p>
            </div>
          </div>
        </div>

        {/* Description */}
        <div className="info-grid">
          <div className="info-card info-card--description">
            <div className="info-card__header">
              <span className="material-symbols-outlined">description</span>
              <h4 className="text-title-md">Descripción de la Patología</h4>
            </div>
            <p className="text-body-lg info-card__body">{description}</p>
          </div>

          <div className="info-card info-card--treatment">
            <div className="info-card__header">
              <span className="material-symbols-outlined">medical_services</span>
              <h4 className="text-title-md">Acción Recomendada</h4>
            </div>
            <p className="text-body-lg info-card__body" style={{ marginBottom: "var(--space-base)" }}>
              {treatment}
            </p>
          </div>
        </div>

        {/* Top 4 Probabilities Card */}
        {top_predictions && top_predictions.length > 0 && (
          <div className="info-card" style={{ background: "var(--surface-container-low)" }}>
            <div className="info-card__header" style={{ marginBottom: 16 }}>
              <span className="material-symbols-outlined">bar_chart</span>
              <h4 className="text-title-md">Diagnósticos Más Probables</h4>
            </div>
            <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
              {top_predictions.map((pred, i) => (
                <div key={i} style={{ display: "flex", flexDirection: "column", gap: 6 }}>
                  <div style={{ display: "flex", justifyContent: "space-between", fontSize: 14, fontWeight: 600 }}>
                    <span style={{ color: "var(--on-surface)" }}>{pred.class_name_es}</span>
                    <span style={{ color: "var(--primary)" }}>{pred.confidence.toFixed(1)}%</span>
                  </div>
                  <div style={{ height: 8, background: "var(--surface-container-highest)", borderRadius: 4, overflow: "hidden" }}>
                    <div
                      style={{
                        height: "100%",
                        width: `${pred.confidence}%`,
                        background: i === 0 ? "var(--primary)" : "var(--outline)",
                        borderRadius: 4,
                        transition: "width 0.6s ease-out"
                      }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* New Analysis Button */}
        <div style={{ display: "flex", justifyContent: "center", paddingTop: 16 }}>
          <button
            className="btn btn--primary btn--large"
            onClick={handleNewAnalysis}
          >
            <span className="material-symbols-outlined">add_a_photo</span>
            Nuevo Análisis
          </button>
        </div>
      </main>

      <BottomNavBar />
    </>
  );
}
