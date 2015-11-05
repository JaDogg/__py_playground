from collections import defaultdict
import os.path
import re
from math import log
import codecs
import sys

from standardiser import standardise
from nltk.tokenize import sent_tokenize as sent_tokenise
from nltk.tokenize import word_tokenize as word_tokenise
import urllib2
from BeautifulSoup import BeautifulSoup

def utf8open(loc, mode='r'):
    return codecs.open(loc, mode, 'utf8')

def localPath(filename):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), filename))

class Document(list):
    def __init__(self, url):
        """
        Build a list of sentences and a bag of words
        """
        list.__init__(self)
        title, text = self._urlToText(url)
        bow = defaultdict(int)
        for i, sentenceStr in enumerate(sent_tokenise(text)):
            sentence = Sentence(sentenceStr, i)
            self.append(sentence)
            for k, v in sentence.bagOfWords.items():
                bow[k] += v
        self.bagOfWords = bow
        self.title = title

    whiteRE = re.compile(r'\s+')
    constraintsRE = re.compile(u'^[^\u2022]|[.!?]$')
    def _urlToText(self, url):
        """
        Terrible text extraction using that ugly swamp beautifulsoup
        """
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page)
        body = soup.findAll('body')
        body = body[0] if body else soup
        parElements = [p for p in body.findAll('p') if not p.attrs]
        for node in [p for p in body(True) if p.find('br', recursive=False)]:
            for par in node.fetchText(True, recursive=False):
                parElements.append(par)
        paragraphs = []
        for paragraph in parElements:
            if isinstance(paragraph, unicode):
                text = paragraph
            else:
                text = ' '.join(paragraph.fetchText(True))
            text = self.whiteRE.sub(' ', text.strip())
            if self.constraintsRE.search(text):
                paragraphs.append(text)
        title = soup.find('title').string
        return title, '\n'.join(paragraphs) 

class IDFWeightedDocument(Document):
    weights = None
    @staticmethod
    def loadWeights(n):
        dfLoc = localPath('wiki_doc_freqs_trim.dat')
        # Read in the document freqs.
        # Have to do this first because we collapse some freqs through
        # standardisation.
        weights = defaultdict(int)
        for line in utf8open(dfLoc):
            term, freq = line.split('\t')
            term = standardise(term)
            if term:
                weights[hash(term)] += int(freq)
        # Turn the frequencies into IDF weights.
        for term, freq in weights.items():
            idf = log(n/freq, 10)
            weights[term] = int(idf)
        IDFWeightedDocument.weights = weights

    def __init__(self, url):
        class_ = self.__class__
        n = 818741.0
        if class_.weights is None:
            class_.loadWeights(n)
        weights = class_.weights
        Document.__init__(self, url)
        # Weight terms in bag of words
        bow = self.bagOfWords
        default = log(n/30)
        for term, freq in bow.items():
            bow[term] = freq*weights.get(term, default)
        
        



class Sentence(object):
    def __init__(self, sentenceStr, position):
        self.string = sentenceStr
        # Lowercase the first word
        if sentenceStr[0].isupper():
            letters = list(sentenceStr)
            letters[0] = letters[0].lower()
            sentenceStr = ''.join(letters)
        tokens = word_tokenise(sentenceStr)
        bow = defaultdict(int)
        for token in tokens:
            term = standardise(token)
            if term:
                hashed = hash(term)
                bow[hashed] += 1
        self.bagOfWords = bow
        self.position = position

    def __unicode__(self):
        return self.string

    def __str__(self):
        return self.string.decode('utf8', 'replace')


def test():
    """
    >>> doc = Document(u"This is a document test. Let's see the test goes.")
    >>> len(doc)
    2
    >>> print max(doc.bow.items(), key=lambda kv: kv[1])
    (u'test', 2)
    """
    pass


if __name__ == '__main__':
    import doctest
    doctest.testmod()
