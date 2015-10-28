# see http://effbot.org/zone/simple-top-down-parsing.htm

import sys
import re

if 1:

    symbol_table = {}

    class symbol_base(object):
        value = None
        def __repr__(self):
            if self.value:
                return "(literal %s)" % self.value
            else:
                return "(%s %s %s)" % (self.id, self.first, self.second)

    def symbol(id, bp=0):
        try:
            s = symbol_table[id]
        except KeyError:
            class s(symbol_base):
                pass
            s.__name__ = "symbol-" + id # for debugging
            s.id = id
            s.value = None
            s.lbp = bp
            symbol_table[id] = s
        else:
            s.lbp = max(bp, s.lbp)
        return s

    symbol("(literal)")
    symbol("+", 10); symbol("-", 10)
    symbol("*", 20); symbol("/", 20)
    symbol("**", 30)
    symbol("(end)")

    # manual configuration

    def led(self, left):
        self.first = left
        self.second = expression(10)
        return self
    symbol("+").led = led
    symbol("-").led = led

    # helpers

    def infix(id, bp):
        def led(self, left):
            self.first = left
            self.second = expression(bp)
            return self
        symbol(id, bp).led = led

    def infix_r(id, bp):
        def led(self, left):
            self.first = left
            self.second = expression(bp-1)
            return self
        symbol(id, bp).led = led

    def prefix(id, bp):
        def nud(self):
            self.first = expression(bp)
            self.second = None
            return self
        symbol(id).nud = nud

    infix("+", 10); infix("-", 10)
    infix("*", 20); infix("/", 20)

    prefix("+", 100); prefix("-", 100)

    infix_r("**", 30)

    symbol("(literal)").nud = lambda self: self

    # tokenizer

    token_pat = re.compile("\s*(?:(\d+)|(\*\*|.))")

    def tokenize(program):
        for number, operator in token_pat.findall(program):
            if number:
                symbol = symbol_table["(literal)"]
                s = symbol()
                s.value = number
                yield s
            else:
                symbol = symbol_table.get(operator)
                if not symbol:
                    raise SyntaxError("Unknown operator")
                yield symbol()
        symbol = symbol_table["(end)"]
        yield symbol()

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
        print program
        print expression()

parse("1")
parse("+1")
parse("-1")
parse("1+2")
parse("1+2+3")
parse("1+2*3")
parse("1*2+3")
