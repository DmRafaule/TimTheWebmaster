function changeCursorOnTableEl(curr_index){
	const els = document.querySelectorAll('#table_of_content_list>li')
	els.forEach((el, index) => {
		if (curr_index == index){
			el.classList.add('table_of_content_element_selected')
		}
		else
			el.classList.remove('table_of_content_element_selected')
	})
}

function CreateHeaderInterObserver(elements, element, element_indx){
	var options = {
		rootMargin: "-50% 0px -50% 0px",
		threshold: 0,
	  };
	var header_observer = new IntersectionObserver((entries, observer) => {
		// Loop through the entries
		for (const entry of entries) {
			// Check if the entry is leaved the viewport
			if (entry.isIntersecting) {
				changeCursorOnTableEl(element_indx)
				document.getElementById('current_header').dataset.current = String(element_indx)
				history.pushState(null, '',`#${element.getAttribute('id')}`)
			}
		}
	}, options);
	header_observer.observe(element);
}


export function initTableOfContent(){
	var headers = document.querySelector('#content_post_article').querySelectorAll('h2,h3,h4,h5,h6')
	var titles = []
	headers.forEach( (header)=>{
		let text = header.textContent
		let ref  = '#ref-' + text
		// Save only alphnumeric chracters and # everything else replace with -
		ref = ref.replace(/[^#a-zA-Z0-9а-яА-Я]/g, '-').toLowerCase();
		let tag_name  = header.nodeName.toLowerCase()
		let padding = "pl-1"
		if( tag_name  == 'h2')
			padding = "pl-1"
		else if (tag_name  == 'h3')
			padding = "pl-3"
		else if (tag_name  == 'h4')
			padding = "pl-5"
		else if (tag_name  == 'h5')
			padding = "pl-7"
		else if (tag_name  == 'h6')
			padding = "pl-9"
		titles.push({"text":text, "ref": ref, "tag_name": tag_name, "padding": padding})
		header.setAttribute('id', ref.replace("#","") )
	});
	
	var headers_container_to_put_in = document.querySelector('#table_of_content_list')
	var header_dom_element = document.querySelector('#table_of_content_element')
	titles.forEach( (title) => {
		var element = header_dom_element.cloneNode(true)
		element.classList.add(title["padding"])
		element.classList.remove("hidden")
		element.querySelector('.table_of_content_sign').textContent = title['tag_name']
		element.querySelector('.table_of_content_text').textContent = title['text']
		element.querySelector('.table_of_content_text').setAttribute('href', title['ref'])
		headers_container_to_put_in.insertAdjacentElement('beforeend', element)
	})
	headers_container_to_put_in.querySelectorAll('li').forEach( (list_element) => {
		list_element.addEventListener('click', (ev)=>{
			ev.preventDefault();
			var element_indx = 0
			var target = list_element.querySelector('.table_of_content_text').getAttribute('href')
			headers.forEach( (header, index) => {
				if ('#' + header.getAttribute('id') == target){
					element_indx = index
				}
			})
			changeCursorOnTableEl(element_indx)
			document.getElementById('current_header').dataset.current = String(element_indx)
			var to = document.querySelector(target)
			jumpTo(to, target)
		})
	})
	headers.forEach( (header, index) => {
		CreateHeaderInterObserver(headers, header, index)
	})
	headers.forEach( (header, index) => {
		header.classList.add('ref_hidden-int')
		var ref = header.getAttribute('id')
		var text = header.textContent
		header.textContent = ""
		var link = document.createElement('a')
		link.textContent = text
		link.setAttribute('href', `#${ref}`)
		header.insertAdjacentElement('afterbegin', link)
		header.addEventListener('click', (ev)=>{
			ev.preventDefault();
			changeCursorOnTableEl(index)
			document.getElementById('current_header').dataset.current = String(index)
			var to = document.querySelector('#'+ref)
			jumpTo(to, '#'+ref)
		})
	})
}

function jumpTo( target, ref ){
	// Предотвращаем скачок к цели
	// Меняем состояние
	history.pushState(null, '',`${ref}`)
	// Прыгаем к цели
	target.scrollIntoView({behavior: "smooth", block: "center", inline: "center"});
}