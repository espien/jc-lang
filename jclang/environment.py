from .tokens import Token

class Environment:
    def __init__(self, enclosing = None):
        self.values: dict = {}
        self.enclosing: Environment = enclosing

    def define(self, name: str, value: object) -> None:
        self.values[name] = value

    def get(self, name: Token):
        if name.lexeme in self.values:
            return self.values.get(name.lexeme)
        if self.enclosing is not None:
            return self.enclosing.get(name)
        print("Error, undefined variable")

    def assign(self, name: Token, value: object):
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return
        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return
        print("Error, undefined variable")