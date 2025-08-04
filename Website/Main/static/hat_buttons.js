/*
	Данный скрипт контролирует кнопки в шапке сайта.
	Он контролирует их таким образом что, только одна кнопка может 
	быть активной за раз, или ни одна не активна
*/
let header_buttons = document.querySelectorAll('.header_button')
let header = document.getElementById("header")
let header_height = header.getBoundingClientRect().height  + "px"

function closeHeaderButton(body){
	body.classList.remove("active_nav")	
	body.style.top = header_height
}

function openHeaderButton(body){
	body.classList.add("active_nav")	
	body.style.top = header_height
}

function onHeaderButton(body){
	if (body.classList.contains('active_nav')){
		closeHeaderButton(body)
	}
	else{
		header_buttons.forEach( (header_button) => {
			var body = document.getElementById(header_button.dataset.body)
			closeHeaderButton(body)
		})
		openHeaderButton(body)
	}
	
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
  
  
header_buttons.forEach( (header_button) => {
	header_button = removeAllEvents(header_button)
	header_button.addEventListener('click', (e) => {
		var body = document.getElementById(header_button.dataset.body)
		onHeaderButton(body)
		onClickOutsideHat(header_button, body, () => closeHeaderButton(body) );
	})
})

