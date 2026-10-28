from typing import Optional
from .tokens import Token
from .expressions import Expression

class Statement:
        pass

class Var(Statement):
    def __init__(self, name: Token, initializer: Expression):
        self.name = name
        self.initializer = initializer
    
    def accept(self, visitor):
        return visitor.visit_var_statement(self)

    def __repr__(self):
        return f"Variable[{self.name.lexeme} {self.initializer}]"

class Print(Statement):
    def __init__(self, expression: Expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_print_statement(self)

    def __repr__(self):
        return f"Print[{self.expression}]"
    
class Block(Statement):
    def __init__(self, statements):
        self.statements = statements

    def accept(self, visitor):
        return visitor.visit_block_statement(self)

    def __repr__(self):
        return f"Block[{self.statements}]"

class If(Statement):
    def __init__(self, condition: Expression, thenBranch: Statement, elseBranch: Statement):
        self.condition = condition
        self.thenBranch = thenBranch
        self.elseBranch = elseBranch

    def accept(self, visitor):
        return visitor.visit_if_statement(self)

    def __repr__(self):
        return f"If[{self.condition} {self.thenBranch} {self.elseBranch}]"
        
class Function(Statement):
    def __init__(self, name: Token, params: list[Token], body: list[Statement]):
        self.name = name
        self.params = params
        self.body = body

    def accept(self, visitor):
        return visitor.visit_function_statement(self)

    def __repr__(self):
        return f"Function[{self.name} {self.params} {self.body}]"
    
class While(Statement):
    def __init__(self, condition: Expression, body: Statement):
        self.condition = condition
        self.body = body

    def accept(self, visitor):
        return visitor.visit_while_statement(self)

    def __repr__(self):
        return f"While[{self.condition} {self.body}]"
    
class Return(Statement):
    def __init__(self, keyword: Token, value: Expression):
        self.keyword = keyword
        self.value = value

    def accept(self, visitor):
        return visitor.visit_return_statement(self)