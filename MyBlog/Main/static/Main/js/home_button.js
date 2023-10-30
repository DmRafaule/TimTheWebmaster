let next_buttons = document.querySelectorAll('.next_button')
let more_news = document.getElementById('more_news')

let number = 3
let offset = 0
let caseOffset = 0
let articleOffset = 0


function loadInitialPost(category, forWhichPage, whereToUpload){
	var localOffset = 0
	if (category === "Cases")
		localOffset = caseOffset	
	else if ( category === "Articles")
		localOffset = articleOffset	
	$.ajax({
		type: "GET",
		url: "/" + language_code + "/load_post_preview/",
		data: {
			'number': 1,
			'offset': localOffset,
			'category': category,
			'forWho': forWhichPage,
		},
		mode: 'same-origin', // Do not send CSRF token to another domain.
		success: function(result){
			if (!whereToUpload.find('.end_list').length){
				whereToUpload.text('')
				whereToUpload.append(result)
			}
			else{
				whereToUpload.prev().find('#scroll_buttons').addClass('active')
			}
			localOffset = localOffset + 1
			if (category === "Cases")
				 caseOffset = localOffset	
			else if ( category === "Articles")
				articleOffset = localOffset 	
		}
	})
}
function loadNextPost(){
	pushIconButton(this)
	var page = $(this.parentElement.parentElement.parentElement.parentElement.querySelector('.post_to_upload'))
	var category = page.data("category")
	var forWho = page.data("forwho")
	loadInitialPost(category,forWho,page)
}

function pushIconButton(el){
	el.classList.add('icon_button_pressed')
	el.addEventListener("animationend", (event) => {
		el.classList.remove('icon_button_pressed')
	});
}
function pushMoreButton(el){
	el.classList.add('icon_button_pressed')
	el.addEventListener("animationend", (event) => {
		el.classList.remove('icon_button_pressed')
	});
}

// Clear all previouse content and insert new (refresh)
function appendNewNewsDesk( result ){
	var page = $('.news_to_upload');
	// Insert 'answer' from server into site code
	if (!page.find('.end_list').length){
		page.text('')
	}
	else{
		page.parent().parent().find('#more_news').addClass('active')
	}
	page.append(result)
	// Remoe first child post
	offset = offset + number
}
// Just append new loaded content 
function appendNewNewsMobile( result ){
	var page = $('.news_to_upload');
	if (page.find('.end_list').length){
		page.parent().parent().find('#more_news').addClass('active')
	}
	page.append(result)
	offset = offset + number
}

function loadMoreNews(){
	// Different functions for different behavior on different devices
	var callback_success = appendNewNewsDesk
	if (isMobile){
		number = 1	
		callback_success = appendNewNewsMobile
	}

	$.ajax({
		type: "GET",
		url: "/" + language_code + "/load_post_preview/",
		data: {
			'number': number,
			'offset': offset,
			'category': 'News',
			'forWho': 'home',
		},
		mode: 'same-origin', // Do not send CSRF token to another domain.
		success: callback_success,
		error: function(jqXHR, textStatus, errorThrown){
		}
	})
}

next_buttons.forEach( (button) => {
	button.addEventListener('click',loadNextPost) 
})

loadInitialPost('Cases','home',$('#case_to_upload'))
loadInitialPost('Articles','home',$('#article_to_upload'))
loadMoreNews()
more_news.addEventListener('click',function(){
	pushMoreButton(this.querySelector("p"))	
	loadMoreNews()
})
