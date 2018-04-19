from bs4 import BeautifulSoup
from lxml import etree

import pandas as pd
import os

class TrecDocs(object):
    def __init__(self, docs={}):
        self.docs = docs

    @classmethod
    def from_file(cls, filename, doc_tag='doc', text_tags=['text'], docid_tag='docid',
                  title_tag='title', encoding='ISO-8859-1'):
        docs = cls({})
        with open(filename, 'r', encoding=encoding) as fp:
            soup = BeautifulSoup(fp, 'lxml')

        ids, titles, texts = [], [], []
            
        for doc in soup.findAll(doc_tag):
            doc_id = doc.findNext(docid_tag).getText().strip()
            doc_title = ''
            if title_tag:
                doc_title = doc.findNext(title_tag).getText().strip()
            doc_text = []
            for text_tag in text_tags:
                doc_text += [text.getText().strip() for text in doc.findAll(text_tag)]
            doc_text = ' '.join(doc_text).strip()

            ids.append(doc_id) ; titles.append(doc_title) ; texts.append(doc_text)

        docs.docs = pd.DataFrame(data={
            'id': ids,
            'title': titles,
            'text': texts
        })

        docs.docs.set_index(['id'], inplace=True)

        return docs

    def __len__(self):
        return len(self.docs)

    def __add__(self, other):
        combined = self.docs.append(other.docs)
        return TrecDocs(combined)
