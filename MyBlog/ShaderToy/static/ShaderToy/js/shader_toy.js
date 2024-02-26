/* Что добавить потом
 *	1) Добавить в настройки холста версию WebGL 1 или 2
 *	2) Обратную связь при сохранении
 *	3) Обратную связь при ошибках
 *	4) Возможность давать имена сохранениям
 *	5) Привязать клавиатуру к некоторым кнопкам
 * */


/* 
 * Генерирует уникальные идентификаторы
 * 
 * */
function GenerateUID(){
	return Math.random().toString(16).slice(2);
}

/*
 *	Коллбэк для обновления текста в зависимости от
 *	того происходит отрисовка или нет.
 *
 * */
function SetToyStatus(source){
	var status = source.dataset.setedStatus
	var to_insert = document.getElementById('render-status')
	to_insert.innerText = status 
}

/*
 *	Присваиваем кнопке остановки рендеринга соответствующую ф-ию
 *	Данная функция останавливает запросы фреймов от браузера
 * */
var pause_shader_button = document.getElementById("pause_shader")
pause_shader_button.addEventListener('click', function(){
	pause_render.select()
	window.cancelAnimationFrame(toy.request_animation_id)
})
var pause_render = new ColoredRadioButton('.switch_action', pause_shader_button, "#f0bb29", "#fff", SetToyStatus, pause_shader_button)

/*
 *	Присваиваем кнопке продолжения рендеринга соответствующую ф-ию
 *	Данная функция запрашивает новый фрейм от браузера.
 * */
var resume_shader_button = document.getElementById("resume_shader")
resume_shader_button.addEventListener('click', function(){
	resume_render.select()
	toy.request_animation_id = window.requestAnimationFrame((time) => toy.update(time, toy))
})
var resume_render = new ColoredRadioButton('.switch_action', resume_shader_button, "#84a8e3", "#fff", SetToyStatus, resume_shader_button)

/*
 *	Присваиваем кнопке перезагрузки шейдера соответствующую ф-ию
 *	Данная функция обновляет все юниформы и аттрибуты, а вместе с
 *	ними и UI элементы вместе с геометрией.
 * */
var reload_shader_button = document.getElementById("reload_shader")
reload_shader_button.addEventListener('click', function(){
	toy.clearLog()
	toy.updateShaderProgram()
	toy.updateUIElements()
	toy.updateGeometry()
})

/*
 *	Выполняет сохранение шейдера в текущую сессию
 * */
function SaveShaderAction(){
	// Генерируем уникальное имя(дату) и id 
	var cd = new Date() 
	var date = cd.getDay() + "." + cd.getMonth() + "." + cd.getFullYear() + "-" + cd.getHours() + ":" + cd.getMinutes() + ":" + cd.getSeconds() + ":" + cd.getMilliseconds()
	var id = GenerateUID()
	// Собираем все буферы и размеры в один большой блоб информации для передачи
	var buffers = {"buffers": []}
	var sizes = {"sizes": []}
	for (var i = 0; i < toy.ui_elements.length; i++){
		var is_raw = false
		if (toy.ui_elements[i].buffer.constructor === Float32Array) {
			is_raw = true
		}
		buffers["buffers"].push({"data": toy.ui_elements[i].buffer, "is_raw": is_raw})
		sizes["sizes"].push({"data": toy.ui_elements[i].size})
	}
	$.ajax({
		type: "POST",
		url: "save_shader/",
		data: {
			'name': date,
			'shader_id': id,
			'fragment_src' : toy.fragment_editor.getValue(),
			'vertex_src' : toy.vertex_editor.getValue(),
			'default_geometry_data_indx' : toy.default_geometry_data_indx,
			'render_mode' : toy.render_mode,
			'bg' : JSON.stringify(toy.bg),
			'buffers' : JSON.stringify(buffers),
			'sizes' : JSON.stringify(sizes),
		},
		headers: {'X-CSRFToken': csrftoken},
		mode: 'same-origin', // Do not send CSRF token to another domain.
		success: function(result) {
			var el_insert_to = document.getElementById('tab_body-8')
			el_insert_to.insertAdjacentHTML('beforeend', result)
			document.getElementById('delete-' + id).addEventListener('click', RemoveShaderAction)
			document.getElementById('upload-' + id).addEventListener('click', UploadShaderAction)
		},
		error: function(jqXHR, textStatus, errorThrown){
		}
	})
}
var save_shader_button = document.getElementById("save_shader")
save_shader_button.addEventListener('click', SaveShaderAction)

/*
 *	Выполняет удаление сохранённого шейдера из текущей сессии
 * */
function RemoveShaderAction(event){
	var id = event.target.attributes.value.nodeValue
	// Удаляем элемент со страницы
	var record = document.getElementById(id)
	record.remove()
	// Делаем запрос на сервер для удаления шейдера
	$.ajax({
		type: 'POST',
		url: 'remove_shader/',
		data: {
			'shader_id': id,
		},
		headers: {
			'X-CSRFToken': csrftoken
		},
		mode: 'same-origin',
		success: function(result){

		},
		error: function(jqXHR, textStatus, errorThrown){

		}
	})
}
// Присваиваем функцию удаления шейдера из сессии, каждой найденой кнопки удаления 
var remove_shader_buttons = document.querySelectorAll('.shader_remove_action')	
remove_shader_buttons.forEach((el) => {
	el.addEventListener('click',RemoveShaderAction)
})

/*
 *	Выполняет загрузку сохранённого шейдера из текущей сессии
 * */
function UploadShaderAction(event){
	var id = event.target.attributes.value.nodeValue
	$.ajax({
		type: 'POST',
		url: 'get_shader/',
		data: {
			'shader_id': id,
		},
		headers: {
			'X-CSRFToken': csrftoken
		},
		mode: 'same-origin',
		success: function(result){
			toy.fragment_editor.setValue(result.fragment_src)
			toy.vertex_editor.setValue(result.vertex_src)

			toy.clearLog()
			toy.updateShaderProgram()
			toy.updateUIElements()
			toy.updateGeometry()

			toy.default_geometry_data_indx = result.dgd_indx 
			toy.render_mode = parseInt(result.render_mode)
			var bg = JSON.parse(result.bg)
			toy.bg_color_btn.update(bg)
			toy.updateBgColor(bg[0], 'r')
			toy.updateBgColor(bg[1], 'g')
			toy.updateBgColor(bg[2], 'b')
			toy.updateBgColor(bg[3], 'a')
			var buffers = JSON.parse(result.buffers)
			var sizes = JSON.parse(result.sizes)
			for (var i = 0; i < toy.ui_elements.length; i++){
				if (buffers["buffers"][i]["is_raw"]){
					var array = []
					for (value in buffers["buffers"][i]["data"]){
						array.push(buffers["buffers"][i]["data"][value])
					}
					toy.ui_elements[i].buffer = new Float32Array(array)
				}
				else{
					toy.ui_elements[i].buffer = buffers["buffers"][i]["data"]
				}
				toy.ui_elements[i].size = sizes["sizes"][i]["data"]
			}
			toy.updateUIElements()
			toy.updateGeometry()
		},
		error: function(jqXHR, textStatus, errorThrown){

		}
	})
}
// Присваиваем функцию загрузки шейдера из сессии каждой найденой кнопке загрузки
var upload_shader_buttons = document.querySelectorAll('.shader_upload_action')	
upload_shader_buttons.forEach((el) => {
	el.addEventListener('click',UploadShaderAction)
})


