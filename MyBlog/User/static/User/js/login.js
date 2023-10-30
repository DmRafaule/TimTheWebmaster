function OnLogin(){
	var username = $("#username").val()	
	var password = $("#password").val()	
	$.ajax({
		type: "POST",
		url:  'verify-login/',
		data: {
			'username': username,
			'password': password,
		},
		headers: {'X-CSRFToken': csrftoken},
		mode: 'same-origin', // Do not send CSRF token to another domain.
		success: function(result){
			$(".hint-required").css("color","green")
			$("#common-error").text(result.common)	
			$("#username-error").text(result.username)	
			$("#password-error").text(result.password)	
			// Redirect to login page
			setTimeout(function(){
				window.location.href = '/' + language_code + '/'
			},1000)
		},
		error: function(jqXHR, textStatus, errorThrown){
			$(".hint-required").css("color","red")
			$("#common-error").text(jqXHR.responseJSON.common)	
			$("#username-error").text(jqXHR.responseJSON.username)	
			$("#password-error").text(jqXHR.responseJSON.password)	
		}
	})
}

$(document).ready( function(){
	$("#login").on('click',OnLogin)
})
