from django.shortcuts import render

import os
import json
import pickle
import numpy as np
import pandas as pd

import tensorflow as tf
from keras import backend as K
# os.environ['KERAS_BACKEND'] = 'tensorflow'
from keras.models import load_model
from keras_contrib.layers import CRF
from keras_contrib.losses import crf_loss
from keras_contrib.metrics import crf_viterbi_accuracy
from keras.preprocessing.sequence import pad_sequences

from predict.att import Attention
from predict.extract_feature import BertVector

# global graph, modelner, modelre

import nltk

nltk.download('punkt')

# tf.disable_v2_behavior()
K.clear_session()
# tf.reset_default_graph()
# tf.enable_eager_execution()

# initializing the graph
# graph = tf.get_default_graph()

# loading ner trained model
print("Keras NER model loading.......")
modelner = load_model(
    os.path.abspath(os.getcwd()) + '/static/NER/model.hdf5',
    custom_objects={
        'CRF': CRF,
        'crf_loss': crf_loss,
        'crf_viterbi_accuracy': crf_viterbi_accuracy
    }
)
print("Model NER loaded!!")

print("Keras RE model loading.......")
modelre = load_model(
    os.path.abspath(os.getcwd()) + '/static/RE/model.hdf5',
    custom_objects={"Attention": Attention})
print("Model RE loaded!!")


def tokenize(s): return nltk.word_tokenize(s)


class group_sentence(object):
    def __init__(self, df):
        self.n_sent = 1
        self.df = df
        self.empty = False
        agg = lambda s: [(w, t) for w, t in zip(s['words'].values.tolist(), s['tags'].values.tolist())]
        self.grouped = self.df.groupby("sentence #").apply(agg)
        self.sentences = [s for s in self.grouped]

    def get_text(self):
        try:
            s = self.grouped['sentence: {}'.format(self.n_sent)]
            self.n_sent += 1
            return s
        except:
            return None


# Create your views here.
def index(request):
    context = {
        'judul': 'NLP - Text Mining | Predict',
        'subjudul': 'Prediksi Entitas dan Relasi suatu Kalimat',
        'author': 'Dimas Dwi Putra',
        'nav': [
            ['/', 'Home'],
            ['/sample/', 'Kalimat'],
            # ['/predict/', 'Predict'],
            ['/about/', 'About'],
        ]
    }

    sentences = ""
    predict_output = []
    group_sentences = []

    plant_output = []
    disease_output = []

    plant_re_output = []
    disease_re_output = []

    relation_output = ""

    if request.method == 'POST':
        sentences = request.POST['sentences']

        max_len = 3000

        with open(os.path.abspath(os.getcwd()) + '/static/NER/word_to_index.pickle', 'rb') as handle:
            word_to_index = pickle.load(handle)

        with open(os.path.abspath(os.getcwd()) + '/static/NER/tag_to_index.pickle', 'rb') as handle:
            tag_to_index = pickle.load(handle)

        with open(os.path.abspath(os.getcwd()) + '/static/NER/words.pickle', 'rb') as handle:
            words = pickle.load(handle)

        with open(os.path.abspath(os.getcwd()) + '/static/NER/tags.pickle', 'rb') as handle:
            tags = pickle.load(handle)

        idx2word = {i: w for w, i in word_to_index.items()}
        idx2tag = {i: w for w, i in tag_to_index.items()}

        predict_sentences = tokenize(sentences)

        x_test_sent = pad_sequences(
            sequences=[[word_to_index.get(w, 0) for w in predict_sentences]],
            padding="post", maxlen=max_len)

        y_pred = modelner.predict(x_test_sent)
        y_pred = np.argmax(y_pred, axis=-1)
        y_pred = [[idx2tag[i] for i in row] for row in y_pred]

        i = np.random.randint(0, x_test_sent.shape[0])
        p = modelner.predict(np.array([x_test_sent[i]]))
        p = np.argmax(p, axis=-1)

        for w, pred in zip(x_test_sent[i], p[0]):
            if w != 0:
                id_sents = "sentence: 1"
                words_output = r"{}".format(words[w - 2])
                tags_output = r"{}".format(idx2tag[pred])
                single_words = words_output

                if tags_output == "plant":
                    words_output = words_output.replace(
                        words_output,
                        f'<a href="http://www.google.com/search?q={words_output}" target="_blank" class="btn btn-sm btn-rounded btn-alt-success mr-10">{words_output}</a>')

                if tags_output == "disease":
                    words_output = words_output.replace(
                        words_output,
                        f'<a href="http://www.google.com/search?q={words_output}" target="_blank" class="btn btn-sm btn-rounded btn-alt-warning mr-10">{words_output}</a>')

                predict_output.append([id_sents, single_words, words_output, tags_output])

        df = pd.DataFrame(predict_output, columns=['sentence #', 'single_words', 'words', 'tags'])
        # print(df)
        getter = group_sentence(df)
        group_sentences = [" ".join([s[0] for s in sent]) for sent in getter.sentences]
        group_sentences = group_sentences[0]

        for v, w, t in zip(df['single_words'].tolist(), df['words'].tolist(), df['tags'].tolist()):
            if t == 'plant' and w not in plant_output:
                plant_output.append(w)
                plant_re_output.append(v)

            if t == 'disease' and w not in disease_output:
                disease_output.append(w)
                disease_re_output.append(v.replace(v, f'#{v}#'))
    
    if (len(plant_output) != 0) and (len(disease_output) != 0):
        po_plant = (','.join(str(po) for po in plant_re_output)).replace(',', ' ')
        do_disease = ("#', '#".join(str(do) for do in disease_re_output)).replace(',', '').replace("##' '##", ' ')

        re_sentences = f"{po_plant}{do_disease}{sentences}"

        print(re_sentences)

        per1, per2, doc = re_sentences.split('#')

        find_plant = doc.find(per1)
        find_disease = doc.find(per2.replace("#", ''))

        print(find_plant, find_disease)

        if find_plant < find_disease:
          text = doc.split(per2)[0] + per2
            
        if find_plant > find_disease:
          text = doc.split(per1)[0] + per1

        text = '$'.join([per1, per2, text.replace(per1, len(per1) * '#').replace(per2, len(per2) * '#')])

        print(text)

        bert_model = BertVector(pooling_strategy="NONE", max_seq_len=512)
        vec = bert_model.encode([text])["encodes"][0]
        x_train = np.array([vec])

        predicted = modelre.predict(x_train)
        y = np.argmax(predicted[0])

        with open(os.path.abspath(os.getcwd()) + '/static/RE/rel_dict.json', 'r', encoding='utf-8') as f:
          rel_dict = json.load(f)

        id_rel_dict = {v: k for k, v in rel_dict.items()}


        relation_output = ('%s' % id_rel_dict[y])
    else:
        relation_output = "Unknown"

    context['ori_sentences'] = sentences
    context['sentences'] = group_sentences
    context['plant_predict'] = (','.join(str(a) for a in plant_output)).replace(',', '')
    context['disease_predict'] = (','.join(str(b) for b in disease_output)).replace(',', '')
    context['relation_predict'] = f'<a href="http://www.google.com/search?q={relation_output}" target="_blank" class="btn btn-sm btn-rounded btn-alt-primary mr-10">{relation_output}</a>'

    return render(request, "index.html", context)
