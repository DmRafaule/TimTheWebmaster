function makeZToWMatrix(fudgeFactor) {
  return [
	1, 0, 0, 0,
	0, 1, 0, 0,
	0, 0, 1, fudgeFactor,
	0, 0, 0, 1,
  ];
}
function SetColorbuffer(gl){
 gl.bufferData(
      gl.ARRAY_BUFFER,
      new Uint8Array([
          // left column front
        200,  70, 120,
        200,  70, 120,
        200,  70, 120,
        200,  70, 120,
        200,  70, 120,
        200,  70, 120,

          // top rung front
        200,  70, 120,
        200,  70, 120,
        200,  70, 120,
        200,  70, 120,
        200,  70, 120,
        200,  70, 120,

          // middle rung front
        200,  70, 120,
        200,  70, 120,
        200,  70, 120,
        200,  70, 120,
        200,  70, 120,
        200,  70, 120,

          // left column back
        80, 70, 200,
        80, 70, 200,
        80, 70, 200,
        80, 70, 200,
        80, 70, 200,
        80, 70, 200,

          // top rung back
        80, 70, 200,
        80, 70, 200,
        80, 70, 200,
        80, 70, 200,
        80, 70, 200,
        80, 70, 200,

          // middle rung back
        80, 70, 200,
        80, 70, 200,
        80, 70, 200,
        80, 70, 200,
        80, 70, 200,
        80, 70, 200,

          // top
        70, 200, 210,
        70, 200, 210,
        70, 200, 210,
        70, 200, 210,
        70, 200, 210,
        70, 200, 210,

          // top rung right
        200, 200, 70,
        200, 200, 70,
        200, 200, 70,
        200, 200, 70,
        200, 200, 70,
        200, 200, 70,

          // under top rung
        210, 100, 70,
        210, 100, 70,
        210, 100, 70,
        210, 100, 70,
        210, 100, 70,
        210, 100, 70,

          // between top rung and middle
        210, 160, 70,
        210, 160, 70,
        210, 160, 70,
        210, 160, 70,
        210, 160, 70,
        210, 160, 70,

          // top of middle rung
        70, 180, 210,
        70, 180, 210,
        70, 180, 210,
        70, 180, 210,
        70, 180, 210,
        70, 180, 210,

          // right of middle rung
        100, 70, 210,
        100, 70, 210,
        100, 70, 210,
        100, 70, 210,
        100, 70, 210,
        100, 70, 210,

          // bottom of middle rung.
        76, 210, 100,
        76, 210, 100,
        76, 210, 100,
        76, 210, 100,
        76, 210, 100,
        76, 210, 100,

          // right of bottom
        140, 210, 80,
        140, 210, 80,
        140, 210, 80,
        140, 210, 80,
        140, 210, 80,
        140, 210, 80,

          // bottom
        90, 130, 110,
        90, 130, 110,
        90, 130, 110,
        90, 130, 110,
        90, 130, 110,
        90, 130, 110,

          // left side
        160, 160, 220,
        160, 160, 220,
        160, 160, 220,
        160, 160, 220,
        160, 160, 220,
        160, 160, 220]),
      gl.STATIC_DRAW);
}


