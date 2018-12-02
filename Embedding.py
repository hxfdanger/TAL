"""


"""
import gensim
from gensim.models import word2vec


class Embedding:


    def __init__(self,corpus_file,type_encoder="word2vec"):

        self.filename = corpus_file
        self.type = type_encoder

        if(self.type == "word2vec"):
            sentences=word2vec.Text8Corpus (self.filename)

            params={
                'alpha': 0.05,  # learning rate
                'size': 100,  # number of dimensions for the dense representations
                #     'window': 5,     # context window size
                #     'iter':   5,     # nb of iterations
                #     'min_count': 1,  # to ignore very rare words
                #     'negative': 5    # we need negative examples, how many?
            }

            my_model=word2vec.Word2Vec (sentences, **params)

            self.model = my_model
            print(my_model)
            print(my_model.wv["Les"])



    def word_vectEmbeddind(self,word=""):

        if(self.type == "word2vec"):
            self.model.wv[word]




if(__name__ == "__main__"):
    em = Embedding("Data/fr_gsd-ud-train.txt")

    p = em.word_vectEmbeddind("Les")
    print(p)





