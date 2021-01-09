import requests
import en_core_web_lg
from nltk.tokenize import sent_tokenize
import nltk
import heapq

spacy = en_core_web_lg.load()
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords

stop_words = stopwords.words('english')
# spacy = spacy.load(en_core_web_lg)
import pandas as pd
import numpy as np

import networkx as nx

"""
def remove_stopwords(sen):
    sen_new = " ".join([i for i in sen if i not in stop_words])
    return sen_new
"""

from sklearn.metrics.pairwise import cosine_similarity

stop_words = stopwords.words('english')


class SummariseAndCategorise:
    class_list = ['Thoughts', 'Saved for later', 'Work', 'School', 'Reminders', 'Schedule', 'Hobby', 'Starred']
    class_list_lower = [s.lower() for s in class_list]
    class_list_rep = ['thoughts', 'later', 'work', 'school', 'reminders', 'schedule', 'hobby'] #starred is user put in
    class_list_vectors = []
    def __init__(self):
        self.word_embeddings = {}
        self.init_word_embeddings()
        self.sentence_vectors = []
        #self.process_categories()


    def process_categories(self):
        for i in self.class_list_lower:
            if len(i) != 0:
                v = sum([self.word_embeddings.get(w, np.zeros((100,))) for w in i.split()]) / (len(i.split()) + 0.001)
            else:
                v = np.zeros((100,))
            self.class_list_vectors.append(v)

    def init_word_embeddings(self):
        f = open('./glove.6B/glove.6B.100d.txt', encoding='utf-8')
        for line in f:
            values = line.split()
            word = values[0]
            coefs = np.asarray(values[1:], dtype='float32')
            self.word_embeddings[word] = coefs
        f.close()


    @staticmethod
    def getNounsAndVerbs(self, text):
        doc = spacy(text)

        # Analyze syntax
        #print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
        # print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])
        toRet = [chunk.text for chunk in doc.noun_chunks]
        toRet.extend([str(entity) for entity in doc.ents])
        toRet = list(set(toRet))
        return toRet



    @staticmethod
    def get_entities_phrases_concepts(self, text):
        doc = spacy(text)
        return [entity for entity in doc.ents]#[[entity.text, entity.label_] for entity in doc.ents]

    # function to remove stopwords
    @staticmethod
    def remove_stopwords(self, sen):
        sen_new = " ".join([i for i in sen if i not in stop_words])
        return sen_new

    def summarise(self, text):
        res = []
        # remove punctuations, numbers and special characters
        sentences = sent_tokenize(text)
        if len(sentences) > 4:
            res = self.summarise_large(sentences)
        else:
            res = self.summarise_short(" ".join(sentences))
        #print(res)
        return res

    def summarise_short(self, sentences):
        return self.getNounsAndVerbs(self,sentences)

    def summarise_large(self, sentences):
        clean_sentences = pd.Series(sentences).str.replace("[^a-zA-Z]", " ")
        # make alphabets lowercase
        clean_sentences = [s.lower() for s in clean_sentences]
        # remove stopwords from the sentences
        clean_sentences = [self.remove_stopwords(self, r.split()) for r in clean_sentences]
        sentence_vectors = []
        for i in clean_sentences:
            if len(i) != 0:
                v = sum([self.word_embeddings.get(w, np.zeros((100,))) for w in i.split()]) / (len(i.split()) + 0.001)
            else:
                v = np.zeros((100,))
            sentence_vectors.append(v)

        sim_mat = np.zeros([len(sentences), len(sentences)])
        for i in range(len(sentences)):
            for j in range(len(sentences)):
                if i != j:
                    sim_mat[i][j] = \
                        cosine_similarity(sentence_vectors[i].reshape(1, 100), sentence_vectors[j].reshape(1, 100))[
                            0, 0]
        nx_graph = nx.from_numpy_array(sim_mat)
        scores = nx.pagerank(nx_graph)
        ranked_sentences = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)
        return [x[1] for x in ranked_sentences[:15]]


    """
        @:param arrProcessed A list of processed strings. Each element is either a phrase or sentence
    """
    def categorise(self, arrProcessed):
     #   print("CATEGORISING")
     #   print(arrProcessed)
        freq = {

        }
        best_cat = ""
        best_freq = -1
        for x in arrProcessed:
            tokens = spacy(x)
            """
            for token1 in tokens:
                for token2 in tokens:
                    print(token1.text, token2.text, token1.similarity(token2))
                    """
            keywords = self.getNounsAndVerbs(self, x)
            keywordTokens = spacy(" ".join(keywords))
            categoryTokens = spacy(" ".join(self.class_list_rep))
            """
            for token1 in keywordTokens:
                for token2 in keywordTokens:
                    print(token1.text, token2.text, token1.similarity(token2))
                    """
            highest_cat = ""
            highest_score = -1
           # print("CATEGORY TOKENS")
           # print(categoryTokens)
            for idx, cat in enumerate(categoryTokens):
                for words in keywordTokens:
                    curscore = cat.similarity(words)
                   # print(curscore)
                #    print(idx)
                    if curscore > highest_score:
                   #     print("HIGHEST")
                        highest_cat = self.class_list[idx]
                        highest_score = curscore
            #print(highest_score,highest_cat)
            if highest_cat in freq:
                freq[highest_cat] += 1
            else:
                freq[highest_cat] = 1
            if freq[highest_cat] > best_freq:
                best_freq = freq[highest_cat]
                best_cat = highest_cat
        #print(freq)
        #print("CATEGORY: " + best_cat)
        if best_cat == "":
            best_cat = "Others"
        return best_cat




"""
class Categorise:
    class_list = ['Thoughts', 'Saved for later', 'Work', 'School', 'Reminders/Schedule', 'Starred', 'Hobby']
    def __init__(self):
        self.PRE_TRAINED_MODEL_NAME = 'bert-base-cased'
        #tokenizer = BertTokenizer.from_pretrained(PRE_TRAINED_MODEL_NAME)
"""