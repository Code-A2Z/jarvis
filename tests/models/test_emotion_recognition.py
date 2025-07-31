import os
import sys
import numpy as np
import cv2
import pytest
from unittest.mock import patch, MagicMock

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from src.apps.pages.models.ImageProcessing import emotion_recognition as er



def test_preprocess_image_shape():
    # Create dummy BGR image (100x100)
    img = np.ones((100, 100, 3), dtype=np.uint8) * 255
    processed = er.preprocess_image(img)
    
    # Should be normalized and reshaped to (1, 48, 48, 1)
    assert processed.shape == (1, 48, 48, 1)
    assert np.all((processed >= 0) & (processed <= 1))


@patch("emotion_recognition.downloadNotebookOutput")
def test_ensure_model_download(mock_download):
    # Ensure model path does not exist
    model_path = er.MODEL_PATH
    if os.path.exists(model_path):
        os.remove(model_path)

    # Mock download
    mock_download.return_value = None

    # Call ensure_model
    with patch("os.path.exists", side_effect=[False, True]):
        result = er.ensure_model()
        assert result == er.MODEL_PATH
        mock_download.assert_called_once()


def test_predict_with_custom_model():
    # Mock model with fake predict
    mock_model = MagicMock()
    mock_model.predict.return_value = np.array([[0, 0, 0, 1, 0, 0, 0]])

    # Dummy image
    img = np.ones((48, 48, 3), dtype=np.uint8)
    emotion, confidence = er.predict_with_custom_model(mock_model, img)

    assert emotion == "Happy"
    assert confidence == 1.0


@patch("emotion_recognition.DeepFace.analyze")
def test_predict_with_deepface(mock_analyze):
    # Mock DeepFace output
    mock_analyze.return_value = [{
        "dominant_emotion": "Sad",
        "emotion": {"Sad": 99.0, "Happy": 1.0}
    }]

    # Dummy numpy image
    img = np.ones((48, 48, 3), dtype=np.uint8)
    emotion, scores = er.predict_with_deepface(img)

    assert emotion == "Sad"
    assert "Sad" in scores
