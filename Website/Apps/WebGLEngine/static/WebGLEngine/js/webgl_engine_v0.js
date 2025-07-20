/*
 * WebDI Это мой ренденер для веба. Первая, самая простая версия. v0
 * Ключевые особенности этой версии рендерена:
 *		1) Instancing drawing
 *		2) Использует в качестве основной функции отрисовки drawElementsInstanced 
 *		3) Может отрисовывать простую геометрию, линиями, точками, полигонами. Без теней и прочего
 *
 * */

class DI {
	constructor(canvas){
		/*	Создаём обозреватель для того чтобы знать,
		*	когда можно прекратить отрисовку и обновление
		*/
		var options = {
			threshold: 0.01,
		};
		var canvas_observer = new IntersectionObserver((entries, observer) => {
		  for (const entry of entries) {
			// Check if the entry is intersecting the viewport
			if (entry.isIntersecting) {
				this.request_animation_id = requestAnimationFrame((time) => this.Scene(time, this))
			}
			else{
				cancelAnimationFrame(this.request_animation_id);
			}
		  }
		}, options);
		canvas_observer.observe(canvas);
		/* Задаём поля класса */
		this.curr = null
		this.attributes = {}
		this.uniforms = {}
		this.primitives = []
		/* Создаём WebGL контекст для переданного холста */
		this.context = canvas.getContext("webgl2");
		if (!this.context) {
			console.log("OpenGl is not avaiable")
		}
		/* Задаём параметры отрисовки */
		// Все полигоны которые не видны, не будут отрисованы.
		this.context.enable(this.context.CULL_FACE);
		// Все пиксели которые находятся за другими пикселями не будут отрисованы.
		this.context.enable(this.context.DEPTH_TEST);
		/* Создаём шейдер */
		// Получаем путь к исходникам шейдера. 
		var vertexShaderPath = canvas.dataset.vertexShader
		var fragmentShaderPath = canvas.dataset.fragmentShader
		// Получаем содержание шейдера.
		var vertexShaderSource = U.readTextFile(vertexShaderPath)
		var fragmentShaderSource = U.readTextFile(fragmentShaderPath);
		// Создаём программу на GPU. То есть шейдер.
		var vertexShader = U.createShader(this.context, this.context.VERTEX_SHADER, vertexShaderSource);
		var fragmentShader = U.createShader(this.context, this.context.FRAGMENT_SHADER, fragmentShaderSource);
		this.program = U.createProgram(this.context, vertexShader, fragmentShader)
	}

	get gl(){
		return this.context;
	}

	SetContext(gl){
		this.context = gl;
	}

	SetProgram(program){
		this.program = program;
	}

	SetUniform(uniform_name){
		this.uniforms[uniform_name] = this.context.getUniformLocation(this.program, uniform_name);
	}

	SetAttribute(attribute_name){
		this.attributes[attribute_name] = this.context.getAttribLocation(this.program, attribute_name);
	}

	StartVAO(primitive, mode){
		var vao = this.context.createVertexArray();
		// Устанавливаем его как текущего в использовании
		this.curr = this.primitives.length;
		this.context.bindVertexArray(vao);
		this.primitives.push({
			vao: vao,
			P: [],
			mode: mode,
			vertices: primitive.vertices,
			indices: primitive.indices,
			num_indices: primitive.num_indices,
			matrices: null,
			matrixData: null,
			matrixBuffer: null,
			numInstances: null,
		})
	}

