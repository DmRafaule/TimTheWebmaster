class InputValueButton{
	constructor(id, callback){
		
		this.elements = document.querySelectorAll(id)
		this.elements.forEach((element) => {
			element.addEventListener('change', function(event){
				var data = event.target.value
				var field = event.target.dataset.field
				callback(data, field)
			})
		})
	}
	update(data){
		for (var i = 0; i < this.elements.length; i++){
			this.elements[i].value = data[i] 
		}
	}
}
