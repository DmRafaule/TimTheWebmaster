import { LoadPosts } from "./pagiscroll.js"

function toggleFilters(event){
    var button = event.detail.button
    var button_img = button.firstElementChild
    var button_img_src = button_img.getAttribute('src')
    button_img.setAttribute('src', button.dataset.closeBtn)
    button.dataset.closeBtn = button_img_src
    var body = document.querySelector(`#${button.dataset.body}`)
    body.classList.toggle('active_filter')
    var main_fieldset = document.querySelector('#filters')
    main_fieldset.classList.toggle('fieldset_filter_toggled')
    var button_filter_out = document.querySelector('#onFilterOut')
    button_filter_out.classList.toggle('active_filter-out')
}

function onFilterOut( event ){
	LoadPosts(1, true)
}

function onReady(){
	var filter_container = document.querySelector('#filters')
	var filter_buttons = filter_container.querySelectorAll('.filter_button')
	// Create an events by name of each button. Can be accessed by their ID
	filter_buttons.forEach((btn) =>{
		let onFilterButtonClick = new CustomEvent(btn.id, {detail: {id: btn.id, button: btn}})
		btn.addEventListener('click', (e)=>{
			document.dispatchEvent(onFilterButtonClick)
		})
	})
	// Show up a filters
	document.addEventListener('filter_main_button', toggleFilters)
	document.addEventListener('onFilterOut', onFilterOut)
}

if (document.readyState === "loading") {
	// Loading hasn't finished yet
	document.addEventListener("DOMContentLoaded", onReady);
} else {
	onReady()
}
