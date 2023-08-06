function quiz_select(quiz_id, alternative) {
    quiz = document.getElementById(quiz_id);
    let i = 0;
    for (li of quiz.getElementsByTagName("li")) {
        if (li.classList.contains('selected') || li.classList.contains('unselected')) {
            if (i == alternative) {
                li.classList.add('selected')
                li.classList.remove('unselected')
            } else {
                li.classList.add('unselected')
                li.classList.remove('selected')
            }
        }
        i = i + 1
    }
    for (div of quiz.getElementsByClassName("card-footer")[0].getElementsByTagName("div")) {
        if (div.getAttribute("data") == "instructions") {
            div.classList.add('visually-hidden')
        } else if (div.getAttribute("data") == "confirm") {
            div.classList.remove('visually-hidden')
        }
    }
}

function quiz_confirm(quiz_id, correct) {
    quiz = document.getElementById(quiz_id);
    let i = 0;
    let selected = -1;
    for (li of quiz.getElementsByTagName("li")) {
        if (i == correct) {
            if (li.classList.contains('selected')) {
                // selected and true
                selected = i
                li.classList.remove('selected')
                li.classList.add('selected-true')
            } else if (li.classList.contains('unselected')) {
                // unselected but true
                li.classList.remove('unselected')
                li.classList.add('unselected-true')
            }
        } else {
            if (li.classList.contains('selected')) {
                // selected but false
                selected = i
                li.classList.remove('selected')
                li.classList.add('selected-false')
            } else if (li.classList.contains('unselected')) {
                // unselected and false
                li.classList.remove('unselected')
                li.classList.add('unselected-false')
            }
        }
        i = i + 1
    }
    for (div of quiz.getElementsByClassName("card-footer")[0].getElementsByTagName("div")) {
        if (div.getAttribute("data") == "confirm") {
            div.classList.add('visually-hidden')
        } else if (div.getAttribute("data") == selected) {
            div.classList.remove('visually-hidden')
        }
    }
}