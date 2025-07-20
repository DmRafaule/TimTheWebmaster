let canvas = document.querySelector("#canvas")
let canvasDI = new DI(canvas)
var perspectiveAngle = 60
var viewAngle = M.Degree2Radian(perspectiveAngle);
var FOVy = M.Degree2Radian(perspectiveAngle/2);
var zNear = 1;
var zFar = 2000;
var cameraPosition = [0, 0, -50];
var rotation = [0, 0, 0];
var scale = [1, 1, 1];
var start = 0
var deltaTime = 0
var terrainShader = new ShaderSimplePCP(canvasDI.context)


canvasDI.CreateVAO(primitives.e_tetrahedron, canvasDI.gl.LINE_LOOP);
canvasDI.SetShader(terrainShader)
canvasDI.SetPrimitive({
	pos: [0, 0, 0], 
	color: [.0,.0,.0,1], 
	scale: [12,12,12],
	rotate: [0,0,1],
	rotateAngle: 45,
	animation: A.rotate_around_y_axis,
});
canvasDI.EndVAO();

canvasDI.CreateVAO(primitives.e_tetrahedron, canvasDI.gl.POINTS);
canvasDI.SetShader(terrainShader)
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