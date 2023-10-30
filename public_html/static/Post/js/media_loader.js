
$(document).ready(function(){
	const imageBlocks = document.querySelectorAll(".content_body__image");
	imageBlocks.forEach( (image) => {
		var options = {
			  threshold: 0.01,
			};
		var image_observer = new IntersectionObserver((entries, observer) => {
		  // Loop through the entries
		  for (const entry of entries) {
			// Check if the entry is intersecting the viewport
			if (entry.isIntersecting) {
				imgs = image.querySelectorAll('img')
				imgs.forEach( (img) => {
					img.setAttribute('src',$(img).data('src'))
				})
			}
		  }
		}, options);
		image_observer.observe(image);
	})
})
