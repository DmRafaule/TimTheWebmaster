class CheckBoxButton{
	constructor(id, callback_on_check, callback_on_uncheck){
		var elements = document.querySelectorAll(id)
		elements.forEach((element) => {
			element.addEventListener('click', function(event){
				var data = event.target.value
				var isChecked = event.target.checked
				if (isChecked){
					callback_on_check(data)
				}else{
					callback_on_uncheck(data)
				}
			})
		})
	}
}
