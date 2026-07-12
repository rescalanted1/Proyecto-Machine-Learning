import { useState, useCallback } from "react";

const API_BASE_URL = import.meta.env.VITE_API_URL ?? "";
/**
 * Custom hook to manage the analysis API call.
 *
 * Returns:
 *   status: "idle" | "loading" | "success" | "error"
 *   data: PredictionResponse | null
 *   error: string | null
 *   analyze: (file: File) => Promise<PredictionResponse>
 *   reset: () => void
 */
export default function useAnalysis() {
  const [status, setStatus] = useState("idle");
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  const analyze = useCallback(async (file) => {
    setStatus("loading");
    setError(null);
    setData(null);

    const formData = new FormData();
    formData.append("file", file);

    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 60000);

    try {
      const url = API_BASE_URL                                      
        ? new URL("/predict", API_BASE_URL).toString()                
        : "/predict";                                                  
      const response = await fetch(url, {
        method: "POST",
        body: formData,
        signal: controller.signal,
      });

      clearTimeout(timeout);

      if (!response.ok) {
        const body = await response.json().catch(() => ({}));
        throw new Error(body.detail || `Error del servidor (${response.status})`);
      }

      const result = await response.json();
      setData(result);
      setStatus("success");
      return result;
    } catch (err) {
      clearTimeout(timeout);
      const message =
        err.name === "AbortError"
          ? "La solicitud tardó demasiado. Intente de nuevo."
          : err.message || "Error desconocido.";
      setError(message);
      setStatus("error");
      throw err;
    }
  }, []);

  const reset = useCallback(() => {
    setStatus("idle");
    setData(null);
    setError(null);
  }, []);

  return { status, data, error, analyze, reset };
}
