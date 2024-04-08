/*
	Данный скрипт контролирует кнопки в шапке сайта.
	Он контролирует их таким образом что, только одна кнопка может 
	быть активной за раз, или ни одна не активна
*/
let header_buttons = document.querySelectorAll('.header_button')
let header = document.getElementById("header")
let header_height = header.getBoundingClientRect().height  + "px"

function onHeaderButton(){
	var body = document.getElementById(this.dataset.body)
	if (body.classList.contains('active_nav')){
		body.classList.remove("active_nav")	
		body.style.top = header_height
	}
	else{
		header_buttons.forEach( (header_button) => {
			var body = document.getElementById(header_button.dataset.body)
			body.classList.remove("active_nav")
			body.style.top = header_height
		})
		var body = document.getElementById(this.dataset.body)
		body.classList.add("active_nav")	
		body.style.top = header_height
	}
	
}

header_buttons.forEach( (header_button) => {
    header_button.addEventListener('click', onHeaderButton)
})