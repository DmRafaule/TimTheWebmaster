let id = 1
function MakeInitialLoad(index){
	$.ajax({
		type: "GET",
		url: "/" + language_code + "/load_case/",
		data: {
			'id': index,
		},
		mode: 'same-origin',
		success: function(result) {
			var list = []
			var prev = $('.prev_case__container');
			var curr = $('.curr_case__container');
			var next = $('.next_case__container');
			list.push(curr)
			list.push(next)
			list.push(prev)
			// Parsing result page ( it has to be splited on 4 separate parts ) 
			result.split('###Mark').forEach(function(sub_result, i){
				list[i].text('')
				list[i].append(sub_result)
			})
		},
	})
}

function NextCase(){
	MakeInitialLoad(-1)
	var left = $(".invs_case__container--left")
	var prev = $(".prev_case__container")
	var curr = $(".curr_case__container") 
	var next = $(".next_case__container") 
	var right = $(".invs_case__container--right") 

	right.removeClass('show_invs_case show_vs_case hide_invs_case hide_vs_case hide')
	next.removeClass('show_invs_case show_vs_case hide_invs_case hide_vs_case hide')
	curr.removeClass('show_invs_case show_vs_case hide_invs_case hide_vs_case hide')
	prev.removeClass('show_invs_case show_vs_case hide_invs_case hide_vs_case hide')
	left.removeClass('show_invs_case show_vs_case hide_invs_case hide_vs_case hide')

	left.addClass('show_invs_case')
	prev.addClass('show_vs_case')
	curr.addClass('hide_invs_case')
	next.addClass('hide_vs_case')
	right.insertBefore(left)

	left.removeClass('invs_case__container--left')
	prev.removeClass("prev_case__container")
	curr.removeClass("curr_case__container") 
	next.removeClass("next_case__container") 
	right.removeClass("invs_case__container--right") 


	left.addClass('prev_case__container')
	prev.addClass('curr_case__container')
	curr.addClass('next_case__container')
	next.addClass('invs_case__container--right')
	right.addClass('invs_case__container--left')
}

function PrevCase(){
	MakeInitialLoad(1)
	var left = $(".invs_case__container--left")
	var prev = $(".prev_case__container")
	var curr = $(".curr_case__container") 
	var next = $(".next_case__container") 
	var right = $(".invs_case__container--right") 

	right.removeClass('show_invs_case show_vs_case hide_invs_case hide_vs_case')
	next.removeClass('show_invs_case show_vs_case hide_invs_case hide_vs_case')
	curr.removeClass('show_invs_case show_vs_case hide_invs_case hide_vs_case')
	prev.removeClass('show_invs_case show_vs_case hide_invs_case hide_vs_case')
	left.removeClass('show_invs_case show_vs_case hide_invs_case hide_vs_case')

	right.addClass('show_invs_case')
	next.addClass('show_vs_case')
	curr.addClass('hide_invs_case')
	prev.addClass('hide_vs_case')

	left.insertAfter(right)

	left.removeClass('invs_case__container--left')
	prev.removeClass("prev_case__container")
	curr.removeClass("curr_case__container") 
	next.removeClass("next_case__container") 
	right.removeClass("invs_case__container--right") 


	right.addClass('next_case__container')
	next.addClass('curr_case__container')
	curr.addClass('prev_case__container')
	prev.addClass('invs_case__container--left')
	left.addClass('invs_case__container--right')
}

$(document).ready( function(){
	MakeInitialLoad(1)
	$("#next_case").on('click', NextCase)
	$("#prev_case").on('click', PrevCase)
})
