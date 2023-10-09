const number = 5
let offset = 0

function playButtonPushed(){
}


function showAddCommentForm(){
	$("#comment_add").toggleClass('active')
	$(".plus_description_addComment").on('click', playButtonPushed)
}

function removeComment(toRemove){
	var post = post_slug
	var comment_id = $(toRemove).attr("commentid")
	$.ajax({
		type: "POST",
		url: "/" + language_code + "/remove_comment/",
		data: {
			'post': post,
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

function sendComment(){
	var post = post_slug
	var about = $("#about").val()	
	$.ajax({
		type: "POST",
		url: "/" + language_code + "/load_comment/",
		data: {
			'post': post,
			'about': about,
		},
		headers: {'X-CSRFToken': csrftoken},
		mode: 'same-origin', // Do not send CSRF token to another domain.
		success: function(result){
			$(result).insertAfter("#comment_add")
			$(".comment_remove__button").on('click', function() {
				removeComment(this)
			})	
		},
	})
}

function loadComments(){
	var post = post_slug
	$.ajax({
		type: "POST",
		url: "/" + language_code + "/load_comments/",
		data: {
			'post': post,
			'number': number,
			'offset': offset,
		},
		headers: {'X-CSRFToken': csrftoken},
		mode: 'same-origin', // Do not send CSRF token to another domain.
		success: function(result){
			$(result).insertBefore("#scroll-sentinel")
			$(".comment_remove__button").on('click', function() {
				removeComment(this)
			})	
			offset = offset + number
		},
	})
}

function likePost(){
	$.ajax({
		type: "POST",
		url: "/" + language_code + "/like_post/",
		data: {
			'slug': post_slug
		},
		headers: {'X-CSRFToken': csrftoken},
		mode: 'same-origin', // Do not send CSRF token to another domain.
		success: function(result){
		},
	})
}

function sharePost(){
	$.ajax({
		type: "POST",
		url: "/" + language_code + "/share_post/",
		data: {
			'slug': post_slug
		},
		headers: {'X-CSRFToken': csrftoken},
		mode: 'same-origin', // Do not send CSRF token to another domain.
		success: function(result){
		},
	})
}

function showShareForm(){
	$("#shares_options").toggleClass("active")
	$("#shares_options").toggleClass("shares_options")
	$(".share_button").on('click', sharePost)
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

	$("#interactions_add__button").on('click', showAddCommentForm)
	$("#interactions_share__button").on('click', showShareForm)
	$("#interactions_like__button").on('click', likePost)
	$("#comment_add__buttonSend").on('click', sendComment)	
})
