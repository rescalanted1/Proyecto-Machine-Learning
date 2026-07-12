"""
AgriScan AI — FastAPI application.

POST /predict  →  receives an image, returns disease prediction + Grad-CAM.
"""

from __future__ import annotations
import io, base64
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from .classes import CLASS_INFO, NUM_CLASSES
from .model import predict, get_interpreter  # ← agregar get_interpreter
from .schemas import PredictionResponse

# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------
app = FastAPI(
    title="AgriScan AI",
    description="Plant disease detection API using EfficientNet + Grad-CAM",
    version="1.0.0",
)

# CORS — allow the React dev server and any local origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.on_event("startup")
def load_model():
    print("[INFO] Precargando modelo en startup...")
    get_interpreter()
    print("[INFO] Modelo listo.")


@app.get("/")
def root():
    return {"status": "ok", "message": "AgriScan AI API is running"}


@app.post("/predict", response_model=PredictionResponse)
async def predict_endpoint(file: UploadFile = File(...)):
    """
    Receive an image of a plant leaf and return the predicted disease,
    confidence score, description, and a the same image.
    """
    # --- Validate file type ---
    if file.content_type and not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail=f"El archivo debe ser una imagen. Tipo recibido: {file.content_type}",
        )

    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
    except Exception:
        raise HTTPException(status_code=400, detail="No se pudo leer la imagen.")

    # --- Predict ---
    class_idx, confidence, img_array, raw_preds = predict(image)

    if class_idx >= NUM_CLASSES:
        raise HTTPException(
            status_code=500,
            detail=f"Índice de clase inesperado: {class_idx}",
        )

    info = CLASS_INFO[class_idx]

    # --- Top 4 Predictions ---
    indexed_preds = list(enumerate(raw_preds))
    indexed_preds.sort(key=lambda x: x[1], reverse=True)
    top_predictions = []
    for idx, prob in indexed_preds[:4]:
        idx_info = CLASS_INFO[int(idx)]
        top_predictions.append({
            "class_name_es": idx_info["name_es"],
            "confidence": float(prob) * 100.0
        })
        
    buffered = io.BytesIO()
    image.convert("RGB").save(buffered, format="PNG")
    imagen_b64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return PredictionResponse(
        class_name=info["name"],
        class_name_es=info["name_es"],
        plant=info["plant"],
        confidence=round(confidence, 2),
        is_healthy=info["is_healthy"],
        description=info["description"],
        severity=info["severity"],
        treatment=info["treatment"],
        gradcam_image=imagen_b64,
        top_predictions=top_predictions,
    )
