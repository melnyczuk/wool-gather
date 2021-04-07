import cv2  # type: ignore

from src.MultiProc import MultiProc
from src.ObjectDetector import ObjectDetector
from src.TextGenerator import TextGenerator


class CLI:
    @staticmethod
    def main():
        p = MultiProc()
        p.loop()
        return

    @staticmethod
    def test_webcam():
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow("test", frame)
            cv2.waitKey(0)
        cap.release()
        cv2.destroyAllWindows()
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
        tg = TextGenerator()
        text = input_text
        for i, line in enumerate(tg.get_sentences(text)):
            print(f"{i}:\t", line)
        return


if __name__ == "__main__":
    from fire import Fire  # type: ignore

    Fire(CLI())
