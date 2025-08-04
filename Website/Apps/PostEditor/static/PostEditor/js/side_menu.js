var quill_side_menu = document.querySelector('#editor-side-menu')

function hideSelectedDropdown(btn, container){
    btn.setAttribute('src', btn.dataset.src)
    btn.classList.remove("active_ql_options")
    container.classList.remove('quill-drop-down-container_active')
    container.classList.remove('quill-drop-down-container_notactive')
    container.classList.add('quill-drop-down-container_notactive')
}

function hideAllDropdowns(){
    document.querySelectorAll('.quill-drop-down-container').forEach( (cont) =>{
        cont.classList.remove('quill-drop-down-container_active')
        cont.classList.remove('quill-drop-down-container_notactive')
        cont.classList.add('quill-drop-down-container_notactive')
    })
}

function onDropDownButton(btn, container){
    // Change to close icon
	if (btn.classList.contains("active_ql_options")){
		btn.setAttribute('src', btn.dataset.src)
	}
	else{
		btn.setAttribute('src', btn.dataset.closeBtn)
	}
	btn.classList.toggle("active_ql_options")
    // Display drop down menu
    container.classList.toggle('quill-drop-down-container_active')
    container.classList.toggle('quill-drop-down-container_notactive')
    // Offset drop down menu bellow button
    var paddingBottom = window.getComputedStyle(btn, null).getPropertyValue('padding-bottom')
    container.style.top = (btn.getBoundingClientRect().height + Number(paddingBottom.replace('px', '')) )+ 'px'
    // Offset dropdown menu to not over flow out the screen
    var outXScreen = screen.width - (container.getBoundingClientRect().width + container.getBoundingClientRect().x) 
    if (outXScreen < 0){
        container.style.left = `${outXScreen}px`
    }
}

const clickOutsideHatEditor = new Event('clickOutsideHatEditor')
let onClickOutsideHat = (button, body, callback) => {
	document.addEventListener('click', e => {
		if (!body.contains(e.target) && !button.contains(e.target)){ 
			document.dispatchEvent(clickOutsideHatEditor)
			callback()
		};
	});
};

function onReady(){
    quill_side_menu.style.top = header.getBoundingClientRect().height + 'px'
    var quill_drop_down_buttons = document.querySelectorAll('.quill-drop-down-button')
    quill_drop_down_buttons.forEach( (btn) => {
        btn.addEventListener('click', (event)=>{
            var container = btn.nextElementSibling
            onDropDownButton(btn, container)
        })
        onClickOutsideHat(btn, btn.nextElementSibling, () => hideSelectedDropdown( btn, btn.nextElementSibling) );
    })

}

if (document.readyState === "loading") {
	// Loading hasn't finished yet
	document.addEventListener("DOMContentLoaded", onReady);
} else {
	onReady()
}