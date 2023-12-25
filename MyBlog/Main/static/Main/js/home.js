let more_news = document.getElementById('more_news')

let number = 3
let offset = 0


function loadInitialPost(category, forWhichPage, whereToUpload){
	var localOffset = whereToUpload.data('offset')
	$.ajax({
		type: "GET",
		url: "load_post_preview-"+category+"/",
		data: {
			'number': 1,
			'offset': localOffset,
			'category': category,
			'is_recent': true,
			'for_who': forWhichPage,
		},
		mode: 'same-origin', // Do not send CSRF token to another domain.
		success: function(result){
			if (!whereToUpload.find('.end_list').length){
				whereToUpload.text('')
				whereToUpload.append(result)
			}
			else{
				whereToUpload.find('.action_button').addClass('active_more_home_button')
			}
			localOffset = localOffset + 1
			whereToUpload.data('offset', localOffset)
			var next_post = document.querySelectorAll(".next_post");
			next_post.forEach( (btn) => {
				btn.addEventListener('click', loadNextPost)
			})
		}
	})
}
function loadNextPost(){
	var page = $(this.parentElement.parentElement.parentElement)
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
		url: "load_post_preview-news/",
		data: {
			'number': number,
			'offset': offset,
			'category': 'news',
			'is_recent': true,
			'for_who': 'home',
		},
		mode: 'same-origin', // Do not send CSRF token to another domain.
		success: callback_success,
	})
}


loadInitialPost('cases','home',$('#case_to_upload'))
loadInitialPost('articles','home',$('#article_to_upload'))
loadMoreNews()
more_news.addEventListener('click',loadMoreNews)
