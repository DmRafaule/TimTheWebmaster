function update_platform_filters(){
    var platforms_id = []
    document.querySelectorAll('.platform_button.selected_order').forEach((el)=>{
        platforms_id.push(el.dataset.platform)
    })
    return platforms_id 
}

function onReady(){
	// Set up buttons effects for filtering by tim
	// Ordering and filtering by date
	var letter_btns = document.querySelectorAll('.platform_button')
	letter_btns.forEach( btn => {
		btn.addEventListener('click', (event) => {
			btn.classList.toggle('selected_order')
		})
	})
}

if (document.readyState === "loading") {
	// Loading hasn't finished yet
	document.addEventListener("DOMContentLoaded", onReady);
} else {
	onReady()
}