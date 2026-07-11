import { useState } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage.jsx";
import ResultsPage from "./pages/ResultsPage.jsx";

export default function App() {
  const [analysisResult, setAnalysisResult] = useState(null);

  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/"
          element={<HomePage onResult={setAnalysisResult} />}
        />
        <Route
          path="/results"
          element={
            <ResultsPage
              result={analysisResult}
              onReset={() => setAnalysisResult(null)}
            />
          }
        />
      </Routes>
    </BrowserRouter>
  );
}
