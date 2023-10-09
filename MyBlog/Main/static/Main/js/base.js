let links = document.getElementsByClassName('nav_ref')
let nav = document.getElementById("main__body__nav")
let wall = document.getElementById("main__body__wall")
let lang_switcher = document.getElementById("lang_switcher")
let lang_switcher_img = document.getElementById('lang_switcher_image')
let menu_button = document.getElementById('menu_button')
let back_button = document.getElementById('back_button')

let isHide = true
let isMobile = false


function switchLang(){
	if (lang_switcher_img.src == PATH+"Main/img/english.png")
		lang_switcher_img.src = PATH+"Main/img/russian.png"
	else
		lang_switcher_img.src = PATH+"Main/img/english.png"
}


function switchMenu(){
    if (!isHide){
        isHide = true
        nav.style.display = "none"
    }
    else{
        isHide = false
		if (isMobile){
			wall.style.display = "none"
		}
        nav.style.display = "flex"
    }
}

function hideMenu(){
    isHide = true
    nav.style.display = "none"
	wall.style.display = "flex"
}

function onResize(){
    if (window.innerWidth > 900){
        nav.style.display = "flex"
        wall.style.display = 'flex'
		back_button.style.display = 'none'
		isMobile = false
    }
    else if (window.innerWidth <= 900){
        nav.style.display = "none"
		back_button.style.display = 'flex'
		isMobile = true 
    }
}

window.addEventListener('resize', onResize)
window.addEventListener('load', onResize)
menu_button.addEventListener('click', switchMenu)
back_button.addEventListener('click', hideMenu)
lang_switcher.addEventListener("click", switchLang)
