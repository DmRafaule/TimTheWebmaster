let FindNextButton = null 
let FindPrevButton = null 

function findNextButtonMobile(el){
	var buttons = $('.home_buttons_mobile')
	return buttons.find('.next_post')
}
function findPrevButtonMobile(el){
	var buttons = $('.home_buttons_mobile')
	return buttons.find('.prev_post')
}
function findNextButtonDesktop(el){
	var buttons = el.next()
	return buttons.find('.next_post')
}
function findPrevButtonDesktop(el){
	var buttons = el.next()
	return buttons.find('.prev_post')
}


function loadPosts(category, forWhichPage, whereToUpload, howMuch, offset){
	$.ajax({
		type: "GET",
		url: "load_post_preview-"+category+"/",
		data: {
			'number':  howMuch,
			'offset': offset,
			'category': category,
			'is_recent': true,
			'for_who': forWhichPage,
		},
		mode: 'same-origin',
		success: function(result){
			// Проверка на то является ли запрашиваемые посты первыми
			if (offset < howMuch){
				var btn = FindPrevButton(whereToUpload)
				btn.addClass('inactive_button')
				btn[0].removeEventListener('click', loadPrevPosts)
			}
			else{
				var btn = FindPrevButton(whereToUpload)
				btn.removeClass('inactive_button')
				btn[0].addEventListener('click', loadPrevPosts, {once: true})
			}

			whereToUpload.append(result)
			// Проверка на то является ли запрашиваемые посты последними
			var lngth = parseInt(whereToUpload.find('.data-holder').data('length'))
			if (lngth > offset){
				whereToUpload.text('')
				whereToUpload.append(result)
				var post = whereToUpload.find('.home_post')
				post.addClass('loader')
				// Если посты последние, то удаляем евенты и
				// дезактивируем кнопки
				if (offset + howMuch >= lngth){
					var btn = FindNextButton(whereToUpload)
					btn.addClass('inactive_button')
					btn[0].removeEventListener('click', loadNextPosts)
				}
				else{
					var btn = FindNextButton(whereToUpload)
					btn.removeClass('inactive_button')
					btn[0].addEventListener('click', loadNextPosts, {once: true})
				}
			}
		}
	})
}

function loadPrevPosts(){
	var id = this.dataset.targetcontainer
	var page = document.getElementById(id)
	var category = page.dataset.category
	var forWho = page.dataset.forwho
	var howMuch = parseInt(page.dataset.howmuch)
	var offset = parseInt(page.dataset.offset)
	// Обновляем данные о том сколько и какие мы хотим получить данных от сервера
	offset -= howMuch
	page.dataset.offset = offset
	loadPosts(category, forWho, $(page), howMuch, offset)
}

function loadNextPosts(){
	var id = this.dataset.targetcontainer
	var page = document.getElementById(id)
	var category = page.dataset.category
	var forWho = page.dataset.forwho
	var howMuch = parseInt(page.dataset.howmuch)
	var offset = parseInt(page.dataset.offset)
	// Обновляем данные о том сколько и какие мы хотим получить данных от сервера
	offset += howMuch
	page.dataset.offset = offset
	loadPosts(category, forWho, $(page), howMuch, offset)
}

function updateButtons(whereToUpload, howMuch, offset){
	// Проверка на то является ли запрашиваемые посты первыми
	if (offset < howMuch){
		var btn = FindPrevButton(whereToUpload)
		btn.addClass('inactive_button')
		btn[0].removeEventListener('click', loadPrevPosts)
	}
	else{
		var btn = FindPrevButton(whereToUpload)
		btn.removeClass('inactive_button')
		btn[0].addEventListener('click', loadPrevPosts, {once: true})
	}

	// Проверка на то является ли запрашиваемые посты последними
	var lngth = parseInt(whereToUpload.find('.data-holder').data('length'))
	if (lngth > offset){
		var post = whereToUpload.find('.home_post')
		// Если посты последние, то удаляем евенты и
		// дезактивируем кнопки
		if (offset + howMuch >= lngth){
			var btn = FindNextButton(whereToUpload)
			btn.addClass('inactive_button')
			btn[0].removeEventListener('click', loadNextPosts)
		}
		else{
			var btn = FindNextButton(whereToUpload)
			btn.removeClass('inactive_button')
			btn[0].addEventListener('click', loadNextPosts, {once: true})
		}
	}
}


