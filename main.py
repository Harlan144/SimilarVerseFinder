from flask import Flask, render_template, request, escape, Blueprint
from functions import findVerseInDF, modifyHTMLForSubmit
from predictVerse import checkUniqueVerse
from predictVerse import checkVerse

app = Flask(__name__)

#Post method sends form to backend,
@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        print(request.form.to_dict(), flush=True)
        allowed_works = request.form['allowed_works']

        checkInfo = [False, False, False, False, False]

        if ("old testament" in allowed_works):
            checkInfo[0]=True
        if ("new testament" in allowed_works):
            checkInfo[1]=True
        if ("book of mormon" in allowed_works):
            checkInfo[2]=True
        if ("d&c" in allowed_works):
            checkInfo[3]=True
        if ("pogp" in allowed_works):
            checkInfo[4]=True

        if checkInfo == [False, False, False, False, False]:
            return render_template("index.html", verse = "No Works", foundVerses = [], checkInfo = checkInfo, form_submit=form1_html)

        if 'sentence' in request.form:
            input = request.form['sentence']

            if input:
                listOfOtherVerses = checkUniqueVerse(input, allowed_works)

                return render_template("index.html", sentence = input, foundVerses = listOfOtherVerses, checkInfo = checkInfo)
            return render_template("index.html", sentence = "Not Found", foundVerses = [], checkInfo=checkInfo)

        else:
            # print(request.form.to_dict(), flush=True)

            # Print the form data to the console
            form1_html= request.form['form1_html']

            work = request.form['work'].lower()
            book = request.form['book'].lower()
            chapter = request.form['chapter'].lower()
            verseNum = request.form['verse'].lower()

            modified_html = modifyHTMLForSubmit(form1_html, work, book, chapter, verseNum)
            returnedRow = findVerseInDF(book, chapter, verseNum)

            if returnedRow!= -1:
                listOfOtherVerses = checkVerse(book, chapter, verseNum, allowed_works)
            else:
                return render_template("index.html", verse = "Not Found", foundVerses = [], checkInfo = checkInfo, form_submit=modified_html)

            return render_template("index.html", verse =returnedRow, foundVerses = listOfOtherVerses, checkInfo=checkInfo, form_submit=modified_html)
    else:
        return render_template("index.html", checkInfo = [True, True, True, True, True])

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host="0.0.0.0", port=5000, debug=True)
