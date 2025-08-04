/*
 *	Simple radio button checker
 * */
export class RadioButton{
	constructor(id, callback, default_to_check){
		var def_i = default_to_check || 0
		this.elements = document.querySelectorAll(id)
		this.elements[def_i].checked = true
		this.elements.forEach((element) => {
			element.addEventListener('click', function(event){
				var data = event.target.value
				callback(data)
			})
		})
	}
	update(default_to_check){
		this.elements[default_to_check].checked = true
	}
}

/* 
 * Create radio button via colored icons
 * 
 * */
export class ColoredRadioButton{
	constructor(id, btn, selected_color, not_selected_color, callback, callbackArgs){
		this.btn = btn
		this.selected_color = selected_color
		this.not_selected_color = not_selected_color
		this.callback = callback || function(){}
		this.callbackArgs = callbackArgs || this.btn
		this.btns = document.querySelectorAll(id)
	}
	select(){
		this.btns.forEach((item)=>{
			item.style.backgroundColor = this.not_selected_color
		})
		this.btn.style.backgroundColor = this.selected_color
		this.callback(this.callbackArgs)
	}
}


