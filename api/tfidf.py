# -*- coding: utf-8 -*-
from collections import namedtuple
from itertools import chain
from math import log
from collections import Counter
from pprint import pprint
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

class TfIdf:

    @staticmethod
    def vector(docs):
        vectorizer = TfidfVectorizer(use_idf=True)
        return vectorizer.fit_transform(docs)

    @staticmethod
    def cluster(vector, clusters=3):
        return KMeans(n_clusters=clusters, random_state=0).fit_predict(vector)