	/*
	 * @args
	 * primitive_data is dict
	 *	*	supported key-value paires:
	 *			pos: [x,y,z]			[Optional]
	 *			color: [r,g,b,a]		[Optional]
	 *			scale: [f1,f2,f3]		[Optional]
	 *			rotate: [f1,f2,f3]		[Optional]
	 *			rotateAngle: angle		[Optional]
	 *			point_size: float		[Optional]
	 *			animation: callback		[Optional]
	 *			animation_args: ARGV	[Optional]
	 * */
	SetPrimitive(primitive_data={}){
		// Задаём позицию по умолчанию 
		primitive_data.pos			= primitive_data.pos || [0,0,0];
		// Задаём цвет по умолчанию
		primitive_data.color		= primitive_data.color || [0.2,0.2,0.2,1];
		// Задаём размер по умолчанию 
		primitive_data.scale		= primitive_data.scale || [1,1,1];
		// Задаём то что будем вращать
		primitive_data.rotate		= primitive_data.rotate || [0,0,0];
		// Задаём то на сколько вращать 
		primitive_data.rotateAngle	= primitive_data.rotateAngle || 0;
		// Задаём пустой коллбэк
		primitive_data.animation	= primitive_data.animation || function(){};
		// Увеличиваем количество для создания
		this.primitives[this.curr].numInstances++;
		this.primitives[this.curr].P.push(primitive_data)
		// Создаём буфер для позиций вершин
		var positionBuffer = this.context.createBuffer();
		// Связываем созданный буфер с ...
		this.context.bindBuffer(this.context.ARRAY_BUFFER, positionBuffer);
		// Включаем атрибут
		this.context.enableVertexAttribArray(this.attributes.a_position);
		// Обозначаем то как читать данные из созданного буфера
		var size = 3;          // Длина одного элемента в буфере
		var type = this.context.FLOAT;   // Тип данных в элементе буфера 
		var normalize = false; // При использовании с gl.FLOAT не имеет эффекта
		var stride = 0;        // Шаг к следующему элементу в буфере вычисляется: sizeof(type) * size
		var offset = 0;        // Откуда начать читать буфер
		this.context.vertexAttribPointer(this.attributes.a_position, size, type, normalize, stride, offset);
		// Отправляем данные в буфер
		this.context.bufferData(this.context.ARRAY_BUFFER, this.primitives[this.curr].vertices, this.context.STATIC_DRAW);

		// Создаём буфер вершин
		var indexBuffer = this.context.createBuffer();
		// Связываем созданный буфер с ...
		this.context.bindBuffer(this.context.ELEMENT_ARRAY_BUFFER, indexBuffer);
		this.context.bufferData(this.context.ELEMENT_ARRAY_BUFFER, this.primitives[this.curr].indices, this.context.STATIC_DRAW);

	}

	EndVAO(){
		// Создаём буфер атрибута для хранения mvp (model view projection матрицы), mat4x4
		var matrixLength = 16;
		this.primitives[this.curr].matrixData = new Float32Array(this.primitives[this.curr].numInstances * matrixLength);
		this.primitives[this.curr].matrices = [];
		for (let i = 0; i < this.primitives[this.curr].numInstances; ++i) {
		  	const byteOffsetToMatrix = i * matrixLength * 4;
		  	const numFloatsForView = matrixLength;
		  	this.primitives[this.curr].matrices.push(new Float32Array(
				this.primitives[this.curr].matrixData.buffer,
				byteOffsetToMatrix,
				numFloatsForView
			));
		}
		this.primitives[this.curr].matrixBuffer = this.context.createBuffer();
		this.context.bindBuffer(this.context.ARRAY_BUFFER, this.primitives[this.curr].matrixBuffer);
		// Выделяем память
		this.context.bufferData(this.context.ARRAY_BUFFER, this.primitives[this.curr].matrixData.byteLength, this.context.STATIC_DRAW);
		var bytesPerMatrix = 4 * 16;
		for (let i = 0; i < 4; ++i) {
		  const loc = this.attributes.a_mvp + i;
		  this.context.enableVertexAttribArray(loc);
		  const offset = i * 16;  // 4 floats на ряд каждый float по 4 байта
		  this.context.vertexAttribPointer(loc, 4, this.context.FLOAT, false,bytesPerMatrix, offset,);
		  // Данный аттрибут изменяется для каждого instance
		  this.context.vertexAttribDivisor(loc, 1);
		}


		// Создаём буфер аттрибута для хранения цвета vec4
		const colorBuffer = this.context.createBuffer();
		var colorData = new Float32Array(this.primitives[this.curr].numInstances * 4);
		for (var i = 0; i < this.primitives[this.curr].numInstances; i++){
			var colors = this.primitives[this.curr].P[i].color;
			colorData[0 + 4*i] = colors[0];
			colorData[1 + 4*i] = colors[1];
			colorData[2 + 4*i] = colors[2];
			colorData[3 + 4*i] = colors[3];
		}
		this.context.bindBuffer(this.context.ARRAY_BUFFER, colorBuffer);
		this.context.bufferData(this.context.ARRAY_BUFFER,colorData,this.context.STATIC_DRAW);
		this.context.enableVertexAttribArray(this.attributes.a_color);
		this.context.vertexAttribPointer(this.attributes.a_color, 4, this.context.FLOAT, false, 0, 0);
		  // Данный аттрибут изменяется для каждого instance
		this.context.vertexAttribDivisor(this.attributes.a_color, 1);
		

		// Создаём буфер для размера точки
		var pointBuffer = this.context.createBuffer();
		var point_size =  new Float32Array(this.primitives[this.curr].numInstances * 1);
		for (var i = 0; i < this.primitives[this.curr].numInstances; i++){
			point_size[i] = this.primitives[this.curr].P[i].point_size;
		}

		// Связываем созданный буфер с ...
		this.context.bindBuffer(this.context.ARRAY_BUFFER, pointBuffer);
		this.context.bufferData(this.context.ARRAY_BUFFER, point_size , this.context.STATIC_DRAW);
		this.context.enableVertexAttribArray(this.attributes.a_pointSize);
		this.context.vertexAttribPointer(this.attributes.a_pointSize, 1, this.context.FLOAT, false, 0, 0);
		// this line says this attribute only changes for each 1 instance
		this.context.vertexAttribDivisor(this.attributes.a_pointSize, 1);
	}

