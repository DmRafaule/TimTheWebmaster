let num_pages = parseInt(document.querySelector('#meta-data').dataset.numpages)
let current_page = parseInt(document.querySelector('#meta-data').dataset.currentpage)
let gallery_intersection_options = {rootMargin: "-10% 0px -10% 0px"}

function UpdateState(page, type){
	history.replaceState(null, '', `/${language_code}/gallery/?page=${page}&type=${type}`)
}

function load(page, type){
	$.ajax({
		type: "GET",
		url: `/${language_code}/gallery/`,
		data: {
			'page': page,
			'type': type
		},
		headers: {'X-CSRFToken': csrftoken},
		mode: 'same-origin', // Do not send CSRF token to another domain.
		success: function(result) {
			var masonry = document.querySelector('#masonry')
			masonry.insertAdjacentHTML('beforeend',result)
			var num_pages = document.querySelector('#meta-data').dataset.numpages
			// Insert sentinel only if the next page is exist
			if (!((page + 1) > num_pages)){
				var sentinel_next = masonry.querySelector(`#scroll-sentinel-${Number(page)+1}`)
				sentinel_next.style.top = masonry.getBoundingClientRect().height + 'px'
				WaitSetinelToInteract(sentinel_next, gallery_intersection_options)
				sentinel_next.addEventListener('onInfinityLoad', onInfinityLoad, {once: true})
				sentinel_next.addEventListener('onInfinityLoad', onInfinityLoadUpdate)
				masonry.insertAdjacentElement('beforeend',sentinel_next)
			}
			// Insert sentinel for previos page load if it is exist
			var is_exist = masonry.querySelector(`#scroll-sentinel-${Number(page)-1}`)
			if (page - 1 > 0 && !is_exist){
				var sentinel_next = masonry.querySelector(`#scroll-sentinel-${Number(page)+1}`)
				var sentinel_prev = null
				// The last sentinel is not going to exist we need to check this
				if (!sentinel_next){
					sentinel_next = masonry.querySelector(`#scroll-sentinel-${Number(page)-1}`)
					sentinel_prev = sentinel_next.cloneNode(true)
				}
				else{
					sentinel_prev = sentinel_next.cloneNode(true)
					sentinel_prev.id = `scroll-sentinel-${Number(page)-1}`
					var current_sentinel = masonry.querySelector(`#scroll-sentinel-${page}`)
					var current_sentinel_top = parseInt(current_sentinel.style.top)
					sentinel_prev.style.top = (current_sentinel_top - (parseInt(sentinel_prev.style.top) - current_sentinel_top)) + 'px'
				}
				sentinel_prev.dataset.page = Number(page) - 1
				WaitSetinelToInteract(sentinel_prev, gallery_intersection_options)
				//sentinel_prev.addEventListener('onInfinityLoad', onInfinityLoad, {once: true})
				sentinel_prev.addEventListener('onInfinityLoad', onInfinityLoadUpdate)
				masonry.insertAdjacentElement('afterbegin',sentinel_prev)
			}
			
			var columns = masonry.querySelectorAll('.masonry-col')
			if (!IS_MOBILE){
				columns.forEach((col,indx) => {
					var column_to_insert = masonry.querySelector(`#masonry-col-${indx+1}-copy`)
					if (column_to_insert){
						
						for (var i=0; i < column_to_insert.children.length; i++){
							var node = column_to_insert.children[i].cloneNode(true)
							col.insertAdjacentElement('beforeend',node)

						}
						column_to_insert.remove()
					}
				})
			}
			else{
				var col_to_insert = masonry.querySelector('#masonry-col-2')
				masonry.querySelectorAll('.masonry-item_forCopy').forEach( (item) => {
					col_to_insert.insertAdjacentElement('beforeend', item)
				})
				masonry.querySelectorAll('.masonry-col_forDelete').forEach( (item) => { item.remove()})
			}
			// Get the current url from response
			UpdateState(page, 'full')
		},
		error: function(jqXHR, textStatus, errorThrown){
		}
	})

}

function onInfinityLoadUpdate(event){
	var page = event.detail.sentinel.dataset.page
	update_paginator(num_pages, page)
	UpdateState(page, 'full')
}

function onInfinityLoad(event){
	var page = event.detail.sentinel.dataset.page
	load(page,'part')
	UpdateState(page, 'full')
}

function onPaginLoad(event){
	var page = event.detail.button.dataset.page
	var sentinel = masonry.querySelector(`#scroll-sentinel-${page}`)
	if (sentinel){
		sentinel.scrollIntoView({behavior: "smooth", block: "center", inline: "center"});
		update_paginator(num_pages, page)
	}
	UpdateState(page, 'full')
}


function onReady(){
	var masonry = document.querySelector('#masonry')
	document.addEventListener('onPaginButtonLoad', onPaginLoad)
	masonry.querySelectorAll(`.scroll-sentinel`).forEach( (sentinel) => {
		sentinel.addEventListener('onInfinityLoad', onInfinityLoad, {once: true})
		sentinel.addEventListener('onInfinityLoad', onInfinityLoadUpdate)
		sentinel.style.top = masonry.getBoundingClientRect().height + 'px'
		masonry.insertAdjacentElement('beforeend',sentinel)
	})
	update_paginator(num_pages, current_page)
}

if (document.readyState === "loading") {
	// Loading hasn't finished yet
	document.addEventListener("DOMContentLoaded", onReady);
} else {
	onReady()
}




















