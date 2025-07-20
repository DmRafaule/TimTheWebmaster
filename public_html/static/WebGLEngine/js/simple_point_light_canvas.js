/* Получаем WebGL2 контекст. Инициализируем WebGL2 */
var canvas = document.querySelector("#canvas");
var gl = canvas.getContext("webgl2");
/* Задаём параметры отрисовки */
// Все полигоны которые не видны, не будут отрисованы.
gl.enable(gl.CULL_FACE);
// Все пиксели которые находятся за другими пикселями не будут отрисованы.
gl.enable(gl.DEPTH_TEST);
if (!gl) {
	console.log("OpenGl is not avaiable")
}

/* Создаём шейдер */
// Получаем путь к исходникам шейдера. 
var vertexShaderPath = canvas.dataset.vertexShader
var fragmentShaderPath = canvas.dataset.fragmentShader
// Получаем содержание шейдера.
var vertexShaderSource = readTextFile(vertexShaderPath)
var fragmentShaderSource = readTextFile(fragmentShaderPath);
// Создаём программу на GPU. То есть шейдер.
var vertexShader = createShader(gl, gl.VERTEX_SHADER, vertexShaderSource);
var fragmentShader = createShader(gl, gl.FRAGMENT_SHADER, fragmentShaderSource);
var program = createProgram(gl, vertexShader, fragmentShader)

/* Получаем все необходимые атрибуты и юниформы шейдера */
// Получаем локацию атрибутов шейдера
var positionAttributeLocation = gl.getAttribLocation(program, "a_position");
var normalAttributeLocation = gl.getAttribLocation(program, "a_normal");
// Получаем локацию юниформ шейдера
var worldViewProjectionLocation = gl.getUniformLocation(program, "u_worldViewProjection");
var worldInverseTransposeLocation = gl.getUniformLocation(program, "u_worldInverseTranspose");
var colorLocation = gl.getUniformLocation(program, "u_color");
var reverseLightDirectionLocation = gl.getUniformLocation(program, "u_reverseLightDirection");
var lightWorldPositionLocation = gl.getUniformLocation(program, "u_lightWorldPosition");
var worldLocation = gl.getUniformLocation(program, "u_world");
var viewWorldPositionLocation = gl.getUniformLocation(program, "u_viewWorldPosition");
var shininessLocation = gl.getUniformLocation(program, "u_shininess");
var lightColorLocation = gl.getUniformLocation(program, "u_lightColor");
var specularColorLocation = gl.getUniformLocation(program, "u_specularColor");

/* Создание объекта */
// Создаём VAO
var vao = gl.createVertexArray();
// Устанавливаем его как текущего в использовании
gl.bindVertexArray(vao);

// Создаём буфер
var positionBuffer = gl.createBuffer();
// Связываем созданный буфер с ...
gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
// Включаем атрибут
gl.enableVertexAttribArray(positionAttributeLocation);
// Обозначаем то как читать данные из созданного буфера
var size = 3;          // Длина одного элемента в буфере
var type = gl.FLOAT;   // Тип данных в элементе буфера 
var normalize = false; // При использовании с gl.FLOAT не имеет эффекта
var stride = 0;        // Шаг к следующему элементу в буфере вычисляется: sizeof(type) * size
var offset = 0;        // Откуда начать читать буфер
gl.vertexAttribPointer(positionAttributeLocation, size, type, normalize, stride, offset);
// Отправляем данные в буфер
setGeometry(gl);


// Создаём буфер
var normalBuffer = gl.createBuffer();
// Связываем созданный буфер с ...
gl.bindBuffer(gl.ARRAY_BUFFER, normalBuffer);
// Включаем атрибут
gl.enableVertexAttribArray(normalAttributeLocation);
// Обозначаем то как читать данные из созданного буфера
var size = 3;          // Длина одного элемента в буфере
var type = gl.FLOAT;   // Тип данных в элементе буфера 
var normalize = false; // При использовании с gl.FLOAT не имеет эффекта
var stride = 0;        // Шаг к следующему элементу в буфере вычисляется: sizeof(type) * size
var offset = 0;        // Откуда начать читать буфер
gl.vertexAttribPointer(normalAttributeLocation, size, type, normalize, stride, offset);
// Отправляем данные в буфер
setNormals(gl);



