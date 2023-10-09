const number = 3
var offset = 0

function LoadPosts(){
	const container = document.querySelector(".page");
	$.ajax({
		type: "GET",
		url: "/" + language_code + "/load_post_preview/",
		data: {
			'number': number,
			'offset': offset,
			'category': category_name,
		},
		mode: 'same-origin', // Do not send CSRF token to another domain.
		success: function(result) {
			var page = $('.page');
			// Insert 'answer' from server into site code
			page.append(result)
			offset = offset + number
		},
		error: function(jqXHR, textStatus, errorThrown){
		}
	})
}




function buildThresholdList() {
  let thresholds = [];
  let numSteps = 20;

  for (let i = 1.0; i <= numSteps; i++) {
    let ratio = i / numSteps;
    thresholds.push(ratio);
  }

  thresholds.push(0);
  return thresholds;
}


$(document).ready( function(){
	const observer = new IntersectionObserver((entries, observer) => {
	  // Loop through the entries
	  for (const entry of entries) {
		// Check if the entry is intersecting the viewport
		if (entry.isIntersecting) {
			// Load more content
			LoadPosts()
		}
	  }
	});
	const scrollSentinel = document.querySelector("#scroll-sentinel");
	observer.observe(scrollSentinel);
})
