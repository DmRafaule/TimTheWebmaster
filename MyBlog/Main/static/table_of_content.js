function changeCursorOnTableEl(curr_index){
	const els = $('.table_of_content_list>li')
	els.each( function(index){
		if (curr_index == index){
			$(this).css('color', 'orange')
		}
		else
			$(this).css('color', 'white')
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
			}
		}
	}, options);
	header_observer.observe(element);
}

document.addEventListener('clickOutsideHat', (ev)=>{
	var side_menu_button_container = $("#table_of_content_groups_container")
	if (!side_menu_button_container.hasClass('padder') && side_menu_button_container.hasClass('active_nav')){
		side_menu_button_container.addClass('padder')
	}
	else{
		side_menu_button_container.removeClass('padder')
	}
})


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
			var side_menu_button_container = $("#table_of_content_groups_container")
			side_menu_button_container.css({color: 'white'})
			side_menu_button_container.append(result)
			var side_menu_button = $("#table_of_content_group")
			side_menu_button.removeClass('active_more_home_button')
			side_menu_button.on('click', function(ev){
				if (!side_menu_button_container.hasClass('padder')){
					side_menu_button_container.addClass('padder')
				}
				else{
					side_menu_button_container.removeClass('padder')
				}
			})

			
			var anch_links = document.querySelectorAll('.table_of_content_text')
			anch_links.forEach( (link) => {
				link.addEventListener('click',function(ev){
					ev.preventDefault();
					var element_indx = 0
					var target = $(link).attr('href')
					headers.each( function(index){
						if ('#' + $(headers[index]).attr('id') == target){
							element_indx = index
						}
					})
					changeCursorOnTableEl(element_indx)
					document.getElementById('current_header').dataset.current = String(element_indx)
					var to = document.querySelector(target)
					jumpTo(to, target)
				}) 
			})
			// Set up observer for h1-h6 headers
			headers.each( function(index){
				CreateHeaderInterObserver(headers, headers[index], index)
			})
			document.getElementById('table_of_content-up').addEventListener('click', function(ev){
				ev.preventDefault();
				var element_indx = Number(document.getElementById('current_header').dataset.current)
				element_indx -= 1
				if (!(element_indx < 0)){
					var target = '#' + $(headers[element_indx]).attr('id')
					changeCursorOnTableEl(element_indx)
					document.getElementById('current_header').dataset.current = String(element_indx)
					var to = document.querySelector(target)
					jumpTo(to, target)
				}
			})
			document.getElementById('table_of_content-down').addEventListener('click', function(ev){
				ev.preventDefault();
				var element_indx = Number(document.getElementById('current_header').dataset.current)
				element_indx += 1
				if (element_indx < headers.length){
					var target = '#' + $(headers[element_indx]).attr('id')
					changeCursorOnTableEl(element_indx)
					document.getElementById('current_header').dataset.current = String(element_indx)
					var to = document.querySelector(target)
					jumpTo(to, target)
				}
			})
		},
	})
})


function jumpTo( target, ref ){
	// Предотвращаем скачок к цели
	// Меняем состояние
	history.pushState(null, '',`${ref}`)
	// Прыгаем к цели
	target.scrollIntoView({behavior: "smooth", block: "center", inline: "center"});
}