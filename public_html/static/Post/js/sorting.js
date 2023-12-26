function UpdatePosts(isRecent = true, mode = 'basic', forWho = ''){
	var postNum = $(".post_preview").length
	$.ajax({
		type: "GET",
		url: "load_post_preview/",
		data: {
			'number': postNum,
			'offset': 0,
			'category': category_name,
			'is_recent': isRecent,
			'mode': mode,
			'for_who': '',
		},
		mode: 'same-origin', // Do not send CSRF token to another domain.
		success: function(result) {
			var page = $('#page');
			page.text('')
			// Insert 'answer' from server into site code
			page.append(result)
		},
		error: function(jqXHR, textStatus, errorThrown){
		}
	})
}

function onSort(){
	var sortButton = $("#onSort")
	var viewsContainer = $("#toViews")
	var isRecent = sortButton.data('sort')
	isRecent = !isRecent
	sortButton.data('sort', isRecent)
	var mode = viewsContainer.data('view')
	var forWho = viewsContainer.data('who')
	UpdatePosts(isRecent, mode, forWho)
}

function onView(mode, forWho = ''){
	var isRecent = $("#onSort").data('sort')
	var viewsContainer = $("#toViews")
	viewsContainer.data('view', mode)
	UpdatePosts(isRecent, mode, forWho)
}

$(document).ready( function(){
	$("#onSort").on('click', function() {
		onSort()
		$(this).toggleClass('rotate_X')
	})
	$("#onBasicView").on('click', function(){
		onView('basic')
		$("#toViews").children().each( function (){
			$(this).removeClass("selected_view")
		})
		$(this).toggleClass("selected_view")
	})
	$("#onSimpleView").on('click', function(){
		onView('simple')
		$("#toViews").children().each( function (){
			$(this).removeClass("selected_view")
		})
		$(this).toggleClass("selected_view")
	})
	$("#onMinimalView").on('click', function(){
		onView('minimal')
		$("#toViews").children().each( function (){
			$(this).removeClass("selected_view")
		})
		$(this).toggleClass("selected_view")
	})
	$("#onRawView").on('click', function(){
		onView('raw')
		$("#toViews").children().each( function (){
			$(this).removeClass("selected_view")
		})
		$(this).toggleClass("selected_view")
	})
	$("#onNotExtendedView").on('click', function(){
		var forWho = $("#toViews").data('who')
		onView('basic', forWho)
		$("#toViews").children().each( function (){
			$(this).removeClass("selected_view")
		})
		$(this).toggleClass("selected_view")
	})
	$("#onExtendedView").on('click', function(){
		var forWho = $("#toViews").data('who')
		onView('extended', forWho)
		$("#toViews").children().each( function (){
			$(this).removeClass("selected_view")
		})
		$(this).toggleClass("selected_view")
	})
	$("#onListView").on('click', function(){
		var forWho = $("#toViews").data('who')
		onView('list', forWho)
		$("#toViews").children().each( function (){
			$(this).removeClass("selected_view")
		})
		$(this).toggleClass("selected_view")
	})
	$("#onGridView").on('click', function(){
		var forWho = $("#toViews").data('who')
		onView('grid', forWho)
		$("#toViews").children().each( function (){
			$(this).removeClass("selected_view")
		})
		$(this).toggleClass("selected_view")
	})

})
