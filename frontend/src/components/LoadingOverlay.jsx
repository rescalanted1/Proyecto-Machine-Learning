export default function LoadingOverlay() {
  return (
    <div className="loading-overlay">
      <div className="loading-spinner" />
      <div className="loading-text">
        <p className="loading-text__title">Analizando muestra…</p>
        <p className="loading-text__sub">
          Ejecutando modelo EfficientNet y generando mapa de calor Grad-CAM
        </p>
      </div>
      <div className="loading-bar">
        <div className="loading-bar__fill" />
      </div>
    </div>
  );
}
