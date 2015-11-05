import sys

import summariser
from document import Document, IDFWeightedDocument
from standardiser import standardise
from math import log

standardise.config(stemming='porter',
                   stopping=False,
                   lower=False)

summariser = summariser.Summariser()
def summarise(url):
    try:
        document = IDFWeightedDocument(url)
    except:
        raise
        return "Unable to download or parse URL"
    
    n = int(log(len(document)))
    sentences = summariser(document, n)
    return document.title, _format(sentences)


def _format(sentences):
    return '\n'.join([u'<p><span style="font-family: arial;">%s</span></p>' % unicode(sentence)
                      for sentence in sentences])

if __name__ == '__main__':
    print summarise('http://www.smh.com.au/national/music-teacher-jailed-for-student-sex-20091120-ipul.html',
            'Frequency', 3)        
