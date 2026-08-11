const clickOutsideTooltip = new Event('clickOutsideTooltip')
let onClickOutsideTooltip = (button, body, callback) => {
	document.addEventListener('click', e => {
		if (!body.contains(e.target) && !button.contains(e.target)){ 
			document.dispatchEvent(clickOutsideTooltip)
			callback()
		};
	});
};

function tooltipClear(block){
    block.classList.remove("tooltiptext_bottom")
    block.classList.remove("tooltiptext_top")
    block.classList.remove("tooltiptext_left")
    block.classList.remove("tooltiptext_right")
}

function tooltipToggle(block){
    tooltipClear(block)
    var viewport_height = window.innerHeight
    var viewport_width = window.innerWidth
    var x = block.getBoundingClientRect().x
    var width = block.getBoundingClientRect().width
    var y = block.getBoundingClientRect().y

    // Выравниваем по вериткали
    if (y < viewport_height/2){
        block.classList.toggle("tooltiptext_bottom")
    }else{
        block.classList.toggle("tooltiptext_top")
    }

    // Выравниваем по левому или по правому краю
    if (x - width/2 < 0){
        block.style.left = width/2 + "px"

    }else if (x + width/2 > viewport_width){
        block.style.left = (-1 * (x + width/2 - viewport_width)) + "px"
    }
    block.classList.toggle("tooltiptext_active")
}

function tooltipOff(block){
    block.classList.remove("tooltiptext_active")
}


export function tooltipInit(){
    document.querySelectorAll(".tooltip").forEach( (tooltip) => {
        var tooltip_hidden_block = tooltip.querySelector('.tooltiptext')
        tooltip.addEventListener('click', (event) => {
            tooltipToggle(tooltip_hidden_block)
        })
	    onClickOutsideTooltip(tooltip, tooltip_hidden_block, () => tooltipOff(tooltip_hidden_block) );
    })
}