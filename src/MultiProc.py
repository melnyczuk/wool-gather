from multiprocessing import Process, Queue

import cv2  # type:ignore
import numpy as np


class MultiProc:
    def loop(self: "MultiProc"):
        from src.Story import Story

        queue: Queue = Queue(8)
        story = Story(queue)
        process = None
        i = 0
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            if i % 100 == 0:
                caption = "..." if queue.empty() else queue.get()
                if not process or not process.is_alive():
                    print("new process")
                    process = None  # do I need this?
                    label = self.__generate_label(frame, caption)
                    process = Process(target=story.generate, args=(label,))
                    process.start()
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
        from src.ObjectDetector import ObjectDetector

        self.od = ObjectDetector()
        return

    def __generate_label(self: "MultiProc", frame: np.ndarray, caption: str):
        (_, label, _), *_ = self.od.predict(frame)
        return f"{caption}. A {label.replace('_', ' ')}"
