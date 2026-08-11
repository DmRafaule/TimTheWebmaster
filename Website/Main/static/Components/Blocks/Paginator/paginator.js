import { IS_MOBILE } from "../../../Components/Base/mobile_check.js"

var paginator_buttons = document.querySelectorAll('.pagin_button')
var next_pagin_button = document.getElementById('next_pagin_button')
var prev_pagin_button = document.getElementById('prev_pagin_button')


export function update_paginator(num_pages, page){
	var paginator_body = document.getElementById('paginator_body')
	paginator_body.innerText = ''
	var default_page_example_in_paginator = document.getElementById('paginator_default_page_example')
	var first_page_example_in_paginator = document.getElementById('paginator_first_page_example')
	var last_page_example_in_paginator = document.getElementById('paginator_last_page_example')
	if (!IS_MOBILE){
		var dots_example_in_paginator = document.getElementById('paginator_dots_example')
	}

	if (num_pages == 0){
		var paginator = document.getElementById('paginator')
		paginator.classList.add('is_none')
		paginator.classList.remove('row')
	}else{
		var paginator = document.getElementById('paginator')
		paginator.classList.remove('is_none')
		paginator.classList.add('row')
		if (num_pages == 1){
			var only_one_page = first_page_example_in_paginator.cloneNode()
			only_one_page.classList.add('current_pagin_button')
			only_one_page.classList.add('pagin_button_1')
			only_one_page.classList.remove('example_pagin_button')
			only_one_page.innerText = '1'
			only_one_page.addEventListener('click', onPaginButton)
			only_one_page.addEventListener('click', onPage)
			only_one_page.dataset.page = 1
			paginator_body.insertAdjacentElement('beforeend', only_one_page)
		}else if (num_pages == 2){
			var first_page = first_page_example_in_paginator.cloneNode()
			first_page.classList.add('current_pagin_button')
			first_page.classList.add('pagin_button_1')
			first_page.classList.remove('example_pagin_button')
			first_page.innerText = '1'
			first_page.addEventListener('click', onPaginButton)
			first_page.addEventListener('click', onPage)
			first_page.dataset.page = 1
			paginator_body.insertAdjacentElement('beforeend', first_page)

			var last_page = last_page_example_in_paginator.cloneNode()
			last_page.innerText = String(num_pages)
			last_page.classList.add('pagin_button_2')
			last_page.addEventListener('click', onPaginButton)
			last_page.addEventListener('click', onPage)
			last_page.dataset.page = 2
			last_page.classList.remove('example_pagin_button')
			paginator_body.insertAdjacentElement('beforeend', last_page)
		}else if (num_pages == 3){
			var first_page = first_page_example_in_paginator.cloneNode()
			first_page.classList.add('current_pagin_button')
			first_page.classList.add('pagin_button_1')
			first_page.classList.remove('example_pagin_button')
			first_page.innerText = '1'
			first_page.addEventListener('click', onPaginButton)
			first_page.addEventListener('click', onPage)
			first_page.dataset.page = 1
			paginator_body.insertAdjacentElement('beforeend', first_page)

			var mid_page = default_page_example_in_paginator.cloneNode(true)
			mid_page.innerText = 2
			mid_page.classList.add('pagin_button_2')
			mid_page.addEventListener('click', onPaginButton)
			mid_page.addEventListener('click', onPage)
			mid_page.dataset.page = 2
			mid_page.classList.remove('example_pagin_button')
			paginator_body.insertAdjacentElement('beforeend', mid_page)

			var last_page = last_page_example_in_paginator.cloneNode()
			last_page.innerText = String(num_pages)
			last_page.classList.add('pagin_button_3')
			last_page.addEventListener('click', onPaginButton)
			last_page.addEventListener('click', onPage)
			last_page.dataset.page = 3
			last_page.classList.remove('example_pagin_button')
			paginator_body.insertAdjacentElement('beforeend', last_page)
		}else if (num_pages >= 4){
			var first_page = first_page_example_in_paginator.cloneNode()
			first_page.classList.add('current_pagin_button')
			first_page.classList.add('pagin_button_1')
			first_page.classList.remove('example_pagin_button')
			first_page.innerText = '1'
			first_page.addEventListener('click', onPaginButton)
			first_page.addEventListener('click', onPage)
			first_page.dataset.page = 1
			paginator_body.insertAdjacentElement('beforeend', first_page)
			
			if (!IS_MOBILE){
				var dots1 = dots_example_in_paginator.cloneNode(true)
				dots1.classList.remove('example_pagin_button')
				paginator_body.insertAdjacentElement('beforeend', dots1)
			}

			
			for (var i = 2; i < num_pages; i++){
				var mid_page = default_page_example_in_paginator.cloneNode(true)
				mid_page.innerText = String(i)
				mid_page.classList.add(`pagin_button_${i}`)
				mid_page.addEventListener('click', onPaginButton)
				mid_page.addEventListener('click', onPage)
				mid_page.dataset.page = i
				mid_page.classList.remove('example_pagin_button')
				paginator_body.insertAdjacentElement('beforeend', mid_page)
			}
			
			if (!IS_MOBILE){
				var dots2 = dots_example_in_paginator.cloneNode(true)
				dots2.classList.remove('example_pagin_button')
				paginator_body.insertAdjacentElement('beforeend', dots2)
			}

			var last_page = last_page_example_in_paginator.cloneNode()
			last_page.innerText = String(num_pages)
			last_page.classList.add(`pagin_button_${num_pages}`)
			last_page.addEventListener('click', onPaginButton)
			last_page.addEventListener('click', onPage)
			last_page.dataset.page = num_pages
			last_page.classList.remove('example_pagin_button')
			paginator_body.insertAdjacentElement('beforeend', last_page)
		}


		var prev_pagin_button = document.getElementById('prev_pagin_button')
		try {
			prev_pagin_button.dataset.page = document.querySelector('.current_pagin_button').dataset.page
			prev_pagin_button.addEventListener('click', function(){
				this.dataset.page = document.querySelector('.current_pagin_button').dataset.page
			})
			prev_pagin_button.addEventListener('click', onPage)	
		} catch (error) {
			
		}
		
		try {
			var next_pagin_button = document.getElementById('next_pagin_button')
			next_pagin_button.dataset.page = document.querySelector('.current_pagin_button').dataset.page
			next_pagin_button.addEventListener('click', function(){
				this.dataset.page = document.querySelector('.current_pagin_button').dataset.page
			})
			next_pagin_button.addEventListener('click', onPage)	
		} catch (error) {
			
		}
		// Set current page
		var current_page = document.querySelector(`.pagin_button_${page}`)
		clearCurrentPaginButton()
		current_page.classList.add('current_pagin_button')
	}
}

function onPage(event){
	var onPaginButtonLoad = new CustomEvent('onPaginButtonLoad', {detail: {button: event.currentTarget}})
    document.dispatchEvent(onPaginButtonLoad)
}

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
    var	 next_button = current_pagin_button.nextElementSibling
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



function onReady(){
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
	update_paginator(15,1)
}

if (document.readyState === "loading") {
// Loading hasn't finished yet
    document.addEventListener("DOMContentLoaded", onReady);
} else {
    onReady()
}
