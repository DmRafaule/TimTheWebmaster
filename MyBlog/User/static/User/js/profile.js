const number = 5
let offset = 0

function removeComment(toRemove){
	var comment_id = $(toRemove).attr("commentid")
	$.ajax({
		type: "POST",
		url: "/" + language_code + "/remove_comment/",
		data: {
			'comment_id': comment_id,
		},
		headers: {'X-CSRFToken': csrftoken},
		mode: 'same-origin', // Do not send CSRF token to another domain.
		success: function(result){
			// Removes only client side part
			$(toRemove).parent().remove()
		},
	})
}


function loadComments(){
	$.ajax({
		type: "POST",
		url: "/" + language_code + "/load_comments_by_user/",
		data: {
			'number': number,
			'offset': offset,
		},
		headers: {'X-CSRFToken': csrftoken},
		mode: 'same-origin', // Do not send CSRF token to another domain.
		success: function(result){
			console.log('loaded comments')
			$(result).insertBefore("#scroll-sentinel")
			$(".comment_remove__button").on('click', function() {
				removeComment(this)
				console.log('removing comments')
			})	
			offset = offset + number
		},
	})
}


$(document).ready(function(){
	const observer = new IntersectionObserver((entries, observer) => {
	  // Loop through the entries
	  for (const entry of entries) {
		// Check if the entry is intersecting the viewport
		if (entry.isIntersecting) {
			// Load more content
			loadComments()
		}
	  }
	});
	const scrollSentinel = document.querySelector("#scroll-sentinel");
	observer.observe(scrollSentinel);
})
