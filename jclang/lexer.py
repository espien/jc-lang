from .tokens import Token, TokenTypes as tokentypes, keys, directives

class Lexer:
    def __init__(self, source):
        self.source  = source
        self.position = 0
        self.line = 1
        self.start = 0
        self.tokens = []

    def scan_tokens(self) -> list[Token]:
        while not self.is_at_end():
            self.start = self.position
            self.scan_token()
        self.add_token(tokentypes.EOF)
        return self.tokens

    def is_at_end(self) -> bool:
        return self.position >= len(self.source)
    
    def advance(self) -> str:
        current_char = self.source[self.position]
        self.position += 1
        return current_char

    def add_token(self, type:tokentypes, literal=None) -> None:
        text = self.source[self.start:self.position]
        if type == tokentypes.EOF:
            text = "EOF"
        self.tokens.append(Token(type=type, lexeme=text, literal=literal, line=self.line))

    def scan_token(self) -> None:
        character = self.advance()
        match character:
            case "(": self.add_token(tokentypes.LEFT_PAREN)
            case ")": self.add_token(tokentypes.RIGHT_PAREN)
            case "{": self.add_token(tokentypes.LEFT_BRACE)
            case "}": self.add_token(tokentypes.RIGHT_BRACE)
            case ":": self.add_token(tokentypes.COLON)
            case ",": self.add_token(tokentypes.COMMA)
            case ".": self.handle_directive()
            case "-": self.add_token(tokentypes.MINUS)
            case "+": self.add_token(tokentypes.PLUS)
            case "*": self.add_token(tokentypes.STAR)
            case ";": self.add_token(tokentypes.SEMICOLON)
            case "#": self.add_token(tokentypes.HASH_REFERENCE)
            case "!":
                if self.match("="):
                    self.add_token(tokentypes.EXCLAMATION_EQUAL)
                else:
                    self.add_token(tokentypes.EXCLAMATION)
            case "=":
                if self.match("="):
                    self.add_token(tokentypes.EQUAL_EQUAL)
                else:
                    self.add_token(tokentypes.EQUAL)
            case "<":
                if self.match("="):
                    self.add_token(tokentypes.LESS_EQUAL)
                else:
                    self.add_token(tokentypes.LESS)
            case ">":
                if self.match("="):
                    self.add_token(tokentypes.GREATER_EQUAL)
                else:
                    self.add_token(tokentypes.GREATER)
            case "/":
                if self.match("/"):
                   self.handle_comment()
                else:
                    self.add_token(tokentypes.SLASH)
            case " ":
                return
            case "\t":
                return
            case "\n": self.line += 1
            case '"': self.handle_string()
            case _: 
                if (self.is_digit(character)):
                    self.handle_number()
                elif (self.is_alpha(character)):
                    self.handle_identifier()
                else:
                    raise SyntaxError(f"Unsupported character: {character}")
                
    def handle_directive(self) -> None:
        dot_position = self.position
        while self.is_alpha(self.peek()):
            self.advance()
        
        text = self.source[self.start:self.position]
        token_type = directives.get(text)
        if token_type is None:
            token_type = tokentypes.DOT
            self.position = dot_position
        self.add_token(token_type)
        
    def match(self, expected: str) -> bool:
        if self.is_at_end():
            return False
        if self.source[self.position] != expected:
            return False

        self.position += 1
        return True
    
    def handle_comment(self) -> None:
        while self.peek() != "\n" and not self.is_at_end():
            self.advance()
        
    def peek(self) -> str:
        if self.is_at_end():
            return "\0"
        return self.source[self.position]

    def handle_string(self) -> None:
        while self.peek() != '"' and not self.is_at_end():
            self.advance()
        
        if self.is_at_end():
            print("Unterminated string: ", self.line)
            return
        
        self.advance()

        value = self.source[self.start + 1: self.position - 1]
        self.add_token(tokentypes.STRING, value)


    def is_digit(self, character: str) -> bool:
        return character >= "0" and character <= "9"

    def handle_number(self) -> None:
        is_float = False
        while self.is_digit(self.peek()):
            self.advance()
        
        if self.peek() == "." and self.is_digit(self.peekNext()):
            is_float = True
            self.advance()

            while self.is_digit(self.peek()):
                self.advance()
    
        number_str = self.source[self.start:self.position]
        number_value = float(number_str) if is_float else int(number_str)

        self.add_token(tokentypes.NUMBER, number_value)
    
    def peekNext(self) -> str:
        if self.position + 1 >= len(self.source):
            return "\0"
        return self.source[self.position + 1]
    
    def is_alpha(self, character: str) -> bool:
        return character >= "a" and character <= "z" or character >= "A" and character <= "Z" or character == "_"

    def is_alpha_numeric(self, character: str) -> bool:
        return self.is_alpha(character) or self.is_digit(character)

    def handle_identifier(self) -> None:
        while self.is_alpha_numeric(self.peek()):
            self.advance()
        
        text = self.source[self.start:self.position]
        token_type = keys.get(text)
        if token_type is None:
            token_type = tokentypes.IDENTIFIER

        self.add_token(token_type)
    
    def print_tokens(self) -> None:
        print(self.tokens)