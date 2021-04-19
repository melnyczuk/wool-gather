from multiprocessing import Process, Queue

import cv2  # type:ignore
import numpy as np


class Story:
    def generate(self: "Story", text_input: str) -> None:
        from src.app import TextGenerator

        txtGen = TextGenerator(line_len=50, max_len=500)
        for sentence in txtGen.get_sentences(text_input):
            self.queue.put(sentence)
        return

    def __init__(self: "Story", queue: Queue):
        self.queue = queue
        return


class MultiProc:
    def loop(self: "MultiProc", device=0):
        queue: Queue = Queue(8)
        story = Story(queue)
        process = None
        i = 0
        cap = cv2.VideoCapture(device)

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            if i % 100 == 0:
                caption = "..." if queue.empty() else queue.get()
                if not process or not process.is_alive():
                    label = self.__generate_label(frame, caption)
                    process = Process(target=story.generate, args=(label,))
                    process.start()
            cv2.putText(frame, label, (100, 100), 0, 0.5, (255, 100, 100), 2)
            cv2.putText(frame, caption, (100, 600), 0, 0.8, (255, 255, 255), 2)
            cv2.imshow("frame", frame)
            i += 1
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        if process:
            process.kill()
        cap.release()
        cv2.destroyAllWindows()
        return

    def __init__(self: "MultiProc"):
        from src.app import ObjectDetector

        self.od = ObjectDetector()
        return

    def __generate_label(self: "MultiProc", frame: np.ndarray, caption: str):
        (_, label, _), *_ = self.od.predict(frame)
        return f"{caption}. A {label.replace('_', ' ')}"
