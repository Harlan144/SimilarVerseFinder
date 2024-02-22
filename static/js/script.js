
document.getElementById("form").addEventListener("submit", function(eventObj) {
  // Create a hidden input element

  var hiddenInput = document.createElement("input");
  // Set attributes for the hidden input
  hiddenInput.type = "hidden";
  hiddenInput.name = "allowed_works";
  // Get the reference to the div element
  let values = [];
  if (document.getElementById("oldtestcheckbox").checked) {
    values.push("old testament");
  }
  if (document.getElementById("newtestcheckbox").checked) {
    values.push("new testament");
  }
  if (document.getElementById("bomcheckbox").checked) {
    values.push("book of mormon");
  }
  if (document.getElementById("dccheckbox").checked) {
    values.push("d&c");
  }
  if (document.getElementById("pogpcheckbox").checked) {
    values.push("pogp");
  }
  hiddenInput.value = values;

  // Append the hidden input to the form
  document.getElementById("form").appendChild(hiddenInput);
  
  // Continue with the form submission
  return true;

});


document.getElementById("form1").addEventListener("submit", function(eventObj) {
  var hiddenInputFormHTML = document.createElement("input");
  // Set attributes for the hidden input
  hiddenInputFormHTML.type = "hidden";
  hiddenInputFormHTML.name = "form1_html";
  var formHtml = document.getElementById("form1").innerHTML;
  hiddenInputFormHTML.value = formHtml;
  document.getElementById("form1").appendChild(hiddenInputFormHTML);

  // Create a hidden input element
  var hiddenInput = document.createElement("input");
  // Set attributes for the hidden input
  hiddenInput.type = "hidden";
  hiddenInput.name = "allowed_works";
  let values = [];
  if (document.getElementById("oldtestcheckbox").checked) {
    values.push("old testament");
  }
  if (document.getElementById("newtestcheckbox").checked) {
    values.push("new testament");
  }
  if (document.getElementById("bomcheckbox").checked) {
    values.push("book of mormon");
  }
  if (document.getElementById("dccheckbox").checked) {
    values.push("d&c");
  }
  if (document.getElementById("pogpcheckbox").checked) {
    values.push("pogp");
  }
  hiddenInput.value = values;

  // Append the hidden input to the form
  document.getElementById("form1").appendChild(hiddenInput);

  // Continue with the form submission
  return true;
});

var slideIndex = 1;
showDivs(slideIndex);

function plusDivs(n) {
  showDivs(slideIndex += n);
}
function currentDiv(n) {
  showDivs(slideIndex = n);
}

function showDivs(n) {
  var i;
  var x = document.getElementsByClassName("similarVerse");
  var dots = document.getElementsByClassName("otherVerse");
  if (n > x.length) { slideIndex = 1 }
  if (n < 1) { slideIndex = x.length };
  for (i = 0; i < x.length; i++) {
    x[i].style.display = "none";
  }
  x[slideIndex - 1].style.display = "block";

  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" fill", "");
  }
  x[slideIndex - 1].style.display = "block";
  dots[slideIndex - 1].className += " fill";
}


function removeOptions(selectElement) {
  var i, L = selectElement.options.length - 1;
  for (i = L; i >= 0; i--) {
    selectElement.remove(i);
  }
}

function toTitleCase(str) {
  return str.replace(
    /\w*/g,
    function (txt) {
      return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
    }
  );
}

function changeVerses() {
  let work = document.getElementById("workDropdown").value;
  let book = document.getElementById("bookDropdown").value;
  let chap = document.getElementById("chapterDropdown").value;

  fetch('/static/js/dropdown.json')
    .then(response => response.json())
    .then(data => {
      let verse_select = document.getElementById("verseDropdown");
      removeOptions(verse_select);

      if (chap=="defaultChapter"){
        let default_verse_option = document.createElement('option');
        default_verse_option.value = "defaultVerse";
        default_verse_option.innerHTML = "Select Verse...";
        verse_select.appendChild(default_verse_option);
      } else {
        let verse_count = data[work][book][chap];
        for (let i = 1; i <= verse_count; i++) {
          let verse_option = document.createElement('option');
          verse_option.value = i;
          verse_option.innerHTML = i;
          verse_select.appendChild(verse_option);
        }
      }

    })
    .catch(error => console.error('Error fetching JSON:', error));
}

//This is kinda crappy code. These two functions could easily be combined. I'm just lazy. Forgive me!
function changeChapters() {
  var work = document.getElementById("workDropdown").value;
  var book = document.getElementById("bookDropdown").value;

  fetch('/static/js/dropdown.json')
    .then(response => response.json())
    .then(data => {
      let chapter_select = document.getElementById("chapterDropdown");
      removeOptions(chapter_select);

      if (book == "defaultBook") {
        let default_chapter_option = document.createElement('option');
        default_chapter_option.value = "defaultChapter";
        default_chapter_option.innerHTML = "Select Chapter...";
        chapter_select.appendChild(default_chapter_option);
      } else {
        let json_work = data[work][book];
        for (const chap of Object.keys(json_work)) {
          let chap_option = document.createElement('option');
          chap_option.value = chap;
          chap_option.innerHTML = toTitleCase(chap);
          chapter_select.appendChild(chap_option);
        }
      }


      changeVerses();
    })
    .catch(error => console.error('Error fetching JSON:', error));
}

function changeBooks() {
  var work = document.getElementById("workDropdown").value;

  fetch('/static/js/dropdown.json')
    .then(response => response.json())
    .then(data => {
      let json_work = data[work];

      let book_select = document.getElementById("bookDropdown");
      removeOptions(book_select);


      if (json_work == undefined) {
        let default_book_option = document.createElement('option');
        default_book_option.value = "defaultBook";
        default_book_option.innerHTML = "Select Book...";
        document.getElementById("bookDropdown").appendChild(default_book_option);
      } else {
        for (const book of Object.keys(json_work)) {
          let book_option = document.createElement('option');
          book_option.value = book;
          book_option.innerHTML = toTitleCase(book);
          book_select.appendChild(book_option);
        }
      }

      changeChapters();
    }
    )
    .catch(error => console.error('Error fetching JSON:', error));
}

