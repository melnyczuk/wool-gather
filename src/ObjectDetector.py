from typing import List, Tuple

import cv2  # type: ignore
import numpy as np
from keras.applications import VGG16  # type: ignore
from keras.applications.imagenet_utils import decode_predictions  # type: ignore
from keras.applications.imagenet_utils import preprocess_input  # type: ignore
from tensorflow.python.keras import backend  # type: ignore

Prediction = Tuple[str, str, float]


class ObjectDetector:
    model: VGG16

    def __init__(self: "ObjectDetector"):
        print("init ObjectDetector")
        self.model = VGG16(weights="imagenet")

    def predict(self: "ObjectDetector", frame: np.ndarray) -> List[Prediction]:
        # classify the image
        image = self.__prepare_image(frame)
        preds, *_ = decode_predictions(self.model.predict(image))
        return preds

    def display_prediction(
        self: "ObjectDetector",
        frame: np.ndarray,
        prediction: Prediction,
    ) -> None:
        (_, label, _) = prediction
        cv2.putText(
            frame,
            f"This is a {label}",
            (200, 400),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2,
        )
        cv2.imshow("", frame)
        cv2.waitKey(0)

    def list_predictions(
        self: "ObjectDetector",
        predictions: List[Prediction],
    ) -> None:
        for (i, (_, label, prob)) in enumerate(predictions):
            print("{}. {}: {:.2f}%".format(i + 1, label, prob * 100))
        return

    def __prepare_image(
        self: "ObjectDetector",
        frame: np.ndarray,
    ) -> np.ndarray:
        img = cv2.resize(frame, (224, 224))
        arr = np.array(img[..., ::-1], dtype=backend.floatx())
        exp = np.expand_dims(arr, axis=0)
        return preprocess_input(exp)
