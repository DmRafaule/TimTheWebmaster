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
			var like_number = document.getElementById('like_number')
			like_number.innerText = result['likes']
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
			var shares_number = document.getElementById('shares_number')
			shares_number.innerText = result['shares']
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


$(document).ready(function(){
	$("#onShare").on('click', showShareForm)
	$("#onLike").on('click', likePost)
})
