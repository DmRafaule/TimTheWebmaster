let toggle_buttons = document.querySelectorAll(".toggle_button") 

function toggleButton(){
	body_of_toggler = this.nextElementSibling
	if (body_of_toggler.classList.contains("active_toggle_button")){
		body_of_toggler.style.height = 0
	}
	else{
		body_of_toggler.style.height = body_of_toggler.firstElementChild.clientHeight + "px"
	}
	body_of_toggler.classList.toggle("active_toggle_button")
	if (this.firstElementChild){
		icon_of_toggler = this.firstElementChild 
		icon_of_toggler.classList.toggle("active_toggle_button_image")
	}
}

toggle_buttons.forEach( (btn) => {
	btn.addEventListener('click', toggleButton)
})
