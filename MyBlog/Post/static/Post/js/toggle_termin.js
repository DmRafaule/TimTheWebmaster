function orReadyTermin(){

	function toggleTerminButton(){
		body_of_toggler = this.nextElementSibling
		if (body_of_toggler.classList.contains("active_toggle_button")){
			body_of_toggler.style.height = 0
		}
		else{
			body_of_toggler.style.height = body_of_toggler.firstElementChild.clientHeight + 50 + "px"
		}
		body_of_toggler.classList.toggle("active_toggle_button")
		if (this.firstElementChild){
			icon_of_toggler = this.firstElementChild 
			icon_of_toggler.classList.toggle("active_toggle_button_image")
		}
	}

	function  WaitTerminToAppear(mutationList, observer) {
		  for (const mutation of mutationList) {
			if (mutation.addedNodes.length > 0){ 
				const termins = mutation.target.querySelectorAll(".toggle_button");
				termins.forEach( (termin) => {
					termin.addEventListener('click', toggleTerminButton)
				})
			}
		  }
		};

	observedElements = document.querySelectorAll(".toObserve")
	const config = { childList: true };
	const observer = new MutationObserver(WaitTerminToAppear);
	observedElements.forEach( (el) => {
		observer.observe(el, config);
	}) 
}

if (document.readyState === "loading") {
  // Loading hasn't finished yet
  document.addEventListener("DOMContentLoaded", orReadyTermin);
} else {
	orReadyTermin()
}
