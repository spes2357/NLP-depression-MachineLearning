

# -*- coding: utf-8 -*-
"""CS5783 Project001
Automatically generated by Colaboratory.
Original file is located at
    https://colab.research.google.com/drive/16d4HKi3na4TfZWN6nIY3TKbq5dBBpOB2
"""
# non depression dataset은 training 시킬 필요가 없다. 어차피 depression dataset에 없는 단어가 곧 non-depression 환자의 데이터 셋이 될거 같다.
# 추가로
import nltk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import seaborn as sns
import time
import re
from wordcloud import WordCloud
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
import random
import os

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')


# dowmload and update
# from google.colab import drive
# drive.mount('/content/drive')

def getTextFromFiles(df, data_path, depression, limit):
    """Return Data Frame """

    for file in os.listdir(data_path)[:limit]:
        with open(data_path + "/" + file, 'r', encoding="ISO-8859-1") as file1:
            file1 = file1.read()
            df = df.append({'text': file1, 'depression': int(depression)}, ignore_index=True)

    return df


def getTextFromFiles_Test(df_test, data_path, limit):
    """Return Data Frame """

    for file in os.listdir(data_path)[:limit]:
        with open(data_path + "/" + file, 'r', encoding="ISO-8859-1") as file1:
            file1 = file1.read()
            df_test = df_test.append({'text': file1}, ignore_index=True)

    return df_test

def dataPreprocessingForX(df, columnName1):
  df[columnName1] = df[columnName1].map(lambda text: text.lower())
  df[columnName1] = df[columnName1].map(lambda text: nltk.tokenize.word_tokenize(text))
  stop_words = set(nltk.corpus.stopwords.words('english'))
  df[columnName1] = df[columnName1].map(lambda tokens: [w for w in tokens if not w in stop_words])
  df[columnName1] = df[columnName1].map(lambda text: ' '.join(text))
  df[columnName1] = df[columnName1].map(lambda text: re.sub('[^A-Za-z]+', ' ', text))
  wnl = nltk.WordNetLemmatizer()
  df[columnName1] = df[columnName1].map(lambda text: wnl.lemmatize(text))


def checkfilesCounts(data_path):
    print(len(os.listdir(data_path)))


data_path_d = "reddit_depression"
data_path_nd = "reddit_non_depression"
data_path_d_test = "reddit_depression_testset"
# data_path_d = "/content/drive/My Drive/NLP Team/code/reddit_depression"
# data_path_nd = "/content/drive/My Drive/NLP Team/code/reddit_non_depression"

checkfilesCounts(data_path_d)
checkfilesCounts(data_path_nd)
#
# # 데이터 전처리
df = pd.DataFrame(columns=['text', 'depression'])
df = getTextFromFiles(df, data_path_d, 1, 50)
# # 이시점까진 우울증 글만 추가
df = getTextFromFiles(df, data_path_nd, 0, 50)
dataPreprocessingForX(df, 'text')
# # print(df) 이 시점까지 우울증 + 우울증 아님 글 추가
# # 모두 소문자로변화
# df['text'] = df['text'].map(lambda text: text.lower())
# # 단어 단위로 분리
# df['text'] = df['text'].map(lambda text: nltk.tokenize.word_tokenize(text))
# # stop word를 통해 불필요한 단어 제거
# stop_words = set(nltk.corpus.stopwords.words('english'))
# df['text'] = df['text'].map(lambda tokens: [w for w in tokens if not w in stop_words])
# # 단어를 문장으로 합침
# df['text'] = df['text'].map(lambda text: ' '.join(text))
# # 특수문자 제거
# df['text'] = df['text'].map(lambda text: re.sub('[^A-Za-z0-9]+', ' ', text))
# df['text'] = df['text'].map(lambda text: re.sub('[-=.#/?:$}]', ' ', text))
#
# wnl = nltk.WordNetLemmatizer()
# df['text'] = df['text'].map(lambda text: wnl.lemmatize(text))
#
# print(df['text'])
#
# # print('df[depression]',df['depression'])
# #
df['depression'] = df['depression'].astype('int32')
#
# print(df['depression'])
#
# print('what is this : ',df.groupby('depression').count())


# Countvectorizer : scikit-learn에서 Naive Bayes 분류기를 사용하기 전에 일단 자연어(텍스트)로 이루어진 문서들을 1과 0 밖에 모르는 컴퓨터가 이해할 수 있는 형식으로 변환해야 할 거다. feature extraction, 어휘(특성) 추출 과정이라 볼 수 있다.
count_vectorizer = CountVectorizer(ngram_range=(1,1))
#  fit_transform : fit과 transform을 합쳐놓은 문법
# fit : it() 메소드를 호출해서 학습 데이터 세트에 등장하는 어휘를 가르쳐놓아야 한다.
#  .transform()는 문자열 목록을 가져와 미리 학습해놓은 사전을 기반으로 어휘의 빈도를 세주는 거다.
counts = count_vectorizer.fit_transform(df['text'].values)

# print(np.array(counts))
dump1 =np.array(counts)
df_dump1 = pd.DataFrame(columns=['text', "count"])
temp = dict()
# for i in dump1:

print(type(dump1))



# dump1 = count_vectorizer.get_feature_names()
dump2 = counts.toarray()
np.savetxt("foo1.csv",dump1,delimiter=",")
# np.savetxt("foo2.csv",dump2,delimiter=",")
# print(counts)
classifier = MultinomialNB()
targets = df['depression'].values
classifier.fit(counts, targets)


df_test = pd.DataFrame(columns=['text'])
df_test = getTextFromFiles_Test(df_test, data_path_d_test,10)
dataPreprocessingForX(df_test, 'text')
print(type(df_test))
example_counts = count_vectorizer.transform(df_test['text'].tolist())
predictions = classifier.predict(example_counts)

print(predictions)



tfidf_vectorizer = TfidfTransformer().fit(counts)
tfidf = tfidf_vectorizer.transform(counts)
classifier = MultinomialNB()
targets = df['depression'].values
classifier.fit(counts, targets)


example_counts = count_vectorizer.transform(df_test['text'].tolist())
example_tfidf = tfidf_vectorizer.transform(example_counts)
predictions_tfidf = classifier.predict(example_tfidf)
print(predictions_tfidf)

# Wordcloud
# def makeWorldCloud():
#   depression_words = ''.join(list(df['text']))
#   depression_wordclod = WordCloud(width = 512,height = 512).generate(depression_words)
#   plt.figure(figsize = (10, 8), facecolor = 'k')
#   plt.imshow(depression_wordclod)
#   plt.axis('off')
#   plt.tight_layout(pad = 0)
#   plt.show()
# makeWorldCloud()

