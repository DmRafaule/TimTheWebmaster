let tabs = document.querySelectorAll(".tab_button")

function subTabs(body){
	var subbody = body.querySelector('.tab_body') 
	if (subbody){
		var tabs = body.parentElement.querySelectorAll(".tab_button")
		tabs.forEach((tab)=>{
			tab.classList.remove('tab_active')
		})
		if (tabs[0]){
			tabs[0].classList.add('tab_active')
		}
		var sub_body_el = subbody.querySelector('#tab_body-1')
		if (sub_body_el){
			sub_body_el.classList.add('tab_element__active')
		}
	}
}

function onTab(){
	/* Then show only needed one*/
	var id = this.dataset.bodyid
	var this_body = this.parentElement.nextElementSibling 
	/* First of all, hide all tab_elements*/
	var all_bodies = this_body.querySelectorAll(".tab_element")
	all_bodies.forEach((body) => {
		body.classList.remove('tab_element__active')
	})
	var body = this_body.querySelector("#tab_body-"+id)
	body.classList.add('tab_element__active')
	/* In the end switch current selected tab*/
	var all_tab_buttons = this.parentElement.querySelectorAll(".tab_button")
	subTabs(body)
	all_tab_buttons.forEach((tab) => {
		tab.classList.remove('tab_active')
	})
	this.classList.add('tab_active')

}

tabs.forEach((tab) => {
	tab.addEventListener('click', onTab)
})
