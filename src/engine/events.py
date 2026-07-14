class Event:
    kind: str
    params: dict[str, object]
    
    def __init__(self, kind: str, /, *args: object, **kwargs: object) -> None:
        self.kind = kind
        self.params = kwargs
