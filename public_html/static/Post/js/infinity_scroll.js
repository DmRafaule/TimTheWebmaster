const number = 5
var offset = 0

function LoadPosts(isRecent = true, mode = 'basic', forWho = ''){
	$.ajax({
		type: "GET",
		url: "load_post_preview/",
		data: {
			'number': number,
			'offset': offset,
			'category': category_name,
			'is_recent': isRecent,
			'mode': mode,
			'for_who': '',
		},
		mode: 'same-origin', // Do not send CSRF token to another domain.
		success: function(result) {
			var page = $('#page');
			// Insert 'answer' from server into site code
			page.append(result)
			// Вставляем анимацию проявления нового поста
			var posts = page.find('.post_preview')
			for (var i = 0; i < posts.length; i++){
				if (!$(posts[i]).hasClass('loader'))
					$(posts[i]).addClass('loader')
			}

			offset = offset + number
		},
		error: function(jqXHR, textStatus, errorThrown){
		}
	})
}

$(document).ready( function(){
	var viewsContainer = $("#toViews")
	var mode = viewsContainer.data('view')
	var forWho = viewsContainer.data('who')
	var isRecent = $("#onSort").data('sort')
	const observer = new IntersectionObserver((entries, observer) => {
	  // Loop through the entries
	  for (const entry of entries) {
		// Check if the entry is intersecting the viewport
		if (entry.isIntersecting) {
			// Load more content
			var viewsContainer = $("#toViews")
			var mode = viewsContainer.data('view')
			var forWho = viewsContainer.data('who')
			var isRecent = $("#onSort").data('sort')
			LoadPosts(isRecent, mode, forWho)
		}
	  }
	});
	const scrollSentinel = document.querySelector("#scroll-sentinel");
	observer.observe(scrollSentinel);
})
