import os
import re
from textwrap import wrap
from typing import List

from transformers import (  # type: ignore
    GPT2Config,
    GPT2LMHeadModel,
    GPT2Tokenizer,
    logging,
    pipeline,
    set_seed,
)
from transformers.pipelines.base import Pipeline  # type: ignore
from unidecode import unidecode


class TextGenerator:
    max_len: int
    generator: Pipeline
    model_dir: str

    def generate(self: "TextGenerator", seed_str: str) -> str:
        data, *_ = self.generator(
            seed_str[: self.max_len - 1],
            max_length=self.max_len,
            num_return_sequences=1,
        )
        return self.__clean(data["generated_text"])

    def lines(
        self: "TextGenerator", seed_str: str, line_len: int = 20
    ) -> List[str]:
        return wrap(self.generate(seed_str), line_len)

    def sentences(
        self: "TextGenerator", seed_str: str, line_len: int = 20
    ) -> List[str]:
        return [
            line
            for sentence in self.__split_sentences(self.generate(seed_str))
            for line in wrap(sentence, line_len)
        ]

    def __init__(
        self: "TextGenerator",
        model_dir: str = "data",
        max_len: int = 100,
        seed: int = 42,
    ) -> None:
        self.max_len = max_len
        self.model_dir = os.path.abspath(model_dir)
        logging.set_verbosity_error()
        config = GPT2Config.from_pretrained("gpt2")
        tokenizer = GPT2Tokenizer(
            self.__model_path("encoder.json"),
            self.__model_path("vocab.bpe"),
        )
        model = GPT2LMHeadModel.from_pretrained(self.model_dir, config=config)
        self.generator = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
        )
        set_seed(seed)
        return

    def __model_path(self: "TextGenerator", target_file: str) -> str:
        return os.path.join(self.model_dir, target_file)

    def __clean(self: "TextGenerator", input_str: str) -> str:
        [*tmps, _] = self.__split_sentences(input_str)
        return " ".join(tmps)

    def __split_sentences(self: "TextGenerator", input_str: str) -> List[str]:
        return re.sub(
            r"([.!?;])\s*([a-zA-Z])",
            lambda m: f"{m.groups()[0]}|{m.groups()[1]}",
            unidecode(input_str).replace("\n", " ").replace('"', ""),
        ).split("|")
