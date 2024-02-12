import pandas as pd
import sys
import json 

standardWorks = sys.argv[1]

df = pd.read_csv(standardWorks)


def removeduplicate(data):
    countdict = {}
    for element in data:
        if element in countdict.keys():
             
            # increasing the count if the key(or element)
            # is already in the dictionary
            countdict[element] += 1
        else:
            # inserting the element as key  with count = 1
            countdict[element] = 1

    res = []
    for key in countdict.keys():
        res.append(key)
    return res


works = df["Work"]
set_works = removeduplicate(works)
output_dic  = {}
for work in set_works:
    print(work)
    work_df = df[df["Work"]==work]

    output_dic[work] = {}
    books = work_df["Book"]
    book_set = removeduplicate(books)
    for book in book_set:
        output_dic[work][book] = {}
        book_df = work_df[work_df["Book"]==book]

        chapters = book_df["Chapter"]
        chapter_set = removeduplicate(chapters)
        for chapter in chapter_set:
            #print(chapter)
            chapter_df  = book_df[book_df["Chapter"]==chapter]
            output_dic[work][book][chapter] = len(chapter_df)


with open("dropdown.json", "w") as outfile: 
    json.dump(output_dic, outfile)