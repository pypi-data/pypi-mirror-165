from nltk.stem import PorterStemmer
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from nltk import download
from gensim.models import KeyedVectors
import gensim.downloader as api
from sentence_transformers import SentenceTransformer, util, InputExample, losses, models
from string import punctuation
from nltk.stem import PorterStemmer
from nltk.stem.isri import ISRIStemmer


def preprocess(sentence, remove_punct, remove_stop_words, stemm, lang='en'):
    if lang.lower() == 'en':
        ps = PorterStemmer()
        # remove punctuations
        if not remove_punct:
            sentence = sentence.translate(str.maketrans('', '', punctuation))
        # remove stop words and stem
        if remove_stop_words and stemm:
            download('stopwords')
            stop_words = stopwords.words('english')
            return ' '.join([ps.stem(w) for w in sentence.lower().split() if w not in stop_words])
        # stem only
        elif not remove_stop_words and stemm:
            return ' '.join([ps.stem(w) for w in sentence.lower().split()])
        else:
            # lower case and remove extra white spaces
            return ' '.join([w for w in sentence.lower().split()])
    elif lang.lower() == 'ar':
        st = ISRIStemmer()
        # remove punctuations
        if not remove_punct:
            sentence = sentence.translate(str.maketrans('', '', punctuation))
        # remove stop words and stem
        if remove_stop_words and stemm:
            download('stopwords')
            stop_words = stopwords.words('arabic')
            return ' '.join([st.stem(w) for w in sentence.lower().split() if w not in stop_words])
        # stem only
        elif not remove_stop_words and stemm:
            return ' '.join([st.stem(w) for w in sentence.lower().split()])
        else:
            # lower case and remove extra white spaces
            return ' '.join([w for w in sentence.lower().split()])
    else:
        raise Exception('non recognized language please specify either en|ar')
        
        
class sentence_tranformer():
    def __init__(self, source_names, target_names, model=None):
        if not source_names:
            raise Exception('Inputs are empty')
        self.source_names = source_names
        self.target_names = [target  for target in target_names if not (pd.isnull(target))] 
        self.model = model
        # if no model is provided use the default model
        if model is None:
            print('initializing the model...')
            self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

        # encode the targets
        self.encoded_targets = self.model.encode(self.target_names)
        


    def match(self, topn=1):
        '''
        Main match function. return only the top candidate for every source string.
        '''
        self.topn = topn
        self.top_cosine_sim()

        match_output = self._make_matchdf()

        return match_output

    def clean_data(self, remove_punct=True, remove_stop_words=True, stemm=False, lang='en'): 
        self.source_names = [preprocess(sent, remove_punct, remove_stop_words, stemm, lang) for sent in self.source_names]
        self.target_names = [preprocess(sent, remove_punct, remove_stop_words, stemm, lang) for sent in self.target_names]


    def max_cosine_sim(self, input):
        cosine_results = util.cos_sim(input, self.encoded_targets)
        sorted = -np.sort(-cosine_results)
        targets = []
        max_cosines = []
        for x in sorted[0]:
            if len(targets) == self.topn:
                break
            for i in (np.where(cosine_results == x)[1]):
                targets.append(self.target_names[i])
                max_cosines.append(x)
                if len(targets) == self.topn:
                    break

        return targets, max_cosines
    

    def top_cosine_sim(self):
        results = np.array([self.max_cosine_sim(self.model.encode(input)) if not (pd.isnull(input)) else (None, None) for input in self.source_names], dtype=object)
        self.targets = results[:, 0]
        self.top_cosine = results[:, 1]

    def _make_matchdf(self):
        ''' Build dataframe for result return '''

        # to list of tuples
        match_list = []
        for source, target, top_score in zip(self.source_names,self.targets, self.top_cosine):
            row = []
            row.append(source)
            if target is not None:
                for x, y in zip(target, top_score):
                    row.append(x)
                    row.append(y) 
            match_list.append(tuple(row))

        # prepare columns names
        colnames = ['source', 'prediction', 'score']
        
        for i in range(2, self.topn+1):
            colnames.append(f'prediction_{i}')
            colnames.append(f'score_{i}')
    
        match_df = pd.DataFrame(match_list, columns=colnames)

        return match_df



class word_mover_distance():
    def __init__(self, source_names, target_names, model):
        if not source_names:
            raise Exception('Inputs are empty')
        self.source_names = source_names
        self.target_names = target_names
        self.model = model
        
        # if no model is provided use the default model
        if model is None:
            print('initializing the model (English model)...')
            self.model = api.load('glove-wiki-gigaword-300')

    def match(self, topn=1):
        '''
        Main match function. return only the top candidate for every source string.
        '''
        self.topn = topn
        
        self.top_wmd_distance()

        match_output = self._make_matchdf()

        return match_output


    def clean_data(self, remove_punct=True, remove_stop_words=True, stemm=False, lang='en'): 
        self.source_names = [preprocess(sent, remove_punct, remove_stop_words, stemm, lang) for sent in self.source_names]
        self.target_names = [preprocess(sent, remove_punct, remove_stop_words, stemm, lang) for sent in self.target_names]


    def min_wmd_distance(self, input):
        wmd_results = np.array([self.model.wmdistance(input, target) for target in self.target_names])
        
        # get topn results
        wmd_sorted = np.sort(wmd_results)
        results = []
        scores = []
        for x in wmd_sorted:
            if len(results) == self.topn:
                break
            # convert distance to score
            scores.append(1 - x)
            for y in np.where(wmd_results == x):
                results.append(y[0])
                if len(results) == self.topn:
                    break    
        targets = [self.target_names[idx] for idx in results]
        
        # fill empty topn results 
        while len(targets) < self.topn:
            targets.append(None)
            scores.append(None)

        return targets, scores
    

    def top_wmd_distance(self):
        results = np.array([self.min_wmd_distance(input) for input in self.source_names])
        self.targets = results[:, 0]
        self.top_scores = results[:, 1]


    def _make_matchdf(self):
        ''' Build dataframe for result return '''

        match_list = []
        for source, target, top_score in zip(self.source_names, self.targets, self.top_scores):
            row = []
            row.append(source)
            if target is not None:
                for x, y in zip(target, top_score):
                    row.append(x)
                    row.append(y) 
            match_list.append(tuple(row))

        # prepare columns names
        colnames = ['source', 'prediction', 'score']
        
        for i in range(2, self.topn+1):
            colnames.append(f'prediction_{i}')
            colnames.append(f'score_{i}')

        match_df = pd.DataFrame(match_list, columns=colnames)
        
        return match_df