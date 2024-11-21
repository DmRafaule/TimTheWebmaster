let status = $("#imagethief-status")
let logs = $("#imagethief-logs")
let update_status_repeater
let update_logs_repeater
let isFocusedLogs = false

function StartImageThief(url, mode){

	formData = new FormData();
	formData.append('url', url)
	formData.append('mode', mode)
	formData.append('csrfmiddlewaretoken', csrftoken)

	$.ajax({
		type: "POST",
		url: "/" + language_code + "/tools/image_thief-start/",
		data: formData,
		processData: false,
		contentType: false,
		mode: 'same-origin', // Do not send CSRF token to another domain.
		// Results of scrapping images success
		success: function(result) {
			clearInterval(update_status_repeater);
			// Disable mode selection
			$('input[name=mod]').attr("disabled",false);
			// Change background color of Modes block
			$("#modes_block").css("color", "black")
			$("#imagethief-results-images").attr("href", result.imgs_path)
			$("#imagethief_text_inButton").text(result.btn)
			$("#current_try").text(result.try)
			$("#total_try").text(result.try_limit)
			$("#container_imagethief-results").show()
			$("#container_imagethief-status").hide()
			// Clear all events handlers before seting up new one
			clearInterval(update_status_repeater);
			$("#start").off()
			$("#start").on('click', InitImageThief)
			$("#imagethief_text_inButton").css("background-color", "var(--acent_color)")
			$("#imagethief_text_inButton").addClass('button')
		},
		// Results of scrapping images fail 
		error: function(jqXHR, textStatus, errorThrown){
			// Disable mode selection
			$('input[name=mod]').attr("disabled",false);
			// Change background color of Modes block
			$("#modes_block").css("color", "black")
			// Show status field of tool
			$("#container_imagethief-status").hide()
			$("#container_imagethief-results").hide()
			// Insert requested text
			$("#imagethief_text_inButton").text(jqXHR.responseJSON.btn)
			$("#verbose-error").text(jqXHR.responseJSON.status_msg)	
			$("#current_try").text(jqXHR.responseJSON.try)
			$("#total_try").text(jqXHR.responseJSON.try_limit)
			// clear interval function
			clearInterval(update_status_repeater);
			// Clear all events handlers before seting up new one
			$("#start").off()
			$("#start").on('click', InitImageThief)
			$("#imagethief_text_inButton").css("background-color", "var(--acent_color)")
			$("#imagethief_text_inButton").addClass('button')
		}
	})
}

function InitImageThief(){
	var url = $("#url").val()
	var mode = $('input[name=mod]:checked').val()
	var proxy_file = 'EMPTY'
	if($('#proxy_file').prop('files').length > 0){
		proxy_file = $('#proxy_file').prop('files')[0];
	}

	var proxy_generate = 'EMPTY'
	if (!$('#proxy_generate').attr('disabled')){
		proxy_generate = $('#proxy_generate').is(':checked')
	}

	var proxy_input = 'EMPTY'
	if ($('#proxy_input').val().length > 0){
		var proxy_input = $('#proxy_input').val()
	}

	formData = new FormData();
	formData.append('url', url)
	formData.append('mode', mode)
	formData.append('proxy_file', proxy_file)
	formData.append('proxy_generate', proxy_generate)
	formData.append('proxy_input', proxy_input)
	formData.append('csrfmiddlewaretoken', csrftoken)

	$.ajax({
		type: "POST",
		url: "/" + language_code + "/tools/image_thief-init/",
		data: formData,
		processData: false,
		contentType: false,
		mode: 'same-origin',
		// Result of initialization of scrapping images 
		success: function(result) {
			// Disable mode selection
			$('input[name=mod]').attr("disabled",true);
			// Change background color of Modes block
			$("#modes_block").css("color", "grey")
			// Show status field of tool
			$("#container_imagethief-status").show()
			$("#container_imagethief-results").hide()
			// Insert requested text
			$("#imagethief_text_inButton").text(result.btn)
			$("#verbose-error").text(result.status_msg)
			// Set interval function
			update_status_repeater = setInterval(UpdateStatus, 1000);
			// Clear all events handlers before seting up new one
			$("#start").off()
			$("#imagethief_text_inButton").css("background-color", "grey")
			$("#imagethief_text_inButton").removeClass('button')
			StartImageThief(result.url, result.mode)
			// Make sure it is empty
			$("#imagethief-logs").text("")
				
		},
		// Errors if some invalid input 
		error: function(jqXHR, textStatus, errorThrown){
			$("#verbose-error").text(jqXHR.responseJSON.status_msg)	
		}
	})
}