var fieldOfViewRadians = Degree2Radian(60);
var fRotationRadians = 0;
var shininess = 1;
var specular = [1, 1, 1]
var lightColor = [1-245/255, 1-245/255, 1-66/255]

drawScene();



/* Создаём кнопки для взаимодействия с шейдром и его данными */
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

// Regulate shininess
slider_rotate_x = document.querySelector("#rotation-x")
slider_rotate_x.parentElement.previousElementSibling.textContent = "Shininess"
slider_rotate_x.addEventListener('input', function(){
	var factor = parseFloat(this.nextElementSibling.value)
	shininess = factor
	drawScene() 
})

// Rotate model
slider_rotate_y = document.querySelector("#rotation-y")
slider_rotate_y.addEventListener('input', function(){
	var degree = parseInt(this.nextElementSibling.value)
	fRotationRadians = Degree2Radian(degree)
	drawScene() 
})

// Regulate specular
slider_rotate_z = document.querySelector("#rotation-z")
slider_rotate_z.parentElement.previousElementSibling.textContent = "Specular"
slider_rotate_z.addEventListener('input', function(){
	var factor = parseFloat(this.nextElementSibling.value)
	specular = [0, factor, 1]
	drawScene() 
})

// Regulate lightColor
field_of_view = document.querySelector("#field-of-view")
field_of_view.parentElement.previousElementSibling.textContent = "Light color"
field_of_view.addEventListener('input', function(){
	var factor = parseFloat(this.nextElementSibling.value)
	lightColor = [1, factor, 0]
	drawScene() 
})

function makeZToWMatrix(fudgeFactor) {
  return [
	1, 0, 0, 0,
	0, 1, 0, 0,
	0, 0, 1, fudgeFactor,
	0, 0, 0, 1,
  ];
}

function setNormals(gl){
	var normals = new Float32Array([
		// left column front
        0, 0, 1,
        0, 0, 1,
        0, 0, 1,
        0, 0, 1,
        0, 0, 1,
        0, 0, 1,
 
        // top rung front
        0, 0, 1,
        0, 0, 1,
        0, 0, 1,
        0, 0, 1,
        0, 0, 1,
        0, 0, 1,
 
        // middle rung front
        0, 0, 1,
        0, 0, 1,
        0, 0, 1,
        0, 0, 1,
        0, 0, 1,
        0, 0, 1,
 
        // left column back
        0, 0, -1,
        0, 0, -1,
        0, 0, -1,
        0, 0, -1,
        0, 0, -1,
        0, 0, -1,
 
        // top rung back
        0, 0, -1,
        0, 0, -1,
        0, 0, -1,
        0, 0, -1,
        0, 0, -1,
        0, 0, -1,
 
        // middle rung back
        0, 0, -1,
        0, 0, -1,
        0, 0, -1,
        0, 0, -1,
        0, 0, -1,
        0, 0, -1,
 
        // top
        0, 1, 0,
        0, 1, 0,
        0, 1, 0,
        0, 1, 0,
        0, 1, 0,
        0, 1, 0,
 
        // top rung right
        1, 0, 0,
        1, 0, 0,
        1, 0, 0,
        1, 0, 0,
        1, 0, 0,
        1, 0, 0,
 
        // under top rung
        0, -1, 0,
        0, -1, 0,
        0, -1, 0,
        0, -1, 0,
        0, -1, 0,
        0, -1, 0,
 
        // between top rung and middle
        1, 0, 0,
        1, 0, 0,
        1, 0, 0,
        1, 0, 0,
        1, 0, 0,
        1, 0, 0,
 
        // top of middle rung
        0, 1, 0,
        0, 1, 0,
        0, 1, 0,
        0, 1, 0,
        0, 1, 0,
        0, 1, 0,
 
        // right of middle rung
        1, 0, 0,
        1, 0, 0,
        1, 0, 0,
        1, 0, 0,
        1, 0, 0,
        1, 0, 0,
 
        // bottom of middle rung.
        0, -1, 0,
        0, -1, 0,
        0, -1, 0,
        0, -1, 0,
        0, -1, 0,
        0, -1, 0,
 
        // right of bottom
        1, 0, 0,
        1, 0, 0,
        1, 0, 0,
        1, 0, 0,
        1, 0, 0,
        1, 0, 0,
 
        // bottom
        0, -1, 0,
        0, -1, 0,
        0, -1, 0,
        0, -1, 0,
        0, -1, 0,
        0, -1, 0,
 
        // left side
        -1, 0, 0,
        -1, 0, 0,
        -1, 0, 0,
        -1, 0, 0,
        -1, 0, 0,
		-1, 0, 0,
	]);
	gl.bufferData(gl.ARRAY_BUFFER, normals, gl.STATIC_DRAW);
}