/*
 *	Загружает сохранённые шейдеры из сессии 
 *	,создаёт соответствующие UI элементы
 *	,присваивает им соответствующие коллбэки
 * */
function LoadSaves(){
	$.ajax({
		type: 'POST',
		url: "load_shader/",
		headers: {'X-CSRFToken': csrftoken},
		mode: 'same-origin', // Do not send CSRF token to another domain.
		success: function(result) {
			var el_insert_to = document.getElementById('tab_body-8')
			el_insert_to.insertAdjacentHTML('beforeend', result)
			var saves = el_insert_to.querySelectorAll('.save_shader')
			saves.forEach( (save) => {
				document.getElementById('delete-' + save.id).addEventListener('click', RemoveShaderAction)
				document.getElementById('upload-' + save.id).addEventListener('click', UploadShaderAction)
			})
		},
		error: function(jqXHR, textStatus, errorThrown){
		}
	})
}
var saves_tab = document.getElementById('tab_button_for_save')	
saves_tab.addEventListener('click',LoadSaves, {once: true})

/**/
function LoadLibrary(){
	$.ajax({
		type: 'POST',
		url: "load_library/",
		headers: {'X-CSRFToken': csrftoken},
		mode: 'same-origin', // Do not send CSRF token to another domain.
		success: function(result) {
			var el_insert_to = document.getElementById('tab_body-5')
			el_insert_to.insertAdjacentHTML('beforeend', result)
			var saves = el_insert_to.querySelectorAll('.save_shader')
			saves.forEach( (save) => {
				document.getElementById('upload-' + save.id).addEventListener('click', UploadShaderAction)
			})
		},
		error: function(jqXHR, textStatus, errorThrown){
		}
	})
}
var upload_library_tab = document.getElementById('tab_button_for_lib')	
upload_library_tab.addEventListener('click',LoadLibrary, {once: true})

/*
 * Возвращает шейдер к состоянию по умолчанию, то есть при инициализации
 *
 * */
var toDefault_shader_button = document.getElementById("toDefault_shader")
toDefault_shader_button.addEventListener('click', function(){
	toy.render_mode = toy.gl.TRIANGLES
	toy.render_mode_btn.update(0)
	toy.bg = [1.0, 1.0, 1.0, 1.0]
	toy.bg_color_btn.update(toy.bg)
	resume_render.select()
	toy.setFromDefaultsShaderSrouceCode()
	toy.updateShaderProgram()
	toy.setFromDefaultsUIElements()
	toy.updateGeometry()
})



/*
 * Конвертирует входящую строку цифр в вектор
 * Также конвертирует получаемый размер и текущий индекс в int 
 * */
function handleRawData(element, data){
	switch(element.tagName){
		case "INPUT":
			if (element.type == 'number'){
				this.size = parseInt(data)
				toy.updateShaderProgram()
				toy.updateUIElements()
				this.loc = toy.gl.getAttribLocation(toy.program, this.name);
				toy.updateGeometry()
			}
			else{
				toy.default_geometry_data_indx = parseInt(data)	
			}
			break;
		case "TEXTAREA":
			this.buffer = new Float32Array(data.split(',').map((item)=>{
				return parseFloat(item)
			}))
			toy.updateShaderProgram()
			toy.updateUIElements()
			this.loc = toy.gl.getAttribLocation(toy.program, this.name);
			toy.updateGeometry()
			break;
	}
}

/*
 * Конвертирует входящую строку в тип float
 * и изменяет соответствующий буфер
 * */
function handleFloat(element, data){
	this.buffer = parseFloat(data);
}

/*
 * Конвертирует входящую строку в тип int
 * и изменяет соответствующий буфер
 * */
function handleInt(element, data){
	this.buffer = parseInt(data);
}

/*
 * Конвертирует входящую строку в тип bool
 * и изменяет соответствующий буфер
 * */
function handleBool(element, data){
	this.buffer = parseInt(data);
}

/*
 * Конвертирует входящую строку в тип float
 * и изменяет соответствующую ячейку в векторе
 * */
function handleFloatVector(element, data){
	var indx = parseInt(element.dataset.vecIndx);
	this.buffer[indx] = parseFloat(data);
}

/*
 * Конвертирует входящую строку в тип bool
 * и изменяет соответствующую ячейку в векторе
 * */
function handleBoolVector(element, data){
	var indx = parseInt(element.dataset.vecIndx);
	this.buffer[indx] = parseInt(data);
}

/*
 * Конвертирует входящую строку в тип int
 * и изменяет соответствующую ячейку в векторе
 * */
function handleIntVector(element, data){
	var indx = parseInt(element.dataset.vecIndx);
	this.buffer[indx] = parseInt(data);
}

/*
 * Конвертирует входящую строку в тип float
 * и изменяет соответствующую ячейку в матрице
 * */
function handleMatrix(element, data){
	var indx = parseInt(element.dataset.vecIndx);
	this.buffer[indx] = parseFloat(data);
}

/*
 *	Изменяет размер холста соответственно ширине дисплея
 * */
function resizeCanvasToDisplaySize(canvas, multiplier) {
	multiplier = multiplier || 1;
	const width  = canvas.clientWidth  * multiplier | 0;
	const height = canvas.clientHeight * multiplier | 0;
	if (canvas.width !== width ||  canvas.height !== height) {
	  canvas.width  = width;
	  canvas.height = height;
	  return true;
	}
	return false;
}


/*
 *	Данная функция следит за тем, что когда появится новое поле для ввода данных
 *	она присвоет ему соответствующий хендлер для изменения данных шейдера
 * */
