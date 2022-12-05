#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import spacy
#spacy.prefer_gpu()

class SequenceTagger():

    def __init__(self):
        self.lang_dict = {  "en": "en_core_web_lg",
                            "fr": "fr_core_news_lg",
                            "it": "it_core_news_lg",
                            "de": "de_core_news_lg",
                            "es": "es_core_news_lg",
                            "da": "da_core_news_lg",
                            "nl": "nl_core_news_lg",
                            "el": "el_core_news_lg",
                            "lt": "lt_core_news_lg",
                            "pl": "pl_core_news_lg",
                            "pt": "pt_core_news_lg",
                            "ro": "ro_core_news_lg"}

        self.universal_pos_list = ['ADJ', 'ADP', 'ADV', 'AUX', 'CONJ',
                         'CCONJ', 'DET', 'INTJ', 'NOUN', 'NUM',
                         'PART', 'PROPN', 'PRON', 'PUNCT', 'SCONJ',
                         'SYM', 'VERB', 'X', 'SPACE']

        self.ner_list = ['PERSON', 'NORP','FAC','ORG','GPE','LOC','PRODUCT','EVENT','WORK_OF_ART','LAW','LANGUAGE' ,
                    'DATE','TIME','PERCENT','MONEY','QUANTITY','ORDINAL','CARDINAL', 'MISC', 'PER']


    def text2ent(self, sdescr, lang):
        model = spacy.load(self.lang_dict[str(lang).lower().rstrip()])
        doc = model(sdescr)
        entlist = [ent.label_ for ent in doc.ents]
        return entlist

    def text2tag(self, sdescr, lang):
        model = spacy.load(self.lang_dict[str(lang).lower().rstrip()])
        doc = model(sdescr)
        taglist = [token.pos_ for token in doc]
        return taglist

    def text2seq(self, sdescr, lang):
        model = spacy.load(self.lang_dict[str(lang).lower().rstrip()])
        doc = model(sdescr)
        entlist = [ent.label_ for ent in doc.ents]
        taglist = [token.pos_ for token in doc]
        return entlist, taglist

    def transform(self, df):
        # lol stands for list of list lol :)
        entlol = []
        taglol = []
        count = 0
        for (sdescr, lang) in zip(df["FINAL_DESCR"], df["SELECTED_ORIG_x"]):
            count += 1
            print(count)
            lang = str(lang).lower().rstrip()
            if lang not in list(self.lang_dict.keys()):
                lang = "en"

            try:
                entlist, taglist = self.text2seq(sdescr, lang)
                entlol.append(entlist)
                taglol.append(taglist)
            except:
                entlol.append("")
                taglol.append("")

        assert len(entlol) == df.shape[0]
        assert len(taglol) == df.shape[0]

        df["POS_LIST"] = taglol
        df["NER_LIST"] = entlol

        return df

    def count_transform(self, df):
        for tag in self.universal_pos_list:
            df["POS_" + tag] = [taglist.count(tag) for taglist in df["POS_LIST"]]

        for label in self.ner_list:
            df["NER_" + label] = [entlist.count(label) for entlist in df["NER_LIST"]]

        return df

if __name__ == "__main__":
    pass