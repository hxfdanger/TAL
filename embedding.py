import numpy as np
from keras.preprocessing.text import one_hot
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers.embeddings import Embedding
from keras.preprocessing.text import Tokenizer
import keras
import keras
import sys
from WordBuffer import WordBuffer
from keras.models import load_model


def create_corpus(pathFile):
    wb = WordBuffer()
    wb.readFromConlluFile(pathFile)
    return wb.corpus.copy()

# prepare tokenizer


def prepare_tokenizer(docs):
    t = Tokenizer(filters='')
    t.fit_on_texts(docs)
    return t


# integer encode the documents
def prepare_docs(t, docs):
    encoded_docs = t.texts_to_sequences(docs)
    padded_docs = pad_sequences(encoded_docs, maxlen=1, padding='post')
    return encoded_docs, padded_docs
# load the whole embedding into memory


def load_embeding_weight(file_path):
    embeddings_index = dict()
    f = open('pre_trained_words/fb_fr/wiki.fr.vec')
    for line in f:
        values = line.split()
        word = values[0]
        # print(values)
        try:
            coefs = np.asarray(values[1:], dtype='float32')
            embeddings_index[word] = coefs
        except:
            pass

    f.close()
    print('Loaded %s word vectors.' % len(embeddings_index))
    return embeddings_index

# create a weight matrix for words in training docs


def create_input_matrix(embeddings_index, vocab_size, t, dim_input):
    cpt_word_found = 0
    embedding_matrix = np.zeros((vocab_size, dim_input))
    for word, i in t.word_index.items():
        embedding_vector = embeddings_index.get(word)
        if embedding_vector is not None:
            embedding_matrix[i] = embedding_vector
            cpt_word_found += 1
    print("number of words pre-trained founds ", cpt_word_found)
    return embedding_matrix


def create_embedding_model(vocab_size, weight_matrix, pre_trained=True, dim_input=300, trainable=True, input_length=1):

    model = Sequential()
    if(pre_trained):
        e = Embedding(vocab_size, dim_input, weights=[
            weight_matrix], trainable=trainable, input_length=input_length)
    else:
        e = Embedding(vocab_size, dim_input, trainable=True,
                      input_length=input_length)

    model.add(e)
    # compile the model
    model.compile(optimizer='adam',
                  loss='binary_crossentropy', metrics=['acc'])
    return model


def save_weight_matrix(file, output_array, padded_docs, token):
    fichier = open("embd.vec", "w")
    for word, i in token.word_index.items():
        itemindex = np.where(padded_docs[:, 0] == i)
        try:
            l = output_array[itemindex[0][0], 0].tolist()
        except:
            print("word not found: ", word, i)
        ch = word + " " + " ".join(map(str, l)) + "\n"
        fichier.write(ch)

    fichier.close()


"""def embedding(file_conllu, pre_trained_file, pre_trained=True, dim_input=300, trainable=True, input_length=1):
    docs = create_corpus(file_conllu)
    token = prepare_tokenizer(docs)
    vocab_size = len(token.word_index) + 1

    encoded_docs, padded_docs = prepare_docs(token, docs)
    embeddings_index = load_embeding_weight(pre_trained_file)
    weight_matrix = create_input_matrix(
        embeddings_index, vocab_size, token, dim_input)
    model = create_embedding_model(
        vocab_size, weight_matrix, pre_trained, weight_matrix.shape[1], trainable=trainable, input_length=input_length)
    output_array = model.predict(padded_docs)
    return output_array"""


# test how use embedding
# exemple create model without pre_trained weight
file_conllu = "UD_French-GSD/fr_gsd-ud-train.conllu"
pre_trained_file = "pre_trained_words/fb_fr/wiki.fr.vec"
save_file_for_wright = "embd.vec"

docs = create_corpus(file_conllu)


token = prepare_tokenizer(docs)
vocab_size = len(token.word_index) + 1
encoded_docs, padded_docs = prepare_docs(token, docs)
embeddings_index = load_embeding_weight(pre_trained_file)
# if u use a pre_trained model, make sure that u use put the same dim in the pre-trained_file
dim_input = 300
weight_matrix = create_input_matrix(
    embeddings_index, vocab_size, token, dim_input)

# i will not use the pre_trained weight in this exemple 'pre_trained=False'
# so i will make 'dim_input=100' to represent a vector's word dim
model = create_embedding_model(
    vocab_size, weight_matrix, pre_trained=False, dim_input=100, trainable=True)
output_array = model.predict(padded_docs)
save_weight_matrix(save_file_for_wright, output_array, padded_docs, token)

model.save('my_model.h5')

del model  # deletes the existing model

# returns a compiled model
# identical to the previous one
model = load_model('my_model.h5')
