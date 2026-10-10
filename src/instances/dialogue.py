import random
from engine.registries import register_dialogue_func

@register_dialogue_func
def choose_random(lst: list[str]) -> str:
    return random.choice(lst)