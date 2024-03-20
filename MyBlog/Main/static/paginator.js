var paginator_buttons = document.querySelectorAll('.pagin_button')
var next_pagin_button = document.getElementById('next_pagin_button')
var prev_pagin_button = document.getElementById('prev_pagin_button')

function clearCurrentPaginButton(){
    var paginator_buttons = document.querySelectorAll('.pagin_button')
    paginator_buttons.forEach( (button) => {
        button.classList.remove('current_pagin_button')
    })
}

function onPaginButton(){
    clearCurrentPaginButton()
    this.classList.add('current_pagin_button')
}

function onPaginButtonNext(){
    var current_pagin_button = document.querySelector('.current_pagin_button')
    var next_button = current_pagin_button.nextElementSibling
    if (next_button != null){
        clearCurrentPaginButton()
        if ( next_button.classList.contains('pagin_dots')){
            next_button = next_button.nextElementSibling
        }
        next_button.classList.add('current_pagin_button')
    }
}
function onPaginButtonPrev(){
    var current_pagin_button = document.querySelector('.current_pagin_button')
    var prev_button = current_pagin_button.previousElementSibling
    if (prev_button != null){
        clearCurrentPaginButton()
        if ( prev_button.classList.contains('pagin_dots')){
            prev_button = prev_button.previousElementSibling
        }
        prev_button.classList.add('current_pagin_button')
    }
}

next_pagin_button.addEventListener('click', onPaginButtonNext)
prev_pagin_button.addEventListener('click', onPaginButtonPrev)
paginator_buttons.forEach( (button) => {
    if (IS_MOBILE){
        var current_pagin_button = document.querySelectorAll(".first_pagin_button, .last_pagin_button")
        current_pagin_button.forEach( (button) => {
            button.classList.remove('first_pagin_button')
            button.classList.remove('last_pagin_button')
        })
        var pagin_dots = document.querySelectorAll('.pagin_dots')
        pagin_dots.forEach( (dots) => {
            dots.remove()
        })
    }
    button.addEventListener('click', onPaginButton)
})