	Scene(time, obj){
		time *= 0.001;
		var deltaTime = time - start;
		start = time;
		/* Подготовка холста. Установление его размеров, цвета заднего фона, и обновления */
		U.resizeCanvasToDisplaySize(obj.gl.canvas);
		obj.gl.viewport(0, 0, obj.gl.canvas.clientWidth, obj.gl.canvas.clientHeight);
		obj.gl.clearColor(0, 0, 0, 0);
		obj.gl.clear(obj.gl.COLOR_BUFFER_BIT | obj.gl.DEPTH_BUFFER_BIT);
		obj.Draw(time)

		obj.request_animation_id = requestAnimationFrame((time) => this.Scene(time, obj))
	}

	Draw(time){
		// Указываем какую шейдерную программу использовать
		this.context.useProgram(this.program);
		for (var i = 0; i < this.primitives.length; i++){

			/* Указываем какой объект собираемся рисовать */
			this.context.bindVertexArray(this.primitives[i].vao);
			// Вычисление матрицы мира и объектов
			// Вычисляем матрицу проекции
			var aspect = this.context.canvas.clientWidth / this.context.canvas.clientHeight;
			var projectionMatrix = M.perspective(fieldOfViewRadians, aspect, zNear, zFar);
			// Вычисляем матрицу камеры ( или view matrix)
			var cameraMatrix = M.translation(cameraPosition[0], cameraPosition[1], cameraPosition[2]);
			// Перемножаем матрицы проекции и камеры 
			var mvp = M.multiplyM(projectionMatrix, cameraMatrix)
			// Вычисляем матрицу объекта
			this.primitives[i].matrices.forEach((mat, ndx) => {
				// Задаём матрицу модели
				M.identity(mat);
				// Вычисляем первоначальное положение
				var pos = this.primitives[i].P[ndx].pos;
				var m_translation = M.translation(pos[0], pos[1], pos[2])
				M.multiplyM(mat,m_translation,mat)
				// Вычисляем первоначальный поворот
				var rotateAngle = this.primitives[i].P[ndx].rotateAngle;
				var toRotate = this.primitives[i].P[ndx].rotate
				var angle = M.Degree2Radian(rotateAngle)
				var m_xrotation = M.xRotation(angle * toRotate[0])
				M.multiplyM(mat,m_xrotation,mat)
				var m_yrotation = M.yRotation(angle * toRotate[1])
				M.multiplyM(mat,m_yrotation,mat)
				var m_zrotation = M.zRotation(angle * toRotate[2])
				M.multiplyM(mat,m_zrotation,mat)
				// Вычисляем первоначальный размер
				var scale = this.primitives[i].P[ndx].scale;
				var m_scaling = M.scaling(scale[0], scale[1], scale[2])
				M.multiplyM(mat,m_scaling,mat)
				// Запускаем анимацию
				this.primitives[i].P[ndx].animation(time,mat,ndx, this.primitives[i].P[ndx].animation_args);
				// Перемножаем матрицу mvp и модели 
				M.multiplyM(mvp, mat, mat)
			});
			this.context.bindBuffer(this.context.ARRAY_BUFFER, this.primitives[i].matrixBuffer);
			this.context.bufferSubData(this.context.ARRAY_BUFFER, 0, this.primitives[i].matrixData);

			this.context.drawElementsInstanced(this.primitives[i].mode, this.primitives[i].num_indices, this.context.UNSIGNED_SHORT, 0, this.primitives[i].numInstances);

		}
	}
}

