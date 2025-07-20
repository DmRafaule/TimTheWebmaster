function CreateRectangle(gl, x, y, width, height){
	var x1 = x;
	var x2 = x + width;
	var y1 = y;
	var y2 = y + height;
 
	gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([
	   x1, y1,
	   x2, y1,
	   x1, y2,
	   x1, y2,
	   x2, y1,
	   x2, y2]), gl.STATIC_DRAW);
}
function createShader(gl, type, source) {
	var shader = gl.createShader(type);   // создание шейдера
	gl.shaderSource(shader, source);      // устанавливаем шейдеру его программный код
	gl.compileShader(shader);             // компилируем шейдер
	var success = gl.getShaderParameter(shader, gl.COMPILE_STATUS);
	if (success) {                        // если компиляция прошла успешно - возвращаем шейдер
		return shader;
	}
 
	console.log(gl.getShaderInfoLog(shader));
	gl.deleteShader(shader);
}
function readTextFile(file) {
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

function createProgram(gl, vertexShader, fragmentShader) {
	var program = gl.createProgram();
    gl.attachShader(program, vertexShader);
    gl.attachShader(program, fragmentShader);
    gl.linkProgram(program);
    var success = gl.getProgramParameter(program, gl.LINK_STATUS);
    if (success) {
      return program;
    }
     
    console.log(gl.getProgramInfoLog(program));
    gl.deleteProgram(program);
}

var canvas = document.querySelector("#canvas");
var gl = canvas.getContext("webgl");

if (!gl) {
	console.log("OpenGl is not avaiable")
}


// Obtain the paths of shaders
var vertexShaderPath = canvas.dataset.vertexShader
var fragmentShaderPath = canvas.dataset.fragmentShader
// Obtain the source of shaders
var vertexShaderSource = readTextFile(vertexShaderPath)
var fragmentShaderSource = readTextFile(fragmentShaderPath);
// Create shader programs 
var vertexShader = createShader(gl, gl.VERTEX_SHADER, vertexShaderSource);
var fragmentShader = createShader(gl, gl.FRAGMENT_SHADER, fragmentShaderSource);
// Link gl and compiled shader programs
var program = createProgram(gl, vertexShader, fragmentShader);
// Get position
var positionAttributeLocation = gl.getAttribLocation(program, "a_position");
var resolutionUniformLocation = gl.getUniformLocation(program, "u_resolution");
var colorUniformLocation = gl.getUniformLocation(program, "u_color");
var positionBuffer = gl.createBuffer();
gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);

CreateRectangle(gl, 100, 100, 200, 50)

gl.viewport(0, 0, gl.canvas.width, gl.canvas.height);
gl.clearColor(0, 0, 0, 0);
gl.clear(gl.COLOR_BUFFER_BIT);
gl.useProgram(program);
gl.enableVertexAttribArray(positionAttributeLocation);
gl.uniform2f(resolutionUniformLocation, gl.canvas.width, gl.canvas.height);
gl.uniform4f(colorUniformLocation, Math.random(), Math.random(), Math.random(), Math.random());
gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
 
var size = 2;          // 2 компоненты на итерацию
var type = gl.FLOAT;   // наши данные - 32-битные числа с плавающей точкой
var normalize = false; // не нормализовать данные
var stride = 0;        // 0 = перемещаться на size * sizeof(type) каждую итерацию для получения следующего положения
var offset = 0;        // начинать с начала буфера
gl.vertexAttribPointer(positionAttributeLocation, size, type, normalize, stride, offset)
var primitiveType = gl.TRIANGLES;
var offset = 0;
var count = 6;
gl.drawArrays(primitiveType, offset, count);
