class ShaderSimplePCPT extends DIShader{
    constructor(context){
        var vertexShaderPath = STATIC+'WebGLEngine/shaders/simple_pcpt.vert'
        var fragmentShaderPath = STATIC+'WebGLEngine/shaders/simple_pcpt.frag'
        super(context, vertexShaderPath, fragmentShaderPath)

        this.a_position = context.getAttribLocation(this.program, 'a_position')
        this.a_mvp = context.getAttribLocation(this.program, 'a_mvp')
        this.a_color = context.getAttribLocation(this.program, 'a_color')
        this.a_pointSize = context.getAttribLocation(this.program, 'a_pointSize')
        this.a_texCoord = context.getAttribLocation(this.program, 'a_texCoord')
        this.u_texture = context.getUniformLocation(this.program, 'u_texture')
    }

    CreateBuffers = async (context, primitives) => {
        // БУФЕР ВЕРШИН
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


		// БУФЕР МАТРИЦЫ MVP (model view projection матрицы), mat4x4
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


		// БУФЕР ЦВЕТА VEC4
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
		

		// БУФЕР РАЗМЕРА ТОЧКИ
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
		context.vertexAttribDivisor(primitives.shader.a_pointSize, 1);

        // БУФЕР ТЕКСТУРЫ
		var texCoordBuffer = context.createBuffer();
		primitives.texCoordBuffer = texCoordBuffer 
		context.bindBuffer(context.ARRAY_BUFFER, texCoordBuffer);
        primitives.texData = new Float32Array([
			1, 1,	// 0 A
			0, 1,	// 1 B
			1, 0,	// 2 C
			0, 0,  // 3 D
		])
		context.bufferData(context.ARRAY_BUFFER, primitives.texData, context.STATIC_DRAW);
		context.enableVertexAttribArray(primitives.shader.a_texCoord);
		var size = 2;          // 2 components per iteration
		var type = context.FLOAT;   // the data is 32bit floats
		var normalize = false; // don't normalize the data
		var stride = 0;        // 0 = move forward size * sizeof(type) each iteration to get the next position
		var offset = 0;        // start at the beginning of the buffer
		context.vertexAttribPointer(primitives.shader.a_texCoord, size, type, normalize, stride, offset)
		
		// ЗАГРУЗКА  ТЕКСТУРЫ
		var image = await canvasDI.LoadTexture()
		
		context.pixelStorei(context.UNPACK_FLIP_Y_WEBGL, true)

		// Create a texture.
		var texture = context.createTexture();
		
		// make unit 0 the active texture unit
		// (i.e, the unit all other texture commands will affect.)
		context.activeTexture(context.TEXTURE0 + 0);
		
		// Bind texture to 'texture unit '0' 2D bind point
		context.bindTexture(context.TEXTURE_2D, texture);
		
		// Set the parameters so we don't need mips and so we're not filtering
		// and we don't repeat
		context.texParameteri(context.TEXTURE_2D, context.TEXTURE_WRAP_S, context.CLAMP_TO_EDGE);
		context.texParameteri(context.TEXTURE_2D, context.TEXTURE_WRAP_T, context.CLAMP_TO_EDGE);
		context.texParameteri(context.TEXTURE_2D, context.TEXTURE_MIN_FILTER, context.NEAREST);
		context.texParameteri(context.TEXTURE_2D, context.TEXTURE_MAG_FILTER, context.NEAREST);
		// Upload the image into the texture.
		context.texImage2D(context.TEXTURE_2D, 0, context.RGBA,context.RGBA,context.UNSIGNED_BYTE, image);
		//context.texImage2D(context.TEXTURE_2D, 0, context.RGBA, 1, 1, 0, context.RGBA, context.UNSIGNED_BYTE, new Uint8Array([0, 0, 255, 100]));
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

        context.uniform1i(primitives.shader.u_texture, 0);
    }
}

