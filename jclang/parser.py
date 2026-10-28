from .tokens import Token, TokenTypes as tokentypes
from .expressions import Binary, Expression, Literal, Variable, Unary, Assignment, Call
from .statements import Statement, Var, Print, If, While, Block, Function, Return

class Parser:
    def __init__(self, tokens: list[Token]):
        self.position = 0
        self.tokens = tokens

    def parse(self) -> list[Statement]:
        statements: list[Statement] = []
        while not self.is_at_end():
            statements.append(self.declaration())
        return statements

    def declaration(self) -> Statement:
        if self.match(token_types=[tokentypes.FUNCTION]):
            return self.function()
        if self.match(token_types=[tokentypes.RETURN_KEY]):
            return self.return_statement()
        if self.match(token_types=[tokentypes.VAR]):
            return self.var_declaration()
        return self.statement()
    
    def statement(self) -> Statement:
        if self.match(token_types=[tokentypes.IF]):
            return self.if_statement()
        if self.match(token_types=[tokentypes.ELSE]):
            self.consume(token_type=tokentypes.LEFT_BRACE)
            return self.statement()
        if self.match(token_types=[tokentypes.PRINT]):
            return self.print_statement()
        if self.match(token_types=[tokentypes.WHILE]):
            return self.while_statement()
        if self.match(token_types=[tokentypes.LOGIC_KEY]):
            return Block(self.block())
        return self.expression()

    def return_statement(self) -> Statement:
        keyword = self.previous()
        value = None
        self.consume(tokentypes.COLON)
        self.consume(tokentypes.LEFT_BRACE)
        self.consume_key_and_colon(tokentypes.VALUE_KEY)
        value = self.expression()

        self.consume(tokentypes.RIGHT_BRACE)
        return Return(keyword, value)

    def function(self) -> Statement:
        self.consume(tokentypes.LEFT_BRACE)
        self.consume_key_and_colon(tokentypes.NAME_KEY)
        name = self.consume(tokentypes.IDENTIFIER)

        self.consume(tokentypes.COMMA)
        self.consume_key_and_colon(tokentypes.PARAMETERS_KEY)
        self.consume(tokentypes.LEFT_BRACE)

        parameters: list[Token] = []

        while not self.check(tokentypes.RIGHT_BRACE):
            self.consume_key_and_colon(tokentypes.PARAM_KEY)
            param = self.consume(tokentypes.IDENTIFIER)
            parameters.append(param)

            if not self.match([tokentypes.COMMA]):
                break

        self.consume(tokentypes.RIGHT_BRACE)
        self.consume(tokentypes.COMMA)
        self.consume(tokentypes.LOGIC_KEY)

        body = self.block()

        self.consume(tokentypes.RIGHT_BRACE)

        return Function(name, parameters, body)

    def var_declaration(self) -> Statement:
        self.consume(token_type=tokentypes.LEFT_BRACE)
        self.consume_key_and_colon(key_type=tokentypes.NAME_KEY)

        name = self.consume(token_type=tokentypes.IDENTIFIER)
        initializer = None
        if self.match(token_types=[tokentypes.COMMA]):
            self.consume_key_and_colon(key_type=tokentypes.VALUE_KEY)
            initializer = self.expression()
        
        self.consume(token_type=tokentypes.RIGHT_BRACE)
        return Var(name, initializer)

    def block(self):
        statements = []
        self.consume(token_type=tokentypes.COLON)
        self.consume(token_type=tokentypes.LEFT_BRACE)

        while not self.check(tokentypes.RIGHT_BRACE) and not self.is_at_end():
            statements.append(self.declaration())

        self.consume(token_type=tokentypes.RIGHT_BRACE)
        return statements

    def if_statement(self) -> Statement:
        self.consume(token_type=tokentypes.LEFT_BRACE)
        self.consume_key_and_colon(key_type=tokentypes.CONDITION_KEY)
        condition: Expression = self.expression()

        self.consume(token_type=tokentypes.COMMA)
        thenBranch: Statement = self.statement()
        elseBranch: Statement = None
        if self.match(token_types=[tokentypes.COMMA]):
            elseBranch = self.statement()
            self.consume(token_type=tokentypes.RIGHT_BRACE)

        self.consume(token_type=tokentypes.RIGHT_BRACE)
        return If(condition, thenBranch, elseBranch)
    
    def while_statement(self) -> Statement:
        self.consume(token_type=tokentypes.LEFT_BRACE)
        self.consume_key_and_colon(key_type=tokentypes.CONDITION_KEY)
        condition: Expression = self.expression()

        self.consume(token_type=tokentypes.COMMA)
        body: Statement = self.statement()

        self.consume(token_type=tokentypes.RIGHT_BRACE)
        return While(condition, body)

    def print_statement(self) -> Statement:
        self.consume(token_type=tokentypes.LEFT_BRACE)
        self.consume(token_type=tokentypes.VALUE_KEY)
        self.consume(token_type=tokentypes.COLON)
        value = self.expression()
        self.consume(token_type=tokentypes.RIGHT_BRACE)
        return Print(value)

    def expression(self) -> Expression:
        return self.assignment()
    
    def assignment(self) -> Expression:
        if self.check(tokentypes.HASH_REFERENCE) and self.check_n(tokentypes.VALUE_KEY, 3):
            self.consume(tokentypes.HASH_REFERENCE)
            name_token = self.consume(tokentypes.IDENTIFIER)
            self.consume(tokentypes.LEFT_BRACE)

            if self.match([tokentypes.VALUE_KEY]):
                self.consume(tokentypes.COLON)
                value = self.expression()
                self.consume(tokentypes.RIGHT_BRACE)
                return Assignment(name_token, value)

        expr = self.equality()
        return expr

    def equality(self) -> Expression:
        expression: Expression = self.comparison()
        while self.match(token_types=[tokentypes.EXCLAMATION_EQUAL, tokentypes.EQUAL_EQUAL]):
            operator = self.previous()
            right = self.comparison()
            expression = Binary(expression, operator, right)
        return expression

    def comparison(self) -> Expression:
        expression = self.term()

        while self.match(token_types=[tokentypes.GREATER, tokentypes.GREATER_EQUAL, tokentypes.LESS, tokentypes.LESS_EQUAL]):
            operator = self.previous()
            right = self.term()
            expression = Binary(expression, operator, right)
        
        return expression

    def term(self) -> Expression:
        expression = self.factor()

        while self.match(token_types=[tokentypes.MINUS, tokentypes.PLUS]):
            operator = self.previous()
            right = self.factor()
            expression = Binary(expression, operator, right)

        return expression
    
    def factor(self) -> Expression:
        expression = self.unary()

        while self.match(token_types=[tokentypes.SLASH, tokentypes.STAR]):
            operator = self.previous()
            right = self.unary()
            expression = Binary(expression, operator, right)
        
        return expression

    def unary(self) -> Expression:
        if self.match(token_types=[tokentypes.EXCLAMATION, tokentypes.MINUS]):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)
        
        return self.primary()

    def call(self) -> Expression:
        callee = self.expression()
        self.consume(tokentypes.LEFT_BRACE)
        arguments: list[Expression] = []

        while not self.check(tokentypes.RIGHT_BRACE):
            self.consume(tokentypes.IDENTIFIER)
            self.consume(tokentypes.COLON)
            value = self.expression()
            arguments.append(value)
            if not self.match([tokentypes.COMMA]):
                break

        self.consume(tokentypes.RIGHT_BRACE)
        expr = Call(callee, arguments)

        return expr


    def primary(self) -> Expression:
        if self.match(token_types=[tokentypes.FALSE]):
            return Literal(False)
        if self.match(token_types=[tokentypes.TRUE]):
            return Literal(True)
        if self.match(token_types=[tokentypes.NULL]):
            return Literal(None)

        if self.match(token_types=[tokentypes.NUMBER, tokentypes.STRING]):
            return Literal(self.previous().literal)
        
        if self.match(token_types=[tokentypes.IDENTIFIER]):
            return Variable(self.previous())

        if self.match(token_types=[tokentypes.HASH_REFERENCE]):
            return self.call()

        raise SyntaxError("Expected expression, found: " + str(self.peek()))


    def match(self, token_types: list[tokentypes]) -> bool:
        for type in token_types:
            if self.check(type):
                self.advance()
                return True
        return False
    
    def consume(self, token_type) -> Token:
        if self.check(token_type):
            return self.advance() 
        raise SyntaxError(f"Expected token of type {token_type}, found {self.peek().type}.")

    def check(self, type):
        if self.is_at_end():
            return False
        return self.peek().type == type
    
    def check_next(self, token_type) -> bool:
        if self.position + 1 >= len(self.tokens):
            return False
        return self.tokens[self.position + 1].type == token_type
    
    def check_n(self, token_type, pos) -> bool:
        if self.position + pos >= len(self.tokens):
            return False
        return self.tokens[self.position + pos].type == token_type

    def advance(self) -> Token:
        if not self.is_at_end():
            self.position += 1
        return self.previous()
    
    def is_at_end(self) -> bool:
        return self.peek().type == tokentypes.EOF
    
    def peek(self) -> Token:
        return self.tokens[self.position]
    
    def previous(self) -> Token:
        return self.tokens[self.position - 1]
    
    def consume_key_and_colon(self, key_type: tokentypes) -> Token:
        self.consume(token_type=key_type)
        self.consume(token_type=tokentypes.COLON)