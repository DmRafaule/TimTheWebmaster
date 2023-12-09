let next_article = document.getElementById('next_article')
let next_case = document.getElementById('next_case')
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
		url: "/" + language_code + "/load_post_preview-home/",
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
				whereToUpload.next().find('.action_button').addClass('active_more_home_button')
			}
			localOffset = localOffset + 1
			if (category === "Cases"){
				caseOffset = localOffset	
				$("#read_case > a").attr("href", $("#home_case_link").attr("href"))
			}
			else if ( category === "Articles"){
				articleOffset = localOffset 	
				$("#read_article > a").attr("href", $("#home_article_link").attr("href"))
			}
		}
	})
}
function loadNextPost(){
	var page = $(this.parentElement.parentElement.querySelector('.post_to_upload'))
	var category = page.data("category")
	var forWho = page.data("forwho")
	loadInitialPost(category,forWho,page)
}

// Clear all previouse content and insert new (refresh)
function appendNewNewsDesk( result ){
	var page = $('.news_to_upload');
	// Insert 'answer' from server into site code
	if (!page.find('.end_list').length){
		page.text('')
	}
	else{
		page.parent().parent().find('#more_news').addClass('active_more_home_button')
	}
	page.append(result)
	// Remoe first child post
	offset = offset + number
}
// Just append new loaded content 
function appendNewNewsMobile( result ){
	var page = $('.news_to_upload');
	if (page.find('.end_list').length){
		$('#more_news').addClass('active_more_home_button')
	}
	page.append(result)
	offset = offset + number
}

function loadMoreNews(){
	// Different functions for different behavior on different devices
	var callback_success = appendNewNewsDesk
	if( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
		number = 1	
		callback_success = appendNewNewsMobile
	}

	$.ajax({
		type: "GET",
		url: "/" + language_code + "/load_post_preview-home/",
		data: {
			'number': number,
			'offset': offset,
			'category': 'News',
			'forWho': 'home',
		},
		mode: 'same-origin', // Do not send CSRF token to another domain.
		success: callback_success,
	})
}


loadInitialPost('Cases','home',$('#case_to_upload'))
loadInitialPost('Articles','home',$('#article_to_upload'))
loadMoreNews()
next_article.addEventListener('click',loadNextPost) 
next_case.addEventListener('click',loadNextPost) 
more_news.addEventListener('click',loadMoreNews)
