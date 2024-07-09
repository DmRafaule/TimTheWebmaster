/* Update main tag in the way that it appears to have some 
 * padding on top. Padding on top of it is a height of header tag
 * */
function updateMain() {
	var header = document.getElementById("header")
	var main   = document.getElementById("main")
	main.style.paddingTop = header.getBoundingClientRect().height  + "px"
} 
window.addEventListener('DOMContentLoaded', updateMain)
