import _stops
import nltk.stem.porter

class _Standardise(object):
    def __init__(self):
        self.stemmer = lambda word: word
        self.stopWords = {}
        self.lower = False
    
    def __call__(self, string):
        if string.lower() in self.stopWords:
            return None
        if self.lower:
            string = string.lower()
        stemmed = self.stemmer(string)
        return stemmed

    def config(self, **kwargs):
        stemmer = kwargs.pop('stemming')
        if stemmer == 'porter':
            self.stemmer = nltk.stem.porter.PorterStemmer().stem_word
        else:
            raise StandardError, "Unknown stemmer specified", stemmer
        stops = kwargs.pop('stopping')
        if stops == True:
            self.stopWords = _stops.nltkStops
        self.lower = kwargs.pop('lower')
        
# Instance for others to access
standardise = _Standardise()
