let tabs = document.querySelectorAll(".tab_button")

function onTab(){
	/* First of all, hide all tab_elements*/
	var all_bodies = document.querySelectorAll(".tab_element")
	all_bodies.forEach((body) => {
		body.classList.remove('tab_element__active')
	})
	/* Then show only needed one*/
	var id = this.dataset.bodyid
	var body = document.getElementById("tab_body-"+id)
	body.classList.add('tab_element__active')
	/* In the end switch current selected tab*/
	var all_tab_buttons = document.querySelectorAll(".tab_button")
	all_tab_buttons.forEach((tab) => {
		tab.classList.remove('tab_active')
	})
	this.classList.add('tab_active')

}

tabs.forEach((tab) => {
	tab.addEventListener('click', onTab)
})
