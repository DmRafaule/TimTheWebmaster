import { LoadPosts } from "./pagiscroll.js"

export function update_alphabet_filters(){
    var letters = []
    document.querySelectorAll('.letter_button.selected_order').forEach((el)=>{
        letters.push(el.dataset.letter)
    })
    return letters 
}

export function update_alphabet_filters_sort(){
    var alphabeticContainer = document.querySelector('#onAlphabet')
    var isAlphabetic = alphabeticContainer.dataset.sort
    return isAlphabetic
}

function onSort(){
    var alphabeticContainer = document.querySelector('#onAlphabet')
    var isAlphabetic = alphabeticContainer.dataset.sort
    if (isAlphabetic == 'true')
        isAlphabetic = false
    else if (isAlphabetic == 'ignore')
        isAlphabetic = false
    else
        isAlphabetic = true
    alphabeticContainer.dataset.sort = isAlphabetic
    
	LoadPosts(1, true)
}


function onReady(){
	// Set up buttons effects for filtering by tim
	// Ordering and filtering by date
	var letter_btns = document.querySelectorAll('.letter_button')
	letter_btns.forEach( btn => {
		btn.addEventListener('click', (event) => {
			btn.classList.toggle('selected_order')
		})
	})

    document.addEventListener('onAlphabet', (event) => {
        var button = event.detail.button
        var button_img = button.firstElementChild
		var button_img_src = button_img.getAttribute('src')
        button_img.setAttribute('src', button.dataset.closeBtn)
        button.dataset.closeBtn = button_img_src
		onSort()
	})
}

if (document.readyState === "loading") {
	// Loading hasn't finished yet
	document.addEventListener("DOMContentLoaded", onReady);
} else {
	onReady()
}