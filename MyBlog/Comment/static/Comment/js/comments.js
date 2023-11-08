const number = 5
let offset = 0
var default_avatar_path = ''


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

function sendComment(path){
	var post = post_slug
	var about = $("#about").val()	
	var username = $("#comments_el__user_name_commentAdd").text()

	$.ajax({
		type: "POST",
		url: "/" + language_code + "/" + path + "/",
		data: {
			'post': post,
			'about': about,
			'username': username,
		},
		headers: {'X-CSRFToken': csrftoken},
		mode: 'same-origin', // Do not send CSRF token to another domain.
		success: function(result){
			$(result).insertAfter("#comment_add")
			$(".comment_remove__button").off()
			$(".comment_remove__button").one('click', function() {
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
			$(".comment_remove__button").off()
			$(".comment_remove__button").one('click', function() {
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


function prepareForCommenting(){
	var username = $("#userID").val()	
	$.ajax({
		type: "GET",
		url: "/" + language_code + "/prepare_user/",
		data: {
			'username': username 
		},
		headers: {'X-CSRFToken': csrftoken},
		mode: 'same-origin', // Do not send CSRF token to another domain.
		success: function(result){
			$("#about").attr('readonly',!result.isValid)
			$("#comments_el__user_name_commentAdd").text(result.username)
			$("#comment_add__buttonShowLoginOptions").toggleClass("active")
			$("#comment_add__buttonSendGuesting").toggleClass("active")
		},
	})
}

function showCommentSubmitForm(){
	$("#loginableSocialNets").toggleClass("active")
	$("#parsingFormSubmit").one("click", prepareForCommenting)
}


$(document).ready(function(){
	default_avatar_path = $("#comments_el__user_avatar_commentAdd").attr('src')
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

	$("#interactions_share__button").on('click', showShareForm)
	$("#interactions_like__button").on('click', likePost)
	$("#comment_add__buttonSendGuesting").on('click', function(){
		sendComment("send_comment_guesting")
	})	
	$("#comment_add__buttonSendAuthorized").on('click', function(){
		sendComment("send_comment_authorized")
	})	
	$("#loginableSocialNets_text").on('click', showCommentSubmitForm)	
})
