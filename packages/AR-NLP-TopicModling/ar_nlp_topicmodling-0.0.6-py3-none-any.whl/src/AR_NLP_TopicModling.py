import pandas as pd
import re
import string
import argparse
from camel_tools.utils.normalize import normalize_alef_maksura_ar
from camel_tools.utils.normalize import normalize_alef_ar
from camel_tools.utils.normalize import normalize_teh_marbuta_ar
from camel_tools.utils.dediac import dediac_ar
from camel_tools.utils.normalize import normalize_unicode
from stop_words import get_stop_words
from sklearn.feature_extraction.text import TfidfVectorizer
import random
from sklearn.decomposition import NMF
from sklearn.decomposition import LatentDirichletAllocation




class Topic_modling:
    def __init__(self,path,column):
        self.stop_words= get_stop_words('arabic')+ get_stop_words('en')
        self.reviews_datasets=reviews_datasets = pd.read_csv(path)
        self.column=column
    def DataCleaning(self) :
        
        arabic_punctuations = '''`÷×؛<>_()*&^%][ـ،/:"؟.,'{}~¦+|!”…“–ـ'''
        english_punctuations = string.punctuation
        punctuations_list = arabic_punctuations + english_punctuations
        arabic_diacritics = re.compile("""
                                     ّ    | # Tashdid
                                     َ    | # Fatha
                                     ً    | # Tanwin Fath
                                     ُ    | # Damma
                                     ٌ    | # Tanwin Damm
                                     ِ    | # Kasra
                                     ٍ    | # Tanwin Kasr
                                     ْ    | # Sukun
                                     ـ     # Tatwil/Kashida
                                 """, re.VERBOSE)
        def normalize_arabic(text):
            text = re.sub("[إأآا]", "ا", text)
            text = re.sub("ى", "ي", text)
            text = re.sub("ؤ", "ء", text)
            text = re.sub("ئ", "ء", text)
            text = re.sub("ة", "ه", text)
            text = re.sub("گ", "ك", text)
            return text
        def remove_diacritics(text):
            text = re.sub(arabic_diacritics, '', text)
            return text
        def remove_punctuations(text):
            translator = str.maketrans('', '', punctuations_list)
            return text.translate(translator)
        def remove_repeating_char(text):
            return re.sub(r'(.)\1+', r'\1', text)
        def normalize_text(text):
            
            text = normalize_unicode(text)
            text = dediac_ar(text)
            # Normalize alef variants to 'ا'
            text = normalize_alef_ar(text)
            # Normalize alef maksura 'ى' to yeh 'ي'
            text = normalize_alef_maksura_ar(text)
            # Normalize teh marbuta 'ة' to heh 'ه'
            text = normalize_teh_marbuta_ar(text)
            
            return text
        parser = argparse.ArgumentParser(description='Pre-process arabic text (remove '
                                                     'diacritics, punctuations, and repeating '
                                                     'characters).') 
        new=[]
        for i in range(len(self.reviews_datasets)):
            print(i)
            text=str(self.reviews_datasets[self.column][i])
            text= normalize_arabic(text)
            text= remove_diacritics(text)
            text= remove_punctuations(text)
            text= remove_repeating_char(text)
            new.append(text)       
        self.reviews_datasets[self.column] = new   
        # reviews_datasets = reviews_datasets.head(30000)
        self.reviews_datasets.dropna()
        self.reviews_datasets.head()
        self.reviews_datasets[self.column][350]
    
    
    
    def TopicModleingNMF(self,num):
        
        tfidf_vect = TfidfVectorizer(max_df=0.8, min_df=2, stop_words=self.stop_words)
        doc_term_matrix = tfidf_vect.fit_transform(self.reviews_datasets[self.column].values.astype('U'))
        
        
        
        nmf = NMF(n_components=(num)+1, random_state=42)
        nmf.fit(doc_term_matrix )
        
        
        for i in range(10):
            random_id = random.randint(0,len(tfidf_vect.get_feature_names()))
            print(tfidf_vect.get_feature_names()[random_id])
        
        
        first_topic = nmf.components_[0]
        top_topic_words = first_topic.argsort()[-10:]
        
        
        for i in top_topic_words:
            print(tfidf_vect.get_feature_names()[i])
            
            
        for i,topic in enumerate(nmf.components_):
            print(f'Top 10 words for topic #{i}:')
            print([tfidf_vect.get_feature_names()[i] for i in topic.argsort()[-10:]])
            print('\n')
        
        topic_values = nmf.transform(doc_term_matrix)
        self.reviews_datasets['Topic'] = topic_values.argmax(axis=1)
        self.reviews_datasets.head()
    def TopicModleingLDA(self,num):
    
        count_vect = TfidfVectorizer(max_df=0.8, min_df=2,stop_words=self.stop_words)
        doc_term_matrix = count_vect.fit_transform(self.reviews_datasets[self.column].values.astype('U'))
        doc_term_matrix
        
        LDA = LatentDirichletAllocation(n_components=num, random_state=42)
        LDA.fit(doc_term_matrix)
        
        
        
        for i in range(15):
            random_id = random.randint(0,len(count_vect.get_feature_names()))
            print(count_vect.get_feature_names()[random_id])
              
        first_topic = LDA.components_[0]
        top_topic_words = first_topic.argsort()[-15:]
        
        for i in top_topic_words:
            print(count_vect.get_feature_names()[i])
        
        
        for i,topic in enumerate(LDA.components_):
            print(f'Top 10 words for topic #{i}:')
            print([count_vect.get_feature_names()[i] for i in topic.argsort()[-15:]])
            print('\n')
            
            
        topic_values = LDA.transform(doc_term_matrix)
        print('Topic Value shape: ',topic_values.shape)
        
        self.reviews_datasets['Topic'] = topic_values.argmax(axis=1)
        print('Dataset head: /n/n ',self.reviews_datasets.head())
