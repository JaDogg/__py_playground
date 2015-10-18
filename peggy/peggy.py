from abc import abstractmethod, ABCMeta
import re
from functools import wraps

_LABEL_FUNCTION = re.compile(r"@(?P<name>[a-zA-Z_]\w*)")


# http://codereview.stackexchange.com/questions/19034/peg-parser-in-python

def memoize_(func):
    data_store = dict()

    @wraps(func)
    def wrapper_function(*args):
        if args not in data_store:
            data_store[args] = func(*args)
        return data_store[args]

    return wrapper_function


def flatten(items):
    for item in items:
        if isinstance(item, tuple):
            for item_ in flatten(item):
                yield item_
        else:
            yield item


def display(items, depth=1):
    for item in items:
        if isinstance(item, tuple):
            display(item, depth + 1)
        else:
            print("{t}({i})".format(t="  " * depth, i=item))


def merge_dictionary(destination, source):
    for key, value in source.items():
        destination[key] = value
    return destination


class TupleUtils(object):
    @staticmethod
    def kill(*_):
        return ()

    @staticmethod
    def join(*atoms):
        return "".join(atoms),

    @staticmethod
    def to_int(value):
        return int(value),

    @staticmethod
    def build_tuple(*atoms):
        return atoms,

    @staticmethod
    def hug(*atoms):
        return atoms,

    @staticmethod
    def remove_brackets(*atoms):
        return atoms[1:-1],

    @staticmethod
    def debug(*atoms):
        print(atoms)
        return atoms


class PackratParser(TupleUtils):
    def __init__(self, rules, text):
        self._rules = rules
        self._text = text

    def parse_text(self, start="parse"):
        _, _, tokens = self.parse_rule(start)
        return tokens

    def try_parse(self, start="parse"):
        rightmost, pos, tokens = self.parse_rule(start)
        if pos is None:
            err_text = "{start}\n{text}\n{arrow}\n{end}\n".format(
                start="=" * 50, end="=" * 50,
                text=self._text, arrow=" " * rightmost + "^")
            raise ValueError(
                "Cannot parse. Error at position {0}\n{1}".format(rightmost,
                                                                  err_text))
        return tokens

    @memoize_
    def parse_rule(self, rule, position=0):
        rightmost = position
        for alternative in self._rules[rule]:
            current_pos, current_values = position, ()
            for token in alternative:
                current_rightmost, current_pos, current_values = \
                    self.parse_token(token, current_pos, current_values)
                rightmost = max(rightmost, current_rightmost)
                if current_pos is None:
                    break
            else:
                return rightmost, current_pos, current_values
        return rightmost, None, ()

    def parse_token(self, token, position, values):

        if isinstance(token, Matcher):
            return token(self, position, values)

        # Match a sub rule
        if token in self._rules:
            rightmost, current_pos, current_values = \
                self.parse_rule(token, position)
            return rightmost, current_pos, () if current_pos is None \
                else values + current_values

        # Call a label function
        matched = _LABEL_FUNCTION.match(token)

        if matched:
            func = getattr(self, matched.group("name"))
            return position, position, func(*values)

        # Do a regex match on current text position
        matched = re.match(token, self._text[position:])

        if matched:
            new_position = position + matched.end()
            return new_position, new_position, values + matched.groups()

        return position, None, ()


class Matcher(object):
    __metaclass__ = ABCMeta

    def __init__(self, *args):
        self._atoms = args

    @abstractmethod
    def __call__(self, parser, position, values):
        pass


class One(Matcher):
    def __init__(self, *args):
        Matcher.__init__(self, *args)

    def __call__(self, parser, position, values):
        current_pos, current_values = position, values
        rightmost = position
        for token in self._atoms:
            current_rightmost, current_pos, current_values = \
                parser.parse_token(token, current_pos, current_values)
            rightmost = max(position, current_rightmost)
            if current_pos is None:
                break
        else:
            return rightmost, current_pos, current_values

        return position, None, ()


class OneOrMore(One):
    def __init__(self, *args):
        Matcher.__init__(self, *args)

    def __call__(self, parser, position, values):
        current_rightmost, current_pos, current_values = position, None, values
        while True:
            prev_rightmost, prev_pos, prev_values = current_rightmost, \
                                                    current_pos, current_values
            current_rightmost, current_pos, current_values = \
                One.__call__(self, parser, current_rightmost,
                             current_values)
            if current_pos is None:
                return prev_rightmost, prev_pos, prev_values

        return position, None, ()


class ZeroOrMore(OneOrMore):
    def __init__(self, *args):
        Matcher.__init__(self, *args)

    def __call__(self, parser, position, values):
        current_rightmost, current_pos, current_values = \
            OneOrMore.__call__(self, parser, position, values)

        if current_pos is None:
            return position, position, values

        return current_rightmost, current_pos, current_values


class ZeroOrOne(One):
    def __init__(self, *args):
        Matcher.__init__(self, *args)

    def __call__(self, parser, position, values):
        current_rightmost, current_pos, current_values = \
            One.__call__(self, parser, position, values)

        if current_pos is None:
            return position, position, values

        return current_rightmost, current_pos, current_values


class Or(Matcher):
    def __init__(self, *args):
        Matcher.__init__(self, *args)

    def __call__(self, parser, position, values):
        for matcher in self._atoms:
            current_rightmost, current_pos, current_values \
                = matcher(parser, position, values)

            if current_pos is not None:
                return current_rightmost, current_pos, current_values

        return position, None, ()


class Not(One):
    def __init__(self, *args):
        Matcher.__init__(self, *args)

    def __call__(self, parser, position, values):
        current_rightmost, current_pos, current_values \
            = One.__call__(self, parser, position, values)

        return current_rightmost, current_rightmost if current_pos is None \
            else None, values if current_pos is None else ()
