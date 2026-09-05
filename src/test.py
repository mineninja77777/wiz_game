# import json
# import os
# from typing import TypedDict

# class CustomDialogue(TypedDict):
#     function: str
#     params: list

# def is_custom_dialogue(x: object) -> bool:
#     if isinstance(x, dict):
#         return x.keys() == CustomDialogue.__annotations__.keys()
#     return False
    

# text = json.load(open(os.path.abspath("src/instances/dialogue.JSON")))
# x = text["events"]["input_name"]
# print(is_custom_dialogue(x))
# raise TypeError("hi")
params: dict[str,str] = {"name": "str", "age": "int"}
new: dict[str,str] = {"age": "int", "hp": "float"}
params.update(new)
print(params)