function ToggleStatus(){
	if (!update_status_repeater){
		update_status_repeater = setInterval(UpdateStatus, 1000);
	}
	else{
		clearInterval(update_status_repeater);
		update_status_repeater = undefined
	}
}

function ToggleVerbose(){
	var verbose = $(this).attr("checked")
	$("#container_imagethief-logs").toggle()
	$("#verbose-error").text("")	
	if (!update_logs_repeater){
		update_logs_repeater = setInterval(UpdateLogs, 1000);
	}
	else{
		clearInterval(update_logs_repeater);
		update_logs_repeater = undefined
	}
}

function UpdateStatus(){
	$.ajax({
		type: "GET",
		url: "/" + language_code + "/tools/image_thief-update_status/",
		mode: 'same-origin', // Do not send CSRF token to another domain.
		success: function(result) {
			i_progressbar = $("#imagethief-progressbar")
			i_statustext = $("#imagethief-statustext")
			i_statustext_current = $("#imagethief-statustext_current")
			i_statustext_total = $("#imagethief-statustext_total")
			i_statustext.text("")
			i_statustext.append(result.period)
			i_statustext_current.text("")
			i_statustext_current.append(result.current)
			i_statustext_total.text("")
			i_statustext_total.append(result.total)
		},
	})
}

function UpdateLogs(){
	$.ajax({
		type: "GET",
		url: "/" + language_code + "/tools/image_thief-update_logs/",
		data: {
		},
		mode: 'same-origin', // Do not send CSRF token to another domain.
		success: function(result) {
			$("#verbose-error").text(result.msg_er)	
			let i_log = $("#imagethief-logs")
			i_log.append(result.msg)
			let new_height = i_log.height()
			let i_log_block = $("#imagethief-logs_block")
			i_log_block.height(new_height)
			i_log_block.on("focus", function() {
				isFocusedLogs = true
			})
			i_log_block.on("focusout", function() {
				isFocusedLogs = false
			})
			if (!isFocusedLogs)
				i_log_block.scrollTop(i_log_block[0].scrollHeight);
		},
		error: function(jqXHR, textStatus, errorThrown){
			clearInterval(update_logs_repeater);
		}
	})
}

// Thanks to https://jsbin.com/muhipoye/1/edit
function clearInputFile(f){
	if(f.value){
		try{
			f.value = ''; //for IE11, latest Chrome/Firefox/Opera...
		}catch(err){
		}
		if(f.value){ //for IE5 ~ IE10
			var form = document.createElement('form'), ref = f.nextSibling;
			form.appendChild(f);
			form.reset();
			ref.parentNode.insertBefore(f,ref);
		}
	}
}

function setCheckbox(el, value){
	el.checked = value
}

function clearInput(el){
	el.value = ''
}

function UpdateProxies(target){
	switch($(target.target).attr('id')){
		case 'proxy_file':
			setCheckbox(document.querySelector('#proxy_generate'), false)
			clearInput(document.querySelector('#proxy_input'))
			break
		case 'proxy_generate':
			clearInputFile(document.querySelector('#proxy_file'))
			clearInput(document.querySelector('#proxy_input'))
			break
		case 'proxy_input':
			setCheckbox(document.querySelector('#proxy_generate'), false)
			clearInputFile(document.querySelector('#proxy_file'))
			break
	}
	//$(".proxy_options").each( (indx, el) => {
	//	$(el).attr("disabled",true);
	//});
	//$(target.target).attr('disabled', false)
}

$(document).ready(function(){
	$("#start").on('click', InitImageThief)
	$("#verbose").on('click', ToggleVerbose)
	$(".proxy_options").each( (indx, el) => {
		$(el).on('click', UpdateProxies)
	});
})

