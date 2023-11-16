let togglers = document.querySelectorAll('.content_body__toggler_header')

function toggleBody(){
	var body = this.nextSibling.nextSibling
	if (body.classList.contains('hidden')){
		var sign = this.querySelector('.content_body__toggler_header--sign')
		sign.innerHTML = "▼"
	}else{
		var sign = this.querySelector('.content_body__toggler_header--sign')
		sign.innerHTML = "▶"
	}
	body.classList.toggle('hidden')
	if (typeof adjustCodeBlocks === "function")
		adjustCodeBlocks()
}

togglers.forEach( (toggler) =>{
	toggler.addEventListener('click', toggleBody)
})
