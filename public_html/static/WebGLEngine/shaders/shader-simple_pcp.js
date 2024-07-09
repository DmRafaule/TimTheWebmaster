class ShaderSimplePCP extends DIShader{
    constructor(context){
        var vertexShaderPath = STATIC+'WebGLEngine/shaders/simple_pcp.vert'
        var fragmentShaderPath = STATIC+'WebGLEngine/shaders/simple_pcp.frag'
        super(context, vertexShaderPath, fragmentShaderPath)

        this.a_position = context.getAttribLocation(this.program, 'a_position')
        this.a_mvp = context.getAttribLocation(this.program, 'a_mvp')
        this.a_color = context.getAttribLocation(this.program, 'a_color')
        this.a_pointSize = context.getAttribLocation(this.program, 'a_pointSize')
    }

    CreateBuffers(context, primitives){
        // Создаём буфер для позиций вершин
		var positionBuffer = context.createBuffer();
		// Связываем созданный буфер с ...
		context.bindBuffer(context.ARRAY_BUFFER, positionBuffer);
		// Включаем атрибут
		context.enableVertexAttribArray(primitives.shader.a_position);
		// Обозначаем то как читать данные из созданного буфера
		var size = 3;          // Длина одного элемента в буфере
		var type = context.FLOAT;   // Тип данных в элементе буфера 
		var normalize = false; // При использовании с gl.FLOAT не имеет эффекта
		var stride = 0;        // Шаг к следующему элементу в буфере вычисляется: sizeof(type) * size
		var offset = 0;        // Откуда начать читать буфер
		context.vertexAttribPointer(primitives.shader.a_position, size, type, normalize, stride, offset);
		// Отправляем данные в буфер
		context.bufferData(context.ARRAY_BUFFER, primitives.vertices, context.STATIC_DRAW);

		// Создаём буфер вершин
		var indexBuffer = context.createBuffer();
		// Связываем созданный буфер с ...
		context.bindBuffer(context.ELEMENT_ARRAY_BUFFER, indexBuffer);
		context.bufferData(context.ELEMENT_ARRAY_BUFFER, primitives.indices, context.STATIC_DRAW);


		// Создаём буфер атрибута для хранения mvp (model view projection матрицы), mat4x4
		var matrixLength = 16;
		primitives.matrixData = new Float32Array(primitives.numInstances * matrixLength);
		primitives.matrices = [];
		for (let i = 0; i < primitives.numInstances; ++i) {
		  	const byteOffsetToMatrix = i * matrixLength * 4;
		  	const numFloatsForView = matrixLength;
		  	primitives.matrices.push(new Float32Array(
				primitives.matrixData.buffer,
				byteOffsetToMatrix,
				numFloatsForView
			));
		}
		primitives.matrixBuffer = context.createBuffer();
		context.bindBuffer(context.ARRAY_BUFFER, primitives.matrixBuffer);
		// Выделяем память
		context.bufferData(context.ARRAY_BUFFER, primitives.matrixData.byteLength, context.STATIC_DRAW);
		var bytesPerMatrix = 4 * 16;
		for (let i = 0; i < 4; ++i) {
		  const loc = primitives.shader.a_mvp + i;
		  context.enableVertexAttribArray(loc);
		  const offset = i * 16;  // 4 floats на ряд каждый float по 4 байта
		  context.vertexAttribPointer(loc, 4, context.FLOAT, false,bytesPerMatrix, offset);
		  // Данный аттрибут изменяется для каждого instance
		  context.vertexAttribDivisor(loc, 1);
		}


		// Создаём буфер аттрибута для хранения цвета vec4
		const colorBuffer = context.createBuffer();
		primitives.colorBuffer = colorBuffer
		var colorData = new Float32Array(primitives.numInstances * 4);
		primitives.colorData = colorData
		for (var i = 0; i < primitives.numInstances; i++){
			var colors = primitives.P[i].color;
			colorData[0 + 4*i] = colors[0];
			colorData[1 + 4*i] = colors[1];
			colorData[2 + 4*i] = colors[2];
			colorData[3 + 4*i] = colors[3];
		}
		context.bindBuffer(context.ARRAY_BUFFER, colorBuffer);
		context.bufferData(context.ARRAY_BUFFER,colorData,context.STATIC_DRAW);
		context.enableVertexAttribArray(primitives.shader.a_color);
		context.vertexAttribPointer(primitives.shader.a_color, 4, context.FLOAT, false, 0, 0);
		  // Данный аттрибут изменяется для каждого instance
		context.vertexAttribDivisor(primitives.shader.a_color, 1);
		

		// Создаём буфер для размера точки
		var pointBuffer = context.createBuffer();
		var point_size =  new Float32Array(primitives.numInstances * 1);
		for (var i = 0; i < primitives.numInstances; i++){
			point_size[i] = primitives.P[i].point_size;
		}

		// Связываем созданный буфер с ...
		context.bindBuffer(context.ARRAY_BUFFER, pointBuffer);
		context.bufferData(context.ARRAY_BUFFER, point_size , context.STATIC_DRAW);
		context.enableVertexAttribArray(primitives.shader.a_pointSize);
		context.vertexAttribPointer(primitives.shader.a_pointSize, 1, context.FLOAT, false, 0, 0);
		// this line says this attribute only changes for each 1 instance
		context.vertexAttribDivisor(primitives.shader.a_pointSize, 1);
    }

    UpdateBuffers(context, primitives, time){
        // Вычисление матрицы мира и объектов
        // Вычисляем матрицу проекции
        var aspect = context.canvas.clientWidth / context.canvas.clientHeight;
        var projectionMatrix = M.perspective(viewAngle, aspect, zNear, zFar);
        // Вычисляем матрицу камеры ( или view matrix)
        var cameraMatrix = M.translation(cameraPosition[0], cameraPosition[1], cameraPosition[2]);
        var m_xrotation = M.xRotation(M.Degree2Radian(rotation[0]))
        M.multiplyM(cameraMatrix,m_xrotation,cameraMatrix)
        var m_yrotation = M.yRotation(M.Degree2Radian(rotation[1]))
        M.multiplyM(cameraMatrix,m_yrotation,cameraMatrix)
        var m_zrotation = M.zRotation(M.Degree2Radian(rotation[2]))
        M.multiplyM(cameraMatrix,m_zrotation,cameraMatrix)
        // Вычисляем первоначальный размер
        var m_scaling = M.scaling(scale[0], scale[1], scale[2])
        M.multiplyM(cameraMatrix,m_scaling,cameraMatrix)
        // Перемножаем матрицы проекции и камеры 
        var mvp = M.multiplyM(projectionMatrix, cameraMatrix)
        // Вычисляем матрицу объекта
        primitives.matrices.forEach((mat, ndx) => {
            // Задаём матрицу модели
            M.identity(mat);
            // Вычисляем первоначальное положение
            var pos = primitives.P[ndx].pos;
            var m_translation = M.translation(pos[0], pos[1], pos[2])
            M.multiplyM(mat,m_translation,mat)
            // Вычисляем первоначальный поворот
            var rotateAngle = primitives.P[ndx].rotateAngle;
            var toRotate = primitives.P[ndx].rotate
            var angle = M.Degree2Radian(rotateAngle)
            var m_xrotation = M.xRotation(angle * toRotate[0])
            M.multiplyM(mat,m_xrotation,mat)
            var m_yrotation = M.yRotation(angle * toRotate[1])
            M.multiplyM(mat,m_yrotation,mat)
            var m_zrotation = M.zRotation(angle * toRotate[2])
            M.multiplyM(mat,m_zrotation,mat)
            // Вычисляем первоначальный размер
            var scale = primitives.P[ndx].scale;
            var m_scaling = M.scaling(scale[0], scale[1], scale[2])
            M.multiplyM(mat,m_scaling,mat)
            // Запускаем анимацию
            primitives.P[ndx].animation(time, mat, ndx, primitives.P[ndx].animation_args);
            // Перемножаем матрицу mvp и модели 
            M.multiplyM(mvp, mat, mat)
        });
        context.bindBuffer(context.ARRAY_BUFFER, primitives.matrixBuffer);
        context.bufferSubData(context.ARRAY_BUFFER, 0, primitives.matrixData);

        context.bindBuffer(context.ARRAY_BUFFER, primitives.colorBuffer);
        context.bufferSubData(context.ARRAY_BUFFER, 0, primitives.colorData);
    }
}
