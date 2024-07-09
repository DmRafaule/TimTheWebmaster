let feed_post_size = 5
let feed_meta = null
let feed_post_offset = 0


function loadPosts( feed_id, offset, sorted, callback ){
	callback 	= callback 	|| function(){}
	var progressbar = document.querySelector('#progressbar')
	progressbar.style.display = 'block'
	var posts = document.getElementById('rss_posts')
	$.ajax({
		type: "GET",
		url: "get-feed-posts/",
		data: {
			'id': feed_id,
			'size': feed_post_size,
			'offset': offset,
			'sorted': sorted,
		},
		headers: {'X-CSRFToken': csrftoken},
		mode: 'same-origin', // Do not send CSRF token to another domain.
		success: function(result) {
			posts.innerText = ''
			posts.insertAdjacentHTML('beforeend', result)
			document.body.scrollTop = document.documentElement.scrollTop = 0;
			feed_meta = document.getElementById('feed_meta_data')
			progressbar.style.display = 'none'
			callback()
		},
		error: function(jqXHR, textStatus, errorThrown){
		}
	})
}

function displayFeed(){
	var feed_id = this.dataset.feedId
	if (IS_MOBILE){
		var groups_container = document.getElementById("rss_aggregator_mobile_groups_container")
		groups_container.classList.toggle("active_nav")	
		groups_container.style.top = header_height
	}
	/* Загружаем первые посты с фида */
	loadPosts(feed_id, 0, false, function(){
		/* Обновляем пагинатор */
		updateRSS_paginator(feed_post_size, 0, feed_id)
		/* Активируем и обновляеем кнопку сортировки постов */
		var sort_button = document.getElementById('onSort')
		sort_button.dataset.sort = 'false'
		sort_button.addEventListener('click', sortFeed)
		sort_button.classList.remove('rotate_X')
	})
}

function sortFeed(){
	var isSorted = this.dataset.sort
	if (isSorted == 'true'){
		isSorted = true
	}else{
		isSorted = false
	}
	this.dataset.sort = !isSorted
	this.classList.toggle('rotate_X')

	var feed_id = feed_meta.dataset.feedId
	var feed_offset = feed_meta.dataset.offset
	feed_meta.dataset.sorted = !isSorted
	loadPosts(feed_id, feed_offset, !isSorted)
	
}


function onPage(){
	var feed_id = feed_meta.dataset.feedId
	var feed_sorted = feed_meta.dataset.sorted
	loadPosts(feed_id, this.dataset.offset, feed_sorted)
}