function onInputChange() {

	function setUpHandler(elements){
		elements.forEach( (el) => {
			var elId = el.dataset.uiElementId;
			el.addEventListener('change', (event)=>{
				toy.ui_elements[elId].handler(event.target, event.target.value);
			})
		})
	}

	// Когда появится новый элемент ввода на странице данная функция зарегистрирует это
	function  WaitUIElementsToAppear(mutationList, observer) {
		  for (const mutation of mutationList) {
			if (mutation.addedNodes.length > 0){ 
				const UIElements = mutation.addedNodes[0].querySelectorAll(".input_el");
				setUpHandler(UIElements)
			}
		  }
		};

	const observedElements = document.querySelectorAll(".toObserve");
	const config = { childList: true };
	const observer = new MutationObserver(WaitUIElementsToAppear);
	observedElements.forEach( (el) => {
		observer.observe(el, config);
	}) 
	// Сначала ищем уже присутствующие элементы ввода на странице
	const UIElements = document.querySelectorAll(".input_el");
	setUpHandler(UIElements)
}
document.addEventListener("DOMContentLoaded", onInputChange);

/*
 *	Данная функция обновляет данные об позиции мыши относительно холста
 * */
function UpdateMousePos(event){
  	var rect = event.target.getBoundingClientRect();
  	var x = event.clientX - rect.left; //x position within the element.
  	var y = event.clientY - rect.top;  //y position within the element.
	toy.mouse_pos[0] = x
	toy.mouse_pos[1] = y
}

document.getElementById('canvas').onmousemove = UpdateMousePos

/*
 * Класс которые регулирует, обновляет и контролирует работу ShaderToy инструмента
 *
 * */
class ShaderToy{
	constructor(){
		window.onerror = this.log;
		// Другие константы
		this.start = 0
		this.default_geometry_data_indx = 0;
		this.mouse_pos = [0, 0]
		this.render_mode_btn = new RadioButton('.render_mode', this.updateRenderMode)
		this.pipeline_work_btn = new CheckBoxButton('.pipeline_work', this.updatePipelineCheck, this.updatePipelineUnCheck)
		this.bg_color_btn = new InputValueButton('.bg_color', this.updateBgColor)
		// Получаем объекты редактора от Ace
		this.fragment_editor = ace.edit("fragment_editor");
		this.fragment_editor.session.setMode("ace/mode/glsl");
		this.vertex_editor = ace.edit("vertex_editor");
		this.vertex_editor.session.setMode("ace/mode/glsl");

		/* Получаем WebGL2 контекст. Инициализируем WebGL2 */
		this.canvas = document.querySelector("#canvas");
		this.gl = this.canvas.getContext("webgl2");
		// Устанавливаем режим отрисовки по умолчанию
		this.render_mode = this.gl.TRIANGLES
		this.bg = [1.0, 1.0, 1.0, 1.0]
		if (!this.gl) {
			this.log("OpenGl is not avaiable")
		}
		resume_render.select()
		/* Создаём шейдер */
		this.setFromDefaultsShaderSrouceCode()
		this.updateShaderProgram()
		this.setFromDefaultsUIElements()
		this.updateGeometry()
	}

	setFromDefaultsShaderSrouceCode(){
		/* Создаём шейдер */
		// Получаем путь к исходникам шейдера. 
		this.vertexShaderPath = this.canvas.dataset.vertexShader
		this.fragmentShaderPath = this.canvas.dataset.fragmentShader
		// Получаем содержание шейдера.
		this.vertex_editor.setValue(this.readTextFile(this.vertexShaderPath))
		this.fragment_editor.setValue(this.readTextFile(this.fragmentShaderPath))

	}

	updateShaderProgram(){
		// Переменные где будет хранится код для создания шейдерной программы
		this.fragment_source_code = this.fragment_editor.getValue() 
		this.vertex_source_code = this.vertex_editor.getValue()
		// Создаём программу на GPU. То есть шейдер.
		this.vertexShader = this.createShader(this.gl, this.gl.VERTEX_SHADER, this.vertex_source_code);
		this.fragmentShader = this.createShader(this.gl, this.gl.FRAGMENT_SHADER, this.fragment_source_code);
		this.program = this.createProgram(this.gl, this.vertexShader, this.fragmentShader)
	}

	setFromDefaultsUIElements(){

		this.uTimeLoc = this.gl.getUniformLocation(this.program, 'u_time')
		this.uResolutionLoc = this.gl.getUniformLocation(this.program, 'u_resolution')
		this.uMousePosLoc = this.gl.getUniformLocation(this.program, 'u_mouse')
		this.uniforms = this.getUniforms;
		this.attributes = this.getAttributes;
		this.ui_elements = [];

		/* Создаём соответствующие UI элементы */
		this.clearwebUIElements();
		this.clearbuffUIElements();
		for (var i = 0; i < this.attributes.length; i++){
			this.setUIElement(this.attributes[i]);
		}
		for (var i = 0; i < this.uniforms.length; i++){
			this.setUIElement(this.uniforms[i]);
		}
		for (var i = 0; i < this.ui_elements.length; i++){
			this.setbufferUIElement(this.ui_elements[i]);
			this.setwebUIElement(this.ui_elements[i]);
			this.setcallbacksUIElement(this.ui_elements[i]);
		}
	}

	updateUIElements(){
		this.uTimeLoc = this.gl.getUniformLocation(this.program, 'u_time');
		this.uResolutionLoc = this.gl.getUniformLocation(this.program, 'u_resolution');
		this.uMousePosLoc = this.gl.getUniformLocation(this.program, 'u_mouse');
		this.uniforms = this.getUniforms;
		this.attributes = this.getAttributes;
		var res_elements = []
		var curr = 0
		this.clearwebUIElements();

		for (; curr < this.attributes.length; curr++){
			res_elements.push({
				buffer: null,
				name: this.attributes[curr].name,
				loc: this.attributes[curr].loc,
				type_data: this.attributes[curr].type,
			})	
			// Присваиваем дефолтные буферы и коллбэки
			this.setbufferUIElement(res_elements[curr])
			this.setcallbacksUIElement(res_elements[curr])
			var id = res_elements.length - 1;
			res_elements[curr].id = id;
		}

		for (var i = 0; i < this.uniforms.length; i++){
			res_elements.push({
				buffer: null,
				name: this.uniforms[i].name,
				loc: this.uniforms[i].loc,
				type_data: this.uniforms[i].type,
			})	
			// Присваиваем дефолтные буферы и коллбэки
			this.setbufferUIElement(res_elements[curr])
			this.setcallbacksUIElement(res_elements[curr])
			var id = res_elements.length - 1;
			res_elements[curr].id = id;
			curr += 1
		}

		// Переносим уже существующие элементы интерфейса
		for (var i = 0; i < res_elements.length; i++){
			for (var j = 0; j < this.ui_elements.length; j++){
				if (res_elements[i].name == this.ui_elements[j].name){
					res_elements[i].buffer = this.ui_elements[j].buffer
					res_elements[i].update =  this.ui_elements[j].update
					res_elements[i].handler = this.ui_elements[j].handler
					res_elements[i].size =  this.ui_elements[j].size
					break
				}
			}
		}
		this.ui_elements = res_elements

		for (var i = 0; i < this.ui_elements.length; i++){
			this.setwebUIElement(this.ui_elements[i]);
			this.setcallbacksUIElement(this.ui_elements[i]);
		}
	}

