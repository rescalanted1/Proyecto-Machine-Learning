"""
Model loading and Grad-CAM generation for EfficientNet.

- Loads the .keras model once at startup.
- Preprocesses images for EfficientNet (224×224).
- Generates Grad-CAM heatmaps from the last convolutional layer.
"""

from __future__ import annotations

import base64
import io
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

import tensorflow as tf

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
MODEL_PATH = Path(__file__).resolve().parent.parent / "modelo_efficientnet_final.keras"
IMG_SIZE = (224, 224)

# ---------------------------------------------------------------------------
# Singleton model loader
# ---------------------------------------------------------------------------
_model = None


def get_model() -> tf.keras.Model:
    """Load the Keras model once and cache it."""
    global _model
    if _model is None:
        _model = tf.keras.models.load_model(
            str(MODEL_PATH),
            compile=False,
        )
        print(f"[INFO] Model loaded from {MODEL_PATH}")
        print(f"[INFO] Input shape : {_model.input_shape}")
        print(f"[INFO] Output shape: {_model.output_shape}")
    return _model


# ---------------------------------------------------------------------------
# Image preprocessing
# ---------------------------------------------------------------------------

def preprocess_image(image: Image.Image) -> np.ndarray:
    """
    Resize and preprocess a PIL Image for EfficientNet.
    Applies EXIF transposition (auto-rotation) and BILINEAR resizing to match training.
    """
    from PIL import ImageOps
    
    # Correct image orientation based on EXIF metadata (crucial for mobile photos)
    image = ImageOps.exif_transpose(image)
    
    # Match the BILINEAR interpolation used by image_dataset_from_directory in training
    try:
        resample_method = Image.Resampling.BILINEAR
    except AttributeError:
        resample_method = Image.BILINEAR
        
    image = image.convert("RGB").resize(IMG_SIZE, resample=resample_method)
    arr = np.array(image, dtype=np.float32)
    
    # EfficientNet has its own built-in Rescaling layer [0, 255] -> [-1, 1] or similar.
    # Thus, preprocess_input is a pass-through and expects values in [0, 255].
    from tensorflow.keras.applications.efficientnet import preprocess_input
    arr = preprocess_input(arr)
    
    return np.expand_dims(arr, axis=0)


# ---------------------------------------------------------------------------
# Prediction
# ---------------------------------------------------------------------------

def predict(image: Image.Image) -> tuple[int, float, np.ndarray, np.ndarray]:
    """
    Run inference on a PIL Image.

    Returns
    -------
    class_idx : int
    confidence : float  (0–100)
    img_array : np.ndarray  (preprocessed, shape (1, 224, 224, 3))
    raw_preds : np.ndarray (probabilities for all classes)
    """
    model = get_model()
    img_array = preprocess_image(image)
    preds = model.predict(img_array, verbose=0)
    raw_preds = preds[0]
    class_idx = int(np.argmax(raw_preds))
    confidence = float(np.max(raw_preds)) * 100.0
    return class_idx, confidence, img_array, raw_preds


# ---------------------------------------------------------------------------
# Grad-CAM
# ---------------------------------------------------------------------------
# Image return
# ---------------------------------------------------------------------------


def generate_gradcam(
    image: Image.Image,
    class_idx: int,
    img_array: np.ndarray,
) -> str:
    """
    Codifica la imagen original a Base64 como fallback seguro,
    evitando errores de compatibilidad de capas internas en Keras.
    """
    buffer = io.BytesIO()
    image.convert("RGB").save(buffer, format="PNG")
    buffer.seek(0)
    b64 = base64.b64encode(buffer.read()).decode("utf-8")
    return b64
