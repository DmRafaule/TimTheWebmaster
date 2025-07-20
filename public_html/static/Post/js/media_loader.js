$(document).ready(function(){
	const images = document.querySelectorAll(".dynamic_image");
	images.forEach( (image) => {
		var options = {
			  threshold: 0.01,
			};
		var image_observer = new IntersectionObserver((entries, observer) => {
		  // Loop through the entries
		  for (const entry of entries) {
			// Check if the entry is intersecting the viewport
			if (entry.isIntersecting) {
				image.setAttribute('src',$(image).data('src'))
				image.classList.add('loader')
			}
		  }
		}, options);
		image_observer.observe(image);
	})
})