var M = {
	identity: function(dst) {
		dst = dst || new Float32Array(16);

		dst[ 0] = 1;
		dst[ 1] = 0;
		dst[ 2] = 0;
		dst[ 3] = 0;
		dst[ 4] = 0;
		dst[ 5] = 1;
		dst[ 6] = 0;
		dst[ 7] = 0;
		dst[ 8] = 0;
		dst[ 9] = 0;
		dst[10] = 1;
		dst[11] = 0;
		dst[12] = 0;
		dst[13] = 0;
		dst[14] = 0;
		dst[15] = 1;

		return dst;
	},
	perspective: function(fieldOfViewInRadians, aspect, near, far) {
		var f = Math.tan(Math.PI * 0.5 - 0.5 * fieldOfViewInRadians);
		var rangeInv = 1.0 / (near - far);
	 
		return [
			f / aspect, 0, 0, 0,
			0, f, 0, 0,
			0, 0, (near + far) * rangeInv, -1,
			0, 0, near * far * rangeInv * 2, 0
		];
	},
	orthographic: function(left, right, bottom, top, near, far) {
		return [
			2 / (right - left), 0, 0, 0,
			0, 2 / (top - bottom), 0, 0,
			0, 0, 2 / (near - far), 0,
	 
			(left + right) / (left - right),
			(bottom + top) / (bottom - top),
			(near + far) / (near - far),
			1,
		];
	},
	inverse: function(m) {
    	var m00 = m[0 * 4 + 0];
    	var m01 = m[0 * 4 + 1];
    	var m02 = m[0 * 4 + 2];
    	var m03 = m[0 * 4 + 3];
    	var m10 = m[1 * 4 + 0];
    	var m11 = m[1 * 4 + 1];
    	var m12 = m[1 * 4 + 2];
    	var m13 = m[1 * 4 + 3];
    	var m20 = m[2 * 4 + 0];
    	var m21 = m[2 * 4 + 1];
    	var m22 = m[2 * 4 + 2];
    	var m23 = m[2 * 4 + 3];
    	var m30 = m[3 * 4 + 0];
    	var m31 = m[3 * 4 + 1];
    	var m32 = m[3 * 4 + 2];
    	var m33 = m[3 * 4 + 3];
    	var tmp_0  = m22 * m33;
    	var tmp_1  = m32 * m23;
    	var tmp_2  = m12 * m33;
    	var tmp_3  = m32 * m13;
    	var tmp_4  = m12 * m23;
    	var tmp_5  = m22 * m13;
    	var tmp_6  = m02 * m33;
    	var tmp_7  = m32 * m03;
    	var tmp_8  = m02 * m23;
    	var tmp_9  = m22 * m03;
    	var tmp_10 = m02 * m13;
    	var tmp_11 = m12 * m03;
    	var tmp_12 = m20 * m31;
    	var tmp_13 = m30 * m21;
    	var tmp_14 = m10 * m31;
    	var tmp_15 = m30 * m11;
    	var tmp_16 = m10 * m21;
    	var tmp_17 = m20 * m11;
    	var tmp_18 = m00 * m31;
    	var tmp_19 = m30 * m01;
    	var tmp_20 = m00 * m21;
    	var tmp_21 = m20 * m01;
    	var tmp_22 = m00 * m11;
    	var tmp_23 = m10 * m01;

    	var t0 = (tmp_0 * m11 + tmp_3 * m21 + tmp_4 * m31) -
    	    (tmp_1 * m11 + tmp_2 * m21 + tmp_5 * m31);
    	var t1 = (tmp_1 * m01 + tmp_6 * m21 + tmp_9 * m31) -
    	    (tmp_0 * m01 + tmp_7 * m21 + tmp_8 * m31);
    	var t2 = (tmp_2 * m01 + tmp_7 * m11 + tmp_10 * m31) -
    	    (tmp_3 * m01 + tmp_6 * m11 + tmp_11 * m31);
    	var t3 = (tmp_5 * m01 + tmp_8 * m11 + tmp_11 * m21) -
    	    (tmp_4 * m01 + tmp_9 * m11 + tmp_10 * m21);

    	var d = 1.0 / (m00 * t0 + m10 * t1 + m20 * t2 + m30 * t3);

    	return [
    		d * t0,
    		d * t1,
    		d * t2,
    		d * t3,
    		d * ((tmp_1 * m10 + tmp_2 * m20 + tmp_5 * m30) -
    		      (tmp_0 * m10 + tmp_3 * m20 + tmp_4 * m30)),
    		d * ((tmp_0 * m00 + tmp_7 * m20 + tmp_8 * m30) -
    		      (tmp_1 * m00 + tmp_6 * m20 + tmp_9 * m30)),
    		d * ((tmp_3 * m00 + tmp_6 * m10 + tmp_11 * m30) -
    		      (tmp_2 * m00 + tmp_7 * m10 + tmp_10 * m30)),
    		d * ((tmp_4 * m00 + tmp_9 * m10 + tmp_10 * m20) -
    		      (tmp_5 * m00 + tmp_8 * m10 + tmp_11 * m20)),
    		d * ((tmp_12 * m13 + tmp_15 * m23 + tmp_16 * m33) -
    		      (tmp_13 * m13 + tmp_14 * m23 + tmp_17 * m33)),
    		d * ((tmp_13 * m03 + tmp_18 * m23 + tmp_21 * m33) -
    		      (tmp_12 * m03 + tmp_19 * m23 + tmp_20 * m33)),
    		d * ((tmp_14 * m03 + tmp_19 * m13 + tmp_22 * m33) -
    		      (tmp_15 * m03 + tmp_18 * m13 + tmp_23 * m33)),
    		d * ((tmp_17 * m03 + tmp_20 * m13 + tmp_23 * m23) -
    		      (tmp_16 * m03 + tmp_21 * m13 + tmp_22 * m23)),
    		d * ((tmp_14 * m22 + tmp_17 * m32 + tmp_13 * m12) -
    		      (tmp_16 * m32 + tmp_12 * m12 + tmp_15 * m22)),
    		d * ((tmp_20 * m32 + tmp_12 * m02 + tmp_19 * m22) -
    		      (tmp_18 * m22 + tmp_21 * m32 + tmp_13 * m02)),
    		d * ((tmp_18 * m12 + tmp_23 * m32 + tmp_15 * m02) -
    		      (tmp_22 * m32 + tmp_14 * m02 + tmp_19 * m12)),
    		d * ((tmp_22 * m22 + tmp_16 * m02 + tmp_21 * m12) -
    		      (tmp_20 * m12 + tmp_23 * m22 + tmp_17 * m02))
    	];
	},
	multiplyM: function(a, b, dst){
		var a00 = a[0 * 4 + 0];
    	var a01 = a[0 * 4 + 1];
    	var a02 = a[0 * 4 + 2];
    	var a03 = a[0 * 4 + 3];
    	var a10 = a[1 * 4 + 0];
    	var a11 = a[1 * 4 + 1];
    	var a12 = a[1 * 4 + 2];
    	var a13 = a[1 * 4 + 3];
    	var a20 = a[2 * 4 + 0];
    	var a21 = a[2 * 4 + 1];
    	var a22 = a[2 * 4 + 2];
    	var a23 = a[2 * 4 + 3];
    	var a30 = a[3 * 4 + 0];
    	var a31 = a[3 * 4 + 1];
    	var a32 = a[3 * 4 + 2];
    	var a33 = a[3 * 4 + 3];
    	var b00 = b[0 * 4 + 0];
    	var b01 = b[0 * 4 + 1];
    	var b02 = b[0 * 4 + 2];
    	var b03 = b[0 * 4 + 3];
    	var b10 = b[1 * 4 + 0];
    	var b11 = b[1 * 4 + 1];
    	var b12 = b[1 * 4 + 2];
    	var b13 = b[1 * 4 + 3];
    	var b20 = b[2 * 4 + 0];
    	var b21 = b[2 * 4 + 1];
    	var b22 = b[2 * 4 + 2];
    	var b23 = b[2 * 4 + 3];
    	var b30 = b[3 * 4 + 0];
    	var b31 = b[3 * 4 + 1];
    	var b32 = b[3 * 4 + 2];
    	var b33 = b[3 * 4 + 3];

		dst = dst || new Float32Array(16);
		dst[ 0] = b00 * a00 + b01 * a10 + b02 * a20 + b03 * a30;
		dst[ 1] = b00 * a01 + b01 * a11 + b02 * a21 + b03 * a31;
		dst[ 2] = b00 * a02 + b01 * a12 + b02 * a22 + b03 * a32;
		dst[ 3] = b00 * a03 + b01 * a13 + b02 * a23 + b03 * a33;
		dst[ 4] = b10 * a00 + b11 * a10 + b12 * a20 + b13 * a30;
		dst[ 5] = b10 * a01 + b11 * a11 + b12 * a21 + b13 * a31;
		dst[ 6] = b10 * a02 + b11 * a12 + b12 * a22 + b13 * a32;
		dst[ 7] = b10 * a03 + b11 * a13 + b12 * a23 + b13 * a33;
		dst[ 8] = b20 * a00 + b21 * a10 + b22 * a20 + b23 * a30;
		dst[ 9] = b20 * a01 + b21 * a11 + b22 * a21 + b23 * a31;
		dst[10] = b20 * a02 + b21 * a12 + b22 * a22 + b23 * a32;
		dst[11] = b20 * a03 + b21 * a13 + b22 * a23 + b23 * a33;
		dst[12] = b30 * a00 + b31 * a10 + b32 * a20 + b33 * a30;
		dst[13] = b30 * a01 + b31 * a11 + b32 * a21 + b33 * a31;
		dst[14] = b30 * a02 + b31 * a12 + b32 * a22 + b33 * a32;
		dst[15] = b30 * a03 + b31 * a13 + b32 * a23 + b33 * a33;

		return dst;
	},
	translation: function(tx, ty, tz) {
		return [
			1, 0, 0, 0,
			0, 1, 0, 0,
			0, 0, 1, 0,
			tx, ty, tz,1,
		];   
	},   
	xRotation: function(angleInRadians) {
		var c = Math.cos(angleInRadians);
		var s = Math.sin(angleInRadians);
	 
		return [
		  	1, 0, 0, 0,
		  	0, c, s, 0,
		  	0, -s, c, 0,
		  	0, 0, 0, 1,
		];
	},
	yRotation: function(angleInRadians) {
		var c = Math.cos(angleInRadians);
		var s = Math.sin(angleInRadians);
	 
		return [
			c, 0, -s, 0,
			0, 1, 0, 0,
			s, 0, c, 0,
			0, 0, 0, 1,
		];    
	},    
	zRotation: function(angleInRadians) {
		var c = Math.cos(angleInRadians);
		var s = Math.sin(angleInRadians);
	     
		return [
			 c, s, 0, 0,
			-s, c, 0, 0,
			 0, 0, 1, 0,
			 0, 0, 0, 1,
		];
	},
	scaling: function(sx, sy, sz) {
		return [
			sx, 0,  0,  0,
			0, sy,  0,  0,
			0,  0, sz,  0,
			0,  0,  0,  1,
		];
	},
	multiplyV: function(v, m, dst) {
		dst = dst || new Float32Array(4);
    	for (var i = 0; i < 4; ++i) {
    		dst[i] = 0.0;
    		for (var j = 0; j < 4; ++j) {
				dst[i] += v[j] * m[j * 4 + i];
    		}
    	}
    	return dst;
	},
	transpose: function(m) {
		return [
		  	m[0], m[4], m[8], m[12],
		  	m[1], m[5], m[9], m[13],
		  	m[2], m[6], m[10], m[14],
		  	m[3], m[7], m[11], m[15],
		];
	},
	// Cross product of 2 vectors
	cross: function(a, b) {
		return [a[1] * b[2] - a[2] * b[1],
				a[2] * b[0] - a[0] * b[2],
				a[0] * b[1] - a[1] * b[0]];
    },
	subtractV: function(a, b) {
		return [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
    },
	normalize: function(v) {
    	var length = Math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2]);
    	// проверяем, что мы не делим на 0
    	if (length > 0.00001) {
			return [v[0] / length, v[1] / length, v[2] / length];
    	} else {
			return [0, 0, 0];
    	}
    },

	Degree2Radian: function(degree){
		return degree * Math.PI/180
	}
}