	updateGeometry(){

		/* Создание объекта */
		// Создаём VAO
		this.vao = this.gl.createVertexArray();
		// Устанавливаем его как текущего в использовании
		this.gl.bindVertexArray(this.vao);


		for (var i = 0; i < this.attributes.length; i++){
			// Создаём буферdfsdf
			var buffer = this.gl.createBuffer();
			// Связываем созданный буфер с ...
			this.gl.bindBuffer(this.gl.ARRAY_BUFFER, buffer);
			this.gl.bufferData(this.gl.ARRAY_BUFFER, this.ui_elements[i].buffer, this.gl.STATIC_DRAW);
			// Включаем атрибут
			this.gl.enableVertexAttribArray(this.ui_elements[i].loc);
			// Обозначаем то как читать данные из созданного буфера
			var size = this.ui_elements[i].size;          // Длина одного элемента в буфере
			var type = this.gl.FLOAT;   // Тип данных в элементе буфера 
			var normalize = false; // При использовании с gl.FLOAT не имеет эффекта
			var stride = 0;        // Шаг к следующему элементу в буфере вычисляется: sizeof(type) * size
			var offset = 0;        // Откуда начать читать буфер
			this.gl.vertexAttribPointer(this.ui_elements[i].loc, size, type, normalize, stride, offset);
		}
	}
	/*
	 * Обновляет текущий режим отрисовки в WebGL2
	 * */
	updateRenderMode(data){
		switch(data){
			case 'TRIANGLES':
				toy.render_mode = toy.gl.TRIANGLES
				break
			case 'POINTS':
				toy.render_mode = toy.gl.POINTS
				break
			case 'LINES':
				toy.render_mode = toy.gl.LINES
				break
			case 'LINE_LOOP':
				toy.render_mode = toy.gl.LINE_LOOP
				break
			case 'LINE_STRIP':
				toy.render_mode = toy.gl.LINE_STRIP
				break
			case 'TRIANGLE_STRIP':
				toy.render_mode = toy.gl.TRIANGLE_STRIP
				break
			case 'TRIANGLE_FAN':
				toy.render_mode = toy.gl.TRIANGLE_FAN
				break
		}
	}

	/*
	 * Деактивирует различные режимы работы конвеера отрисовки в WebGL2
	 * */
	updatePipelineUnCheck(data){
		switch(data){
			case 'BLEND':
				toy.gl.disable(toy.gl.BLEND)
				break
			case 'CULL_FACE':
				toy.gl.disable(toy.gl.CULL_FACE)
				break
			case 'DEPTH_TEST':
				toy.gl.disable(toy.gl.DEPTH_TEST)
				break
			case 'DITHER':
				toy.gl.disable(toy.gl.DITHER)
				break
			case 'POLYGON_OFFSET_FILL':
				toy.gl.disable(toy.gl.POLYGON_OFFSET_FILL)
				break
			case 'SAMPLE_ALPHA_TO_COVERAGE':
				toy.gl.disable(toy.gl.SAMPLE_ALPHA_TO_COVERAGE)
				break
			case 'SAMPLE_COVERAGE':
				toy.gl.disable(toy.gl.SAMPLE_COVERAGE)
				break
			case 'SCISSOR_TEST':
				toy.gl.disable(toy.gl.SCISSOR_TEST)
				break
			case 'STENCIL_TEST':
				toy.gl.disable(toy.gl.STENCIL_TEST)
				break
		}
	}

	/*
	 * Активирует различные режимы работы конвеера отрисовки в WebGL2
	 * */
	updatePipelineCheck(data){
		switch(data){
			case 'BLEND':
				toy.gl.enable(toy.gl.BLEND)
				break
			case 'CULL_FACE':
				toy.gl.enable(toy.gl.CULL_FACE)
				break
			case 'DEPTH_TEST':
				toy.gl.enable(toy.gl.DEPTH_TEST)
				break
			case 'DITHER':
				toy.gl.enable(toy.gl.DITHER)
				break
			case 'POLYGON_OFFSET_FILL':
				toy.gl.enable(toy.gl.POLYGON_OFFSET_FILL)
				break
			case 'SAMPLE_ALPHA_TO_COVERAGE':
				toy.gl.enable(toy.gl.SAMPLE_ALPHA_TO_COVERAGE)
				break
			case 'SAMPLE_COVERAGE':
				toy.gl.enable(toy.gl.SAMPLE_COVERAGE)
				break
			case 'SCISSOR_TEST':
				toy.gl.enable(toy.gl.SCISSOR_TEST)
				break
			case 'STENCIL_TEST':
				toy.gl.enable(toy.gl.STENCIL_TEST)
				break
		}
	}

	/*
	 * Обновляет буфер заднего фона
	 * */
	updateBgColor(data, field){
		var number = parseFloat(data)
		switch(field){
			case 'r':
				toy.bg[0] = number
				break;
			case 'g':
				toy.bg[1] = number
				break;
			case 'b':
				toy.bg[2] = number
				break;
			case 'a':
				toy.bg[3] = number
				break;
		}
	}

	isBuiltIn(info) {
	  const name = info.name;
	  return name.startsWith("gl_") || name.startsWith("webgl_");
	}

	glEnum2String(value) {
		if (typeof(value) != 'string'){
			const keys = [];
			for (const key in this.gl) {
			if (this.gl[key] === value) {
			  keys.push(key);
			}
			}
			return keys.length ? keys.join(' | ') : `0x${value.toString(16)}`;
		}
		else{
			return value;
		}
	}

