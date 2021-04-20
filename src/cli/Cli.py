import cv2  # type: ignore
from fire import Fire  # type: ignore

from src.app import ObjectDetector, TextGenerator

from .MultiProc import MultiProc


class Cli:
    def __init__(self: "Cli"):
        Fire(self)

    @staticmethod
    def test_main_process(device: int = 0):
        p = MultiProc()
        p.loop(device)
        return

    @staticmethod
    def detect_object(input_path: str):
        objD = ObjectDetector()
        frame = cv2.imread(input_path)
        predictions = objD.predict(frame)
        objD.list_predictions(predictions)
        objD.display_prediction(frame, predictions[0])
        return

    @staticmethod
    def generate_text(input_text: str):
        tg = TextGenerator(model_dir="data/folktales")
        text = input_text
        for i, line in enumerate(tg.lines(text)):
            print(f"{i}:\t", line)
        return


if __name__ == "__main__":
    Cli()
