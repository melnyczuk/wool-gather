from random import randint
from textwrap import wrap
from typing import List

from transformers import logging, pipeline, set_seed  # type: ignore
from transformers.pipelines.base import Pipeline  # type: ignore


class TextGenerator:
    line_len: int
    max_len: int
    generator: Pipeline

    def get_sentences(
        self: "TextGenerator",
        seed_str: str,
    ) -> List[str]:
        return wrap(self.__generate(seed_str), self.line_len)

    def __init__(
        self: "TextGenerator", line_len: int = 20, max_len: int = 100
    ) -> None:
        print("init TextGenerator")
        self.line_len = line_len
        self.max_len = max_len
        logging.set_verbosity_error()
        self.generator = pipeline("text-generation", model="gpt2")
        set_seed(randint(42, 84))
        return

    def __clean(self: "TextGenerator", input: str) -> str:
        return input.replace("\n", " ").replace('"', "")

    def __generate(self: "TextGenerator", input: str) -> str:
        data, *_ = self.generator(
            input[: self.max_len - 1],
            max_length=self.max_len,
            num_return_sequences=1,
        )
        return self.__clean(data["generated_text"])
