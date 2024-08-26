let num_pages = parseInt(document.querySelector('#meta-data').dataset.numpages)
let current_page = parseInt(document.querySelector('#meta-data').dataset.currentpage)
let url = document.querySelector('#meta-data').dataset.url
let gallery_intersection_options = {rootMargin: "-10% 0px -10% 0px"}

function LoadPosts(page, type, isRecent = true, mode = 'basic'){
	$.ajax({
		type: "GET",
		url: url,
		data: {
            'page': page,
            'type': type,
			'is_recent': isRecent,
			'mode': mode,
		},
		mode: 'same-origin', // Do not send CSRF token to another domain.
		success: function(result) {
			var page_container = document.querySelector('#page');
			// Insert 'answer' from server into site code
			page_container.insertAdjacentHTML('beforeend', result)
			// Insert animation for newly loade posts
			page_container.querySelectorAll('.post_preview').forEach( (post) => {
                if (!post.classList.contains('loader'))
					post.classList.add('loader')
            })
			var num_pages = document.querySelector('#meta-data').dataset.numpages
			// Insert sentinel only if the next page is exist
			if (!((page + 1) > num_pages)){
				var sentinel_next = page_container.querySelector(`#scroll-sentinel-${Number(page)+1}`)
				WaitSetinelToInteract(sentinel_next)
				sentinel_next.addEventListener('onInfinityLoad', onInfinityLoad, {once: true})
				sentinel_next.addEventListener('onInfinityLoad', onInfinityLoadUpdate)
			}
			// Insert sentinel for previos page load if it is exist
			var is_exist = page_container.querySelector(`#scroll-sentinel-${Number(page)-1}`)
			if (page - 1 > 0 && !is_exist){
				var sentinel_next = page_container.querySelector(`#scroll-sentinel-${Number(page)+1}`)
				var sentinel_prev = null
				// The last sentinel is not going to exist we need to check this
				if (!sentinel_next){
					sentinel_next = page_container.querySelector(`#scroll-sentinel-${Number(page)-1}`)
					sentinel_prev = sentinel_next.cloneNode(true)
				}
				else{
					sentinel_prev = sentinel_next.cloneNode(true)
					sentinel_prev.id = `scroll-sentinel-${Number(page)-1}`
				}
				sentinel_prev.dataset.page = Number(page) - 1
				WaitSetinelToInteract(sentinel_prev, gallery_intersection_options)
				//sentinel_prev.addEventListener('onInfinityLoad', onInfinityLoad, {once: true})
				sentinel_prev.addEventListener('onInfinityLoad', onInfinityLoadUpdate)
				page_container.insertAdjacentElement('afterbegin',sentinel_prev)
			}
			UpdateState(page, 'full', isRecent, mode)
		},
		error: function(jqXHR, textStatus, errorThrown){
		}
	})
}

function UpdateState(page, type, isRecent = true, mode = 'basic'){
	history.replaceState(null, '', `${url}?page=${page}&type=${type}&is_recent=${isRecent}&mode=${mode}`)
}

function UpdatePosts(page, type, isRecent = true, mode = 'basic'){
	$.ajax({
		type: "GET",
		url: url,
		data: {
			'page': page,
            'type': type,
			'is_recent': isRecent,
			'mode': mode,
		},
		mode: 'same-origin', // Do not send CSRF token to another domain.
		success: function(result) {
			var page_container = document.querySelector('#page');
			page_container.innerHTML = ''
			page_container.insertAdjacentHTML('beforeend', result)
			// Insert animation for newly loade posts
			page_container.querySelectorAll('.post_preview').forEach( (post) => {
                if (!post.classList.contains('loader'))
					post.classList.add('loader')
            })
			var num_pages = document.querySelector('#meta-data').dataset.numpages
			// Insert sentinel only if the next page is exist
			if (!((page + 1) > num_pages)){
				var sentinel_next = page_container.querySelector(`#scroll-sentinel-${Number(page)+1}`)
				WaitSetinelToInteract(sentinel_next)
				sentinel_next.addEventListener('onInfinityLoad', onInfinityLoad, {once: true})
				sentinel_next.addEventListener('onInfinityLoad', onInfinityLoadUpdate)
			}
			// Insert sentinel for previos page load if it is exist
			var is_exist = page_container.querySelector(`#scroll-sentinel-${Number(page)-1}`)
			if (page - 1 > 0 && !is_exist){
				var sentinel_next = page_container.querySelector(`#scroll-sentinel-${Number(page)+1}`)
				var sentinel_prev = null
				// The last sentinel is not going to exist we need to check this
				if (!sentinel_next){
					sentinel_next = page_container.querySelector(`#scroll-sentinel-${Number(page)-1}`)
					sentinel_prev = sentinel_next.cloneNode(true)
				}
				else{
					sentinel_prev = sentinel_next.cloneNode(true)
					sentinel_prev.id = `scroll-sentinel-${Number(page)-1}`
				}
				sentinel_prev.dataset.page = Number(page) - 1
				WaitSetinelToInteract(sentinel_prev, gallery_intersection_options)
				//sentinel_prev.addEventListener('onInfinityLoad', onInfinityLoad, {once: true})
				sentinel_prev.addEventListener('onInfinityLoad', onInfinityLoadUpdate)
				page_container.insertAdjacentElement('afterbegin',sentinel_prev)
			}
			UpdateState(page, 'full', isRecent, mode)
		},
		error: function(jqXHR, textStatus, errorThrown){
		}
	})
}

