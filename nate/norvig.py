"""
Peter Norvig's spell corrector
http://norvig.com/spell-correct.html
"""

from __future__ import absolute_import
from __future__ import print_function

import collections
import re

from nate.util import read_data


def words(text):
    return re.findall('[a-z]+', text.lower())


def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model


N_WORDS = train(words(read_data("big.txt")))

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'


def edits1(word):
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [a + b[1:] for a, b in splits if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b) > 1]
    replaces = [a + c + b[1:] for a, b in splits for c in ALPHABET if b]
    inserts = [a + c + b for a, b in splits for c in ALPHABET]
    return set(deletes + transposes + replaces + inserts)


def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in N_WORDS)


def known(words_):
    return set(w for w in words_ if w in N_WORDS)


def correct(word):
    candidates = known([word]) or known(edits1(word)) or \
                 known_edits2(word) or [word]
    return max(candidates, key=N_WORDS.get)


class Norvig(object):
    def process(self, text):
        from nltk.tokenize import word_tokenize
        words_ = word_tokenize(str(text))
        words_ = [correct(word) for word in words_]
        return " ".join(words_)
