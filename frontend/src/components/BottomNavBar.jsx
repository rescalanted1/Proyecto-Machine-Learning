import { useNavigate, useLocation } from "react-router-dom";

export default function BottomNavBar() {
  const navigate = useNavigate();
  const location = useLocation();
  const isHome = location.pathname === "/";

  return (
    <nav className="bottom-nav">
      <button
        className={`bottom-nav__item ${isHome ? "active" : ""}`}
        onClick={() => navigate("/")}
      >
        <span className={`material-symbols-outlined ${isHome ? "filled" : ""}`}>
          dashboard
        </span>
        <span className="bottom-nav__label">Dashboard</span>
      </button>
      <button
        className={`bottom-nav__item ${!isHome ? "active" : ""}`}
        onClick={() => { }}
      >
        <span className={`material-symbols-outlined ${!isHome ? "filled" : ""}`}>
          photo_camera
        </span>
        <span className="bottom-nav__label">Análisis</span>
      </button>
      {/*<button className="bottom-nav__item" onClick={() => {}}>
        <span className="material-symbols-outlined">database</span>
        <span className="bottom-nav__label">Biblioteca</span>
      </button>*/}
    </nav>
  );
}
