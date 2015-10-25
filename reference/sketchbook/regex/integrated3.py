"""
Integrate the right-to-left top-down operator-precedence parser with
the simplest terminating NFA code. Practically C-level code now for realz.
"""

def match(re, s): return run(prepare(re), s)

op_expect, op_jump, op_split = range(3)
op_names = 'expect jump split'.split()
ops_shift = 2

def encode(op, arg): return op | (arg << ops_shift)
def decode(insn): return insn & ((1 << ops_shift) - 1), insn >> ops_shift

wordlen = 32

class Bitset:
    def __init__(self, size):
        self.words = [0] * ((size + (wordlen-1)) // wordlen)
    def clear(self): 
        for i in range(len(self.words)): self.words[i] = 0
    def is_empty(self): return all(w == 0 for w in self.words)
    def has(self, i): return 0 != (self.words[i//wordlen] & (1 << (i%wordlen)))
    def add(self, i): self.words[i//wordlen] |= 1 << (i%wordlen)

def spread(insns, pc, agenda, visited):
    while True:
        op, arg = decode(insns[pc])
        if op == op_expect:
            agenda.add(pc)
            return
        elif op == op_jump:
            pc = arg
        elif op == op_split:
            if visited.has(pc):
                return
            visited.add(pc)
            spread(insns, arg, agenda, visited)
            pc -= 1

def step(insns, agenda, next, visited, c):
    visited.clear()
    for w, bits in enumerate(agenda.words):
        pc = wordlen * w
        while bits:
            if bits & 1:
                op, arg = decode(insns[pc])
                assert op == op_expect
                if arg == ord(c): spread(insns, pc-1, next, visited)
            pc += 1; bits >>= 1
    
def run(insns, s):
    agenda = Bitset(len(insns))
    visited = Bitset(len(insns))
    spread(insns, len(insns)-1, agenda, visited)
    next = Bitset(len(insns))
    for c in s:
        step(insns, agenda, next, visited, c)
        agenda, next = next, agenda
        if agenda.is_empty(): break # Redundant test, can speed it
        next.clear()
    return agenda.has(0) # (The accepting state is state #0)

def emit_fork(insns, k): return emit(insns, op_split, 0, k)

def patch(insns, k, target):
    op, arg = decode(insns[k])
    insns[k] = encode(op, target)

def emit(insns, op, arg, k):
    emit_jump(insns, k)
    insns.append(encode(op, arg))
    return len(insns) - 1

def emit_jump(insns, k):
    if len(insns) - 1 != k:
        insns.append(encode(op_jump, k))

def prepare(re):
    ts = list(re)
    insns = []

    def parse_expr(precedence, k):
        rhs = parse_factor(k)
        while ts:
            if ts[-1] == '(': break
            prec = 2 if ts[-1] == '|' else 4
            if prec < precedence: break
            if chomp('|'):
                rhs = emit(insns, op_split, rhs, parse_expr(prec+1, k))
            else:
                rhs = parse_expr(prec+1, rhs)
        return rhs

    def parse_factor(k):
        if not ts or ts[-1] in '|(':
            return k
        elif chomp(')'):
            e = parse_expr(0, k)
            assert chomp('(')
            return e
        elif chomp('*'):
            fork = emit_fork(insns, k)
            patch(insns, fork, parse_expr(6, fork))
            return fork
        else:
            return emit(insns, op_expect, ord(ts.pop()), k)

    def chomp(token):
        matches = (ts and ts[-1] == token)
        if matches: ts.pop()
        return matches

    # (256 == an impossible character)
    start = parse_expr(0, emit(insns, op_expect, 256, -1))
    assert not ts
    emit_jump(insns, start)
    return insns


def show(insns, pc):
    for k, insn in enumerate(insns):
        op, arg = decode(insn)
        print ('%2d %s %-6s %r' 
               % (k, '*' if k == pc else ' ',
                  op_names[op], 
                  chr(arg) if op == op_expect and 0 <= arg < 256 else arg))

## match('', '')
#. True
## match('', 'a')
#. False
## match('a', '')
#. False
## match('a', 'a')
#. True
## match('a', 'aa')
#. False
## match('ab', '')
#. False
## match('ab', 'ab')
#. True
## match('abc', 'ab')
#. False
## match('abc', 'abc')
#. True
## match('abc', 'abcd')
#. False
## match('a|b|c', '')
#. False
## match('a|b|c', 'a')
#. True
## match('a|b|c', 'b')
#. True
## match('a|b|c', 'c')
#. True
## match('a|b|c', 'd')
#. False
## match('ab||c', '')
#. True
## match('ab||c', 'a')
#. False
## match('ab||c', 'b')
#. False
## match('ab||c', 'c')
#. True
## match('ab||c', 'ab')
#. True
## match('a*', '')
#. True
## match('a*', 'a')
#. True
## match('a*', 'aa')
#. True
## match('a*', 'aab')
#. False
## match('ab*c', '')
#. False
## match('ab*c', 'ab')
#. False
## match('ab*c', 'ac')
#. True
## match('ab*c', 'abc')
#. True
## match('ab*c', 'abbbbc')
#. True
## match('ab*c', 'abbbbd')
#. False
## match('a(bc|d|)*e', '')
#. False
## match('a(bc|d|)*e', 'a')
#. False
## match('a(bc|d|)*e', 'ae')
#. True
## match('a(bc|d|)*e', 'abe')
#. False
## match('a(bc|d|)*e', 'ade')
#. True
## match('a(bc|d|)*e', 'abce')
#. True
## match('a(bc|d|)*e', 'abcde')
#. True
## match('(ab*c)', '')
#. False
## match('(ab*c)', 'abbbbc')
#. True
## match('()', '')
#. True
## match('()', 'a')
#. False
## match('()', 'a')
#. False
## match('()*', 'a')
#. False
## match('()*', '')
#. True
## match('a**', 'aaa')
#. True
## match('a**', 'b')
#. False

## prepare('a(bc|d|)*e')
#. [1024, 404, 34, 400, 10, 9, 396, 392, 18, 9, 388]
## show(prepare('a**'), 4)
#.  0   expect 256
#.  1   split  2
#.  2   split  3
#.  3   expect 'a'
#.  4 * jump   1
#. 
