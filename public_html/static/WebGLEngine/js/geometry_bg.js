{
/* Получаем WebGL2 контекст. Инициализируем WebGL2 */
let canvasDI = new DI(document.querySelector("#canvas"))

canvasDI.SetAttribute("a_position");
canvasDI.SetAttribute("a_mvp");
canvasDI.SetAttribute("a_color");
canvasDI.SetAttribute("a_pointSize");

canvasDI.StartVAO(primitives.e_tetrahedron, canvasDI.gl.LINE_LOOP);
canvasDI.SetPrimitive({
	pos: [-30, 10, -20], 
	color: [0.9,0.9,0.9,1], 
	rotate: [0,0,1],
	rotateAngle: 45,
	animation: A.rotate_around_y_axis,
});
canvasDI.SetPrimitive({
	pos: [5, 20, -100], 
	color: [0.3,0.3,0.3,1], 
	rotate: [0,1,0],
	rotateAngle: 10,
	animation: A.rotate_around_z_axis,
});
canvasDI.EndVAO();

canvasDI.StartVAO(primitives.e_cube, canvasDI.gl.LINE_LOOP);
canvasDI.SetPrimitive({pos: [30,10,10], scale: [2,2,2], animation: A.rotate_around_z_axis});
canvasDI.SetPrimitive({pos: [30,10,10], scale: [1,1,1], animation: A.rotate_around_x_axis});
canvasDI.SetPrimitive({pos: [30,10,10], scale: [0.5,0.5,0.5], animation: A.rotate_around_y_axis});
canvasDI.EndVAO();

canvasDI.StartVAO(primitives.e_arrow, canvasDI.gl.LINE_LOOP);
canvasDI.SetPrimitive({color: [0.1,0.1,0.1,1], pos: [0,-20,0], scale: [1,2,2], animation: 
	function(time, mat, ndx){
		var speed = 5;
		var m_xTranslate = M.translation(0,Math.sin(time) * (speed/2),0)
		M.multiplyM(mat,m_xTranslate,mat);
		var m_yRotate = M.yRotation(time * speed * M.Degree2Radian(5))
		M.multiplyM(mat,m_yRotate,mat);
	}
});
canvasDI.EndVAO();

canvasDI.StartVAO(primitives.e_point, canvasDI.gl.POINTS);
for (var i = 0; i < 4000; i++)
	canvasDI.SetPrimitive({
		pos: U.getRndVec(-50,50), 
		color: [0.8,0.8,0.8,1],		
		point_size: Math.random()*5, 
		animation: A.rotate_around_pointA, 
		animation_args: {
			speed: U.getRndInteger(1,2),
			direction: [
				U.getRndInteger(-1,1),
				U.getRndInteger(-1,1),
				U.getRndInteger(-1,1),
			]
		}
	});
canvasDI.EndVAO();



var fieldOfViewRadians = M.Degree2Radian(60);
var zNear = 1;
var zFar = 2000;
var cameraPosition = [0, 0, -50];
var rotation = [0, 0, 0];
var scale = [1, 1, 1];
var start = 0


}
