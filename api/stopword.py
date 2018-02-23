# -*- coding: utf-8 -*-
import os
import urllib.request
from collections import Counter
from pprint import pprint

class StopWord:

    def __init__(self, tokens = '', stopwords = []):
        self.tokens = tokens
        # new_stopwords = self.get_stopwords(tokens)
        # self.stopwords = list(new_stopwords.union(stopwords))
        self.stopwords = list(stopwords)

    def remove_stopwords(self):
        tokens = [token for token in self.tokens if token.word not in self.stopwords]
        return tokens

    @staticmethod
    def get_stopwords(tokens, max_freq_ratio = 0.07, min_freq = 1):
        max_freq = len(tokens) * max_freq_ratio
        fdist = Counter()
        for token in tokens:
            fdist[token.word] += 1
        common_words = {word for word, freq in fdist.items() if freq >= max_freq}
        rare_words = {word for word, freq in fdist.items() if freq <= min_freq}
        short_words = {word for word, freq in fdist.items() if len(word) <= 1}
        stopwords = common_words.union(rare_words).union(short_words)
        return stopwords
