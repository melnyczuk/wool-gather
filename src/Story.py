from multiprocessing import Queue

from src.TextGenerator import TextGenerator

txtGen = TextGenerator(line_len=50, max_len=500)


class Story:
    queue: Queue

    def __init__(self: "Story", queue: Queue):
        self.queue = queue
        return

    def generate(self: "Story", text_input: str) -> None:
        for sentence in txtGen.get_sentences(text_input):
            self.queue.put(sentence)
        return
