import os
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


class TextGenerator:
    line_len: int
    max_len: int
    generator: Pipeline
    model_dir: str

    def get_sentences(
        self: "TextGenerator",
        seed_str: str,
    ) -> List[str]:
        return wrap(self.__generate(seed_str), self.line_len)

    def __init__(
        self: "TextGenerator",
        model_dir: str = "data",
        line_len: int = 20,
        max_len: int = 100,
    ) -> None:
        self.line_len = line_len
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
        set_seed(42)
        return

    def __generate(self: "TextGenerator", input: str) -> str:
        data, *_ = self.generator(
            input[: self.max_len - 1],
            max_length=self.max_len,
            num_return_sequences=1,
        )
        return self.__clean(data["generated_text"])

    def __clean(self: "TextGenerator", input: str) -> str:
        return input.replace("\n", " ").replace('"', "")

    def __model_path(self: "TextGenerator", target_file: str) -> str:
        return os.path.join(self.model_dir, target_file)
