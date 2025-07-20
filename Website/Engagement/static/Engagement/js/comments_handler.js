let POSTED_COMMENTS = 0

function goToCommentForm(){
	document.querySelector('#toSendCommentContainer').scrollIntoView({behavior: "smooth", block: "center", inline: "center"});
    document.querySelector('#id_name').focus()
}

function openReplyContainer(id){
    document.querySelector(`#comment-replies-${id}`).classList.remove('is_none')
}

function commentReply(container){
    goToCommentForm()
    var target_comment_id = container.dataset.commentReplyTo
    var form_input = document.querySelector('#comment_reply_to') 
    form_input.value = target_comment_id
    form_input.dataset.from = container.dataset.from
    form_input.parentElement.classList.remove('is_none')
    form_input.parentElement.querySelector('label').innerText = form_input.dataset.from
}

function removeReply(){
    var form_input = document.querySelector('#comment_reply_to') 
    form_input.value = "false"
    form_input.parentElement.classList.add('is_none')
}

function loadComments(){
    var url = `${window.location.pathname}`
    var load_comments_btn = document.querySelector('#onCommentLoad')
    var page_number = load_comments_btn.dataset.pageNumber
    var form_data = new FormData()
    form_data.append('csrfmiddlewaretoken', csrftoken)
    form_data.append('url', url)
    form_data.append('page_number', page_number)
    form_data.append('posted_comments', POSTED_COMMENTS)
    fetch(`/${language_code}/load_comments/`,{
        method: 'POST',
        body: form_data,
    })
    .then( response => {
        if (!response.ok)
            return response.json().then( response => {
                notificator.notify(response['msg'],'error')   
            })
        else
            return response.json().then( response =>{
                var is_next_page = Boolean(response['is_next_page'])
                load_comments_btn.dataset.pageNumber = response['next_page_number']
                if (!is_next_page){
                    load_comments_btn.remove()
                }
                var comments_doc = response['comments_doc']
                var comments_container = document.querySelector('#comments_container')
                comments_container.insertAdjacentHTML('beforeend', comments_doc)
                comments_container.querySelectorAll(".reply-to-this-comment").forEach((comment_reply)=>{
                    comment_reply.addEventListener('click', ()=>commentReply(comment_reply))
                })
                comments_container.querySelectorAll(".comment_reply_init").forEach( (reply_show_all) => {
                    var new_reply_show_all = reply_show_all.cloneNode(true)
                    reply_show_all.replaceWith(new_reply_show_all);
                    new_reply_show_all.addEventListener('click', ()=>loadReplies(null, reply_show_all.dataset.commentId))
                })
            })
    })
    .catch(error => {
        notificator.notify(error,'error')
        console.error('There was a problem with your fetch operation:', error);
    });
}

function loadReplies(parent_comment_id, this_comment_id, page_number = 1){
    var form_data = new FormData()
    form_data.append('csrfmiddlewaretoken', csrftoken)
    form_data.append('comment_root_id', this_comment_id)
    form_data.append('page_number', page_number)
    form_data.append('posted_comments', POSTED_COMMENTS)
    fetch(`/${language_code}/load_replies/`,{
        method: 'POST',
        body: form_data,
    })
    .then( response => {
        if (!response.ok)
            return response.json().then( response => {
                notificator.notify(response['msg'],'error')   
            })
        else
            return response.json().then( response =>{
                if (parent_comment_id == null){
                    document.querySelector(`#show-all-replies-${this_comment_id}>div>.comment_reply_init`).remove()
                }
                var is_next_page = Boolean(response['is_next_page'])
                document.querySelector(`#comment-replies-${this_comment_id}`).dataset.pageNumber = response['next_page_number']
                openReplyContainer(this_comment_id)
                if (!is_next_page){
                    document.querySelector(`#comment-replies-next-${this_comment_id}`).remove()
                }
                else{
                    document.querySelector(`#comment-replies-next-${this_comment_id}`).addEventListener('click', (ev)=>{
                        loadReplies(ev.currentTarget.dataset.parentCommentId, this_comment_id, response['next_page_number'])
                    })
                }
                var comments_doc = response['comments_doc']
                var comments_container = document.querySelector(`#comment-replies-body-${this_comment_id}`)
                comments_container.insertAdjacentHTML('beforeend', comments_doc)
                comments_container.querySelectorAll(".comment_reply_init").forEach( (reply_show_all) => {
                    reply_show_all.addEventListener('click', ()=>loadReplies(null, reply_show_all.dataset.commentId))
                })
                comments_container.querySelectorAll(".reply-to-this-comment").forEach((comment_reply)=>{
                    comment_reply.addEventListener('click', ()=>commentReply(comment_reply))
                })
            })
    })
    .catch(error => {
        notificator.notify(error,'error')
        console.error('There was a problem with your fetch operation:', error);
    });
}

