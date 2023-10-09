function OnButton(){
	$("#plus_description").addClass("plus_desctipion_active")
	$("#plus").addClass("plus_active")
	$("#plus_description>a").text('Send new case')
}

function OnSignup(){
	var form_data = new FormData();
	form_data.append("csrfmiddlewaretoken", csrftoken);
	form_data.append("username", $("#username").val())
	form_data.append("email", $("#email").val())
	form_data.append("website",  $("#website").val())
	form_data.append("about", $("#about").val())
	form_data.append("file", document.getElementById('file').files[0]);
	$.ajax({
		type: "POST",
		// What kind of addres our server expectin for (gonna handle sended data)
		url: "verify-send/",
		// Data to send on server
		// I need pass to server parent name because I need to hide one of field (ManyToMany django DB relation)
		data: form_data,
		// If we use FormData you have to specify them
		processData: false,
		contentType: false,
		// For activating feature of django csrf-tokent protection
		headers: {'X-CSRFToken': csrftoken},
		mode: 'same-origin', // Do not send CSRF token to another domain.
		success: function(result) {
			$(".hint-required").css("color","green")
			$("#common-error").text(result.common)	
			$("#username-error").text(result.username)	
			$("#email-error").text(result.email)	
			$("#website-error").text(result.website)	
			// Redirect to login page
			setTimeout(function(){
				window.location.href = '/cases/'
			},3000)
		},
		error: function(jqXHR, textStatus, errorThrown){
			$(".hint-required").css("color","red")
			$("#common-error").text(jqXHR.responseJSON.common)	
			$("#username-error").text(jqXHR.responseJSON.username)	
			$("#email-error").text(jqXHR.responseJSON.email)	
			$("#website-error").text(jqXHR.responseJSON.website)	
		}
	});
}

$(document).ready(function(){
	$("#plus").on('click',OnButton)			
	$("#send").on('click',OnSignup)
})
