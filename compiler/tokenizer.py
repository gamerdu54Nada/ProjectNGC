"""
ConnectScript Tokenizer
Convertit le code source en tokens
"""
from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional, Iterator


class TokenType(Enum):
    # Keywords
    PAGE = auto()
    ON = auto()
    END = auto()
    IF = auto()
    SET = auto()
    ADD = auto()
    SUBTRACT = auto()
    ALERT = auto()
    CONNECT_GOTO = auto()
    PLAY = auto()
    WAIT = auto()
    
    # Delimiters
    MINUS = auto()  # -
    DOUBLE_MINUS = auto()  # --
    LPAREN = auto()  # (
    RPAREN = auto()  # )
    
    # Literals
    IDENTIFIER = auto()  # nom_variable
    STRING = auto()  # "texte"
    NUMBER = auto()  # 123
    COLOR = auto()  # blue, #FF00FF
    
    # Operators
    EQUALS = auto()  # =
    
    # Special
    NEWLINE = auto()
    EOF = auto()
    COMMENT = auto()


@dataclass
class Token:
    """Représente un token unique"""
    type: TokenType
    value: any
    line: int
    column: int
    
    def __repr__(self):
        return f"Token({self.type.name}, {self.value!r}, {self.line}:{self.column})"


class Tokenizer:
    """Tokenize le code ConnectScript"""
    
    KEYWORDS = {
        'page': TokenType.PAGE,
        'on': TokenType.ON,
        'end': TokenType.END,
        'if': TokenType.IF,
        'set': TokenType.SET,
        'add': TokenType.ADD,
        'subtract': TokenType.SUBTRACT,
        'alert': TokenType.ALERT,
        'play': TokenType.PLAY,
        'wait': TokenType.WAIT,
    }
    
    COLORS = {
        'red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink',
        'black', 'white', 'gray', 'lightblue', 'lightyellow', 'lightcolorange',
        'darkorange', 'darkblue', 'darkgreen'
    }
    
    def __init__(self, code: str):
        self.code = code
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
    
    def tokenize(self) -> List[Token]:
        """Retourne la liste de tous les tokens"""
        while self.position < len(self.code):
            self._skip_whitespace_same_line()
            
            if self.position >= len(self.code):
                break
            
            # Comments
            if self._match('#'):
                self._skip_comment()
                continue
            
            # Newline
            if self._match('\n'):
                self.tokens.append(self._create_token(TokenType.NEWLINE))
                self.line += 1
                self.column = 1
                self.position += 1
                continue
            
            # Double minus
            if self._match('--'):
                self.tokens.append(self._create_token(TokenType.DOUBLE_MINUS))
                self.position += 2
                self.column += 2
                continue
            
            # Single minus
            if self._match('-'):
                self.tokens.append(self._create_token(TokenType.MINUS))
                self.position += 1
                self.column += 1
                continue
            
            # Parentheses
            if self._match('('):
                self.tokens.append(self._create_token(TokenType.LPAREN))
                self.position += 1
                self.column += 1
                continue
            
            if self._match(')'):
                self.tokens.append(self._create_token(TokenType.RPAREN))
                self.position += 1
                self.column += 1
                continue
            
            # Equals
            if self._match('='):
                self.tokens.append(self._create_token(TokenType.EQUALS))
                self.position += 1
                self.column += 1
                continue
            
            # Strings
            if self._match('"'):
                self._tokenize_string()
                continue
            
            # Numbers
            if self._current_char().isdigit():
                self._tokenize_number()
                continue
            
            # Identifiers, keywords, colors
            if self._current_char().isalpha() or self._current_char() == '_':
                self._tokenize_identifier()
                continue
            
            # Caractère inconnu
            raise SyntaxError(
                f"Caractère inattendu '{self._current_char()}' "
                f"à la ligne {self.line}, colonne {self.column}"
            )
        
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens
    
    def _current_char(self) -> str:
        """Obtient le caractère courant"""
        if self.position < len(self.code):
            return self.code[self.position]
        return '\0'
    
    def _peek_char(self, offset: int = 1) -> str:
        """Regarde le caractère à distance"""
        pos = self.position + offset
        if pos < len(self.code):
            return self.code[pos]
        return '\0'
    
    def _match(self, s: str) -> bool:
        """Vérifie si la position courante correspond à s"""
        return self.code[self.position:self.position + len(s)] == s
    
    def _skip_whitespace_same_line(self):
        """Ignore les espaces/tabs"""
        while self.position < len(self.code) and self._current_char() in ' \t':
            self.position += 1
            self.column += 1
    
    def _skip_comment(self):
        """Ignore un commentaire jusqu'à la fin de ligne"""
        while self.position < len(self.code) and self._current_char() != '\n':
            self.position += 1
    
    def _create_token(self, token_type: TokenType, value=None) -> Token:
        """Crée un token"""
        return Token(token_type, value, self.line, self.column)
    
    def _tokenize_string(self):
        """Tokenize une string"""
        start_line = self.line
        start_column = self.column
        self.position += 1
        self.column += 1
        
        value = ""
        while self.position < len(self.code) and self._current_char() != '"':
            if self._current_char() == '\\' and self._peek_char() == '"':
                # Escape \"
                value += '"'
                self.position += 2
                self.column += 2
            else:
                value += self._current_char()
                self.position += 1
                self.column += 1
        
        if self.position >= len(self.code):
            raise SyntaxError(f"String non fermée à la ligne {start_line}")
        
        self.position += 1  # Consume closing "
        self.column += 1
        self.tokens.append(Token(TokenType.STRING, value, start_line, start_column))
    
    def _tokenize_number(self):
        """Tokenize un nombre"""
        start_column = self.column
        value = ""
        
        while self.position < len(self.code) and self._current_char().isdigit():
            value += self._current_char()
            self.position += 1
            self.column += 1
        
        self.tokens.append(Token(TokenType.NUMBER, int(value), self.line, start_column))
    
    def _tokenize_identifier(self):
        """Tokenize identifier, keyword ou color"""
        start_column = self.column
        value = ""
        
        while (self.position < len(self.code) and 
               (self._current_char().isalnum() or self._current_char() in '_.')):
            value += self._current_char()
            self.position += 1
            self.column += 1
        
        # Vérifier si c'est un keyword (sans le point)
        base_value = value.split('.')[0] if '.' in value else value
        if base_value in self.KEYWORDS:
            token_type = self.KEYWORDS[base_value]
            self.tokens.append(Token(token_type, value, self.line, start_column))
            return
        
        # Vérifier si c'est une couleur (pas de points)
        if '.' not in value:
            if value in self.COLORS or value.startswith('#'):
                self.tokens.append(Token(TokenType.COLOR, value, self.line, start_column))
                return
        
        # Sinon c'est un identifiant
        self.tokens.append(Token(TokenType.IDENTIFIER, value, self.line, start_column))
