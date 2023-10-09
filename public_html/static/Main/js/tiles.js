const tiles_headers = document.querySelectorAll('.content_body__tile'); 
function toggleTile(){
	tiles_headers.forEach( (card) => {
		card.classList.remove('tile_choosen')
	})
	var body = this.querySelector('.content_body__tile_body')
	this.classList.add('tile_choosen')
	sibling = this.nextElementSibling
	while (sibling != null){
		this.parentElement.insertBefore(sibling, this )
		sibling = this.nextElementSibling
	}
}

tiles_headers.forEach( (tile) => {
	tile.addEventListener('click', toggleTile)
})
