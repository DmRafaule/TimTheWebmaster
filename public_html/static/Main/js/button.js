let buttons = document.querySelectorAll('.basic_button')


function pushBaseButton(el){
	el.classList.add('icon_button_pressed')
	el.addEventListener("animationend", (event) => {
		el.classList.remove('icon_button_pressed')
	});
}

buttons.forEach( (button) => {
	button.addEventListener('click', function(){
		pushBaseButton(button)
	}) 
})