	// Получаем все задействованные юниформы в шейдере
	get getUniforms(){
		var res = [];
		const numUniforms = this.gl.getProgramParameter(this.program, this.gl.ACTIVE_UNIFORMS);
		const indices = [...Array(numUniforms).keys()];
		const blockIndices = this.gl.getActiveUniforms(this.program, indices, this.gl.UNIFORM_BLOCK_INDEX);
		const offsets = this.gl.getActiveUniforms(this.program, indices, this.gl.UNIFORM_OFFSET);

		for (let ii = 0; ii < numUniforms; ++ii) {
			const uniformInfo = this.gl.getActiveUniform(this.program, ii);
			if (this.isBuiltIn(uniformInfo)) {
				continue;
			}
			const {name, type, size} = uniformInfo;
			if (name == 'u_time' || name == 'u_resolution' || name == 'u_mouse')
				continue;
			const blockIndex = blockIndices[ii];
			const offset = offsets[ii];
			const loc = this.gl.getUniformLocation(this.program, name);
			res.push({
				loc: loc,
				name: name,
				type: type,
			})
		}
		return res;
	}

	// Получаем все задействованные аттрибуты в шейдере
	get getAttributes(){
		var res = [];
		const numAttribs = this.gl.getProgramParameter(this.program, this.gl.ACTIVE_ATTRIBUTES);
		for (let ii = 0; ii < numAttribs; ++ii) {
		  const {name, type, size} = this.gl.getActiveAttrib(this.program, ii);
		  const loc = this.gl.getAttribLocation(this.program, name);
			res.push({
				loc: loc,
				name: name,
				type: 'RAW_DATA',
			})
		}
		return res;
	}

	// Сохраняем данные об элементе интерфейса в памяти 
	setUIElement(ui_element){
		this.ui_elements.push({
			buffer: ui_element.buffer,
			name: ui_element.name,
			loc: ui_element.loc,
			size: null,
			update: ()=>{},
			handler: ()=>{},
			type_data: ui_element.type,
		})	
		var id = this.ui_elements.length - 1;
		this.ui_elements[id].id = id;
	}


	updateUIElement(ui_element, id){
		this.ui_elements[id].name = ui_element.name
		this.ui_elements[id].loc = ui_element.loc
		this.ui_elements[id].type_data = ui_element.type
		this.ui_elements[id].id = id;
	}

