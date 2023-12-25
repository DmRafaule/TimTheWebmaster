function onReady() {
	function toggleDescription(){
		var id = this.dataset.id
		body_of_toggler = document.getElementById('post_preview_body-'+id)
		if (body_of_toggler.classList.contains("active_toggle_button")){
			body_of_toggler.style.height = 0
		}
		else{
			body_of_toggler.style.height = (body_of_toggler.firstElementChild.clientHeight + 50) + "px"
		}
		body_of_toggler.classList.toggle("active_toggle_button")
	}

	// Callback function to execute when mutations are observed
	function  WaitMediaToAppear(mutationList, observer) {
		  for (const mutation of mutationList) {
			if (mutation.addedNodes.length > 0){ 
				const more_buttons = mutation.target.querySelectorAll(".toggle_button");
				more_buttons.forEach( (btn) => {
					btn.addEventListener('click', toggleDescription)
				})
			}
		  }
		};


	// Observe only those elements that I have explicitly assign
	// This observe those elements that gonna have new children via ajax or
	// Other technologies
	const observedElements = document.querySelectorAll(".toObserve");
	// This observer have to observe only those elements that have new children
	const config = { childList: true };
	// Set up callback
	const observer = new MutationObserver(WaitMediaToAppear);
	// Start observing the target node for configured mutations
	observedElements.forEach( (el) => {
		observer.observe(el, config);
	}) 
}

if (document.readyState === "loading") {
  // Loading hasn't finished yet
  document.addEventListener("DOMContentLoaded", onReady);
} else {
	onReady()
}
