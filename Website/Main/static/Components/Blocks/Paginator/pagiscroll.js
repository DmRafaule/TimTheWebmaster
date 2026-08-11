import {update_paginator} from './paginator.js';
import {WaitSetinelToInteract} from  './infinity_scroll.js'
let num_pages = parseInt(document.querySelector('#meta-data').dataset.numpages)
let current_page = parseInt(document.querySelector('#meta-data').dataset.currentpage)
let url = document.querySelector('#meta-data').dataset.url

function onSort(){
	var metaContainer = document.querySelector("#meta-data")
	var isRecent = metaContainer.dataset.sort
	if (isRecent == 'true')
		isRecent = false
	else
		isRecent = true
	metaContainer.dataset.sort = isRecent
	LoadPosts(1, true)
}

// Get all data in filters, if they are available
function updateFilters(){
	var metaContainer = document.querySelector("#meta-data")
	var isRecent = metaContainer.dataset.sort
	var tags = JSON.parse(metaContainer.dataset.tags)

	return [isRecent, tags]
}
// To send over GET request lists, like tags
function buildURLList(list, list_el_name){
	var url_list = ''
	list.forEach( (el) => {
		url_list += `&${list_el_name}=${el}`
	})
	return url_list
}
// Return a UTR with all possible parameters
function buildURL(page, tags, is_recent){
	var new_url = `${url}?page=${page}${buildURLList(tags, 'tag')}${buildURLList([is_recent],'is_recent')}`
	return new_url
}
// Update state of URL bar, will whow only page number and list of tags
function updateState(page, tags = [], is_recent){
	var new_url = `${url}?page=${page}${buildURLList(tags, 'tag')}${buildURLList([is_recent],'is_recent')}`
	history.replaceState(null, '', new_url)
}

export function LoadPosts(page, isUpdate=false){
	var progressbar = document.querySelector('#progressbar')
	progressbar.style.display = 'block'
	const [isRecent, tags] = updateFilters()
	const URL = buildURL(page, tags, isRecent)
	const form_data = new FormData()
	form_data.append('page', page)
	form_data.append('tag', JSON.stringify(tags))
	form_data.append('is_recent', isRecent)
    form_data.append('csrfmiddlewaretoken', csrftoken)
	window.contextLoader.startLoad('pagiscroll')
	fetch(URL, {
		method: 'POST',
		body: form_data,
		headers: {
			'mode': 'same-origin'
		}
	}).then( response => {
		if (response.ok){// если HTTP-статус в диапазоне 200-299
			window.contextLoader.stopLoad('pagiscroll')
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
				updateState(page, tags, isRecent)
			})
		}else{ // если HTTP-статус в диапазоне 300 - 599
			window.contextLoader.stopLoad('pagiscroll')
			window.toaster.notify(gettext(`Не смог получить страницу`), 'error')
			update_paginator(0, page)
			response.text().then(text =>{
				var page_container = document.querySelector('#page');
				page_container.innerHTML = ''
				page_container.insertAdjacentHTML('beforeend', text)
			})
		}
	}).catch( error => {
		window.toaster.notify(gettext(`Что-то пошло не так `), 'error')
		update_paginator(0, page)
		window.contextLoader.stopLoad('pagiscroll')
	}).finally(()=>{
		progressbar.style.display = 'none'
		window.contextLoader.stopLoad('pagiscroll')
	})
}

function onInfinityLoadUpdate(event){
    var metaContainer = document.querySelector("#meta-data")
	var page = event.detail.sentinel.dataset.page
	var tags = JSON.parse(metaContainer.dataset.tags)
	var isRecent = metaContainer.dataset.sort
	update_paginator(num_pages, page)
	updateState(page, tags, isRecent)
}

function onInfinityLoad(event){
	var page = event.detail.sentinel.dataset.page
	LoadPosts(page, false)
}

function onPaginLoad(event){
	var metaContainer = document.querySelector("#meta-data")
	var page = event.detail.button.dataset.page
	var sentinel = document.querySelector(`#scroll-sentinel-${page}`)
	var isRecent = metaContainer.dataset.sort
	var tags = JSON.parse(metaContainer.dataset.tags)
	updateState(page, tags, isRecent)
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
	document.querySelector('#onSort').addEventListener('click', (event) => {
		onSort()
	})
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