/* Наблюдатель за входами на экран, который отрабатывает только один раз*/
function onHome() {

	// Обновляем кнопки навигации по постам. Только для мобильной версии
	function WaitButtonsToUpdate(post){
		var options = {
			  threshold: 0.7,
			};
		var post_observer = new IntersectionObserver((entries, observer) => {
		  // Loop through the entries
		  for (const entry of entries) {
			// Check if the entry is intersecting the viewport
			if (entry.isIntersecting) {
				var prev_post_button = document.querySelector(".prev_post");
				prev_post_button.dataset.targetcontainer = post.id
				var next_post_button = document.querySelector(".next_post");
				next_post_button.dataset.targetcontainer = post.id
				
				// Обновляем состояния кнопок в зависимости от 
				// текущего блока на странице
				var page = document.getElementById(post.id)
				var howMuch = parseInt(page.dataset.howmuch)
				var offset = parseInt(page.dataset.offset)
				updateButtons($(page), howMuch, offset)
			}
		  }
		}, options);
		post_observer.observe(post);
	}
	
	// Обновляем кнопки навигации по постам, только единожды
	function WaitPostToUpload(post){
		var options = {
			  threshold: 0,
			};
		var post_observer = new IntersectionObserver((entries, observer) => {
		  for (const entry of entries) {
			if (entry.isIntersecting) {
				var id = post.id
				var page = document.getElementById(id)
				var category = post.dataset.category
				var forWhichPage = post.dataset.forwho
				var howMuch = parseInt(post.dataset.howmuch)
				var offset = parseInt(post.dataset.offset)
				loadPosts(category,forWhichPage,$(page), howMuch, offset)
				post_observer.disconnect()
			}
		  }
		}, options);
		post_observer.observe(post);
	}

	const posts = document.querySelectorAll(".toLoad");
	posts.forEach( (post) => {
		WaitPostToUpload(post)
		if (IS_MOBILE){
			WaitButtonsToUpdate(post)
		}
	})

	// Кнопки загрузки постов для мобилок 
	if (IS_MOBILE){
		FindNextButton = findNextButtonMobile
		FindPrevButton = findPrevButtonMobile
		// Удалим все кроме первой пары
		const post_buttons = document.querySelectorAll(".home_buttons");
		for (var i = 1; i < post_buttons.length; i++){
			post_buttons[i].remove()
		}
		const post_button = post_buttons[0]
		// Перемещаем данную пару на низ и меняем стили
		var position_to_move = document.querySelector('.home_title')
		position_to_move.insertAdjacentElement('afterend', post_button)
		post_button.classList.add('home_buttons_mobile')
		// Меняем стили для остальной страницы
		var titles = document.querySelectorAll('h2')
		titles.forEach( (title) => {
			title.classList.remove('in_middle-self')
		})
	}
	// Кнопки загрузки для десктопа
	else{
		FindNextButton = findNextButtonDesktop
		FindPrevButton = findPrevButtonDesktop
		const prev_post_buttons = document.querySelectorAll(".prev_post");
		prev_post_buttons.forEach( (btn) => {
			btn.addEventListener('click', loadPrevPosts)
		})
		const next_post_buttons = document.querySelectorAll(".next_post");
		next_post_buttons.forEach( (btn) => {
			btn.addEventListener('click', loadNextPosts)
		})
	}

}

if (document.readyState === "loading") {
  // Loading hasn't finished yet
  document.addEventListener("DOMContentLoaded", onHome);
} else {
	onHome()
}
