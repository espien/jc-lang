from __future__ import annotations

from typing import TYPE_CHECKING

from .statements import Function
from .environment import Environment
from .exceptions import ReturnException

if TYPE_CHECKING:
    from .interpreter import Interpreter

class Callable:
    pass

class UserFunction(Callable):
    def __init__(self, declaration: Function):
        self.declaration = declaration

    def call(self, interpreter: Interpreter, arguments: list[object]):
        environment = Environment(interpreter.environment)
        
        for param, arg in zip(self.declaration.params, arguments):
            environment.define(param.lexeme, arg)

        try:
            interpreter.execute_block(self.declaration.body, environment)
        except ReturnException as return_value:
            return return_value.value

        return None
