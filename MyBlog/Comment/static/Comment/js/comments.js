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
	var username = $("#toUsername").text()

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
			$(result).insertAfter("#toComment")
			$(".remove_action_button").off()
			$("#common-error").text('')	
			$(".remove_action_button").one('click', function() {
				removeComment(this)
			})	
		},
		error: function(jqXHR, textStatus, errorThrown){
			$(".hint-required").css("color","red")
			$("#common-error").text(jqXHR.responseJSON.message)	
		}
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
			$(".remove_action_button").off()
			$(".remove_action_button").one('click', function() {
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
	share_options = document.getElementById("share_options")
	if (share_options.classList.contains("active_share_options")){
		share_options.style.height = 0
	}
	else{
		share_options.style.height = share_options.firstElementChild.clientHeight + "px"
	}
	share_options.classList.toggle("active_share_options")
	$(".share_button").off()
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
			$("#toUsername").text(result.username)
			$("#toSendVerify-guesting").toggleClass("active")
			$("#onSend-guesting").toggleClass("active")
		},
	})
}

function showCommentSubmitForm(){
	$("#toNewUsername").toggleClass("active")
	$("#onNewUsername").one("click", prepareForCommenting)
}


$(document).ready(function(){
	default_avatar_path = $("#toAvatar").attr('src')
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

	$("#onShare").on('click', showShareForm)
	$("#onLike").on('click', likePost)
	$("#onSend-guesting").on('click', function(){
		sendComment("send_comment_guesting")
	})	
	$("#onSend-authorized").on('click', function(){
		sendComment("send_comment_authorized")
	})	
	$("#onSendVerify-guesting").on('click', showCommentSubmitForm)	
})
