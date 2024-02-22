from sentence_transformers import SentenceTransformer, util
import pandas as pd
import numpy as np
import re
import torch

df = pd.read_csv('static/standworksDFWebsite')

def works_to_verses(allowed_works):
    work_list = allowed_works.strip().split(",")

    allowed_ranges = []
    for work in work_list:
        if work=="old testament":
            allowed_ranges.append((18208,41362))
        if work=="pogp":
            allowed_ranges.append((41363,41987))
        if work=="new testament":
            allowed_ranges.append((10251,18207))
        if work=="d&c":
            allowed_ranges.append((6597,10250))
        if work=="book of mormon":
            allowed_ranges.append((0,6596))
    return allowed_ranges

def checkUniqueVerse(inputSentance, allowed_works):    
    model = SentenceTransformer('static/nlpModel')
    #remove punctuation
    desc = re.sub('[^a-zA-Z]', ' ', inputSentance)

    #remove tags
    desc=re.sub("&lt;/?.*?&gt;"," &lt;&gt; ",desc)

    #remove digits and special chars
    desc=re.sub("(\\d|\\W)+"," ",desc)

    sentenceEmbedded = model.encode(desc, convert_to_tensor=True)
    embeddings = torch.load("static/tensor.pt")

    cosine_scores = util.cos_sim(sentenceEmbedded, embeddings).squeeze().tolist()

    sorted_cosine_scores = np.argsort(cosine_scores)

    work_range = works_to_verses(allowed_works)
    
    count = 0
    top_5 = []
    
    for verse in reversed(sorted_cosine_scores):
        if count==5:
            break
        for r in work_range:
            if verse in range(*r):
                top_5.append(verse)
                count +=1
    
    listOfDic = []
    for i in top_5:
        row = df.iloc[i]
        book = row['Book']
        chapter = row["Chapter"]
        verseNum = row["VerseNum"]
        verse = row["Verse"]
        similarity_score = round(cosine_scores[i]*100,2)
        listOfDic.append({'index': i,'book': book, 'chapter': chapter, 'verseNum': verseNum, 'verse': verse, 'similarity_score':similarity_score})

    return listOfDic


def checkVerse(book, chapter, verseNum, allowed_works):    
    model = SentenceTransformer('static/nlpModel')

    index = df.index[(df['Book'] == book) & (df['Chapter'] == int(chapter)) & (df["VerseNum"]== int(verseNum))]
    row = df.iloc[index[0]]
    verse  = row["Verse"]


    #remove punctuation
    desc = re.sub('[^a-zA-Z]', ' ', verse)

    #remove tags
    desc=re.sub("&lt;/?.*?&gt;"," &lt;&gt; ",desc)

    #remove digits and special chars
    desc=re.sub("(\\d|\\W)+"," ",desc)

    sentenceEmbedded = model.encode(desc, convert_to_tensor=True)
    embeddings = torch.load("static/tensor.pt")

    cosine_scores = util.cos_sim(sentenceEmbedded, embeddings).squeeze().tolist()

    sorted_cosine_scores = np.argsort(cosine_scores)

    work_range = works_to_verses(allowed_works)

    count = 0
    top_5 = []
    for verse in reversed(sorted_cosine_scores):
        if count==5:
            break
        for r in work_range:
            if verse in range(*r):
                if index!=verse:
                    top_5.append(verse)
                    count +=1
    
    listOfDic = []
    for i in top_5:
        row = df.iloc[i]
        book = row['Book']
        chapter = row["Chapter"]
        verseNum = row["VerseNum"]
        verse = row["Verse"]
        similarity_score = round(cosine_scores[i]*100,2)

        listOfDic.append({'index': i,'book': book, 'chapter': chapter, 'verseNum': verseNum, 'verse': verse, 'similarity_score':similarity_score})

    return listOfDic