function updateRSS_paginator(size, offset, feed_id){
	var paginator_body = document.getElementById('paginator_body')
	paginator_body.innerText = ''
	var default_page_example_in_paginator = document.getElementById('rss-paginator_default_page_example')
	var first_page_example_in_paginator = document.getElementById('rss-paginator_first_page_example')
	var last_page_example_in_paginator = document.getElementById('rss-paginator_last_page_example')
	if (!IS_MOBILE){
		var dots_example_in_paginator = document.getElementById('rss-paginator_dots_example')
	}

	var length = parseInt(feed_meta.dataset.elementsInFeed)
	var num_pages = length/size


	if (num_pages == 1){
		var only_one_page = first_page_example_in_paginator.cloneNode()
		only_one_page.classList.add('current_pagin_button')
		only_one_page.classList.remove('example_pagin_button')
		only_one_page.innerText = '1'
		only_one_page.addEventListener('click', onPaginButton)
		only_one_page.addEventListener('click', onPage)
		only_one_page.dataset.offset = 0
		only_one_page.dataset.feedId = feed_id
		paginator_body.insertAdjacentElement('beforeend', only_one_page)
	}else if (num_pages == 2){
		var first_page = first_page_example_in_paginator.cloneNode()
		first_page.classList.add('current_pagin_button')
		first_page.classList.remove('example_pagin_button')
		first_page.innerText = '1'
		first_page.addEventListener('click', onPaginButton)
		first_page.addEventListener('click', onPage)
		first_page.dataset.offset = 0
		first_page.dataset.feedId = feed_id
		paginator_body.insertAdjacentElement('beforeend', first_page)

		var last_page = last_page_example_in_paginator.cloneNode()
		last_page.innerText = String(num_pages)
		last_page.addEventListener('click', onPaginButton)
		last_page.addEventListener('click', onPage)
		last_page.dataset.offset = (num_pages - 1) * feed_post_size
		last_page.dataset.feedId = feed_id
		last_page.classList.remove('example_pagin_button')
		paginator_body.insertAdjacentElement('beforeend', last_page)
	}else if (num_pages == 3){
		var first_page = first_page_example_in_paginator.cloneNode()
		first_page.classList.add('current_pagin_button')
		first_page.classList.remove('example_pagin_button')
		first_page.innerText = '1'
		first_page.addEventListener('click', onPaginButton)
		first_page.addEventListener('click', onPage)
		first_page.dataset.offset = 0
		first_page.dataset.feedId = feed_id
		paginator_body.insertAdjacentElement('beforeend', first_page)

		var mid_page = default_page_example_in_paginator.cloneNode(true)
		mid_page.innerText = '2'
		mid_page.addEventListener('click', onPaginButton)
		mid_page.addEventListener('click', onPage)
		first_page.dataset.offset = feed_post_size
		first_page.dataset.feedId = feed_id
		mid_page.classList.remove('example_pagin_button')
		paginator_body.insertAdjacentElement('beforeend', mid_page)

		var last_page = last_page_example_in_paginator.cloneNode()
		last_page.innerText = String(num_pages)
		last_page.addEventListener('click', onPaginButton)
		last_page.addEventListener('click', onPage)
		last_page.dataset.offset = (num_pages - 1) * feed_post_size
		last_page.dataset.feedId = feed_id
		last_page.classList.remove('example_pagin_button')
		paginator_body.insertAdjacentElement('beforeend', last_page)
	}else if (num_pages >= 4){
		var first_page = first_page_example_in_paginator.cloneNode()
		first_page.classList.add('current_pagin_button')
		first_page.classList.remove('example_pagin_button')
		first_page.innerText = '1'
		first_page.addEventListener('click', onPaginButton)
		first_page.addEventListener('click', onPage)
		first_page.dataset.offset = 0
		first_page.dataset.feedId = feed_id
		paginator_body.insertAdjacentElement('beforeend', first_page)
		
		if (!IS_MOBILE){
			var dots1 = dots_example_in_paginator.cloneNode(true)
			dots1.classList.remove('example_pagin_button')
			paginator_body.insertAdjacentElement('beforeend', dots1)
		}

		
		for (var i = 2; i < num_pages; i++){
			var mid_page = default_page_example_in_paginator.cloneNode(true)
			mid_page.innerText = String(i)
			mid_page.addEventListener('click', onPaginButton)
			mid_page.addEventListener('click', onPage)
			mid_page.dataset.offset = (i - 1) * feed_post_size
			mid_page.dataset.feedId = feed_id
			mid_page.classList.remove('example_pagin_button')
			paginator_body.insertAdjacentElement('beforeend', mid_page)
		}
		
		if (!IS_MOBILE){
			var dots2 = dots_example_in_paginator.cloneNode(true)
			dots2.classList.remove('example_pagin_button')
			paginator_body.insertAdjacentElement('beforeend', dots2)
		}

		var last_page = last_page_example_in_paginator.cloneNode()
		last_page.innerText = String(num_pages)
		last_page.addEventListener('click', onPaginButton)
		last_page.addEventListener('click', onPage)
		last_page.dataset.offset = (num_pages - 1) * feed_post_size
		last_page.dataset.feedId = feed_id
		last_page.classList.remove('example_pagin_button')
		paginator_body.insertAdjacentElement('beforeend', last_page)
	}

	var prev_pagin_button = document.getElementById('prev_pagin_button')
	try {
		prev_pagin_button.dataset.feedId = feed_id
		prev_pagin_button.dataset.offset = document.querySelector('.current_pagin_button').dataset.offset
		prev_pagin_button.addEventListener('click', function(){
			this.dataset.offset = document.querySelector('.current_pagin_button').dataset.offset
		})
		prev_pagin_button.addEventListener('click', onPage)	
	} catch (error) {
		
	}
	
	try {
		var next_pagin_button = document.getElementById('next_pagin_button')
		next_pagin_button.dataset.feedId = feed_id
		next_pagin_button.dataset.offset = document.querySelector('.current_pagin_button').dataset.offset
		next_pagin_button.addEventListener('click', function(){
			this.dataset.offset = document.querySelector('.current_pagin_button').dataset.offset
		})
		next_pagin_button.addEventListener('click', onPage)	
	} catch (error) {
		
	}
}

