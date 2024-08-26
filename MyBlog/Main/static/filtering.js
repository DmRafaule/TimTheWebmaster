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
}

if (document.readyState === "loading") {
	// Loading hasn't finished yet
	document.addEventListener("DOMContentLoaded", onReady);
} else {
	onReady()
}
