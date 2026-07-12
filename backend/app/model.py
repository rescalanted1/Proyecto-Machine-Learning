"""
Model loading and prediction for EfficientNet TFLite.

- Loads the .tflite model once at startup.
- Preprocesses images for EfficientNet (224×224).
"""

from __future__ import annotations
from pathlib import Path
import numpy as np
from PIL import Image, ImageOps
import tflite_runtime.interpreter as tflite

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
MODEL_PATH = Path(__file__).resolve().parent.parent / "modelo_efficientnet.tflite"
IMG_SIZE = (224, 224)

# ---------------------------------------------------------------------------
# Singleton TFLite Interpreter loader
# ---------------------------------------------------------------------------
_interpreter = None
_input_details = None
_output_details = None


def get_interpreter() -> tuple[tflite.Interpreter, list[dict], list[dict]]:
    """Load the TFLite interpreter once and cache it."""
    global _interpreter, _input_details, _output_details
    if _interpreter is None:
        _interpreter = tflite.Interpreter(model_path=str(MODEL_PATH))
        _interpreter.allocate_tensors()
        _input_details = _interpreter.get_input_details()
        _output_details = _interpreter.get_output_details()
        print(f"[INFO] TFLite Model loaded from {MODEL_PATH}")
        print(f"[INFO] Input details : {_input_details}")
        print(f"[INFO] Output details: {_output_details}")
    return _interpreter, _input_details, _output_details


# ---------------------------------------------------------------------------
# Image preprocessing
# ---------------------------------------------------------------------------

def preprocess_image(image: Image.Image) -> np.ndarray:
    """
    Resize and preprocess a PIL Image for EfficientNet.
    Applies EXIF transposition (auto-rotation) and BILINEAR resizing to match training.
    """    
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
    # Thus, values remain in [0, 255] and we just expand the dimensions.
    return np.expand_dims(arr, axis=0)


# ---------------------------------------------------------------------------
# Prediction
# ---------------------------------------------------------------------------

def predict(image: Image.Image) -> tuple[int, float, np.ndarray, np.ndarray]:
    """
    Run inference on a PIL Image using TFLite.

    Returns
    -------
    class_idx : int
    confidence : float  (0–100)
    img_array : np.ndarray  (preprocessed, shape (1, 224, 224, 3))
    raw_preds : np.ndarray (probabilities for all classes)
    """
    interpreter, input_details, output_details = get_interpreter()
    img_array = preprocess_image(image)
    
    # Set input tensor
    interpreter.set_tensor(input_details[0]['index'], img_array)
    
    # Run inference
    interpreter.invoke()
    
    # Get output tensor
    preds = interpreter.get_tensor(output_details[0]['index'])
    
    raw_preds = preds[0]
    class_idx = int(np.argmax(raw_preds))
    confidence = float(np.max(raw_preds)) * 100.0
    return class_idx, confidence, img_array, raw_preds


# ---------------------------------------------------------------------------
# Grad-CAM
# ---------------------------------------------------------------------------
# Image return
# ---------------------------------------------------------------------------


