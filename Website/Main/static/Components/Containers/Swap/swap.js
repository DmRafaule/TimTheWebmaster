let swap_buttons = document.querySelectorAll(".ttw-button_swap") 

const clickOutsideSwap = new Event('clickOutsideSwap')
let onClickOutsideSwap = (button, body, callback) => {
	document.addEventListener('click', e => {
		if (!body.contains(e.target) && !button.contains(e.target)){ 
			document.dispatchEvent(clickOutsideSwap)
			callback()
		};
	});
};

export class SwapButton{
	constructor(button){
        this.button = button
        this.button.addEventListener('click', ()=>{
            for (var i = 0; i < this.button.childElementCount; i++){
                this.button.children[i].classList.toggle("ttw-button_swap_not_active")
            }
        })
	}

    swapOn(){
        this.button.children[0].classList.add("ttw-button_swap_not_active")
        this.button.children[1].classList.remove("ttw-button_swap_not_active")
    }
    swapOff(){
        this.button.children[0].classList.remove("ttw-button_swap_not_active")
        this.button.children[1].classList.add("ttw-button_swap_not_active")
    }
    swap(){
        for (var i = 0; i < this.button.childElementCount; i++){
            this.button.children[i].classList.toggle("ttw-button_swap_not_active")
        }
    }
}

swap_buttons.forEach( (btn) => {
    var swapBtn = new SwapButton(btn)
    var body = btn
    if (btn.dataset.body){
        body = document.getElementById(btn.dataset.body)
    }
    // Кнопка не будет выполнять "обмен" если клик был не на ней
    if (!btn.classList.contains("ttw-button_swap_not_close_on_outsite")){
        onClickOutsideSwap(btn, body, () => swapBtn.swapOff() );
    }
})