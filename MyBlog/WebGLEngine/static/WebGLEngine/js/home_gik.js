let canvasDI = new DI(document.querySelector("#canvas"))

canvasDI.SetAttribute("a_position");
canvasDI.SetAttribute("a_mvp");
canvasDI.SetAttribute("a_color");
canvasDI.SetAttribute("a_pointSize");


canvasDI.StartVAO(primitives.e_tetrahedron, canvasDI.gl.LINE_LOOP);
canvasDI.SetPrimitive({
	pos: [0, 0, 0], 
	color: [.0,.0,.0,1], 
	scale: [12,12,12],
	rotate: [0,0,1],
	rotateAngle: 45,
	animation: A.rotate_around_y_axis,
});
canvasDI.EndVAO();

canvasDI.StartVAO(primitives.e_tetrahedron, canvasDI.gl.POINTS);
canvasDI.SetPrimitive({
	pos: [0, 0, 0], 
	color: [217.0/255.0,140.0/255.0,69.0/255.0,1], 
	scale: [12,12,12],
	rotate: [0,0,1],
	rotateAngle: 45,
	animation: A.rotate_around_y_axis,
	point_size: 5.0
});
canvasDI.EndVAO();



var fieldOfViewRadians = M.Degree2Radian(60);
var zNear = 1;
var zFar = 2000;
var cameraPosition = [0, 0, -50];
var rotation = [0, 0, 0];
var scale = [1, 1, 1];
var start = 0