function submitFeed(){
	var feedname = $("#feedname").val()
	$.ajax({
		type: "POST",
		url: "submit-feed/",
		data: {
			'feedname': feedname
		},
		headers: {'X-CSRFToken': csrftoken},
		mode: 'same-origin', // Do not send CSRF token to another domain.
		success: function(result) {
			var feeds = document.getElementById('rss_feeds')
			feeds.insertAdjacentHTML('beforeend', result)
			var modal = document.getElementById("myModal");
			modal.style.display = "none";
			// Добавляем хендлеры для удаления фида и его показа
			var delete_feeds = document.getElementsByClassName('onDeleteFeed')
			for (var i = 0; i < delete_feeds.length; i++){
				delete_feeds[i].addEventListener('click', deleteFeed)
			}
			var display_feeds = document.getElementsByClassName('onDisplayFeed')
			for (var i = 0; i < display_feeds.length; i++){
				display_feeds[i].addEventListener('click', displayFeed)
			}
		},
		error: function(jqXHR, textStatus, errorThrown){
			var errorMsg = document.getElementById('feedurl-error')
			errorMsg.innerText = jqXHR.responseJSON.common
		}
	})
}

function deleteFeed(){
	var feed_id = this.dataset.feedId
	var container = this.parentElement.parentElement
	$.ajax({
		type: "POST",
		url: "delete-feed/",
		data: {
			'id': feed_id,
		},
		headers: {'X-CSRFToken': csrftoken},
		mode: 'same-origin', // Do not send CSRF token to another domain.
		success: function(result) {
			container.remove()
		},
		error: function(jqXHR, textStatus, errorThrown){
		}
	})
}

function loadFeeds(data){
	$.ajax({
		type: "POST",
		url: "load-feeds/",
		data: {
		},
		headers: {'X-CSRFToken': csrftoken},
		mode: 'same-origin', // Do not send CSRF token to another domain.
		success: function(result) {
			var feeds = document.getElementById('rss_feeds')
			feeds.insertAdjacentHTML('beforeend', result)
			// Обновляем стили
			if (IS_MOBILE){
				var rss_aggregator_groups = document.getElementById('rss_aggregator_groups')
				rss_aggregator_groups.classList.remove('el-40-half')
				var icons = rss_aggregator_groups.getElementsByTagName('img')
				for (var i = 0; i < icons.length; i++){
					icons[i].classList.add('svg_icon_inverted')
				}
			}
			// Добавляем хендлеры для удаления фида и его показа
			var delete_feeds = document.getElementsByClassName('onDeleteFeed')
			for (var i = 0; i < delete_feeds.length; i++){
				delete_feeds[i].addEventListener('click', deleteFeed)
			}
			var display_feeds = document.getElementsByClassName('onDisplayFeed')
			for (var i = 0; i < display_feeds.length; i++){
				display_feeds[i].addEventListener('click', displayFeed)
			}

		},
		error: function(jqXHR, textStatus, errorThrown){
		}
	})	
}

function clearMessageOnAddFeed(){
	document.getElementById('feedurl-error').innerText = ''
}


function onRSSAggregator(){
	$(document).ready(function() {
		$(window).keydown(function(event){
		  if(event.keyCode == 13) {
			event.preventDefault();
			return false;
		  }
		});
	});

	let add_feed_button_submit = document.getElementById('onAddFeedSubmit')
	add_feed_button_submit.addEventListener('click', submitFeed)
	let clear_feed_msg = document.getElementById('onAddFeed')
	clear_feed_msg .addEventListener('click', clearMessageOnAddFeed)


	if (IS_MOBILE){
		var feeds_group = document.getElementById('feeds_group')	
		feeds_group.classList.remove('active_group_button')
		var rss_aggregator_main = document.getElementById('rss_aggregator_main')
		rss_aggregator_main.classList.replace('row', 'column')
		var rss_aggregator_groups = document.getElementById('rss_aggregator_groups')
		rss_aggregator_groups.classList.remove('el-40-half')
		var icons = rss_aggregator_groups.getElementsByTagName('img')
		for (var i = 0; i < icons.length; i++){
			icons[i].classList.add('svg_icon_inverted')
		}
		var h_line = rss_aggregator_groups.getElementsByTagName('hr')
		h_line[0].style.borderTopColor = "white"
		var rss_aggregator_groups_container = document.getElementById('rss_aggregator_mobile_groups_container')
		rss_aggregator_groups_container.insertAdjacentElement('afterbegin', rss_aggregator_groups)
	}

	loadFeeds()

}

if (document.readyState === "loading") {
  // Loading hasn't finished yet
  document.addEventListener("DOMContentLoaded", onRSSAggregator);
} else {
	onRSSAggregator()
}
