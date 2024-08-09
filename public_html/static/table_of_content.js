function changeCursorOnTableEl(curr_index){
	const els = $('.table_of_content_list>li')
	els.each( function(index){
		if (curr_index == index){
			$(this).prepend('<div id="table_od_content-current-arrow">➥</div>')
		}
		else
			$(this).find('#table_od_content-current-arrow').remove()
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
				ChangeATileOfTableElement(element)
				changeCursorOnTableEl(element_indx)
				document.getElementById('current_header').dataset.current = String(element_indx)
			}
		}
	}, options);
	header_observer.observe(element);
}

function ChangeATileOfTableElement(element){
	var max_size = 50
	if (document.getElementById('table_of_content-text').innerText.length > max_size)
		document.getElementById('table_of_content-text').innerText = $(element).text().substring(0,max_size) + '...'
	else
		document.getElementById('table_of_content-text').innerText = $(element).text().substring(0,max_size)
	let tag_name  = $(element).prop("tagName").toLowerCase()
	document.getElementById('table_of_content-sign').innerText = tag_name
}

function CreateNavigationBar(){
	var toc_minified = $('#table_of_content-minified')
	var limiter_left = $('.limiter').offset().left
	toc_minified.css({left: limiter_left, transform: `translateY(${header_height})`})
}

function RemoveNavigationBar(){
	var toc_minified = $('#table_of_content-minified')
	toc_minified.css({transform: `translateY(0)`})

}

function WaitToBeHidden(element){
	var options = {
		threshold: 0,
	  };
	var table_of_content_observer = new IntersectionObserver((entries, observer) => {
		// Loop through the entries
		for (const entry of entries) {
			// Check if the entry is leaved the viewport
			if (!entry.isIntersecting) {
				if (!$('#table_of_content_groups_container').hasClass('active_nav'))
					CreateNavigationBar()
			}
			else{
				RemoveNavigationBar()
			}
		}
	}, options);
	table_of_content_observer.observe(element);
}

$(document).ready( function(){
	var headers = $('h2, h3, h4, h5, h6');
	var titles = []

	headers.each( function(index){
		let text = $(this).text()
		let ref  = '#ref-'+text
		// Save only alphnumeric chracters and # everything else replace with -
		ref = ref.replace(/[^#a-zA-Z0-9а-яА-Я]/g, '-').toLowerCase();
		let tag_name  = this.nodeName.toLowerCase()
		let padding = "padder-5"
		if( tag_name  == 'h2')
			padding = "padder-5"
		else if (tag_name  == 'h3')
			padding = "padder-10"
		else if (tag_name  == 'h4')
			padding = "padder-15"
		else if (tag_name  == 'h5')
			padding = "padder-20"
		else if (tag_name  == 'h6')
			padding = "padder-25"
		titles.push({"text":text, "ref": ref, "tag_name": tag_name, "padding": padding})
		$(this).attr('id', ref.replace("#","") )
	});

	$.ajax({
		type: "POST",
		url: "/" + language_code + "/load_table_of_content/",
		data: {
			'titles': JSON.stringify(titles)
		},
		headers: {'X-CSRFToken': csrftoken},
		mode: 'same-origin', // Do not send CSRF token to another domain.
		success: function(result) {
			var title = $('h1');
			$('<hr>').insertAfter(title)
			var side_menu_button_container = $("#table_of_content_groups_container")
			side_menu_button_container.css({color: 'white'})
			side_menu_button_container.append(result)
			var side_menu_button = $("#table_of_content_group")
			side_menu_button.removeClass('active_more_home_button')
			side_menu_button.on('click', function(ev){
				if (!side_menu_button_container.hasClass('padder')){
					side_menu_button_container.addClass('padder')
					RemoveNavigationBar()
				}
				else{
					side_menu_button_container.removeClass('padder')
					CreateNavigationBar()
				}
			})

			
			var anch_links = document.querySelectorAll('.table_of_content_text')
			anch_links.forEach( (link) => {
				link.addEventListener('click',function(){
					var element_indx = 0
					var target = $(link).attr('href')
					headers.each( function(index){
						if ('#' + $(headers[index]).attr('id') == target){
							element_indx = index
						}
					})
					ChangeATileOfTableElement(target)
					changeCursorOnTableEl(element_indx)
					document.getElementById('current_header').dataset.current = String(element_indx)
					var offset = 200
					jumpTo(target, offset)
				}) 
			})
			// Set up observer for h1-h6 headers
			WaitToBeHidden($('.title').get(0))
			headers.each( function(index){
				CreateHeaderInterObserver(headers, headers[index], index)
			})
			document.getElementById('table_of_content-up').addEventListener('click', function(ev){
				var element_indx = Number(document.getElementById('current_header').dataset.current)
				element_indx -= 1
				if (!(element_indx < 0)){
					var target = '#' + $(headers[element_indx]).attr('id')
					ChangeATileOfTableElement(headers[element_indx])
					changeCursorOnTableEl(element_indx)
					document.getElementById('current_header').dataset.current = String(element_indx)
					var offset = 300
					jumpTo(target, offset)
				}
			})
			document.getElementById('table_of_content-down').addEventListener('click', function(ev){
				var element_indx = Number(document.getElementById('current_header').dataset.current)
				element_indx += 1
				if (element_indx < headers.length){
					var target = '#' + $(headers[element_indx]).attr('id')
					ChangeATileOfTableElement(headers[element_indx])
					changeCursorOnTableEl(element_indx)
					document.getElementById('current_header').dataset.current = String(element_indx)
					var offset = 300
					jumpTo(target, offset)
				}
			})
		},
	})
})


function jumpTo( target, offset ){
	var offsetObj = $(target).offset()
	offsetObj.top -= offset
	window.scrollTo(offsetObj)
}