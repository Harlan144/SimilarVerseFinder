from sentence_transformers import SentenceTransformer, util
import pandas as pd
import numpy as np
import re
import torch

df = pd.read_csv('static/standworksDFWebsite')

def checkVerse(inputSentance):
    model = SentenceTransformer('static/nlpModel')
    #remove punctuation
    desc = re.sub('[^a-zA-Z]', ' ', inputSentance)

    #remove tags
    desc=re.sub("&lt;/?.*?&gt;"," &lt;&gt; ",desc)

    #remove digits and special chars
    desc=re.sub("(\\d|\\W)+"," ",desc)

    sentenceEmbedded = model.encode(desc, convert_to_tensor=True)
    embeddings = torch.load("static/tensor.pt")

    cosine_scores = util.cos_sim(sentenceEmbedded, embeddings)
    sorted = np.argsort(cosine_scores.squeeze().tolist())[-5:]
    
    listOfDic = []
    for i in sorted:
        row = df.iloc[i]
        book = row['Book']
        chapter = row["Chapter"]
        verseNum = row["VerseNum"]
        verse  = row["Verse"]
        listOfDic.append({'index': i,'book': book, 'chapter': chapter, 'verseNum': verseNum, 'verse': verse})

    return listOfDic