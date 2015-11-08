from __future__ import absolute_import

import re

import pattern.en as english
from compiler import get_nate_logic
from peggy.peggy import flatten
from peggy_test.keyvalue import parse_keyvalue, KeyValueListParser
from nate.util import *
from vm import NateVm

DEFAULT_REPLACEMENTS = parse_keyvalue(read_data("initial_replace.txt"),
                                      parser=KeyValueListParser)


class RegexpReplacer(object):
    def __init__(self, patterns=DEFAULT_REPLACEMENTS):
        self.patterns = [(re.compile(regex), repl) for (regex, repl) in
                         patterns]

    def replace(self, text):
        s = text
        for (pattern, repl) in self.patterns:
            (s, count) = re.subn(pattern, repl, s)
        return s


class Rebuilder(object):
    # TODO Make this awesome, make this rule based
    def __init__(self):
        self._sp_after = [",", "."]
        self._sp_none = ["'s", "'", "@", "(", ")", "[", "]"]
        self._sp_both = ["?", "<", ">"]
        self._text = ""

    def rebuild(self, processed_):
        self._text = ""
        processed = flatten(processed_)
        processed = [atom if is_str(atom) else atom.string for atom in processed]
        for atom in processed:
            if atom in self._sp_after:
                self._text += atom + " "
            elif atom in self._sp_none:
                self._text += atom
            elif atom in self._sp_both:
                self._text += " " + atom + " "
            else:
                self._text += " " + atom
        self._text = self._text.strip().replace("  ", " ")

    @property
    def text(self):
        return self._text


class Nate(object):
    def __init__(self, text):
        self._text = text
        self._regex = RegexpReplacer()
        self._rebuilder = Rebuilder()
        self._logic = get_nate_logic()

    def process(self):
        text = self._regex.replace(self._text)
        pt = english.parsetree(text, lemmata=True)
        processed = []
        vm = NateVm()
        english.pprint(pt)
        for sentence in pt:
            words = sentence
            pos = 0
            last = len(words)
            while pos < last:
                for pattern, code in self._logic:
                    matched = pattern.match(words, start=pos)
                    if matched:
                        vm.run(matched, code)
                        pos = matched.stop
                        processed += vm.get()
                        break
                else:
                    processed.append(words[pos])
                    pos += 1
        self.rebuild_text(processed)

    def rebuild_text(self, processed):
        self._rebuilder.rebuild(processed)
        self._text = self._rebuilder.text

    @property
    def text(self):
        return self._text
