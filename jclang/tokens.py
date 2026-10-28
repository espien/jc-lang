from enum import Enum

class TokenTypes(Enum):
    LEFT_BRACE = "LEFT_BRACE"
    RIGHT_BRACE = "RIGHT_BRACE"
    LEFT_PAREN = "LEFT_PAREN"
    RIGHT_PAREN = "RIGHT_PAREN"
    COLON = "COLON"
    COMMA = "COMMA"
    DOT = "DOT"
    SEMICOLON = "SEMICOLON"
    
    PLUS = "PLUS"
    MINUS = "MINUS"
    STAR = "STAR"
    SLASH = "SLASH"

    LESS = "LESS"
    LESS_EQUAL = "LESS_EQUAL"
    GREATER = "GREATER"
    GREATER_EQUAL = "GREATER_EQUAL"
    EQUAL_EQUAL = "EQUAL_EQUAL"
    EQUAL = "EQUAL"
    EXCLAMATION_EQUAL = "EXCLAMATION_EQUAL"
    EXCLAMATION = "EXCLAMATION"

    STRING = "STRING"
    NUMBER = "NUMBER"
    IDENTIFIER = "IDENTIFIER"

    VAR = "VAR"
    FUNCTION = "FUNCTION"
    PRINT = "PRINT"
    IF = "IF"
    ELSE = "ELSE"
    WHILE = "WHILE"
    CLASS = "CLASS"

    NAME_KEY = "NAME_KEY"
    VALUE_KEY = "VALUE_KEY"
    PARAMETERS_KEY = "PARAMETERS_KEY"
    PARAM_KEY = "PARAM_KEY"
    LOGIC_KEY = "LOGIC_KEY"
    RETURN_KEY = "RETURN_KEY"
    CONDITION_KEY = "CONDITION_KEY"

    HASH_REFERENCE = "HASH_REFERENCE"
    TRUE = "TRUE"
    FALSE = "FALSE"
    NULL = "NULL"
    EOF = "EOF"

directives = {
    ".var": TokenTypes.VAR,
    ".function": TokenTypes.FUNCTION,
    ".print": TokenTypes.PRINT,
    ".if": TokenTypes.IF,
    ".else": TokenTypes.ELSE,
    ".while": TokenTypes.WHILE,
}

keys = {
    "name": TokenTypes.NAME_KEY,
    "condition": TokenTypes.CONDITION_KEY,
    "value": TokenTypes.VALUE_KEY,
    "parameters": TokenTypes.PARAMETERS_KEY,
    "param": TokenTypes.PARAM_KEY,
    "logic": TokenTypes.LOGIC_KEY,
    "true": TokenTypes.TRUE,
    "false": TokenTypes.FALSE,
    "null": TokenTypes.NULL,
    "return": TokenTypes.RETURN_KEY
}


class Token:
    def __init__(self, type: TokenTypes, lexeme: str, literal: any, line: int):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __repr__(self):
        return f"[{self.type.name} {self.lexeme}]"
