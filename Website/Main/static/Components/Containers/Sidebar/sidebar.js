/*
	Данный скрипт контролирует кнопки в шапке сайта.
	Он контролирует их таким образом что, только одна кнопка может 
	быть активной за раз, или ни одна не активна
*/
let sidebar_buttons_to_open = document.querySelectorAll('.ttw-sidebar_button_open')
let sidebar_buttons_to_close = document.querySelectorAll('.ttw-sidebar_button_close')

function closeHeaderButton(body){
	body.classList.add("ttw-sidebar_body_not_active")	
}

function openHeaderButton(body){
	body.classList.remove("ttw-sidebar_body_not_active")	
}

const clickOutsideHat = new Event('clickOutsideHat')
export let onClickOutsideHat = (button, body, callback) => {
	document.addEventListener('click', e => {
		if (!body.contains(e.target) && !button.contains(e.target)){ 
			document.dispatchEvent(clickOutsideHat)
			callback()
		};
	});
};

function removeAllEvents(element) {
  // Get the parent of the element
  const parent = element.parentNode;

  // Clone the element (true for deep clone, false for shallow clone)
  // Event listeners are NOT copied during cloning
  const clonedElement = element.cloneNode(true);

  // Replace the original element with the cloned element
  if (parent) {
    parent.replaceChild(clonedElement, element);
  }
  
  return clonedElement
}
  
  
sidebar_buttons_to_open.forEach( (sidebar) => {
	var body = document.getElementById(sidebar.dataset.body)
	sidebar.addEventListener('click', (e) => {
		openHeaderButton(body)
	})
	onClickOutsideHat(sidebar, body, () => closeHeaderButton(body) );
})

sidebar_buttons_to_close.forEach( (sidebar) => {
	var body = document.getElementById(sidebar.dataset.body)
	sidebar.addEventListener('click', (e) => {
		closeHeaderButton(body)
	})
})