	// Очищается массив элементов интерфейса в памяти
	// И удаляются все элементы интерфейса на странице
	clearwebUIElements(){
		var el_insert_to = document.getElementById("tab_body-4")	
		var children_of_insterted_el = el_insert_to.querySelectorAll('.mat-type')	
		children_of_insterted_el.forEach( (el) => {
			el.remove()
		})
	}
	clearbuffUIElements(){
		this.ui_elements.length = 0;
	}
	setcallbacksUIElement(ui_element){
		switch(this.glEnum2String(ui_element.type_data)){
			case "RAW_DATA":
				ui_element.handler = handleRawData;
				ui_element.update = ()=>{};
				break;
			case "FLOAT":
				ui_element.handler = handleFloat;
				ui_element.update = function(){
					toy.gl.uniform1f(ui_element.loc, ui_element.buffer);
				}
				break;
			case "BOOL":
				ui_element.handler = handleBool;
				ui_element.update = function(){
					toy.gl.uniform1i(ui_element.loc, ui_element.buffer);
				}
				break;
			case "INT":
				ui_element.handler = handleInt;
				ui_element.update = function(){
					toy.gl.uniform1i(ui_element.loc, ui_element.buffer);
				}
				break;
			case "FLOAT_VEC2":
				ui_element.handler = handleFloatVector;
				ui_element.update = function(){
					toy.gl.uniform2fv(ui_element.loc, ui_element.buffer);
				}
				break;
			case "FLOAT_VEC3":
				ui_element.handler = handleFloatVector;
				ui_element.update = function(){
					toy.gl.uniform3fv(ui_element.loc, ui_element.buffer);
				}
				break;
			case "FLOAT_VEC4":
				ui_element.handler = handleFloatVector;
				ui_element.update = function(){
					toy.gl.uniform4fv(ui_element.loc, ui_element.buffer);
				}
				break;
			case "BOOL_VEC2":
				ui_element.handler = handleBoolVector;
				ui_element.update = function(){
					toy.gl.uniform2iv(ui_element.loc, ui_element.buffer);
				}
				break;
			case "BOOL_VEC3":
				ui_element.handler = handleBoolVector;
				ui_element.update = function(){
					toy.gl.uniform3iv(ui_element.loc, ui_element.buffer);
				}
				break;
			case "BOOL_VEC4":
				ui_element.handler = handleBoolVector;
				ui_element.update = function(){
					toy.gl.uniform4iv(ui_element.loc, ui_element.buffer);
				}
				break;
			case "INT_VEC2":
				ui_element.handler = handleIntVector;
				ui_element.update = function(){
					toy.gl.uniform2iv(ui_element.loc, ui_element.buffer);
				}
				break;
			case "INT_VEC3":
				ui_element.handler = handleIntVector;
				ui_element.update = function(){
					toy.gl.uniform3iv(ui_element.loc, ui_element.buffer);
				}
				break;
			case "INT_VEC4":
				ui_element.handler = handleIntVector;
				ui_element.update = function(){
					toy.gl.uniform4iv(ui_element.loc, ui_element.buffer);
				}
				break;
			case "FLOAT_MAT2":
				ui_element.handler = handleMatrix;
				ui_element.update = function(){
					toy.gl.uniformMatrix2fv(ui_element.loc, false, ui_element.buffer);
				}
				break;
			case "FLOAT_MAT3":
				ui_element.handler = handleMatrix;
				ui_element.update = function(){
					toy.gl.uniformMatrix3fv(ui_element.loc, false, ui_element.buffer);
				}
				break;
			case "FLOAT_MAT4":
				ui_element.handler = handleMatrix;
				ui_element.update = function(){
					toy.gl.uniformMatrix4fv(ui_element.loc, false, ui_element.buffer);
				}
				break;
		}

	}
	setwebUIElement(ui_element){
		var fragment = ''

		switch(this.glEnum2String(ui_element.type_data)){
			case "RAW_DATA":
				// Set up checked radio button
				// if current active index is eaqual to index of ui_element
				var isForGeometry = null
				if (ui_element.id == this.default_geometry_data_indx)
					var isForGeometry = 'checked'
				else
					var isForGeometry = ''
					
				fragment = `<fieldset class="mat-type">
	<legend>
		${ui_element.name} | RAW_DATA	
	</legend>
	<div class="input_data column min_row_gap">
		<div class="row min_col_gap no_wrap">
			<p>step</p>
			<input data-ui-element-id="${ui_element.id}" class="input_el" value="${ui_element.size}" type="number" id="tentacles" name="tentacles" step="1"/>
		</div>
		<div class="row min_col_gap no_wrap">
			<p>is for geometry</p>
			<input data-ui-element-id="${ui_element.id}" class="input_el" value="${ui_element.id}" type="radio" name="geometry" ${isForGeometry}/>
		</div>
		<hr>
		<textarea data-ui-element-id="${ui_element.id}" class="input_el" name="about" id="">
${ui_element.buffer}
		</textarea>
	</div>
</fieldset>`;
				break;
			case "FLOAT":
				fragment = `<fieldset class="mat-type">
	<legend>
		${ui_element.name} | FLOAT
	</legend>
	<input data-ui-element-id="${ui_element.id}" class="input_el" value="${ui_element.buffer}" type="number" id="tentacles" name="tentacles" step="0.01"/>
</fieldset>`;
				break;
			case "BOOL":
				fragment = `<fieldset class="mat-type">
	<legend>
		${ui_element.name} | BOOL 
	</legend>
	<input data-ui-element-id="${ui_element.id}" class="input_el" value="${ui_element.buffer}" min="0" max="1" type="number" id="tentacles" name="tentacles" step="1"/>
</fieldset>`;
				break;
			case "INT":
				fragment = `<fieldset class="mat-type">
	<legend>
		${ui_element.name} | INT
	</legend>
	<input data-ui-element-id="${ui_element.id}" class="input_el" value="${ui_element.buffer}" type="number" id="tentacles" name="tentacles" step="1"/>
</fieldset>`;
				break;
			case "FLOAT_VEC2":
				fragment = `<fieldset class="mat-type">
	<legend>
		${ui_element.name} | FLOAT VECTOR_2
	</legend>
	<div class="input_vector">
		<input data-ui-element-id="${ui_element.id}" data-vec-indx="0" class="input_el" value="${ui_element.buffer[0]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
		<input data-ui-element-id="${ui_element.id}" data-vec-indx="1" class="input_el" value="${ui_element.buffer[1]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
	</div>
</fieldset>`;
				break;
			case "FLOAT_VEC3":
				fragment = `<fieldset class="mat-type">
	<legend>
		${ui_element.name} | FLOAT VECTOR_3
	</legend>
	<div class="input_vector">
		<input data-ui-element-id="${ui_element.id}" data-vec-indx="0" class="input_el" value="${ui_element.buffer[0]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
		<input data-ui-element-id="${ui_element.id}" data-vec-indx="1" class="input_el" value="${ui_element.buffer[1]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
		<input data-ui-element-id="${ui_element.id}" data-vec-indx="2" class="input_el" value="${ui_element.buffer[2]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
	</div>
</fieldset>`;
				break;
			case "FLOAT_VEC4":
				fragment = `<fieldset class="mat-type">
	<legend>
		${ui_element.name} | FLOAT VECTOR_4
	</legend>
	<div class="input_vector">
		<input data-ui-element-id="${ui_element.id}" data-vec-indx="0" class="input_el" value="${ui_element.buffer[0]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
		<input data-ui-element-id="${ui_element.id}" data-vec-indx="1" class="input_el" value="${ui_element.buffer[1]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
		<input data-ui-element-id="${ui_element.id}" data-vec-indx="2" class="input_el" value="${ui_element.buffer[2]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
		<input data-ui-element-id="${ui_element.id}" data-vec-indx="3" class="input_el" value="${ui_element.buffer[3]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
	</div>
</fieldset>`;
				break;
			case "BOOL_VEC2":
				fragment = `<fieldset class="mat-type">
	<legend>
		${ui_element.name} | BOOL VECTOR_2
	</legend>
	<div class="input_vector">
		<input data-ui-element-id="${ui_element.id}" data-vec-indx="0" class="input_el" value="${ui_element.buffer[0]}" min="0" max="1" type="number" id="tentacles" name="tentacles" step="1"/>
		<input data-ui-element-id="${ui_element.id}" data-vec-indx="1" class="input_el" value="${ui_element.buffer[1]}" min="0" max="1" type="number" id="tentacles" name="tentacles" step="1"/>
	</div>
</fieldset>`;
				break;
			case "BOOL_VEC3":
				fragment = `<fieldset class="mat-type">
	<legend>
		${ui_element.name} | BOOL VECTOR_3
	</legend>
	<div class="input_vector">
		<input data-ui-element-id="${ui_element.id}" data-vec-indx="0" class="input_el" value="${ui_element.buffer[0]}" min="0" max="1" type="number" id="tentacles" name="tentacles" step="1"/>
		<input data-ui-element-id="${ui_element.id}" data-vec-indx="1" class="input_el" value="${ui_element.buffer[1]}" min="0" max="1" type="number" id="tentacles" name="tentacles" step="1"/>
		<input data-ui-element-id="${ui_element.id}" data-vec-indx="2" class="input_el" value="${ui_element.buffer[2]}" min="0" max="1" type="number" id="tentacles" name="tentacles" step="1"/>
	</div>
</fieldset>`;
				break;
			case "BOOL_VEC4":
				fragment = `<fieldset class="mat-type">
	<legend>
		${ui_element.name} | BOOL VECTOR_4
	</legend>
	<div class="input_vector">
		<input data-ui-element-id="${ui_element.id}" data-vec-indx="0" class="input_el" value="${ui_element.buffer[0]}" min="0" max="1" type="number" id="tentacles" name="tentacles" step="1"/>
		<input data-ui-element-id="${ui_element.id}" data-vec-indx="1" class="input_el" value="${ui_element.buffer[1]}" min="0" max="1" type="number" id="tentacles" name="tentacles" step="1"/>
		<input data-ui-element-id="${ui_element.id}" data-vec-indx="2" class="input_el" value="${ui_element.buffer[2]}" min="0" max="1" type="number" id="tentacles" name="tentacles" step="1"/>
		<input data-ui-element-id="${ui_element.id}" data-vec-indx="3" class="input_el" value="${ui_element.buffer[3]}" min="0" max="1" type="number" id="tentacles" name="tentacles" step="1"/>
	</div>
</fieldset>`;
				break;
			case "INT_VEC2":
				fragment = `<fieldset class="mat-type">
	<legend>
		${ui_element.name} | INT VECTOR_2
	</legend>
	<div class="input_vector">
		<input data-ui-element-id="${ui_element.id}" data-vec-indx="0" class="input_el" value="${ui_element.buffer[0]}" type="number" id="tentacles" name="tentacles" step="1"/>
		<input data-ui-element-id="${ui_element.id}" data-vec-indx="1" class="input_el" value="${ui_element.buffer[1]}" type="number" id="tentacles" name="tentacles" step="1"/>
	</div>
</fieldset>`;
				break;
			case "INT_VEC3":
				fragment = `<fieldset class="mat-type">
	<legend>
		${ui_element.name} | INT VECTOR_3
	</legend>
	<div class="input_vector">
		<input data-ui-element-id="${ui_element.id}" data-vec-indx="0" class="input_el" value="${ui_element.buffer[0]}" type="number" id="tentacles" name="tentacles" step="1"/>
		<input data-ui-element-id="${ui_element.id}" data-vec-indx="1" class="input_el" value="${ui_element.buffer[1]}" type="number" id="tentacles" name="tentacles" step="1"/>
		<input data-ui-element-id="${ui_element.id}" data-vec-indx="2" class="input_el" value="${ui_element.buffer[2]}" type="number" id="tentacles" name="tentacles" step="1"/>
	</div>
</fieldset>`;
				break;
			case "INT_VEC4":
				fragment = `<fieldset class="mat-type">
	<legend>
		${ui_element.name} | INT VECTOR_4
	</legend>
	<div class="input_vector">
		<input data-ui-element-id="${ui_element.id}" data-vec-indx="0" class="input_el" value="${ui_element.buffer[0]}" type="number" id="tentacles" name="tentacles" step="1"/>
		<input data-ui-element-id="${ui_element.id}" data-vec-indx="1" class="input_el" value="${ui_element.buffer[1]}" type="number" id="tentacles" name="tentacles" step="1"/>
		<input data-ui-element-id="${ui_element.id}" data-vec-indx="2" class="input_el" value="${ui_element.buffer[2]}" type="number" id="tentacles" name="tentacles" step="1"/>
		<input data-ui-element-id="${ui_element.id}" data-vec-indx="3" class="input_el" value="${ui_element.buffer[3]}" type="number" id="tentacles" name="tentacles" step="1"/>
	</div>
</fieldset>`;
				break;
			case "FLOAT_MAT2":
				fragment = `<fieldset class="mat-type">
						<legend>
							${ui_element.name} | MATRIX_2x2
						</legend>
						<div class="input_matrix">
							<div class="input_vector">
								<input data-ui-element-id="${ui_element.id}" data-vec-indx="0" class="input_el" value="${ui_element.buffer[0]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
								<input data-ui-element-id="${ui_element.id}" data-vec-indx="1" class="input_el" value="${ui_element.buffer[1]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
							</div>
							<div class="input_vector">
								<input data-ui-element-id="${ui_element.id}" data-vec-indx="2" class="input_el" value="${ui_element.buffer[2]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
								<input data-ui-element-id="${ui_element.id}" data-vec-indx="3" class="input_el" value="${ui_element.buffer[3]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
							</div>
						</div>
					</fieldset>`;
				break;
			case "FLOAT_MAT3":
				fragment = `<fieldset class="mat-type">
						<legend>
							${ui_element.name} | MATRIX_3x3
						</legend>
						<div class="input_matrix">
							<div class="input_vector">
								<input data-ui-element-id="${ui_element.id}" data-vec-indx="0" class="input_el" value="${ui_element.buffer[0]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
								<input data-ui-element-id="${ui_element.id}" data-vec-indx="1" class="input_el" value="${ui_element.buffer[1]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
								<input data-ui-element-id="${ui_element.id}" data-vec-indx="2" class="input_el" value="${ui_element.buffer[2]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
							</div>
							<div class="input_vector">
								<input data-ui-element-id="${ui_element.id}" data-vec-indx="3" class="input_el" value="${ui_element.buffer[3]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
								<input data-ui-element-id="${ui_element.id}" data-vec-indx="4" class="input_el" value="${ui_element.buffer[4]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
								<input data-ui-element-id="${ui_element.id}" data-vec-indx="5" class="input_el" value="${ui_element.buffer[5]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
							</div>
							<div class="input_vector">
								<input data-ui-element-id="${ui_element.id}" data-vec-indx="6" class="input_el" value="${ui_element.buffer[6]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
								<input data-ui-element-id="${ui_element.id}" data-vec-indx="7" class="input_el" value="${ui_element.buffer[7]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
								<input data-ui-element-id="${ui_element.id}" data-vec-indx="8" class="input_el" value="${ui_element.buffer[8]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
							</div>
						</div>
					</fieldset>`;
				break;
			case "FLOAT_MAT4":
				fragment = `<fieldset class="mat-type">
						<legend>
							${ui_element.name} | MATRIX_4x4
						</legend>
						<div class="input_matrix">
							<div class="input_vector">
								<input data-ui-element-id="${ui_element.id}" data-vec-indx="0" class="input_el" value="${ui_element.buffer[0]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
								<input data-ui-element-id="${ui_element.id}" data-vec-indx="1" class="input_el" value="${ui_element.buffer[1]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
								<input data-ui-element-id="${ui_element.id}" data-vec-indx="2" class="input_el" value="${ui_element.buffer[2]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
								<input data-ui-element-id="${ui_element.id}" data-vec-indx="3" class="input_el" value="${ui_element.buffer[3]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
							</div>
							<div class="input_vector">
								<input data-ui-element-id="${ui_element.id}" data-vec-indx="4" class="input_el" value="${ui_element.buffer[4]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
								<input data-ui-element-id="${ui_element.id}" data-vec-indx="5" class="input_el" value="${ui_element.buffer[5]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
								<input data-ui-element-id="${ui_element.id}" data-vec-indx="6" class="input_el" value="${ui_element.buffer[6]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
								<input data-ui-element-id="${ui_element.id}" data-vec-indx="7" class="input_el" value="${ui_element.buffer[7]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
							</div>
							<div class="input_vector">
								<input data-ui-element-id="${ui_element.id}" data-vec-indx="8" class="input_el" value="${ui_element.buffer[8]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
								<input data-ui-element-id="${ui_element.id}" data-vec-indx="9" class="input_el" value="${ui_element.buffer[9]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
								<input data-ui-element-id="${ui_element.id}" data-vec-indx="10" class="input_el" value="${ui_element.buffer[10]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
								<input data-ui-element-id="${ui_element.id}" data-vec-indx="11" class="input_el" value="${ui_element.buffer[11]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
							</div>
							<div class="input_vector">
								<input data-ui-element-id="${ui_element.id}" data-vec-indx="12" class="input_el" value="${ui_element.buffer[12]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
								<input data-ui-element-id="${ui_element.id}" data-vec-indx="13" class="input_el" value="${ui_element.buffer[13]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
								<input data-ui-element-id="${ui_element.id}" data-vec-indx="14" class="input_el" value="${ui_element.buffer[14]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
								<input data-ui-element-id="${ui_element.id}" data-vec-indx="15" class="input_el" value="${ui_element.buffer[15]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
							</div>
						</div>
					</fieldset>`;
				break;
		}
		var el_insert_to = document.getElementById("tab_body-4")	
		el_insert_to.insertAdjacentHTML('beforeend', fragment)
	}


