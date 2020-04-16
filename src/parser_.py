from tokens import TokenType
from nodes import *

class Parser:
    def __init__(self, tokens):
        self.tokens = iter(tokens)
        self.advance()

    def advance(self):
        try:
            self.current_token = next(self.tokens)
        except StopIteration:
            self.current_token = None

    def raise_error(self):
        raise Exception("Invalid syntax")

    def parse(self):
        if self.current_token == None:
            return None

        result = self.expr()

        if self.current_token != None:
            self.raise_error()

        return result

    def expr(self):
        result = self.term()

        while self.current_token != None and self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            if self.current_token.type == TokenType.PLUS:
                self.advance()
                result = AddNode(result, self.term())
            elif self.current_token.type == TokenType.MINUS:
                self.advance()
                result = SubtractNode(result, self.term())

        return result

    def term(self):
        result = self.expon()

        while self.current_token != None and self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE):
            if self.current_token.type == TokenType.MULTIPLY:
                self.advance()
                result = MultiplyNode(result, self.expon())
            elif self.current_token.type == TokenType.DIVIDE:
                self.advance()
                result = DivideNode(result, self.expon())
                
        return result

    def expon(self):        # exponentiation
        result = self.factor()

        while self.current_token != None and self.current_token.type == TokenType.POWER:
            if self.current_token.type == TokenType.POWER:
                self.advance()
                result = PowerNode(result, self.factor())         

        return result    

    def factor(self):
        token = self.current_token

        if token.type == TokenType.LPAREN:
            self.advance()
            result = self.expr()

            if self.current_token.type !=TokenType.RPAREN:
                self.raise_error()

            self.advance()
            return result

        if token.type == TokenType.NUMBER:
            self.advance()
            return NumberNode(token.value)

        elif token.type == TokenType.LETTER:
            self.advance()
            if self.current_token != None and self.current_token.type == TokenType.NUMBER:
                return IndexNode(token.value, self.factor())
            else:
                return LetterNode(token.value)

        elif token.type == TokenType.PLUS:
            self.advance()
            return PlusNode(self.factor())

        elif token.type == TokenType.MINUS:
            self.advance()
            return MinusNode(self.factor())

        elif token.type == TokenType.SIN:
            self.advance()
            return SinusNode(self.factor())

        elif token.type == TokenType.COS:
            self.advance()
            return CosinusNode(self.factor())

        elif token.type == TokenType.EXP:
            self.advance()
            return ExponentNode(self.factor())

        elif token.type == TokenType.SQRT:
            self.advance()
            return SquareNode(self.factor())

        self.raise_error()