__author__ = 'ssm'

'''
online training word embedding for paper words
'''


import gensim, logging, os
from gensim.models.word2vec import LineSentence
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def train_save(sentences):
    if os.path.isfile('w2v'):
        model = gensim.models.Word2Vec.load('w2v')
    else:
        model = gensim.models.Word2Vec(sentences, hs=1)
        model.save('w2v')
        return model
    model.train(sentences)
    model.save('w2v')

sentences = LineSentence("paper_wanfang_2.txt")
train_save(sentences)

