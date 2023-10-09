var menu_toggler = document.getElementById("menu_button") 
var body_wall = document.getElementById("main__body__wall") 
var header = document.getElementById("content_header")
var left_header_position = header.getBoundingClientRect().left + "px"
var top_header_position = 0 + "px"
// Get the offset position of the navbar
var sticky = header.offsetTop;

function updateHeaderOnScroll() {
	if (window.pageYOffset > sticky) {
		var width_header_position = body_wall.getBoundingClientRect().width + "px"
		var left_header_position = header.getBoundingClientRect().left + "px"
		header.classList.add("sticky");
		header.style.left = left_header_position
		header.style.top = top_header_position
		header.style.width = width_header_position
	} else {
		header.classList.remove("sticky");
	}
} 

function updateHeaderOnClick(){
	var width_header_position = body_wall.getBoundingClientRect().width + "px"
	header.style.width = width_header_position
}

function updateHeaderOnLoad(){
	var width_header_position = body_wall.getBoundingClientRect().width + "px"
	header.style.left = left_header_position
	header.style.top = top_header_position
	header.style.width = width_header_position
}

function updateHeaderOnResize(){
	var width_header_position = body_wall.getBoundingClientRect().width + "px"
	header.style.left = left_header_position
	header.style.top = top_header_position
	header.style.width = width_header_position
}

window.addEventListener('onresize', updateHeaderOnResize)
window.addEventListener('scroll', updateHeaderOnScroll)
window.addEventListener('onload', updateHeaderOnLoad)
menu_toggler.addEventListener('click', updateHeaderOnClick)