	setbufferUIElement(ui_element, type){
		var type_to_choose = type || this.glEnum2String(ui_element.type_data);
		switch(type_to_choose){
			case "RAW_DATA":
				ui_element.buffer = new Float32Array([
					-1.0, 1.0,
					1.0, 1.0,
					-1.0, -1.0,
					-1.0, -1.0,
					1.0, 1.0,
					1.0, -1.0,
				])
				// Число элементов для одной вершины в буфере
				ui_element.size = 2;
				break;
			case "FLOAT":
				ui_element.buffer = 1.0;
				break;
			case "BOOL":
				ui_element.buffer = true;
				break;
			case "INT":
				ui_element.buffer = 1;
				break;
			case "FLOAT_VEC2":
				ui_element.buffer = [1.0, 1.0];
				break;
			case "FLOAT_VEC3":
				ui_element.buffer = [1.0, 1.0, 1.0];
				break;
			case "FLOAT_VEC4":
				ui_element.buffer = [1.0, 1.0, 1.0, 1.0];
				break;
			case "BOOL_VEC2":
				ui_element.buffer = [0, 0];
				break;
			case "BOOL_VEC3":
				ui_element.buffer = [0, 0, 0];
				break;
			case "BOOL_VEC4":
				ui_element.buffer = [0, 0, 0, 0];
				break;
			case "INT_VEC2":
				ui_element.buffer = [1, 1];
				break;
			case "INT_VEC3":
				ui_element.buffer = [1, 1, 1];
				break;
			case "INT_VEC4":
				ui_element.buffer = [1, 1, 1, 1];
				break;
			case "FLOAT_MAT2":
				ui_element.buffer = [
					1.0, 0.0, 
					0.0, 1.0];
				break;
			case "FLOAT_MAT3":
				ui_element.buffer = [
					1.0, 0.0, 0.0, 
					0.0, 1.0, 0.0,
					0.0, 0.0, 1.0];
				break;
			case "FLOAT_MAT4":
				ui_element.buffer = [
					1.0, 0.0, 0.0, 0.0, 
					0.0, 1.0, 0.0, 0.0,
					0.0, 0.0, 1.0, 0.0,
					0.0, 0.0, 0.0, 1.0];
				break;
		}
	}

