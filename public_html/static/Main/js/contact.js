function OnSend(){
	var form_data = new FormData();
	form_data.append("csrfmiddlewaretoken", csrftoken);
	form_data.append("username", $("#username").val())
	form_data.append("email", $("#email").val())
	form_data.append("about", $("#about").val())
	$.ajax({
		type: "POST",
		// What kind of addres our server expectin for (gonna handle sended data)
		url: "load_message/",
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
		},
		error: function(jqXHR, textStatus, errorThrown){
			$(".hint-required").css("color","red")
			$("#common-error").text(jqXHR.responseJSON.common)	
			$("#username-error").text(jqXHR.responseJSON.username)	
			$("#email-error").text(jqXHR.responseJSON.email)	
		}
	});
}

$(document).ready( function(){
	$("#send_button").on('click',OnSend)
})
