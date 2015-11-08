from __future__ import absolute_import

import re

import pattern.en as english
import pattern.en.wordnet as wordnet

from peggy_test.keyvalue import parse_keyvalue, KeyValueListParser
from nate.util import *

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


class RepeatReplacer(object):
    def __init__(self):
        self.repeat_regexp = re.compile(r'(\w*)(\w)\2(\w*)')
        self.repl = r'\1\2\3'

    def replace(self, word):
        if wordnet.synsets(word):
            return word
        repl_word = self.repeat_regexp.sub(self.repl, word)
        if repl_word != word:
            return self.replace(repl_word)
        else:
            return repl_word


class Nate(object):
    def __init__(self, text):
        self._text = text
        self._regex = RegexpReplacer()

    def process(self):
        text = self._regex.replace(self._text)
        pt = english.parsetree(text, relations=True, lemmata=True)
        with GrabStdOut() as p:
            english.pprint(pt)
            print "---------------------------"
            for sent in pt:
                for wd in sent:
                    print (wd.string, wd.tag),
                print
        self._text = p.text

    @property
    def text(self):
        return self._text

#
#


#
#
# def tokenize_text(text):
#     sentences = tok.sent_tokenize(text)
#     for sent in sentences:
#         for token in _treebank(sent):
#             yield token

# from nltk.corpus import wordnet
# from nltk.corpus import stopwords
#
# stops = set(stopwords.words("english") + ["I"])
# b = text_
# from nltk.tokenize import WhitespaceTokenizer
#
# c = WhitespaceTokenizer().tokenize(b)
# outputty = """
# """
# for word in c:
#     syn = wordnet.synsets(word)
#     if word not in stops and syn:
#         syn = syn[0].lemma_names()
#         outputty += " " + syn[0]
#     else:
#         outputty += " " + word

# print(outputty)
