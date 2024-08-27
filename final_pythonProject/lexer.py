from collections import namedtuple

Token = namedtuple('Token', ['type', 'value'])

# Token types
t_INT = 'INT'
t_PLUS = 'PLUS'
t_MINUS = 'MINUS'
t_MULTIPLY = 'MUL'
t_DIVIDE = 'DIV'
t_MODULO = 'MODULO'
t_AND = 'AND'
t_OR = 'OR'
t_NOT = 'NOT'
t_EQ = 'EQ'
t_NEQ = 'NEQ'
t_GT = 'GT'
t_LT = 'LT'
t_GEQ = 'GEQ'
t_LEQ = 'LEQ'
t_TRUE = 'TRUE'
t_FALSE = 'FALSE'
t_LPAREN = 'LPAREN'
t_RPAREN = 'RPAREN'
t_LCBRACKET = 'LCBRACKET'
t_RCBRACKET = 'RCBRACKET'
t_COMMA = 'COMMA'
t_DO = 'DO'
digits = '0123456789'

t_LAMBDA = 'LAMBDA'
t_FUNCTION = 'FUNCTION'
t_COMMENTS = 'COMMENT'
t_DOT = "DOT"
t_SQUOTE = "SQUOTE"
t_PARAM = 'PARAM'
t_COLON = "COLON"

KEYWORDS = {
    'do': t_DO,
    'lambda': t_LAMBDA,
    'defun': t_FUNCTION
}
# error class
class Error:
    def __init__(self, error_name, details):
        self.error_name = error_name
        self.details = details

    def as_string(self):
        return f'{self.error_name}: {self.details}'

class IllegalCharError(Error):
    def __init__(self, details):
        super().__init__('Illegal Character', details)

# tokens
class Token:
    def __init__(self, type, value=None, parent=None):
        self.type = type
        self.value = value
        self.parent = parent

    def __repr__(self):
        if self.value:
            return f'{self.type} : {self.value}'
        return f'{self.type}'
# lexer

# init lexer
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = -1  # starts before the first char
        self.current_char = None  # holds the first char
        self.advance()  # advance to the next char

    def advance(self):  # advance to the next char
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

# add all tokens we have created
    def make_tokens(self):
        tokens = []  # define empty tokens
        while self.current_char is not None:  # while I have a char
            if self.current_char in ' \t\n':  # if found a space then next
                self.advance()
            elif self.current_char.isdigit() or (self.current_char == '-' and self.peek().isdigit()):
                tokens.append(self.make_number())
            elif self.current_char.isalpha():
                token, error = self.make_keyword_or_boolean()
                if error:
                    return [], error
                tokens.append(token)
            elif self.current_char == '(':
                self.advance()
                tokens.append(Token(t_LPAREN))
            elif self.current_char == ')':
                self.advance()
                tokens.append(Token(t_RPAREN))
            elif self.current_char == '{':
                self.advance()
                tokens.append(Token(t_LCBRACKET))
            elif self.current_char == '}':
                self.advance()
                tokens.append(Token(t_RCBRACKET))
            elif self.current_char == ',':
                self.advance()
                tokens.append(Token(t_COMMA))
            elif self.current_char == '.':
                self.advance()
                tokens.append(Token(t_DOT))
            elif self.current_char == '\'':
                self.advance()
                tokens.append(Token(t_SQUOTE))
            elif self.current_char == ':':
                self.advance()
                tokens.append(Token(t_COLON))
            else:
                token, error = self.make_symbol()
                if error:
                    return [], error  # if token does not exist -error
                tokens.append(token)
        return tokens, None

    # method that create a number (int or float)
    def make_number(self):
        num_str = ''
        dot_count = 0
        if self.current_char == '-':
            num_str += self.current_char
            self.advance()
        while self.current_char is not None and self.current_char.isdigit():
            num_str += self.current_char
            self.advance()
        # if dot_count == 0:
        return Token(t_INT, int(num_str))  # casting str into an int

    # create keyword
    def make_keyword_or_boolean(self):
        keyword_str = ''
        while self.current_char is not None and self.current_char.isalpha():
            keyword_str += self.current_char
            self.advance()
        if keyword_str in KEYWORDS:
            return Token(KEYWORDS[keyword_str], keyword_str), None
        if keyword_str == 'true':
            return Token(t_TRUE, True), None
        elif keyword_str == 'false':
            return Token(t_FALSE, False), None
        else:
            return Token(t_PARAM, keyword_str), None

    def make_symbol(self):
        if self.current_char == '+':
            self.advance()
            return Token(t_PLUS), None
        elif self.current_char == '-':
            self.advance()
            return Token(t_MINUS), None
        elif self.current_char == '*':
            self.advance()
            return Token(t_MULTIPLY), None
        elif self.current_char == '/':
            self.advance()
            return Token(t_DIVIDE), None
        elif self.current_char == '%':
            self.advance()
            return Token(t_MODULO), None
        elif self.current_char == '&' and self.peek() == '&':
            self.multiAdvance()
            return Token(t_AND), None
        elif self.current_char == '|' and self.peek() == '|':
            self.multiAdvance()
            return Token(t_OR), None
        elif self.current_char == '!':
            if self.peek() == '=':
                self.multiAdvance()
                return Token(t_NEQ), None
            else:
                self.advance()
                return Token(t_NOT), None
        elif self.current_char == '=' and self.peek() == '=':
            self.multiAdvance()
            return Token(t_EQ), None
        elif self.current_char == '>':
            if self.peek() == '=':
                self.multiAdvance()
                return Token(t_GEQ), None
            else:
                self.advance()
                return Token(t_GT), None
        elif self.current_char == '<':
            if self.peek() == '=':
                self.multiAdvance()
                return Token(t_LEQ), None
            else:
                self.advance()
                return Token(t_LT), None
        else:
            char = self.current_char
            self.advance()
            return None, IllegalCharError("'" + char + "'")

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos >= len(self.text):
            return None
        return self.text[peek_pos]

    def multiAdvance(self,times=2):
        for _ in range(times):
            self.advance()
