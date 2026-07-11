import { useNavigate, useLocation } from "react-router-dom";

export default function TopAppBar({ showBack = false }) {
  const navigate = useNavigate();

  return (
    <header className="top-app-bar">
      <div className="top-app-bar__brand">
        {showBack ? (
          <button
            className="icon-btn"
            aria-label="Volver al inicio"
            onClick={() => navigate("/")}
          >
            <span className="material-symbols-outlined">arrow_back</span>
          </button>
        ) : (
          <span className="material-symbols-outlined filled top-app-bar__logo">
            eco
          </span>
        )}
        <h1 className="top-app-bar__title">AgriScan AI</h1>
      </div>
    </header>
  );
}
