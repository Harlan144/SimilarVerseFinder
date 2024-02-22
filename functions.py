import pandas as pd
import re

df = pd.read_csv('static/standworksDFWebsite')


def findVerseInDF(book, chapter, verseNum):
    try:
        index = df.index[(df['Book'] == book) & (df['Chapter'] == int(chapter)) & (df["VerseNum"]== int(verseNum))]
        row = df.iloc[index[0]]
        rowNum  = index[0]
        originalRow = row["originalIndex"]
        book = row['Book']
        chapter = row["Chapter"]
        verseNum = row["VerseNum"]
        verse  = row["Verse"]
        work = row["Work"]
        return {'index': rowNum, 'origIndex': originalRow, 'work': work, 'book': book, 'chapter': chapter, 'verseNum': verseNum, 'verse': verse}
    except:
        return -1

def findSimilarVerses(work, index):
    works = {"book of mormon": "bom", "d&c": "dc","old testament": "oldTest","new testament": "newTest", "pearl of great price": "pogp"}
    with open("static/similarVerses/"+works[work]+"SimilarVerses") as file:
        for i, line in enumerate(file):
            if i== index:
                regex = '\((\d+)\,'
                similarVerses = re.findall(regex, line) 
    listOfDic = []
    for i in similarVerses:
        row = df.iloc[int(i)]
        rowNum  = int(i)
        book = row['Book']
        chapter = row["Chapter"]
        verseNum = row["VerseNum"]
        verse  = row["Verse"]
        #I can add the work and original index if needed
        listOfDic.append({'index': rowNum,'book': book, 'chapter': chapter, 'verseNum': verseNum, 'verse': verse})
    return listOfDic

def modifyHTMLForSubmit(html, work, book, chapter, verse):
    #change html to find selected elements and add select. 
    removed_selected = html.replace(' selected=""', '')
    if "&" in work:
        work = work.replace("&","&amp;")

    select_work = re.sub(rf'value="{work}">', rf'value="{work}" selected>', removed_selected, count=1, flags=0)
    select_book = re.sub(rf'value="{book}">', rf'value="{book}" selected>', select_work, count=1, flags=0)
    select_chap = re.sub(rf'value="{chapter}">(.*?)</select>\r\n        <p>Verse', rf'value="{chapter}" selected>\g<1></select>\r\n        <p>Verse', select_book, count=1, flags=re.DOTALL)
    select_verse = re.sub(rf'Verse Number:</p>(.*?)value="{verse}">', rf'Verse Number:</p>\g<1>value="{verse}" selected>', select_chap, count=1, flags=re.DOTALL)



    return select_verse