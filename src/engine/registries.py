from collections.abc import Callable

dialogue_funcs_registry: dict[str, Callable[..., str]] = {}

def register_dialogue_func(func: Callable[..., str]):
    dialogue_funcs_registry[func.__name__] = func
    return func


action_registry: list[type] = []

def register_action(cls: type) -> type:
    action_registry.append(cls)
    return cls


class_registry: list[type] = []

def register_class(cls: type) -> type:
    class_registry.append(cls)
    return cls


enemy_registry: list[type] = []

def register_enemy(cls: type) -> type:
    enemy_registry.append(cls)
    return cls
