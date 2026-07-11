action_registry: list[type] = []

def register_action(cls):
    action_registry.append(cls)
    return cls


class_registry: list[type] = []

def register_class(cls):
    class_registry.append(cls)
    return cls


enemy_registry: list[type] = []

def register_enemy(cls):
    enemy_registry.append(cls)
    return cls