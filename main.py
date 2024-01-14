from flask import Flask, render_template, request, escape
from functions import *
from predictVerse import checkVerse
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'sentence' in request.form:
            input = request.form['sentence']
            if input:
                listOfOtherVerses = checkVerse(input)
                #print(listOfOtherVerses)
                return render_template("index.html", sentence = input, foundVerses = listOfOtherVerses)
            return render_template("index.html", sentence = "Not Found", foundVerses = [])
            
        else:
            # Print the form data to the console
            book = request.form['book'].lower()
            chapter = request.form['chapter']
            verseNum = request.form['verseNum']
            returnedRow = findVerseInDF(book, chapter, verseNum)
            if returnedRow!= -1:
                
                index= returnedRow['origIndex']
                work = returnedRow['work'].lower()
                listOfOtherVerses = findSimilarVerses(work, index)
            else: 
                return render_template("index.html", verse = "Not Found", foundVerses = [])
            
            return render_template("index.html", verse =returnedRow, foundVerses = listOfOtherVerses)
    else:
        return render_template("index.html")


if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host="0.0.0.0", port=5000, debug=True)