var A = {

	rotate_around_x_axis: function(time, mat, ndx){
		var m_rotation = M.xRotation(time * (0.1 + 0.1 * ndx))
		M.multiplyM(mat,m_rotation,mat);
	},

	rotate_around_y_axis: function(time, mat, ndx){
		var m_rotation = M.yRotation(time * (0.1 + 0.1 * ndx))
		M.multiplyM(mat,m_rotation,mat);
	},

	rotate_around_z_axis: function(time, mat, ndx){
		var m_rotation = M.zRotation(time * (0.1 + 0.1 * ndx))
		M.multiplyM(mat,m_rotation,mat);
	},

	rotate_around_pointA: function(time, mat, ndx, aargs){
		var point = [0,0,0];
		var speed = aargs.speed;
		var direction = aargs.direction;
		var m_xTranslate = M.translation(Math.sin(time) * speed * direction[0] , Math.cos(time) * speed * direction[1], Math.sin(time) * speed * direction[1]);
		M.multiplyM(mat,m_xTranslate,mat);
	},
	move_to: function(time, mat, ndx, aargs){
		var speed = aargs.speed;
		var direction = aargs.direction;
		var m_translate = M.translation(time * speed * direction[0] ,time * speed * direction[1], time * speed * direction[2]);

		M.multiplyM(mat,m_translate,mat);
	},
}

