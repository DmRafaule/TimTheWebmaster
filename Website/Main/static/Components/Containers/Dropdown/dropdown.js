let dropdown_buttons = document.querySelectorAll(".ttw-button_dropdown") 

const clickOutsideDropdown = new Event('clickOutsideDropdown')
let onClickOutsideDropdown = (button, body, callback) => {
	document.addEventListener('click', e => {
		if (!body.contains(e.target) && !button.contains(e.target)){ 
			document.dispatchEvent(clickOutsideDropdown)
			callback()
		};
	});
};

export class DropdownButton{
	constructor(button){
        this.button = button
        this.body = document.getElementById(button.dataset.body)
        this.button.addEventListener('click', ()=>{
            this.dropdown()
        })
	}

    dropdownOn(){
        this.body.classList.remove('not_active_dropdown')
    }
    dropdownOff(){
        this.body.classList.add('not_active_dropdown')
    }
    dropdown(){
        this.body.classList.toggle('not_active_dropdown')
    }
}

dropdown_buttons.forEach( (btn) => {
    var dropdownBtn = new DropdownButton(btn)
    var body = btn
    if (dropdownBtn.body){
        body = dropdownBtn.body
    }
    // Добавляем только один евент на закрытие при нажатии вне контейнера
    if (btn.classList.contains('ttw-button_swap_front')){
	    onClickOutsideDropdown(btn, body, () => dropdownBtn.dropdownOff() );
    }else if (!btn.classList.contains('ttw-button_swap_back')){
        // Если у контейнера нет и 'ttw-button_swap_back' значит это не swap кнопка.
        // В таком случае добавляем ещё один евент на закрытие при нажатии вне контейнера
	    onClickOutsideDropdown(btn, body, () => dropdownBtn.dropdownOff() );
    }
})