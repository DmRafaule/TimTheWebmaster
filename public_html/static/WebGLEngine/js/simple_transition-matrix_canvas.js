function CreateF_Letter(gl){
  gl.bufferData(
      gl.ARRAY_BUFFER,
      new Float32Array([
          // left column
          0, 0,
          30, 0,
          0, 150,
          0, 150,
          30, 0,
          30, 150,
 
          // top rung
          30, 0,
          100, 0,
          30, 30,
          30, 30,
          100, 0,
          100, 30,
 
          // middle rung
          30, 60,
          67, 60,
          30, 90,
          30, 90,
          67, 60,
          67, 90,
      ]),
      gl.STATIC_DRAW);
}

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
function CreateTriangle(gl, points){
	var x1 = points[0];
	var y1 = points[1];
	var x2 = points[2];
	var y2 = points[3];
	var x3 = points[4];
	var y3 = points[5];
 
	gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([
	   x1, y1,
	   x2, y2,
	   x3, y3,
	   ]), gl.STATIC_DRAW);
}


function Degree2Radian(degree){
	return degree * Math.PI/180
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

function drawScene() {
	gl.viewport(0, 0, gl.canvas.width, gl.canvas.height);
	gl.clearColor(0, 0, 0, 0);
	gl.clear(gl.COLOR_BUFFER_BIT);
	gl.useProgram(program);
	gl.enableVertexAttribArray(positionAttributeLocation);
	gl.uniform2f(resolutionUniformLocation, gl.canvas.width, gl.canvas.height);
	gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);

	var size = 2;          // 2 компоненты на итерацию
	var type = gl.FLOAT;   // наши данные - 32-битные числа с плавающей точкой
	var normalize = false; // не нормализовать данные
	var stride = 0;        // 0 = перемещаться на size * sizeof(type) каждую итерацию для получения следующего положения
	var offset = 0;        // начинать с начала буфера
	gl.vertexAttribPointer(positionAttributeLocation, size, type, normalize, stride, offset)
	gl.uniform4fv(colorLocation, color);
	// Compute the matrices
	// Compute the matrices
	var projectionMatrix = math.projection(gl.canvas.clientWidth, gl.canvas.clientHeight);
  	var translationMatrix = math.translation(translation[0], translation[1])
  	var rotationMatrix = math.rotation(rotation)
  	var scaleMatrix = math.scaling(scale[0],scale[1])
	// make a matrix that will move the origin of the 'F' to its center.
	var moveOriginMatrix = math.translation(-50, -75);
 	// Multiply the matrices.
 	var matrix = math.multiply(projectionMatrix, translationMatrix);
 	matrix = math.multiply(matrix, rotationMatrix);
 	matrix = math.multiply(matrix, scaleMatrix);
	matrix = math.multiply(matrix, moveOriginMatrix);
 
  	// Set the matrix.
  	gl.uniformMatrix3fv(matrixUniformLocation, false, matrix);

	// Make draw call
	gl.drawArrays(gl.TRIANGLES, 0, 18);

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
var positionAttributeLocation	= gl.getAttribLocation(program, "a_position");
var resolutionUniformLocation	= gl.getUniformLocation(program, "u_resolution");
var matrixUniformLocation		= gl.getUniformLocation(program, "u_matrix");
var colorLocation				= gl.getUniformLocation(program, "u_color");
var positionBuffer = gl.createBuffer();
gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);


var translation = [300, 300];
var rotation = 0;
var scale = [1, 1];
var width = 100;
var height = 30;
var color = [Math.random(), Math.random(), Math.random(), 1];
// Make initial draw call
CreateF_Letter(gl)
drawScene();




slider_transform_y = document.querySelector("#transform-y")
slider_transform_y.addEventListener('input', function(){
	var value = parseInt(this.nextElementSibling.value)
	translation[1] = value
	drawScene() 
})

slider_transform_x = document.querySelector("#transform-x")
slider_transform_x.addEventListener('input', function(){
	var value = parseInt(this.nextElementSibling.value)
	translation[0] = value
	drawScene() 
})

slider_scale_x = document.querySelector("#scale-x")
slider_scale_x.addEventListener('input', function(){
	var factor = parseFloat(this.nextElementSibling.value)
	scale[0] = factor 
	drawScene() 
})

slider_scale_y = document.querySelector("#scale-y")
slider_scale_y.addEventListener('input', function(){
	var factor = parseFloat(this.nextElementSibling.value)
	scale[1] = factor 
	drawScene() 
})

slider_rotate = document.querySelector("#rotation")
slider_rotate.addEventListener('input', function(){
	var degree = parseInt(this.nextElementSibling.value)
	rotation = Degree2Radian(degree)
	drawScene() 
})
