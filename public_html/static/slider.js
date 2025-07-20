let sliders = document.querySelectorAll('.slider') 

function updateSlider(){
	this.nextElementSibling.value = this.value
}

sliders.forEach( (slider) => {
	// Set up update callback
	slider.firstElementChild.oninput = updateSlider
	// Init output value
	slider.querySelector('output').value = slider.firstElementChild.value	
})
