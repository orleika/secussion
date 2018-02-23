# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup

class Clean:

    def __init__(self, raw = ''):
        self.raw = raw
        self.text = raw

    def clean_text(self):
        text = self.text
        replaced_text = text.lower()
        replaced_text = re.sub(r'[【】「」『』−（）()［］\[\]!"#$%&\'=\~\-^\\|{}`+;:*/?_]', ' ', replaced_text)
        replaced_text = re.sub(r'\xa0', ' ', replaced_text)
        replaced_text = re.sub(r'\t', ' ', replaced_text)
        replaced_text = re.sub(r'[@＠]\w+', '', replaced_text)
        replaced_text = re.sub(r'\d+[年月日時分秒]', '', replaced_text)
        replaced_text = re.sub(r'https?:\/\/.*?[\r\n ]', '', replaced_text)
        replaced_text = re.sub(r'　', ' ', replaced_text)
        replaced_text = re.sub(r' +', ' ', replaced_text)
        self.text = replaced_text
        return self

    def clean_html_tags(self):
        soup = BeautifulSoup(self.text, 'html.parser')
        cleaned_text = soup.get_text()
        # cleaned_text = ''.join(cleaned_text.splitlines())
        self.text = cleaned_text
        return self

    def clean_html_and_js_tags(self):
        soup = BeautifulSoup(self.text, 'html.parser')
        [x.extract() for x in soup.findAll(['script', 'style'])]
        cleaned_text = soup.get_text()
        # cleaned_text = ''.join(cleaned_text.splitlines())
        self.text = cleaned_text
        return self

    def clean_code(self):
        soup = BeautifulSoup(self.text, 'html.parser')
        [x.extract() for x in soup.findAll(class_="code-frame")]
        cleaned_text = soup.get_text()
        # cleaned_text = ''.join(cleaned_text.splitlines())
        self.text = cleaned_text
        return self
