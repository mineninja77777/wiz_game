import random
from engine.registries import register_dialogue_func

@register_dialogue_func
def choose_random(*lst: str) -> str:
    return random.choice(lst)

@register_dialogue_func
def conditional_pick(*options: dict[str, str]) -> str: 
    # options is a list of singleton dicts, so that order is preserved
    def eval_(stmt: str) -> bool | float:
        stmt = stmt.replace(" ", "")
        stmt = stmt.replace("\n", "")

        rpn_stmt: list[str] = []
        operator_stack = []
        # convert to RPN -- note: 
        operators: dict[str, int] = {
            '—': 4,
            '*': 3,
            '/': 3,
            '+': 2,
            '-': 2,
            '<': 1,
            '<=': 1,
            '>': 1,
            '>=': 1,
            '==': 0,
            '=': 0,
            '!=': 0,
            '&&': -1,
            '||': -2
        }
        i = 0
        current = ""
        while i < len(stmt):
            current += stmt[i]
            i += 1

            if current[-1] in "0123456789." and (i >= len(stmt) or not stmt[i] in "0123456789."):
                rpn_stmt.append(current)
                current = ""
            elif current in operators.keys():
                if current == '-' and not (i != 0 and i != 1 and stmt[i-2] in "0123456789."):
                    # negation
                    current = "—"
                elif current == '<' and stmt[i] == '=':
                    current += stmt[i]
                    i += 1
                elif current == '>' and stmt[i] == '=':
                    current += stmt[i]
                    i += 1
                elif current == '=' and stmt[i] == '=':
                    current += stmt[i]
                    i += 1
                elif current == '!' and stmt[i] == '=':
                    current += stmt[i]
                    i += 1
                elif current == '&' and stmt[i] == '&':
                    current += stmt[i]
                    i += 1
                elif current == '|' and stmt[i] == '|':
                    current += stmt[i]
                    i += 1



                while (len(operator_stack) > 0) and (operator_stack[-1] != '(') and (operators[operator_stack[-1]] >= operators[current]):
                    rpn_stmt.append(operator_stack.pop())
                operator_stack.append(current)
                current = ""
            elif current == '(':
                operator_stack.append(current)
                current = ""
            elif current == ')':
                current = ""
                while operator_stack[-1] != '(':
                    rpn_stmt.append(operator_stack.pop())
                operator_stack.pop()

        while len(operator_stack) > 0:
            rpn_stmt.append(operator_stack.pop())
        

        # eval
        stack: list[bool | float] = []

        for char in rpn_stmt:
            if char == "—":
                stack.append(-stack.pop())
            elif char == "+":
                stack.append(stack.pop() + stack.pop())
            elif char == "-":
                stack.append(-stack.pop() + stack.pop())
            elif char == "*":
                stack.append(stack.pop() * stack.pop())
            elif char == "/":
                stack.append(1/stack.pop() * stack.pop())
            elif char == "<":
                stack.append(stack.pop() > stack.pop())
            elif char == "<=":
                stack.append(stack.pop() >= stack.pop())
            elif char == ">":
                stack.append(stack.pop() < stack.pop())
            elif char == ">=":
                stack.append(stack.pop() <= stack.pop())
            elif char == "==" or char == '=':
                stack.append(stack.pop() == stack.pop())
            elif char == "!=":
                stack.append(stack.pop() != stack.pop())
            elif char == "&&" or char == '&':
                stack.append(stack.pop() and stack.pop())
            elif char == "||" or char == '|':
                stack.append(stack.pop() or stack.pop())
            else:
                stack.append(float(char))
        
        return stack[-1]
    
    for stmt in options:
        key = list(stmt.keys())[0]
        if key == "default":
            return stmt[key]
        else:
            if eval_(key):
                return stmt[key]

    
    return "\0"