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
		type: "GET",
		url: "/" + language_code + "/load_table_of_content/",
		data: {
			'titles': JSON.stringify(titles)
		},
		mode: 'same-origin', // Do not send CSRF token to another domain.
		success: function(result) {
			var title = $('h1');
			$(result).insertAfter(title)
			var up_button  = document.querySelectorAll('.up_button')
			up_button.forEach( (button) => {
				button.addEventListener('click',function(){
					pushUpButton(this)
				}) 
			})
			var anch_links = document.querySelectorAll('.table_of_content_text')
			anch_links.forEach( (link) => {
				link.addEventListener('click',function(){
					var target = $(link).attr('href')
					var offset = 100
					jumpTo(target, offset)
				}) 
			})

		},
	})
})


function jumpTo( target, offset ){
	var offsetObj = $(target).offset()
	offsetObj.top -= offset
	window.scrollTo(offsetObj)
}

function pushUpButton(el){
	el.classList.add('icon_button_pressed')
	el.addEventListener("animationend", (event) => {
		el.classList.remove('icon_button_pressed')
	});
}