var U = {
	resizeCanvasToDisplaySize: function(canvas, multiplier) {
    	multiplier = multiplier || 1;
    	const width  = canvas.clientWidth  * multiplier | 0;
    	const height = canvas.clientHeight * multiplier | 0;
    	if (canvas.width !== width ||  canvas.height !== height) {
    	  canvas.width  = width;
    	  canvas.height = height;
    	  return true;
    	}
    	return false;
	},
	getRndInteger: function(min, max) {
		return Math.floor(Math.random() * (max - min + 1) ) + min;
	},
	getRndVec: function(min, max){
		return [
			U.getRndInteger(min,max),
			U.getRndInteger(min,max),
			U.getRndInteger(min,max) 
		];
	},
	createShader: function(gl, type, source) {
		var shader = gl.createShader(type);   // создание шейдера
		gl.shaderSource(shader, source);      // устанавливаем шейдеру его программный код
		gl.compileShader(shader);             // компилируем шейдер
		var success = gl.getShaderParameter(shader, gl.COMPILE_STATUS);
		if (success) {                        // если компиляция прошла успешно - возвращаем шейдер
			return shader;
		}
	 
		console.log(gl.getShaderInfoLog(shader));
		gl.deleteShader(shader);
	},
	readTextFile: function(file) {
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
	},
	createProgram: function(gl, vertexShader, fragmentShader) {
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
}

var primitives = {
	e_point: {
		vertices: new Float32Array([
			0, 0, 0,
		]),
		indices: new Uint16Array([
			0,
		]),
		num_indices: 1,
	},

	e_tetrahedron: {
		vertices: new Float32Array([
			1, 1, 1,	// 0 A
			-1, 1, -1,	// 1 B
			1, -1, -1,	// 2 C
			-1, -1, 1,  // 3 D
		]),
		indices: new Uint16Array([
			0, 3, 2,
			2, 0, 1,
			1, 2, 3,
			3, 1, 0,
		]),
		num_indices: 12,

	},

	e_cube: {
		vertices: new Float32Array([
			1, 1, 1,	// 0 A
			-1, 1, 1,	// 1 B
			-1, 1, -1,	// 2 C
			1, 1, -1,	// 3 D
			1, -1, 1,	// 4 A1
			-1, -1, 1,	// 5 B1
			-1, -1, -1,	// 6 C1
			1, -1, -1,	// 7 D1
		]),
		indices: new Uint16Array([
			0, 1, 2,
			0, 2, 3,

			0, 3, 4,
			3, 7, 4,

			0, 4, 1,
			1, 4, 5,

			1, 5, 2,
			2, 6, 5,

			2, 7, 3,
			2, 6, 7,

			6, 4, 5,
			6, 7, 4,
		]),
		num_indices: 36,
	},
	e_arrow: {
		vertices: new Float32Array([
			// Front
			1,2,1,	// E 0
			2,0,1,	// G 1
			1,0,1,	// F 2
			-1,2,1, // D 3
			-1,0,1,	// C 4
			-2,0,1,	// B 5
			0,-1,1, // A 6
			// Back
			1,2,-1,	// E1 7
			2,0,-1,	// G1 8
			1,0,-1,	// F1 9
			-1,2,-1,// D1 10
			-1,0,-1,// C1 11
			-2,0,-1,// B1 12
			0,-1,-1,// A1 13
		]),
		indices: new Uint16Array([
			6, 5, 1,
			4, 3, 0,
			4, 0, 2,
			13, 12, 8,
			11, 10, 7,
			11, 0, 9,
			6, 5, 12,
			6, 12, 13,
			6, 1, 8,
			6, 8, 13, 
			5, 4, 11, 
			5, 11, 12,
			2, 9, 8,
			2, 8, 1,
			2, 0, 7 ,
			2, 7, 9,
			3, 10, 7,
			3, 7, 0,
			4, 3, 10,
			4, 10, 11,
		]),
		num_indices: 60,
	},
	e_quad: {
		vertices: new Float32Array([
			1, 1, 0,	// 0 A
			-1, 1, 0,	// 1 B
			1, -1, 0,	// 2 C
			-1, -1, 0,  // 3 D
		]),
		indices: new Uint16Array([
			0, 1, 2,
			2, 3, 1,
		]),
		num_indices: 6,
	},
	e_triangle: {
		vertices: new Float32Array([
			0, 1, 0,	// 0 A
			-1, -1, 0,	// 1 B
			1, -1, 0,	// 2 C
		]),
		indices: new Uint16Array([
			0, 1, 2,
		]),
		num_indices: 3,
	},
	a_cube: {
		vertices: new Float32Array([
			-1,-1,-1,
			-1,-1, 1,
			-1, 1, 1,
			1, 1,-1,
			-1,-1,-1,
			-1, 1,-1,

			1,-1, 1,
			-1,-1,-1,
			1,-1,-1,
			1, 1,-1,
			1,-1,-1,
			-1,-1,-1,

			-1,-1,-1,
			-1, 1, 1,
			-1, 1,-1,
			1,-1, 1,
			-1,-1, 1,
			-1,-1,-1,

			-1, 1, 1,
			-1,-1, 1,
			1,-1, 1,
			1, 1, 1,
			1,-1,-1,
			1, 1,-1,

			1,-1,-1,
			1, 1, 1,
			1,-1, 1,
			1, 1, 1,
			1, 1,-1,
			-1, 1,-1,

			1, 1, 1,
			-1, 1,-1,
			-1, 1, 1,
			1, 1, 1,
			-1, 1, 1,
			1,-1, 1,
		]),
		normals: new Float32Array([
			-1,0,0,
			-1,0,0,
			-1,0,0,
			0,0,-1,
			0,0,-1,
			0,0,-1,
			0,-1,0,
			0,-1,0,
			0,-1,0,
			0,0,-1,
			0,0,-1,
			0,0,-1,
			-1,0,0,
			-1,0,0,
			-1,0,0,
			0,-1,0,
			0,-1,0,
			0,-1,0,
			0,0,1,
			0,0,1,
			0,0,1,
			1,0,0,
			1,0,0,
			1,0,0,
			1,0,0,
			1,0,0,
			1,0,0,
			0,1,0,
			0,1,0,
			0,1,0,
			0,1,0,
			0,1,0,
			0,1,0,
			0,0,1,
			0,0,1,
			0,0,1,
		]),
	},
}
