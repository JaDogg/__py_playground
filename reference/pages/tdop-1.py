# see http://effbot.org/zone/simple-top-down-parsing.txt

import sys
import re

if 1:

    class literal_token:
        def __init__(self, value):
            self.value = value
        def nud(self):
            return self.value

    class operator_add_token:
        lbp = 10
        def nud(self):
            return expression(100)
        def led(self, left):
            return left + expression(10)

    class operator_sub_token:
        lbp = 10
        def nud(self):
            return -expression(100)
        def led(self, left):
            return left - expression(10)

    class operator_mul_token:
        lbp = 20
        def led(self, left):
            return left * expression(20)

    class operator_div_token:
        lbp = 20
        def led(self, left):
            return left / expression(20)

    class operator_pow_token:
        lbp = 30
        def led(self, left):
            return left ** expression(30-1)

    class end_token:
        lbp = 0

    def tokenize(program):
        for number, operator in re.findall("\s*(?:(\d+)|(\*\*|.))", program):
            if number:
                yield literal_token(int(number))
            elif operator == "+":
                yield operator_add_token()
            elif operator == "-":
                yield operator_sub_token()
            elif operator == "*":
                yield operator_mul_token()
            elif operator == "/":
                yield operator_div_token()
            elif operator == "**":
                yield operator_pow_token()
            else:
                raise SyntaxError("unknown operator: %r" % operator)
        yield end_token()

    def expression(rbp=0):
        global token
        t = token
        token = next()
        left = t.nud()
        while rbp < token.lbp:
            t = token
            token = next()
            left = t.led(left)
        return left

    def parse(program):
        global token, next
        next = tokenize(program).next
        token = next()
        print program, "->", expression()

parse("+1")
parse("-1")
parse("10")
parse("1**2**3")
parse("1+2")
parse("1+2+3")
parse("1+2*3")
parse("1*2+3")
parse("1*2/3")
parse("*1") # invalid syntax
