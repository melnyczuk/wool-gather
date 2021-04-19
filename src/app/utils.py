import random
from typing import List

SEEDS = [
    "A {} and a {} and a {}",
    "What does the future hold for {}?",
    "I saw a {} with a {} holding a {}",
    "A {} can tell you the future using a {}",
    "Ask what a {} is for. Can a {} help you?",
    "The man wanted a {} for predicting the future",
]


def seed_from(labels: List[str]) -> str:
    clean = (lab.replace("_", " ") for lab in labels[::-1])
    return random.choice(SEEDS).format(*clean)
