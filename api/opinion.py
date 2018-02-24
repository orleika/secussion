# -*- coding: utf-8 -*-
from gsearch import GoogleScrapy
from clean import Clean
from stopword import StopWord
from tokenizer import MeCabTokenizer
from tfidf import TfIdf
from db import DB
import numpy
import re
from itertools import chain
from pprint import pprint
from collections import namedtuple

class Opinion:

    def __init__(self, keywords, opinion):
        self.keywords = ' '.split(keywords)
        self.opinion = opinion

    @staticmethod
    def search_articles(keywords):
        search_word = ' '.join(keywords)
        google = GoogleScrapy(search_word)
        google.start()
        return google.articles

    @staticmethod
    def tokenize(sentence, pos='default'):
        tokenizer = MeCabTokenizer(user_dic_path = '/usr/local/lib/mecab/dic/mecab-ipadic-neologd')
        if pos == 'noun':
            tokens = tokenizer.extract_noun_baseform(sentence)
        elif pos == 'verbs':
            tokens = tokenizer.extract_verbs_baseform(sentence)
        elif pos == 'noun_verbs':
            tokens = tokenizer.extract_noun_verbs_baseform(sentence)
        else:
            tokens = tokenizer.extract_baseform(sentence)
        return tokens

    @staticmethod
    def tokenize_surface(pos='noun_verbs'):
        def surface(sentence):
            return [token.surface for token in Teheme.tokenize(sentence, pos)]

    @staticmethod
    def clean(sentence):
        return Clean(sentence).clean_html_and_js_tags().clean_text().text

    @staticmethod
    def trimmed_stopwords(tokens):
        db = DB(host = 'mysql')
        stopwords = db.get_stopwords()
        sw = StopWord(tokens = tokens, stopwords = [stopword.word for stopword in stopwords])
        return sw.remove_stopwords()

    @staticmethod
    def divide(article):
        return list(filter(None, map(str.strip, re.findall(r'[^。．？！…?!　\n]+(?:[。。．？！…?!　\n]|$)', article))))

    @staticmethod
    def is_sentence(sentence):
        tokens = Opinion.tokenize(sentence, pos='verbs')
        if len(tokens) == 0 or len(sentence) > 100 or len(sentence) < 10:
            return False
        else:
            return True

    @staticmethod
    def senti(sentence):
        db = DB(host = 'mysql')
        tokenizer = MeCabTokenizer(user_dic_path = '/usr/local/lib/mecab/dic/mecab-ipadic-neologd')
        tokens = tokenizer.extract_senti_baseform(sentence)
        score = 0.0
        for token in tokens:
            pn = db.get_pn(surface = token.surface, reading = token.reading, pos = token.pos)
            if len(pn) == 0:
                continue
            else:
                score += pn[0].score
        return score / len(tokens)

    def get(self):
        # standardize
        keywords = self.trimmed_stopwords(self.tokenize(self.opinion, pos='noun_verbs'))
        # search about opinion with keywords
        articles = self.search_articles(self.keywords + [keyword.surface for keyword in keywords][:3])
        # clean
        docs = map(self.clean, articles)
        # divide sentences
        sentences_cand = map(self.divide, docs)
        sent = []
        for s in sentences_cand:
            sent.append(list(filter(self.is_sentence, s)))
        sentences = list(chain.from_iterable(sent))
        # tfidf format
        sentence_tokens = []
        for sentence in sentences:
            noun_tokens = [token.surface for token in self.tokenize(sentence, pos='noun')]
            sentence_tokens.append(' '.join(noun_tokens))
        # vectorize
        vector = TfIdf.vector(sentence_tokens)
        # clustering
        cluster = numpy.array(TfIdf.cluster(vector, clusters=3))
        # retrieve opinion with tf
        tfidf_score = numpy.array([sum(v) for v in vector.toarray()])
        # retrieve opinion with senti
        # senti_score = numpy.array([self.senti(s) for s in sentences])
        senti_score = []
        for s in sentences:
            senti_score.append(self.senti(s))
        senti_score = numpy.array(senti_score)
        score_index = numpy.argsort(tfidf_score * senti_score)
        positives = []
        negatives = []
        for i in range(3):
            # retrieve vector index by cluster
            c_index = numpy.where(cluster == i)
            for k in score_index:
                if k in c_index[0]:
                    negatives.append(sentences[k])
                    break
            for k in score_index[::-1]:
                if k in c_index[0]:
                    positives.append(sentences[k])
                    break
        opinion = namedtuple('Opinion', 'positives, negatives')
        return opinion(positives, negatives)