function CreateF_Letter3d(gl){
	var positions = new Float32Array([
          // left column front
          0,   0,  0,
          0, 150,  0,
          30,   0,  0,
          0, 150,  0,
          30, 150,  0,
          30,   0,  0,

          // top rung front
          30,   0,  0,
          30,  30,  0,
          100,   0,  0,
          30,  30,  0,
          100,  30,  0,
          100,   0,  0,

          // middle rung front
          30,  60,  0,
          30,  90,  0,
          67,  60,  0,
          30,  90,  0,
          67,  90,  0,
          67,  60,  0,

          // left column back
            0,   0,  30,
           30,   0,  30,
            0, 150,  30,
            0, 150,  30,
           30,   0,  30,
           30, 150,  30,

          // top rung back
           30,   0,  30,
          100,   0,  30,
           30,  30,  30,
           30,  30,  30,
          100,   0,  30,
          100,  30,  30,

          // middle rung back
           30,  60,  30,
           67,  60,  30,
           30,  90,  30,
           30,  90,  30,
           67,  60,  30,
           67,  90,  30,

          // top
            0,   0,   0,
          100,   0,   0,
          100,   0,  30,
            0,   0,   0,
          100,   0,  30,
            0,   0,  30,

          // top rung right
          100,   0,   0,
          100,  30,   0,
          100,  30,  30,
          100,   0,   0,
          100,  30,  30,
          100,   0,  30,

          // under top rung
          30,   30,   0,
          30,   30,  30,
          100,  30,  30,
          30,   30,   0,
          100,  30,  30,
          100,  30,   0,

          // between top rung and middle
          30,   30,   0,
          30,   60,  30,
          30,   30,  30,
          30,   30,   0,
          30,   60,   0,
          30,   60,  30,

          // top of middle rung
          30,   60,   0,
          67,   60,  30,
          30,   60,  30,
          30,   60,   0,
          67,   60,   0,
          67,   60,  30,

          // right of middle rung
          67,   60,   0,
          67,   90,  30,
          67,   60,  30,
          67,   60,   0,
          67,   90,   0,
          67,   90,  30,

          // bottom of middle rung.
          30,   90,   0,
          30,   90,  30,
          67,   90,  30,
          30,   90,   0,
          67,   90,  30,
          67,   90,   0,

          // right of bottom
          30,   90,   0,
          30,  150,  30,
          30,   90,  30,
          30,   90,   0,
          30,  150,   0,
          30,  150,  30,

          // bottom
          0,   150,   0,
          0,   150,  30,
          30,  150,  30,
          0,   150,   0,
          30,  150,  30,
          30,  150,   0,

          // left side
          0,   0,   0,
          0,   0,  30,
          0, 150,  30,
          0,   0,   0,
          0, 150,  30,
          0, 150,   0]);
  // Center the F around the origin and Flip it around. We do this because
  // we're in 3D now with and +Y is up where as before when we started with 2D
  // we had +Y as down.

  // We could do by changing all the values above but I'm lazy.
  // We could also do it with a matrix at draw time but you should
  // never do stuff at draw time if you can do it at init time.
  var matrix = math.xRotation(Math.PI);
  matrix = math.translate(matrix, -50, -75, -15);

  for (var ii = 0; ii < positions.length; ii += 3) {
    var vector = math.vectorMultiply([positions[ii + 0], positions[ii + 1], positions[ii + 2], 1], matrix);
    positions[ii + 0] = vector[0];
    positions[ii + 1] = vector[1];
    positions[ii + 2] = vector[2];
  }
  gl.bufferData(gl.ARRAY_BUFFER, positions, gl.STATIC_DRAW);
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
	resizeCanvasToDisplaySize(gl.canvas)
	gl.viewport(0, 0, gl.canvas.width, gl.canvas.height);
	gl.clearColor(0, 0, 0, 0);
	gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
	gl.useProgram(program);

	gl.enableVertexAttribArray(positionAttributeLocation);
	gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
	var size = 3;          // 3 компоненты на итерацию
	var type = gl.FLOAT;   // наши данные - 32-битные числа с плавающей точкой
	var normalize = false; // не нормализовать данные
	var stride = 0;        // 0 = перемещаться на size * sizeof(type) каждую итерацию для получения следующего положения
	var offset = 0;        // начинать с начала буфера
	gl.vertexAttribPointer(positionAttributeLocation, size, type, normalize, stride, offset)
	// Send color to gpu
    gl.enableVertexAttribArray(colorAttributeLocation);
    gl.bindBuffer(gl.ARRAY_BUFFER, colorBuffer);
    var size = 3;
    var type = gl.UNSIGNED_BYTE;
    var normalize = true;
    var stride = 0;
    var offset = 0;
    gl.vertexAttribPointer(
        colorAttributeLocation, size, type, normalize, stride, offset)



 	// Multiply the matrices.
	var aspect = gl.canvas.clientWidth / gl.canvas.clientHeight;
	var projectionMatrix = math.perspective(fieldOfView, aspect, zNear, zFar);
	console.log(projectionMatrix)

	var numFs = 5;
	var radius = 200;
	// Вычисление матрицы камеры
	var cameraMatrix = math.yRotation(cameraAngle);
	cameraMatrix = math.translate(cameraMatrix, 0, 0, radius * 1.5);
	var viewMatrix = math.inverse(cameraMatrix);
	var viewProjectionMatrix = math.multiply4x4(projectionMatrix, viewMatrix);
	console.log(viewMatrix)

	for (var ii = 0; ii < numFs; ++ii) {
    	var angle = ii * Math.PI * 2 / numFs;
    	var x = Math.cos(angle) * radius;
    	var y = Math.sin(angle) * radius;

    	// starting with the view projection matrix
    	// compute a matrix for the F
    	var matrix = math.translate(viewProjectionMatrix, x, 0, y);

    	// Set the matrix.
    	gl.uniformMatrix4fv(matrixUniformLocation, false, matrix);

    	// Draw the geometry.
    	var primitiveType = gl.TRIANGLES;
    	var offset = 0;
    	var count = 16 * 6;
    	gl.drawArrays(primitiveType, offset, count);
    }

}

var canvas = document.querySelector("#canvas");
var gl = canvas.getContext("webgl");
// Will not see unseen faces
gl.enable(gl.CULL_FACE);
// Will not see pixels that behind other pixels
gl.enable(gl.DEPTH_TEST);
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
var colorAttributeLocation	= gl.getAttribLocation(program, "a_color");
var matrixUniformLocation		= gl.getUniformLocation(program, "u_matrix");
var positionBuffer = gl.createBuffer();
gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);

var cameraAngle = 0
var fieldOfView = Degree2Radian(60) // In radian
var zNear = 1;
var zFar = 2000;
var translation = [0, 0, -400];
var rotation = [1, 1, 1];
var scale = [1, 1, 1];
var width = 100;
var height = 30;
var color = [Math.random(), Math.random(), Math.random(), 1];
// Make initial draw call
CreateF_Letter3d(gl)

var colorBuffer = gl.createBuffer();
gl.bindBuffer(gl.ARRAY_BUFFER, colorBuffer);
SetColorbuffer(gl)

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

slider_transform_z = document.querySelector("#transform-z")
slider_transform_z.addEventListener('input', function(){
	var value = parseInt(this.nextElementSibling.value)
	translation[2] = value
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

slider_rotate_x = document.querySelector("#rotation-x")
slider_rotate_x.addEventListener('input', function(){
	var degree = parseInt(this.nextElementSibling.value)
	rotation[0] = Degree2Radian(degree)
	drawScene() 
})

slider_rotate_y = document.querySelector("#rotation-y")
slider_rotate_y.addEventListener('input', function(){
	var degree = parseInt(this.nextElementSibling.value)
	cameraAngle = Degree2Radian(degree)
	drawScene() 
})

slider_rotate_z = document.querySelector("#rotation-z")
slider_rotate_z.addEventListener('input', function(){
	var degree = parseInt(this.nextElementSibling.value)
	rotation[2] = Degree2Radian(degree)
	drawScene() 
})

field_of_view = document.querySelector("#field-of-view")
field_of_view.addEventListener('input', function(){
	var degree = parseInt(this.nextElementSibling.value)
	fieldOfView = Degree2Radian(degree)
	drawScene() 
})

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
