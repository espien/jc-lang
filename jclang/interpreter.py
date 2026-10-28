from .expressions import Binary, Expression, Literal, Unary, Grouping, Variable, Assignment, Call
from .statements import Print, Statement, Var, If, While, Block, Function, Return
from .tokens import Token, TokenTypes as tokentypes
from .environment import Environment
from .callables import UserFunction
from .exceptions import ReturnException

class Interpreter:
    def __init__(self):
        self = self
        self.environment = Environment()

    def interpret(self, statements):
        for statement in statements:
            self.execute(statement)

    def execute(self, statement: Statement):
        return statement.accept(self)

    def visit_function_statement(self, stmt: Function):
        function = UserFunction(stmt)
        self.environment.define(stmt.name.lexeme, function)
        return None

    def visit_return_statement(self, stmt: Return):
        value = None
        if stmt.value is not None:
            value = self.evaluate(stmt.value)
        raise ReturnException(value)

    def visit_call_expression(self, expr: Call):
        callee = self.evaluate(expr.callee)

        arguments = []
        for argument in expr.arguments:
            arguments.append(self.evaluate(argument))

        function: UserFunction = callee
        return function.call(self, arguments)

    def visit_print_statement(self, stmt: Print):
        value = self.evaluate(stmt.expression)
        print(value)
        return None
    
    def visit_block_statement(self, stmt: Block):
        self.execute_block(stmt.statements, Environment(self.environment))
        return None

    def visit_if_statement(self, stmt: If):
        if Interpreter.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.thenBranch)
        elif stmt.elseBranch is not None:
            self.execute(stmt.elseBranch)
        return None

    def visit_while_statement(self, stmt: While):
        while Interpreter.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.body)
        return None

    def visit_assignment_expression(self, expr: Assignment):
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value

    def visit_var_statement(self, stmt: Var):
        value = None
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)
        
        self.environment.define(stmt.name.lexeme, value)
        return None
        
    def visit_variable_expression(self, expr: Variable):
        return self.environment.get(expr.name)

    def visit_literal_expression(self, expr: Literal):
        return expr.value
    
    def visit_grouping_expression(self, expr: Grouping):
        return self.evaluate(expr.expression)
    
    def visit_unary_expression(self, expr: Unary):
        right = self.evaluate(expr.right)
        operator_type = expr.operator.type
        match operator_type:
            case tokentypes.EXCLAMATION:
                return not Interpreter.is_truthy(right)
            case tokentypes.MINUS:
                self.check_number_operand(expr.operator, right)
                return -right
            
        return None
    
    def check_number_operand(self, operator: Token, operand):
        if isinstance(operand, (int, float)):
            return
        raise SyntaxError(f"{operator}, Operand must be a number.")


    def is_truthy(object):
        if object is None:
            return False
        if isinstance(object, bool):
            return object
        return True

    def visit_binary_expression(self, expr: Binary):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)
        operator_type = expr.operator.type

        match operator_type:
            case tokentypes.PLUS:
                if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                    return left + right
                if isinstance(left, str) and isinstance(right, str):
                    return left + right
            case tokentypes.MINUS:
                self.check_number_operands(expr, left, right)
                return left - right
            case tokentypes.SLASH:
                self.check_number_operands(expr, left, right)
                return left / right
            case tokentypes.STAR:
                self.check_number_operands(expr, left, right)
                return left * right
            case tokentypes.GREATER:
                self.check_number_operands(expr, left, right)
                return left > right
            case tokentypes.GREATER_EQUAL:
                self.check_number_operands(expr, left, right)
                return left >= right
            case tokentypes.LESS:
                self.check_number_operands(expr, left, right)
                return left < right
            case tokentypes.LESS_EQUAL:
                self.check_number_operands(expr, left, right)
                return left <= right
            case tokentypes.EXCLAMATION_EQUAL:
                return not self.is_equal(left, right)
            case tokentypes.EQUAL_EQUAL:
                return self.is_equal(left, right)
        
        return None

    def execute_block(self, statements, environment):
        previous = self.environment
        try:
            self.environment = environment

            for statement in statements:
                self.execute(statement)
                
        finally:
            self.environment = previous

    def check_number_operands(self, operator, left, right):
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return
        raise SyntaxError(f"{operator}, Operands must be a number.")

    def is_equal(self, a, b):
        if a is None and b is None:
            return True
        if a is None:
            return False
        
        return a == b

    def evaluate(self, expr: Expression):
        return expr.accept(self)