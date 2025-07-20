function onReady() {
	let onMediaUploaded = new CustomEvent('onMediaUploaded')
	function WaitImageToUpload(image){
		var options = {
			  threshold: 0,
			};
		var image_observer = new IntersectionObserver((entries, observer) => {
		  // Loop through the entries
		  for (const entry of entries) {
			// Check if the entry is intersecting the viewport
			if (entry.isIntersecting) {
				image.setAttribute('src',image.getAttribute('data-src'))
				image.classList.add('loader')

				image_observer.disconnect()
			}
		  }
		}, options);
		image_observer.observe(image);
	}


	// Callback function to execute when mutations are observed
	function  WaitMediaToAppear(mutationList, observer) {
		  for (const mutation of mutationList) {
			if (mutation.addedNodes.length > 0){ 
				document.dispatchEvent(onMediaUploaded)
				const images = mutation.target.querySelectorAll(".dynamic_image");
				images.forEach( (image) => {
						WaitImageToUpload(image)
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

	// Observe images if they are intersecting with main viewport
	const images = document.querySelectorAll(".dynamic_image");
	images.forEach( (image) => {
			WaitImageToUpload(image)
	})

}

if (document.readyState === "loading") {
  // Loading hasn't finished yet
  document.addEventListener("DOMContentLoaded", onReady);
} else {
	onReady()
}