	/*
	 *	Компилируем шейдерную программу
	 * */
	createProgram(gl, vertexShader, fragmentShader) {
		var program = gl.createProgram();
		gl.attachShader(program, vertexShader);
		gl.attachShader(program, fragmentShader);
		gl.linkProgram(program);
		var success = gl.getProgramParameter(program, gl.LINK_STATUS);
		if (success) {
		  return program;
		}
		 
		this.log(gl.getProgramInfoLog(program));
		gl.deleteProgram(program);
	}
	
	/*
	 *	Создаём шейдер из исходника
	 * */
	createShader(gl, type, source) {
		var shader = gl.createShader(type);   // создание шейдера
		gl.shaderSource(shader, source);      // устанавливаем шейдеру его программный код
		gl.compileShader(shader);             // компилируем шейдер
		var success = gl.getShaderParameter(shader, gl.COMPILE_STATUS);
		if (success) {                        // если компиляция прошла успешно - возвращаем шейдер
			return shader;
		}
 
		this.log(gl.getShaderInfoLog(shader));
		gl.deleteShader(shader);
	}
	
	/* 
	 * Читаем содержимое файла и возвращаем его как одну строку
	 * */
	readTextFile(file) {
		var rawFile = new XMLHttpRequest();
		var result = ""
		rawFile.open("GET", file, false);
		rawFile.onreadystatechange = function () {
		  if(rawFile.readyState === 4)  {
			if(rawFile.status === 200 || rawFile.status == 0) {
			  result = rawFile.responseText;
			 }
		  }
		}
		rawFile.send(null);
		return result
	}

	/*
	 *	Записывает ошибки в отдельный таб на странице
	 * */
	log(msg){
		var tab_button = document.getElementById("tab_button_for_err")
		tab_button.style.display = "flex"
		var container_to_paste = document.getElementById("tab_body-7")
		var element=`\n<div class="logs_and_erros">${msg}</div>`
		container_to_paste.insertAdjacentHTML('beforeend', element)
	}

	/*
	 *	Удаляет все записи в табе об ошибках
	 * */
	clearLog(){
		var tab_button = document.getElementById("tab_button_for_err")
		tab_button.style.display = "none"
		var container_to_paste = document.getElementById("tab_body-7")	
		container_to_paste.innerHTML = ''
	}

	/*
	 *	Обновляем время, юниформы(которые по-умолчанию тоже), viewport,
	 *	шейдерную программу.
	 *	И после отрисовкии делаем запрос следующего фрейма
	 * */
	update(time, inst){
		time *= 0.001;
		inst.deltaTime = time - inst.start;
		inst.start = time;

		resizeCanvasToDisplaySize(inst.canvas);
		// Tell WebGL how to convert from clip space to pixels
		inst.gl.viewport(0, 0, inst.gl.canvas.width, inst.gl.canvas.height);

		// Clear the canvas
		inst.gl.clearColor(inst.bg[0], inst.bg[1], inst.bg[2], inst.bg[3]);
		inst.gl.clear(inst.gl.COLOR_BUFFER_BIT | inst.gl.DEPTH_BUFFER_BIT);
		inst.gl.useProgram(inst.program);
		inst.gl.bindVertexArray(inst.vao);
		for (var i=0; i < inst.ui_elements.length; i++){
			inst.ui_elements[i].update()
		}
		inst.gl.uniform1f(inst.uTimeLoc, time);
		inst.gl.uniform2fv(inst.uResolutionLoc, [inst.gl.canvas.width, inst.gl.canvas.height]);
		inst.gl.uniform2fv(inst.uMousePosLoc, inst.mouse_pos);
		inst.draw(time)
		inst.request_animation_id = window.requestAnimationFrame((time) => this.update(time, inst))
	}

	/*
	 *	Производим отрисовку буфера
	 * */
	draw(time){

		var primitiveType = this.render_mode;
		var offset = 0;
		var count = this.ui_elements[this.default_geometry_data_indx].buffer.length / this.ui_elements[this.default_geometry_data_indx].size;
		this.gl.drawArrays(primitiveType, offset, count);
	}

	/*
	 *	Запрашивает первый фрейм для начала рендеринга
	 * */
	run(){
		this.request_animation_id = window.requestAnimationFrame((time) => this.update(time, this))
	}
}
let toy = new ShaderToy();
toy.run()