function onSort(){
	var sortButton = document.querySelector("#onSort")
	var isRecent = sortButton.dataset.sort
	if (isRecent == 'true')
		isRecent = false
	else
		isRecent = true
	sortButton.dataset.sort = isRecent
	var viewsContainer = document.querySelector("#toViews")
	var mode = viewsContainer.dataset.view
	UpdatePosts(1, 'part', isRecent, mode)
}

function onView(mode, forWho = ''){
	var sortButton = document.querySelector("#onSort")
	var isRecent = sortButton.dataset.sort
	var viewsContainer = document.querySelector("#toViews")
	viewsContainer.dataset.view = mode
	UpdatePosts(1, 'part', isRecent, mode)
}

function onInfinityLoadUpdate(event){
    var viewsContainer = document.querySelector("#toViews")
	var mode = viewsContainer.dataset.view
	var isRecent = document.querySelector("#onSort").dataset.sort
	var page = event.detail.sentinel.dataset.page
	update_paginator(num_pages, page)
	UpdateState(page, 'full', isRecent, mode)
}

function onInfinityLoad(event){
    var viewsContainer = document.querySelector("#toViews")
	var mode = viewsContainer.dataset.view
	var isRecent = document.querySelector("#onSort").dataset.sort
	var page = event.detail.sentinel.dataset.page
	LoadPosts(page, 'part', isRecent, mode)
}

function onPaginLoad(event){
	var viewsContainer = document.querySelector("#toViews")
	var mode = viewsContainer.dataset.view
	var isRecent = document.querySelector("#onSort").dataset.sort
	var page = event.detail.button.dataset.page
	var sentinel = document.querySelector(`#scroll-sentinel-${page}`)
	if (sentinel){
		sentinel.scrollIntoView({behavior: "smooth", block: "center", inline: "center"});
		update_paginator(num_pages, page)
	}
	UpdateState(page, 'full', isRecent, mode)
}

function onReady(){
	document.addEventListener('onSort', (event) => {
		onSort()
		event.detail.button.classList.toggle('rotate_X')
	})
	document.addEventListener('onBasicView', (event) =>{
		onView('basic')
		var container = document.querySelector('#toViews')
		container.querySelectorAll('.filter_button').forEach((btn) => {
			btn.classList.remove("selected_view")
		})
		event.detail.button.classList.toggle("selected_view")
	})
	document.addEventListener('onSimpleView', (event) =>{
		onView('simple')
		var container = document.querySelector('#toViews')
		container.querySelectorAll('.filter_button').forEach((btn) => {
			btn.classList.remove("selected_view")
		})
		event.detail.button.classList.toggle("selected_view")
	})
	document.addEventListener('onNotExtendedView', (event) =>{
		var container = document.querySelector('#toViews')
		var forWho = container.dataset.who
		onView('basic', forWho)
		container.querySelectorAll('.filter_button').forEach((btn) => {
			btn.classList.remove("selected_view")
		})
		event.detail.button.classList.toggle("selected_view")
	})
	document.addEventListener('onExtendedView', (event) =>{
		var container = document.querySelector('#toViews')
		var forWho = container.dataset.who
		onView('extended', forWho)
		var container = document.querySelector('#toViews')
		container.querySelectorAll('.filter_button').forEach((btn) => {
			btn.classList.remove("selected_view")
		})
		event.detail.button.classList.toggle("selected_view")
	})
	document.addEventListener('onListView', (event) =>{
		var container = document.querySelector('#toViews')
		var forWho = container.dataset.who
		onView('list', forWho)
		var container = document.querySelector('#toViews')
		container.querySelectorAll('.filter_button').forEach((btn) => {
			btn.classList.remove("selected_view")
		})
		event.detail.button.classList.toggle("selected_view")
	})
	document.addEventListener('onGridView', (event) =>{
		var container = document.querySelector('#toViews')
		var forWho = container.dataset.who
		onView('grid', forWho)
		var container = document.querySelector('#toViews')
		container.querySelectorAll('.filter_button').forEach((btn) => {
			btn.classList.remove("selected_view")
		})
		event.detail.button.classList.toggle("selected_view")
	})

    var page = document.querySelector('#page')
	document.addEventListener('onPaginButtonLoad', onPaginLoad)
	page.querySelectorAll(`.scroll-sentinel`).forEach( (sentinel) => {
        if (sentinel.dataset.page != 1)
		    sentinel.addEventListener('onInfinityLoad', onInfinityLoad, {once: true})
		sentinel.addEventListener('onInfinityLoad', onInfinityLoadUpdate)
		sentinel.style.top = page.getBoundingClientRect().height + 'px'
        if (sentinel.dataset.page != 1)
		    page.insertAdjacentElement('beforeend',sentinel)
	})
	update_paginator(num_pages, current_page)
}

if (document.readyState === "loading") {
	// Loading hasn't finished yet
	document.addEventListener("DOMContentLoaded", onReady);
} else {
	onReady()
}