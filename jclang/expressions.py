from .tokens import Token

class Expression:
        pass

class Binary(Expression):
    def __init__(self, left: Expression, operator: Token, right: Expression):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_binary_expression(self)

    def __repr__(self):
        return f"Binary[{self.left} {self.operator.lexeme} {self.right}]"

class Grouping(Expression):
    def __init__(self, expression: Expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_grouping_expression(self)

    def __repr__(self):
        return f"Grouping[{self.expression}]"

class Unary(Expression):
    def __init__(self, operator: Token, right: Expression):
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_unary_expression(self)
    
    def __repr__(self):
        return f"Unary[{self.operator} {self.right}]"

class Literal(Expression):
    def __init__(self, value: object):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_literal_expression(self)

    def __repr__(self):
        return f"Literal[{self.value}]"

class Variable(Expression):
    def __init__(self, name: Token):
        self.name = name

    def accept(self, visitor):
        return visitor.visit_variable_expression(self)
    
    def __repr__(self):
        return f"Variable[{self.name.lexeme}]"
    
class Assignment(Expression):
    def __init__(self, name: Token, value: Expression):
        self.name = name
        self.value = value

    def accept(self, visitor):
        return visitor.visit_assignment_expression(self)

    def __repr__(self):
        return f"Assignment[{self.name} {self.value}]"
    
class Call(Expression):
    def __init__(self, callee: Expression, arguments: list[Expression]):
        self.callee = callee
        self.arguments = arguments

    def accept(self, visitor):
        return visitor.visit_call_expression(self)
    
    def __repr__(self):
        return f"Call[{self.callee} {self.arguments}]"
    