function sendComment(){
    var url = `${window.location.pathname}`
    var rating_cont = document.querySelector('#id_rating')
    var rating = 0
    var is_rating = false
    if (rating_cont.getAttribute('type') != 'hidden'){
        is_rating = true
        rating_check = rating_cont.querySelector('input[name="rating"]:checked')
        if (rating_check)
            rating = rating_check.value;

        if (rating == 0){
            var rating_msg = document.querySelector('#id_rating_0').dataset.msg
            notificator.notify(`${rating_msg}`, 'error')
            return
        }
    }
    var form_doc = document.querySelector('#toSendCommentContainer')
    var form_data = new FormData();
	form_data.append("csrfmiddlewaretoken", csrftoken);
	form_data.append("name", form_doc.querySelector("#id_name").value)
	form_data.append("url", url)
    form_data.append("rating", rating)
    form_data.append("is_rating", is_rating)
	form_data.append("comment_reply_to", form_doc.querySelector("#comment_reply_to").value)
	form_data.append("message", form_doc.querySelector("#id_message").value)
	form_data.append("captcha_0", form_doc.querySelector("#id_captcha_0").value)
	form_data.append("captcha_1", form_doc.querySelector("#id_captcha_1").value)
	fetch('/' + language_code + "/send_comment/", {
		method: 'POST',
		body: form_data
	})
    .then( response => {
        if (!response.ok)
            return response.json().then( response => {
                // Send feedback msg
                notificator.notify(response['msg'],'error')  
				// Order is matter, since we replace old toSendCommentContainer, we need to get
				// A new version of this node
                // Update comment form
				document.querySelector('#toSendCommentContainer').outerHTML = response['form'] 
				document.querySelector('#onCommentSend').addEventListener('click', sendComment)
            })
        else
            return response.json().then( response =>{
                POSTED_COMMENTS += 1
                history.pushState(null, '', '#comments_limiter')
                location.reload()
            })
    })
}

function emptyStars(){
    document.querySelectorAll("#id_rating > * > label").forEach((star) => {
        star.classList.remove('selected_star')
        star.classList.add('not_selected_star')
    })
}

function onStar(value){
    emptyStars()
    for (var i = 1; i <= value; i++){
        var star = document.getElementById(`id_rating_${i}`)
        star.parentElement.classList.add('selected_star')
        star.parentElement.classList.remove('not_selected_star')
    }
}

function initStars(){
    document.querySelectorAll("#id_rating > * > label").forEach((star, num, stars) => {
        star.firstChild.nextSibling.textContent = ""
        star.classList.add('not_selected_star')
        star.addEventListener('click', ()=>onStar(num))
    })
}

function initStarRating(){
    const config = { childList: true };
    const observer = new MutationObserver((mutationList, observer) =>{
        for (const mutation of mutationList) {
            if (mutation.addedNodes.length > 0){ 
                initStars()
            }
          }
    });
    var comments_limiter = document.getElementById('comments_limiter') 
    if (comments_limiter){
        observer.observe(comments_limiter, config);
        initStars()
    }
}

function onReady(){
    document.querySelectorAll('#onComment').forEach( (onComment) => {
		onComment.addEventListener('click', goToCommentForm)
    })
    document.querySelectorAll(".comment_reply_init").forEach( (reply_show_all) => {
        reply_show_all.addEventListener('click', ()=>loadReplies(null, reply_show_all.dataset.commentId))
    })
    document.querySelectorAll(".reply-to-this-comment").forEach((comment_reply)=>{
        comment_reply.addEventListener('click', ()=>commentReply(comment_reply))
    })
    var onReplyRemove = document.querySelector('#onReplyRemove')
    if (onReplyRemove){
        onReplyRemove.addEventListener('click', removeReply)
    }
    var onCommentLoad = document.querySelector('#onCommentLoad')
    if (onCommentLoad){
        onCommentLoad.addEventListener('click', loadComments)
    }
    var onCommentSend = document.querySelector('#onCommentSend')
    if (onCommentSend){
        onCommentSend.addEventListener('click', sendComment)
    }
    initStarRating()
}

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", onReady);
} else {
  onReady()
}