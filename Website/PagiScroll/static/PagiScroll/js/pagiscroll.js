let num_pages = parseInt(document.querySelector('#meta-data').dataset.numpages)
let current_page = parseInt(document.querySelector('#meta-data').dataset.currentpage)
let url = document.querySelector('#meta-data').dataset.url

// Get all data in filters, if they are available
function updateFilters(){
	var metaContainer = document.querySelector("#meta-data")
	var mode = metaContainer.dataset.view
	var isRecent = metaContainer.dataset.sort
	var tags = JSON.parse(metaContainer.dataset.tags)
	var this_time = ''
	var is_alphabetic = 'ignored'
	var week_day = [], month_day = [], month =[], year = [], letters = [], platforms_id = []

	if (typeof update_time_filters !== "undefined") { 
		[this_time, week_day, month_day, month, year] = update_time_filters()
	}
	if (typeof update_alphabet_filters !== "undefined") { 
		letters = update_alphabet_filters()
	}
	if (typeof update_alphabet_filters_sort !== "undefined") { 
		is_alphabetic = update_alphabet_filters_sort()
	}
	if (typeof update_platform_filters !== "undefined") { 
		platforms_id = update_platform_filters()
	}

	return [mode, isRecent, tags, this_time, week_day, month_day, month, year, letters, is_alphabetic, platforms_id]
}
// To send over GET request lists, like tags
function buildURLList(list, list_el_name){
	url_list = ''
	list.forEach( (el) => {
		url_list += `&${list_el_name}=${el}`
	})
	return url_list
}
// Return a UTR with all possible parameters
function buildURL(page, tags){
	var new_url = `${url}?page=${page}${buildURLList(tags, 'tag')}`
	return new_url
}
// Update state of URL bar, will whow only page number and list of tags
function updateState(page, tags = []){
	var new_url = `${url}?page=${page}${buildURLList(tags, 'tag')}`
	history.replaceState(null, '', new_url)
}

function LoadPosts(page, isUpdate=false){
	var progressbar = document.querySelector('#progressbar')
	progressbar.style.display = 'block'
	const [mode, isRecent, tags, relative_this, week_day, month_day, month, year, letters, is_alphabetic, platforms_id] = updateFilters()
	const URL = buildURL(page, tags)
	const form_data = new FormData()
	form_data.append('page', page)
	form_data.append('tag', JSON.stringify(tags))
	form_data.append('mode', mode)
	form_data.append('is_recent', isRecent)
	form_data.append('relative_this', relative_this)
	form_data.append('week_day', JSON.stringify(week_day))
	form_data.append('month_day', JSON.stringify(month_day))
	form_data.append('month', JSON.stringify(month))
	form_data.append('year', JSON.stringify(year))
	form_data.append('letter', JSON.stringify(letters))
	form_data.append('is_alphabetic', is_alphabetic)
	form_data.append('platform', JSON.stringify(platforms_id))
    form_data.append('csrfmiddlewaretoken', csrftoken)
	fetch(URL, {
		method: 'POST',
		body: form_data,
		headers: {
			'mode': 'same-origin'
		}
	}).then( response => {
		if (response.ok){// если HTTP-статус в диапазоне 200-299
			response.text().then(text =>{
				var page_container = document.querySelector('#page');
				if (isUpdate){
					page_container.innerHTML = ''
				}
				// Insert 'answer' from server into site code
				page_container.insertAdjacentHTML('beforeend', text)
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
				progressbar.style.display = 'none'
				updateState(page, tags)
			})
		}else{ // если HTTP-статус в диапазоне 300 - 599
			notificator.notify(gettext(`Не смог получить страницу`), 'error')
			update_paginator(0, page)
			response.text().then(text =>{
				var page_container = document.querySelector('#page');
				page_container.innerHTML = ''
				page_container.insertAdjacentHTML('beforeend', text)
			})
		}
	}).catch( error => {
		notificator.notify(gettext(`Что-то пошло не так `), 'error')
		update_paginator(0, page)
	}).finally(()=>{
		progressbar.style.display = 'none'
	})
}

function onInfinityLoadUpdate(event){
    var metaContainer = document.querySelector("#meta-data")
	var page = event.detail.sentinel.dataset.page
	var tags = JSON.parse(metaContainer.dataset.tags)
	update_paginator(num_pages, page)
	updateState(page, tags)
}

function onInfinityLoad(event){
	var page = event.detail.sentinel.dataset.page
	LoadPosts(page, false)
}

function onPaginLoad(event){
	var metaContainer = document.querySelector("#meta-data")
	var page = event.detail.button.dataset.page
	var sentinel = document.querySelector(`#scroll-sentinel-${page}`)
	var tags = JSON.parse(metaContainer.dataset.tags)
	updateState(page, tags)
	if (sentinel){
		sentinel.scrollIntoView({behavior: "smooth", block: "center", inline: "center"});
		update_paginator(num_pages, page)
	}
	else{
		document.querySelector('h1').scrollIntoView({behavior: "instant", block: "center", inline: "center"});
		LoadPosts(page, true)
	}
}

function onReady(){

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
	document.addEventListener("DOMContentLoaded", onReady);
} else {
	onReady()
}