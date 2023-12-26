/*Update a nav tag in the way that it is always ontop and in fixed position
 * */
let menu_button = document.getElementById('menu_button')
let header = document.getElementById("header")
let header_height = header.getBoundingClientRect().height  + "px"

function toggleMenu(){
	var nav = document.getElementById("nav")
	nav.classList.toggle("active_nav")	
	nav.style.top = header_height
}

menu_button.addEventListener('click', toggleMenu)
