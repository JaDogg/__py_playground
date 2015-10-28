# see http://effbot.org/zone/simple-top-down-parsing.htm

import sys
import re

if 1:

    class literal_token:
        def __init__(self, value):
            self.value = value
        def nud(self):
            return self
        def __repr__(self):
            return "(literal %s)" % self.value

    class operator_add_token:
        lbp = 10
        def nud(self):
            self.first = expression(100)
            self.second = None
            return self
        def led(self, left):
            self.first = left
            self.second = expression(10)
            return self
        def __repr__(self):
            return "(add %s %s)" % (self.first, self.second)

    class operator_sub_token:
        lbp = 10
        def nud(self):
            self.first = expression(100)
            self.second = None
            return self
        def led(self, left):
            self.first = left
            self.second = expression(10)
            return self
        def __repr__(self):
            return "(sub %s %s)" % (self.first, self.second)

    class operator_mul_token:
        lbp = 20
        def led(self, left):
            self.first = left
            self.second = expression(20)
            return self
        def __str__(self):
            return "(mul %s %s)" % (self.first, self.second)

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

parse("1")
parse("+1")
parse("-1")
parse("1+2")
parse("1+2+3")
parse("1+2*3")
parse("1*2+3")
