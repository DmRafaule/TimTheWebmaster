function askToBookmarkIt(){
	var url = `${window.location.pathname}${window.location.search}`
	var formData = new FormData()
    formData.append('url', url)
    formData.append('csrfmiddlewaretoken', csrftoken)
    fetch("/" + language_code + "/bookmark_post/", {
        method: 'POST',
        body: formData,
    })
    .then( response => {
        if (!response.ok)
            return response.json().then( response => {
                notificator.notify(response['msg'],'error')
            })
        else
            return response.json().then( response =>{
                notificator.notify(response['msg'],'info', 15)
				//var like_number = document.getElementById('like_number')
				//like_number.innerText = response['likes']
            })
    })
}

function likePost(){
	var url = `${window.location.pathname}${window.location.search}`
	var formData = new FormData()
    formData.append('url', url)
    formData.append('csrfmiddlewaretoken', csrftoken)
    fetch("/" + language_code + "/like_post/", {
        method: 'POST',
        body: formData,
    })
    .then( response => {
        if (!response.ok)
            return response.json().then( response => {
                notificator.notify(response['msg'],'error')
            })
        else
            return response.json().then( response =>{
                notificator.notify(response['msg'],'success')
				//var like_number = document.getElementById('like_number')
				//like_number.innerText = response['likes']
            })
    })
}

function sharePost(){
	var url = `${window.location.pathname}${window.location.search}`
	var formData = new FormData()
    formData.append('url', url)
    formData.append('csrfmiddlewaretoken', csrftoken)
    fetch("/" + language_code + "/share_post/", {
        method: 'POST',
        body: formData,
    })
    .then( response => {
        if (!response.ok)
            return response.json().then( response => {
                notificator.notify(response['msg'],'error')   
				closeShareForm()     
            })
        else
            return response.json().then( response =>{
                notificator.notify(response['msg'],'success')
				//var shares_number = document.getElementById('shares_number')
				//shares_number.innerText = response['shares']
				closeShareForm()
            })
    })
    .catch(error => {
        notificator.notify(error,'error')
        console.error('There was a problem with your fetch operation:', error);
    });
}

function feedbackPost(){
	var sendFeedbackModal = document.querySelector('#toSendFeedbackModal')
	var form_data = new FormData();
	form_data.append("csrfmiddlewaretoken", csrftoken);
	form_data.append("username", sendFeedbackModal.querySelector("#id_username").value)
	form_data.append("email", sendFeedbackModal.querySelector("#id_email").value)
	form_data.append("message", sendFeedbackModal.querySelector("#id_message").value)
	form_data.append("captcha_0", sendFeedbackModal.querySelector("#id_captcha_0").value)
	form_data.append("captcha_1", sendFeedbackModal.querySelector("#id_captcha_1").value)
	fetch('/' + language_code + "/feedback_post/", {
		method: 'POST',
		body: form_data
	})
    .then( response => {
        if (!response.ok)
            return response.json().then( response => {
                notificator.notify(response['msg'],'error')  
				// Order is matter, since we replace old toSendFeedbackModal, we need to get
				// A new version of this node
				document.querySelector('#toSendFeedbackModal').outerHTML = response['form'] 
				var sendFeedbackModal = document.querySelector('#toSendFeedbackModal')
				openModal(sendFeedbackModal)
				initModals()
				document.querySelector('#send_feedback_submit').addEventListener('click', feedbackPost)
            })
        else
            return response.json().then( response =>{
                notificator.notify(response['msg'],'success')
				document.querySelector('#toSendFeedbackModal').outerHTML = response['form'] 
				initModals()
				document.querySelector('#send_feedback_submit').addEventListener('click', feedbackPost)
				closeModal(document.querySelector('#toSendFeedbackModal'))
            })
    })
}

function closeShareForm(){
	var share_button = document.querySelector('#onShare')
	if (share_button){
		share_button.classList.remove('active_engagement_button')
		var share_options = document.querySelector('#share_options')
		share_options.classList.add("active_share_options")
		var share_button_img = share_button.children[0]
		share_button_img.setAttribute('src', share_button.dataset.shareBtn)
		share_button_img.classList.remove('svg_icon_inverted')
	}
}

function showShareForm(){
	var share_options = this.querySelector("#share_options")
	if (share_options.classList.contains("active_share_options")){
		this.classList.add('active_engagement_button')
		this.children[0].classList.add('svg_icon_inverted')
		this.children[0].setAttribute('src', this.children[0].dataset.closeBtn)
	}
	else{
		this.classList.remove('active_engagement_button')
		this.children[0].setAttribute('src', this.dataset.shareBtn)
		this.children[0].classList.remove('svg_icon_inverted')
	}
	share_options.classList.toggle("active_share_options")
}

function toggleEngagementActions(){
	var action_options = document.getElementById("engagement_body_body")
	if (action_options.classList.contains("active_engagement_body_body")){
	}
	else{
	}
	action_options.classList.toggle("active_engagement_body_body")
}

function closeEngagementButtons( body ){
	body.classList.add("active_engagement_body_body")	
	closeShareForm()
}

function onReady(){
	document.querySelectorAll('#onBookmark').forEach( (onBookmark) => {
		onBookmark.addEventListener('click', askToBookmarkIt)
	})
	document.querySelectorAll('#onShare').forEach( (onShare) => {
		onShare.addEventListener('click', showShareForm)
		document.querySelectorAll('.share_button').forEach((btn)=>{
			btn.addEventListener('click', sharePost)
		})
	})
	document.querySelectorAll('#onLike').forEach( (onLike) => {
		onLike.addEventListener('click', likePost)
	})
	document.querySelectorAll('#onFeedback').forEach( (onFeedback) => {
		document.querySelectorAll('#send_feedback_submit').forEach((send_feedback_submit) => {
			send_feedback_submit.addEventListener('click', feedbackPost)
		})
	})

	var engagement_actions_button = document.querySelector('#engagement_actions_button')
	if (engagement_actions_button){
		engagement_actions_button.addEventListener('click', toggleEngagementActions)
		onClickOutsideHat(
			engagement_actions_button,
			document.getElementById("engagement_body_body"), 
			() => closeEngagementButtons(document.getElementById("engagement_body_body")) );

		var footer = document.querySelector('footer')
		if (footer.getBoundingClientRect().height <= 100){
			document.querySelector("#engagement_body").style.bottom = footer.getBoundingClientRect().height + "px"
		}
		var paginator = document.querySelector('#paginator_container')
		if (paginator && IS_MOBILE){
			document.querySelector("#engagement_body").classList.add('engagement_body_mobile')
		}
	
	}

}

if (document.readyState === "loading") {
  	document.addEventListener("DOMContentLoaded", onReady);
} else {
	onReady()
}