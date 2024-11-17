let status = $("#imagethief-status")
let logs = $("#imagethief-logs")
let update_status_repeater
let update_logs_repeater
let isFocusedLogs = false

function StartImageThief(url, mode){
	$.ajax({
		type: "GET",
		url: "/" + language_code + "/tools/image_thief-start/",
		data: {
			"url": url,
			"mode": mode,
		},
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
	$.ajax({
		type: "GET",
		url: "/" + language_code + "/tools/image_thief-init/",
		data: {
			'url': url,
			'mode': mode,
		},
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

function TabClosed(){
	$.ajax({
		type: "GET",
		url: "/" + language_code + "/tools/image_thief-tabclosed/",
		data: {
		},
		mode: 'same-origin', // Do not send CSRF token to another domain.
		success: function(result) {
			clearInterval(update_logs_repeater);
			clearInterval(update_status_repeater);
		},
	})
}

$(document).ready(function(){
	$("#start").on('click', InitImageThief)
	$("#verbose").on('click', ToggleVerbose)
	window.addEventListener("beforeunload", TabClosed);
})

