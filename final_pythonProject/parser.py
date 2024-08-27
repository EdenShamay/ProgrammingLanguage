import math
from lexer import (t_INT, t_PLUS, t_MINUS, t_MULTIPLY, t_DIVIDE, t_MODULO, t_NOT, t_EQ,
                   t_NEQ,
                   t_GT, t_LT, t_GEQ, t_LEQ, t_TRUE, t_FALSE, t_LPAREN, t_RPAREN, t_AND, t_OR,
                   t_FUNCTION, t_LCBRACKET, t_RCBRACKET, t_PARAM, t_COMMA, t_COLON, t_SQUOTE, t_LAMBDA, t_DOT)


## nodes for each variable
class AST:
    pass


class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f'{self.left} {self.op} {self.right}'


class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __repr__(self):
        return f'{self.value}'


class Bool(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class UnaryOp(AST):
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr


class Function(AST):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body


class FunctionCall(AST):
    def __init__(self, name, args):
        self.name = name
        self.args = args


class Parameter(AST):
    def __init__(self, value, fname=None):
        self.value = value
        self.fname = fname

    def set_fname(self, fname):
        self.fname = fname


############################### lambda ########################
class Lambda(AST):
    def __init__(self, params, body):
        self.params = params
        self.body = body

    def __repr__(self):
        return f"(Lambd {self.params}.({self.body}))"


############################### lambda ########################
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos]

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.pos += 1
            if self.pos < len(self.tokens):
                self.current_token = self.tokens[self.pos]
        else:
            raise Exception(f"Invalid syntax: expected {token_type}")

    def factor(self, fname=None):
        token = self.current_token
        if token.type == t_INT:
            self.eat(t_INT)
            return Num(token)
        elif token.type == t_TRUE:
            self.eat(t_TRUE)
            return Bool(token)
        elif token.type == t_FALSE:
            self.eat(t_FALSE)
            return Bool(token)
        elif token.type == t_NOT:
            self.eat(t_NOT)
            return UnaryOp(op=token, expr=self.statement(fname))
        elif token.type == t_LPAREN:
            self.eat(t_LPAREN)
            node = self.statement(fname)
            self.eat(t_RPAREN)
            return node
        elif token.type == t_PARAM:
            node = self.current_token.value
            self.eat(t_PARAM)
            return Parameter(node,fname)

        else:
            raise Exception("Invalid syntax")

    def term(self, fname=None):
        node = self.factor(fname)
        while self.current_token.type in (t_MULTIPLY, t_DIVIDE, t_MODULO):
            token = self.current_token
            if token.type == t_MULTIPLY:
                self.eat(t_MULTIPLY)
            elif token.type == t_DIVIDE:
                self.eat(t_DIVIDE)
            elif token.type == t_MODULO:
                self.eat(t_MODULO)
            node = BinOp(left=node, op=token, right=self.statement(fname))
        return node

    def expr(self,fname=None):
        node = self.term(fname)
        while self.current_token.type in (t_PLUS, t_MINUS):
            token = self.current_token
            if token.type == t_PLUS:
                self.eat(t_PLUS)
            elif token.type == t_MINUS:
                self.eat(t_MINUS)
            node = BinOp(left=node, op=token, right=self.statement(fname))
        return node

    def condition(self,fname=None):
        node = self.expr(fname)
        if self.current_token.type in (t_EQ, t_NEQ, t_GT, t_LT, t_GEQ, t_LEQ, t_AND, t_OR):
            token = self.current_token
            self.eat(token.type)
            node = BinOp(left=node, op=token, right=self.statement(fname))
        return node

    def statement(self,fname=None):
        if self.current_token.type == t_FUNCTION:
            return self.function()
        if self.current_token.type == t_PARAM and self.tokens[self.pos + 1].type == t_LPAREN:
            return self.function_call()
        if self.current_token.type == t_LAMBDA:
            return self.lambda_expression()
        return self.condition(fname)

    def function(self):
        self.eat(t_FUNCTION)
        self.eat(t_LCBRACKET)
        function_name = self.get_function_name()
        self.consume_param(t_COLON)
        arguments = self.get_args(function_name)
        self.eat(t_RCBRACKET)
        return Function(function_name.value, arguments, self.statement(function_name.value))

    def function_call(self):
        function_name = self.current_token
        self.eat(t_PARAM)
        arguments = self.get_args(function_name)
        return FunctionCall(function_name, arguments)

    def get_args(self, fname):
        args = []
        self.eat(t_LPAREN)
        while self.current_token.type != t_RPAREN:
            arg = self.statement(fname.value)
            args.append(arg)
            self.eat(t_COMMA)
        self.eat(t_RPAREN)
        return args

    # def get_args_for_builtIn_functions(self):
    #     args = []
    #     self.eat(t_LPAREN)
    #     while self.current_token.type != t_RPAREN:
    #         if self.current_token.type == t_COMMA:
    #             self.eat(t_COMMA)
    #             continue
    #         args.append(self.factor().value)
    #         if self.current_token.type == t_COMMA:
    #             self.eat(t_COMMA)
    #     self.eat(t_RPAREN)
    #     return args

    def get_function_name(self):
        self.consume_param(t_COLON)
        return self.consume_param(t_COMMA)

    def consume_param(self, typeToConsume):
        self.eat(t_SQUOTE)  # consume '
        p_name = self.current_token
        self.eat(t_PARAM)  # consume name
        self.eat(t_SQUOTE)  # consume '
        self.eat(typeToConsume)
        return p_name

    def lambda_expression(self):
        self.eat(t_LAMBDA)
        param = self.current_token.value  # Get the parameter for the lambda
        self.eat(t_PARAM)
        self.eat(t_DOT)
        body = self.statement()  # Parse the body of the lambda expression
        lambda_node = Lambda([param], body)  # Create the Lambda node

        # Handle immediate application of lambda (e.g., lambda 2.)
        while self.current_token.type == t_LPAREN:
            self.eat(t_LPAREN)
            arg = self.expr()  # Parse the argument being passed to the lambda
            self.eat(t_RPAREN)
            lambda_node = FunctionCall(lambda_node, [arg])

        return lambda_node

    def parse(self):
        return self.statement()