function setGeometry(gl){
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
          0, 150,   0,
  ]);

  // Center the F around the origin and Flip it around. We do this because
  // we're in 3D now with and +Y is up where as before when we started with 2D
  // we had +Y as down.

  // We could do by changing all the values above but I'm lazy.
  // We could also do it with a matrix at draw time but you should
  // never do stuff at draw time if you can do it at init time.
  var matrix = math.xRotation(Math.PI);
  matrix = math.translate(matrix, -50, -75, -15);

  for (var ii = 0; ii < positions.length; ii += 3) {
    var vector = math.transformVector(matrix, [positions[ii + 0], positions[ii + 1], positions[ii + 2], 1]);
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

function drawScene() {
	resizeCanvasToDisplaySize(canvas);
	// Tell WebGL how to convert from clip space to pixels
    gl.viewport(0, 0, gl.canvas.width, gl.canvas.height);

    // Clear the canvas
    gl.clearColor(0, 0, 0, 0);
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

    // turn on depth testing
    gl.enable(gl.DEPTH_TEST);

    // tell webgl to cull faces
    gl.enable(gl.CULL_FACE);

    // Tell it to use our program (pair of shaders)
    gl.useProgram(program);

    // Bind the attribute/buffer set we want.
    gl.bindVertexArray(vao);

    // Compute the matrix
    var aspect = gl.canvas.clientWidth / gl.canvas.clientHeight;
    var zNear = 1;
    var zFar = 2000;
    var projectionMatrix = math.perspective(fieldOfViewRadians, aspect, zNear, zFar);

    // Compute the camera's matrix
    var camera = [100, 150, 200];
    var target = [0, 35, 0];
    var up = [0, 1, 0];
    var cameraMatrix = math.lookAt(camera, target, up);

    // Make a view matrix from the camera matrix.
    var viewMatrix = math.inverse(cameraMatrix);

    // create a viewProjection matrix. This will both apply perspective
    // AND move the world so that the camera is effectively the origin
    var viewProjectionMatrix = math.multiply4x4(projectionMatrix, viewMatrix);

    // Draw a F at the origin with rotation
    var matrix = math.yRotate(viewProjectionMatrix, fRotationRadians);

    var worldMatrix = math.yRotation(fRotationRadians);
    var worldViewProjectionMatrix = math.multiply4x4(viewProjectionMatrix,worldMatrix);
	var worldInverseMatrix = math.inverse(worldMatrix);
	var worldInverseTransposeMatrix = math.transpose(worldInverseMatrix);
     
    // Set the matrices
	gl.uniformMatrix4fv(worldLocation, false, worldMatrix);
    gl.uniformMatrix4fv(worldViewProjectionLocation, false, worldViewProjectionMatrix);
	gl.uniformMatrix4fv(worldInverseTransposeLocation, false, worldInverseTransposeMatrix);
	// Set the light positon
	gl.uniform3fv(lightWorldPositionLocation, [20, 30, 50]);
	gl.uniform3fv(lightColorLocation, lightColor);
	gl.uniform3fv(specularColorLocation, specular);
	gl.uniform1f(shininessLocation, shininess);

    // Set the color to use
    gl.uniform4fv(colorLocation, [0.2, 1, 0.2, 1]); // green

    // set the light direction.
    gl.uniform3fv(reverseLightDirectionLocation, math.normalize([0.5, 0.7, 1]));
	gl.uniform3fv(viewWorldPositionLocation, camera);

    // Draw the geometry.
    var primitiveType = gl.TRIANGLES;
    var offset = 0;
    var count = 16 * 6;
    gl.drawArrays(primitiveType, offset, count);
}



