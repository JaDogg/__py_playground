"""
A draft of compiling PEGs to Python code. I expect to actually use
something like this in parson instead of peglet.
"""

import collections, re

def Parser(grammar):
    # Map the name of each grammar rule to a list of its alternatives.
    parts = re.split(' ('+_identifier+') += ',
                     ' '+re.sub(r'\s', ' ', grammar))
    if len(parts) == 1 or parts[0].strip():
        raise BadGrammar("Missing left hand side", parts[0])
    if len(set(parts[1::2])) != len(parts[1::2]):
        raise BadGrammar("Multiply-defined rule(s)", grammar)
    rules = dict((lhs, [alt.split() for alt in (' '+rhs+' ').split(' | ')])
                 for lhs, rhs in zip(parts[1::2], parts[2::2]))

    def comp():
        yield 'import re'
        for rule, alternatives in rules.items():
            for line in comp_rule(rule, alternatives):
                yield line

    def comp_rule(rule, alternatives):
        yield 'def rule_%s(text, far, i):' % rule
        for a, alternative in enumerate(alternatives):
            yield '    def alt_%s(i):' % a
            for line in comp_alternative(alternative):
                yield '        ' + line
        yield ('    return '
               + ' or '.join('alt_%d(i)' % a
                             for a, _ in enumerate(alternatives)))

    def comp_alternative(alternative):
        yield 'vals = ()'
        for token in alternative:
            for line in comp_token(token):
                yield line
        yield 'return i, vals'

    def comp_token(token):
        if token.startswith('$$'):
            yield 'st = %s({}, text, far, (i, vals))' % token[2:]
            yield 'if st is None: return None'
            yield 'i, vals = st'
        elif re.match(r'[$]\w+$', token):
            yield 'vals = (%s(*vals),)' % token[1:]
        elif token.startswith('!'):
            yield 'def inverted(text, far, i, vals):'
            for line in comp_token(token[1:]):
                yield '    ' + line
            yield '    return i, vals'
            yield 'if inverted(text, [0], i, vals): return None'
        elif token in rules:
            yield 'st = rule_%s(text, far, i)' % token
            yield 'if st is None: return None'
            yield 'i, vals = st[0], vals + st[1]'
        else:
            if re.match(r'/.', token): token = token[1:]
            yield 'm = re.match(%r, text[i:])' % token
            yield 'if not m: return None'
            yield 'i += m.end()'
            yield 'far[0] = max(far[0], i)'
            yield 'vals += m.groups()'

    return '\n'.join(comp())

_identifier = r'[A-Za-z_]\w*'

## exec(nums_grammar)
## rule_num('42,123 hag', [0], 0)
#. (2, (42,))
## rule_nums('42,123 hag', [0], 0)
#. (6, (42, 123))
## rule_allnums('42,123', [0], 0)
#. (6, (42, 123))
## rule_allnums('42,123 hag', [0], 0)

## print nums_grammar
#. import re
#. def rule_num(text, far, i):
#.     def alt_0(i):
#.         vals = ()
#.         m = re.match('([0-9]+)', text[i:])
#.         if not m: return None
#.         i += m.end()
#.         far[0] = max(far[0], i)
#.         vals += m.groups()
#.         vals = (int(*vals),)
#.         return i, vals
#.     return alt_0(i)
#. def rule_allnums(text, far, i):
#.     def alt_0(i):
#.         vals = ()
#.         st = rule_nums(text, far, i)
#.         if st is None: return None
#.         i, vals = st[0], vals + st[1]
#.         def inverted(text, far, i, vals):
#.             m = re.match('.', text[i:])
#.             if not m: return None
#.             i += m.end()
#.             far[0] = max(far[0], i)
#.             vals += m.groups()
#.             return i, vals
#.         if inverted(text, [0], i, vals): return None
#.         return i, vals
#.     return alt_0(i)
#. def rule_nums(text, far, i):
#.     def alt_0(i):
#.         vals = ()
#.         st = rule_num(text, far, i)
#.         if st is None: return None
#.         i, vals = st[0], vals + st[1]
#.         m = re.match(',', text[i:])
#.         if not m: return None
#.         i += m.end()
#.         far[0] = max(far[0], i)
#.         vals += m.groups()
#.         st = rule_nums(text, far, i)
#.         if st is None: return None
#.         i, vals = st[0], vals + st[1]
#.         return i, vals
#.     def alt_1(i):
#.         vals = ()
#.         st = rule_num(text, far, i)
#.         if st is None: return None
#.         i, vals = st[0], vals + st[1]
#.         return i, vals
#.     def alt_2(i):
#.         vals = ()
#.         return i, vals
#.     return alt_0(i) or alt_1(i) or alt_2(i)
#. 

nums_grammar = Parser(r"""
allnums =  nums !.

nums =  num , nums
     |  num
     |  

num =   ([0-9]+) $int
""")
