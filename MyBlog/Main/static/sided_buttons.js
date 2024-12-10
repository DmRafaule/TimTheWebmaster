let sided_buttons = document.querySelectorAll('.sided-button')

function closeSideBody(body, btn){
    var header_height = header.getBoundingClientRect().height  + "px"
	body.classList.remove("active_nav")	
	body.classList.remove("padder")
    body.style.top = header_height
    var icon = btn.querySelector('img')
    if (icon.classList.contains('flip_vert')){
        icon.classList.remove('flip_vert')
    }else{
        icon.classList.add('flip_vert')
    }
}

function openSideBody(body, btn){
    var header_height = header.getBoundingClientRect().height  + "px"
	body.classList.add("active_nav")
    body.classList.add("padder")
	body.style.top = header_height
    var icon = btn.querySelector('img')
    if (icon.classList.contains('flip_vert')){
        icon.classList.remove('flip_vert')
    }else{
        icon.classList.add('flip_vert')
    }
}

function onSideButtonClick(btn){
    var side_body = btn.nextElementSibling
    if (side_body.classList.contains('active_nav')){
		closeSideBody(side_body, btn)
	}
	else{
		openSideBody(side_body, btn)
	}
}

sided_buttons.forEach((btn)=>{
    btn.addEventListener('click', (event) => {
        onSideButtonClick(btn)
    })
})