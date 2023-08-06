# similarity_check

similarity_check is a Python package for measuring the similarity of two texts.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install similarity_check.

```bash
pip install similarity_check 
```

## Usage
### sentence tranformer
```python
from similarity_check.checkers import sentence_tranformer

X = ['test', 'remove test']
y =  ['tests', 'stop the test']

st = sentence_tranformer(X, y)
st.clean_data()
match_df = st.match(topn=2)
```
* sentence_tranformer(source_names, target_names, model=None):
  * source_names: a list of input texts to find closest match for.
  * target_names: a list of targets text to compare with.
  * model (optional): a sentence tranformer model to use instead of the default one for more [details](https://www.sbert.net/).
* sentence_tranformer.clean_data(remove_punct=True, remove_stop_words=True, stemm=False, lang='en'):
  * remove_punct: boolean flag to indicate whatever to remove punctuations. 
  * remove_stop_words: boolean flag to indicate whatever to remove stop words.
  * stemm: boolean flag to indicate whatever to do stemming.
  * lang: language of the text to clean ('en', 'ar').
* sentence_tranformer.match(topn=1):
  * topn: number of matches to return.
  * return_match_idx: return an extra column for each match containing the index of the match within the target_names.
  * returns: a data frame with 3 columns (source, target, score), and two extra columns for each extra match (target_2, score_2 ...)
### word mover distance
#### english
```python
# for medical use #
# from gensim.models import KeyedVectors
# download the model from here: https://github.com/ncbi-nlp/BioSentVec
# model = KeyedVectors.load_word2vec_format('BioWordVec_PubMed_MIMICIII_d200.vec.bin', binary=True)

# for general usage #
import gensim.downloader as api
from similarity_check.checkers import word_mover_distance

model = api.load('glove-wiki-gigaword-300')

X = ['test now', 'remove test']
y =  ['tests', 'stop the test']

wmd = word_mover_distance(X, y, model)
wmd.clean_data()
match_df = wmd.match(topn=3)
```
#### arabic
```python
from gensim.models import Word2Vec
from similarity_check.checkers import word_mover_distance

# download the embedding from here: https://github.com/bakrianoo/aravec (N-Grams Models, Wikipedia-SkipGram, Vec-Size:300)
model = Word2Vec.load('full_grams_sg_300_wiki/full_grams_sg_300_wiki.mdl')
# take the keydvectors as the model
model = model.wv

X = ['حذف الاختبار', 'اختبار']
y =  ['اختبارات', 'ايقاف الاختبار']

wmd = word_mover_distance(X, y, model)
wmd.clean_data()
match_df = wmd.match(topn=3)
match_df
```
* word_mover_distance(source_names, target_names, model, return_match_idx=False):
  * source_names: a list of input texts to find closest match for.
  * target_names: a list of targets text to compare with.
  * model (optional): a keyed vectors model (embeddings) to use for more [details](https://radimrehurek.com/gensim/auto_examples/tutorials/run_word2vec.html).
* word_mover_distance.clean_data(remove_punct=True, remove_stop_words=True, stemm=False, lang='en'):
  * remove_punct: boolean flag to indicate whatever to remove punctuations. 
  * remove_stop_words: boolean flag to indicate whatever to remove stop words.
  * stemm: boolean flag to indicate whatever to do stemming.
  * lang: language of the text to clean ('en', 'ar').
* sentence_tranformer.match(topn=1):
  * topn: number of matches to return.
  * return_match_idx: return an extra column for each match containing the index of the match within the target_names.
  * returns: a data frame with 3 columns (source, target, score), and two extra columns for each extra match (target_2, score_2 ...)
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)