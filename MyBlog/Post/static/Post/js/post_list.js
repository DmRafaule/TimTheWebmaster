let num_pages = parseInt(document.querySelector('#meta-data').dataset.numpages)
let current_page = parseInt(document.querySelector('#meta-data').dataset.currentpage)
let url = document.querySelector('#meta-data').dataset.url
let gallery_intersection_options = {rootMargin: "-10% 0px -10% 0px"}

function LoadPosts(page, type, isRecent = true, mode = 'basic', tags=[], relative_this = '', week_day = '', month_day = '', month = '', year = ''){
	var progressbar = document.querySelector('#progressbar')
	progressbar.style.display = 'block'
	$.ajax({
		type: "GET",
		url: url,
		// This option enable ability to send a list parameters in URL via &var=value&var=value2 ...
		// Instead of &var[]=value&var[]=value2 ... 
		traditional: true,
		data: {
            'page': page,
            'type': type,
			'is_recent': isRecent,
			'mode': mode,
			'tag': tags,
			'relative_this': relative_this,
			'week_day': week_day,
			'month_day': month_day,
			'month': month,
			'year': year,
		},
		mode: 'same-origin', // Do not send CSRF token to another domain.
		success: function(result) {
			var page_container = document.querySelector('#page');
			// Insert 'answer' from server into site code
			page_container.insertAdjacentHTML('beforeend', result)
			// Insert animation for newly loade posts
			page_container.querySelectorAll('.post_preview').forEach( (post) => {
				num_pages = post.dataset.numpages
                if (!post.classList.contains('loader'))
					post.classList.add('loader')
            })
			update_paginator(num_pages, page)
			// Insert sentinel only if the next page is exist
			if (!((Number(page) + 1) > num_pages)){
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
			progressbar.style.display = 'none'
			UpdateState(page, 'full', isRecent, mode, tags)
		},
		error: function(jqXHR, textStatus, errorThrown){
		}
	})
}

function UpdateState(page, type, isRecent = true, mode = 'basic', tags = []){
	if (tags.length == 0)
		history.replaceState(null, '', `${url}?page=${page}&type=${type}&is_recent=${isRecent}&mode=${mode}`)
	else{
		var base_url = `${url}?page=${page}&type=${type}&is_recent=${isRecent}&mode=${mode}`
		tags.forEach( (tag) => {
			base_url += `&tag=${tag}`
		})
		history.replaceState(null, '', base_url)
	}
}

function UpdatePosts(page, type, isRecent = true, mode = 'basic', tags = [], relative_this = '', week_day = '', month_day = '', month = '', year = '' ){
	var progressbar = document.querySelector('#progressbar')
	progressbar.style.display = 'block'
	$.ajax({
		type: "GET",
		url: url,
		// This option enable ability to send a list parameters in URL via &var=value&var=value2 ...
		// Instead of &var[]=value&var[]=value2 ... 
		traditional: true,
		data: {
			'page': page,
            'type': type,
			'is_recent': isRecent,
			'mode': mode,
			'tag': tags,
			'relative_this': relative_this,
			'week_day': week_day,
			'month_day': month_day,
			'month': month,
			'year': year,
		},
		mode: 'same-origin', // Do not send CSRF token to another domain.
		success: function(result) {
			var page_container = document.querySelector('#page');
			page_container.innerHTML = ''
			page_container.insertAdjacentHTML('beforeend', result)
			// Insert animation for newly loade posts
			page_container.querySelectorAll('.post_preview').forEach( (post) => {
				num_pages = post.dataset.numpages
                if (!post.classList.contains('loader'))
					post.classList.add('loader')
            })
			update_paginator(num_pages, page)
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
			progressbar.style.display = 'none'
			UpdateState(page, 'full', isRecent, mode, tags)
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
	var tagButton = document.querySelector("#onTags")
	var tags = JSON.parse(tagButton.dataset.tags)
	var this_time = document.querySelector('input[name="thisTime"]:checked');
	if (!this_time)
		this_time = ''
	else
		this_time = this_time.value
	var week_day = []
	document.querySelectorAll('.week_day.selected_order').forEach((el)=>{
		week_day.push(el.dataset.time)
	})
	var month_day = []
	document.querySelectorAll('.month_day.selected_order').forEach((el)=>{
		month_day.push(el.dataset.time)
	})
	var month = []
	document.querySelectorAll('.month.selected_order').forEach((el)=>{
		month.push(el.dataset.time)
	})
	var year = []
	document.querySelectorAll('.year.selected_order').forEach((el)=>{
		year.push(el.dataset.time)
	})
	UpdatePosts(1, 'part', isRecent, mode, tags, this_time, week_day, month_day, month, year)
}

function onView(mode, forWho = ''){
	var sortButton = document.querySelector("#onSort")
	var isRecent = sortButton.dataset.sort
	var viewsContainer = document.querySelector("#toViews")
	viewsContainer.dataset.view = mode
	var tagButton = document.querySelector("#onTags")
	var tags = JSON.parse(tagButton.dataset.tags)
	var this_time = document.querySelector('input[name="thisTime"]:checked');
	if (!this_time)
		this_time = ''
	else
		this_time = this_time.value
	var week_day = []
	document.querySelectorAll('.week_day.selected_order').forEach((el)=>{
		week_day.push(el.dataset.time)
	})
	var month_day = []
	document.querySelectorAll('.month_day.selected_order').forEach((el)=>{
		month_day.push(el.dataset.time)
	})
	var month = []
	document.querySelectorAll('.month.selected_order').forEach((el)=>{
		month.push(el.dataset.time)
	})
	var year = []
	document.querySelectorAll('.year.selected_order').forEach((el)=>{
		year.push(el.dataset.time)
	})
	UpdatePosts(1, 'part', isRecent, mode, tags, this_time, week_day, month_day, month, year)
}

function onOrderTime(selected_order_btns, this_time){
	var sortButton = document.querySelector("#onSort")
	var isRecent = sortButton.dataset.sort
	var viewsContainer = document.querySelector("#toViews")
	var mode = viewsContainer.dataset.view
	var tagButton = document.querySelector("#onTags")
	var tags = JSON.parse(tagButton.dataset.tags)
	var week_day = []
	document.querySelectorAll('.week_day.selected_order').forEach((el)=>{
		week_day.push(el.dataset.time)
	})
	var month_day = []
	document.querySelectorAll('.month_day.selected_order').forEach((el)=>{
		month_day.push(el.dataset.time)
	})
	var month = []
	document.querySelectorAll('.month.selected_order').forEach((el)=>{
		month.push(el.dataset.time)
	})
	var year = []
	document.querySelectorAll('.year.selected_order').forEach((el)=>{
		year.push(el.dataset.time)
	})
	UpdatePosts(1, 'part', isRecent, mode, tags, this_time.value, week_day, month_day, month, year)
}

function onInfinityLoadUpdate(event){
    var viewsContainer = document.querySelector("#toViews")
	var mode = viewsContainer.dataset.view
	var isRecent = document.querySelector("#onSort").dataset.sort
	var page = event.detail.sentinel.dataset.page
	var tagButton = document.querySelector("#onTags")
	var tags = JSON.parse(tagButton.dataset.tags)
	update_paginator(num_pages, page)
	UpdateState(page, 'full', isRecent, mode, tags)
}

function onInfinityLoad(event){
    var viewsContainer = document.querySelector("#toViews")
	var mode = viewsContainer.dataset.view
	var isRecent = document.querySelector("#onSort").dataset.sort
	var page = event.detail.sentinel.dataset.page
	var tagButton = document.querySelector("#onTags")
	var tags = JSON.parse(tagButton.dataset.tags)
	var this_time = document.querySelector('input[name="thisTime"]:checked');
	if (!this_time)
		this_time = ''
	else
	this_time = this_time.value
	var week_day = []
	document.querySelectorAll('.week_day.selected_order').forEach((el)=>{
		week_day.push(el.dataset.time)
	})
	var month_day = []
	document.querySelectorAll('.month_day.selected_order').forEach((el)=>{
		month_day.push(el.dataset.time)
	})
	var month = []
	document.querySelectorAll('.month.selected_order').forEach((el)=>{
		month.push(el.dataset.time)
	})
	var year = []
	document.querySelectorAll('.year.selected_order').forEach((el)=>{
		year.push(el.dataset.time)
	})
	LoadPosts(page, 'part', isRecent, mode, tags, this_time, week_day, month_day, month, year)
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
	var tagButton = document.querySelector("#onTags")
	var tags = JSON.parse(tagButton.dataset.tags)
	UpdateState(page, 'full', isRecent, mode, tags)
}

function onReady(){

	// Ordering and filtering by date
	var order_btns = document.querySelectorAll('.week_day,.month_day,.month,.year')
	order_btns.forEach( btn => {
		btn.addEventListener('click', (event) => {
			var this_time = document.querySelector('input[name="thisTime"]:checked');
			btn.classList.toggle('selected_order')
			selected_order_btns = document.querySelectorAll('.selected_order')
			onOrderTime(selected_order_btns, this_time)
		})
	})
	var this_time_btns = document.querySelectorAll('input[name="thisTime"]')
	this_time_btns.forEach( btn => {
		btn.addEventListener('click', (event) => {
			var order_btns = document.querySelectorAll('.week_day,.month_day,.month,.year')
			order_btns.forEach( btn => {
				btn.classList.remove('selected_order')
			})
			selected_order_btns = document.querySelectorAll('.selected_order')
			onOrderTime(selected_order_btns, btn)
		})
	})

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