import cv2  # type: ignore

from src.app import ObjectDetector, TextGenerator

from .MultiProc import MultiProc


class Cli:
    @staticmethod
    def test_main_process(device: int = 0):
        p = MultiProc()
        p.loop(device)
        return

    @staticmethod
    def test_webcam(device: int = 0):
        cap = cv2.VideoCapture(device)
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
