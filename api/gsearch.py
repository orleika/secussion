# -*- coding: utf-8 -*-
import os
import sys, io
from collections import namedtuple
# from selenium import webdriver
# from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver.common.keys import Keys
from pprint import pprint
from joblib import Parallel, delayed
import requests
from bs4 import BeautifulSoup, Comment
import html5lib
import re

SearchResultRow = namedtuple(
    'SearchResultRow',
    ['title', 'url', 'display_url', 'dis']
)

ArticleResultRow = namedtuple(
    'ArticleResultRow',
    ['html']
)

# os.environ['MOZ_HEADLESS'] = '1'
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class GoogleScrapy:
    def __init__(self, keyword, default_wait=1):
        self.url = 'https://www.google.co.jp/search?pws=0&tbs=qdr:w'
        self.keyword = keyword
        # self.default_wait = default_wait
        # self.driver = None
        self.searches = []
        self.articles = []

    def enter_keyword(self):
        self.driver.get(self.url)
        self.driver.find_element_by_id('lst-ib').send_keys(self.keyword)
        self.driver.find_element_by_id('lst-ib').send_keys(Keys.RETURN)

    # def get_search(self):
    #     all_search = self.driver.find_elements_by_class_name('rc')
    #     for data in all_search:
    #         title = data.find_element_by_tag_name('h3').text
    #         url = data.find_element_by_css_selector(
    #             'h3 > a').get_attribute('href')
    #         display_url = data.find_element_by_tag_name('cite').text
    #         try:
    #             dis = data.find_element_by_class_name('st').text
    #         except NoSuchElementException:
    #             dis = ''
    #         result = SearchResultRow(title, url, display_url, dis)
    #         self.searches.append(result)

    def get_search(self):
        resp = requests.get(self.url + '&q=' + self.keyword)
        soup = BeautifulSoup(resp.content, 'html5lib')
        el_url = soup.select('.r a')
        n_articles = min(10, len(el_url))
        for i in range(n_articles):
            url = 'http://google.co.jp' + el_url[i].get('href')
            self.searches.append(SearchResultRow('title', url, 'display_url', 'desc'))

    # @staticmethod
    # def get_article(url):
    #     pprint(url)
    #     driver = webdriver.Firefox()
    #     driver.get(url)
    #     driver.implicitly_wait(1)
    #     try:
    #         html = driver.execute_script("return document.body.innerHTML")
    #     except NoSuchElementException:
    #         html = ''
    #     except:
    #         html = ''
    #     return html
    @staticmethod
    def get_article(url):
        resp = requests.get(url)
        soup = BeautifulSoup(resp.content, 'html5lib')
        # [s.decompose() for s in soup('style')]
        # [s.decompose() for s in soup('script')]
        [s.replace_with('\n') for s in soup('style')]
        [s.replace_with('\n') for s in soup('script')]
        article = soup.get_text()
        # for comment in soup(text=lambda x: isinstance(x, Comment)):
        #     comment.extract()
        # for script in soup.find_all('script', src=False):
        #     script.decompose()
        # for text in soup.find_all(text=True):
        #     if text.strip():
        #         article += text
        return article

    def start(self):
        # try:
            # self.driver = webdriver.Firefox()
            # self.driver.implicitly_wait(self.default_wait)
            # self.enter_keyword()
        self.get_search()
        self.articles = Parallel(n_jobs=-1)([delayed(self.get_article)(search.url) for search in self.searches])
        # finally:
            # self.driver.quit()
