from __future__ import absolute_import, print_function

text_ = """
In computational linguistics, word-sense disambiguation (WSD) is an open problem of natural language processing and ontology. WSD is identifying which sense of a word (i.e. meaning) is used in a sentence, when the word has multiple meanings. The solution to this problem impacts other computer-related writing, such as discourse, improving relevance of search engines, anaphora resolution, coherence, inference et cetera.

The human brain is quite proficient at word-sense disambiguation. The fact that natural language is formed in a way that requires so much of it is a reflection of that neurologic reality. In other words, human language developed in a way that reflects (and also has helped to shape) the innate ability provided by the brain's neural networks. In computer science and the information technology that it enables, it has been a long-term challenge to develop the ability in computers to do natural language processing and machine learning.

To date, a rich variety of techniques have been researched, from dictionary-based methods that use the knowledge encoded in lexical resources, to supervised machine learning methods in which a classifier is trained for each distinct word on a corpus of manually sense-annotated examples, to completely unsupervised methods that cluster occurrences of words, thereby inducing word senses. Among these, supervised learning approaches have been the most successful algorithms to date.

Current accuracy is difficult to state without a host of caveats. In English, accuracy at the coarse-grained (homograph) level is routinely above 90%, with some methods on particular homographs achieving over 96%. On finer-grained sense distinctions, top accuracies from 59.1% to 69.0% have been reported in recent evaluation exercises (SemEval-2007, Senseval-2), where the baseline accuracy of the simplest possible algorithm of always choosing the most frequent sense was 51.4% and 57%, respectively.
"""
#
# _treebank = tok.TreebankWordTokenizer().tokenize
#
# replacement_patterns = [
#     (r'won\'t', 'will not'),
#     (r'can\'t', 'cannot'),
#     (r'i\'m', 'i am'),
#     (r'ain\'t', 'is not'),
#     (r'(\w+)\'ll', '\g<1> will'),
#     (r'(\w+)n\'t', '\g<1> not'),
#     (r'(\w+)\'ve', '\g<1> have'),
#     (r'(\w+)\'s', '\g<1> is'),
#     (r'(\w+)\'re', '\g<1> are'),
#     (r'(\w+)\'d', '\g<1> would')
# ]
#
#
# class RegexpReplacer(object):
#     def __init__(self, patterns=replacement_patterns):
#         self.patterns = [(re.compile(regex), repl) for (regex, repl) in
#                          patterns]
#
#     def replace(self, text):
#         s = text
#         for (pattern, repl) in self.patterns:
#             (s, count) = re.subn(pattern, repl, s)
#         return s
#
#
# class RepeatReplacer(object):
#     def __init__(self):
#         self.repeat_regexp = re.compile(r'(\w*)(\w)\2(\w*)')
#         self.repl = r'\1\2\3'
#
#     def replace(self, word):
#         if wordnet.synsets(word):
#             return word
#         repl_word = self.repeat_regexp.sub(self.repl, word)
#         if repl_word != word:
#             return self.replace(repl_word)
#         else:
#             return repl_word
#
#
# def tokenize_text(text):
#     sentences = tok.sent_tokenize(text)
#     for sent in sentences:
#         for token in _treebank(sent):
#             yield token

from nltk.corpus import wordnet
from nltk.corpus import stopwords

stops = set(stopwords.words("english") + ["I"])
b = text_
from nltk.tokenize import WhitespaceTokenizer

c = WhitespaceTokenizer().tokenize(b)
outputty = """
"""
for word in c:
    syn = wordnet.synsets(word)
    if word not in stops and syn:
        syn = syn[0].lemma_names()
        outputty += " " + syn[0]
    else:
        outputty += " " + word

print(outputty)