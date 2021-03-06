from typing import List, Tuple

import cv2  # type: ignore
import numpy as np
from keras.applications import VGG16, imagenet_utils  # type: ignore
from tensorflow.python.keras import backend  # type: ignore

Prediction = Tuple[str, str, float]


class ObjectDetector:
    model: VGG16

    def __init__(self: "ObjectDetector"):
        self.model = VGG16(weights="imagenet")

    def predict(self: "ObjectDetector", frame: np.ndarray) -> List[Prediction]:
        image = self.__prepare_image(frame)
        prediction = self.model.predict(image)
        class_names, *_ = imagenet_utils.decode_predictions(prediction)
        return class_names

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
        return imagenet_utils.preprocess_input(exp)
