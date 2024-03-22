function makeZToWMatrix(e){return[1,0,0,0,0,1,0,0,0,0,1,e,0,0,0,1]}function setNormals(e){var t=new Float32Array([0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,-1,0,0,-1,0,0,-1,0,0,-1,0,0,-1,0,0,-1,0,0,-1,0,0,-1,0,0,-1,0,0,-1,0,0,-1,0,0,-1,0,0,-1,0,0,-1,0,0,-1,0,0,-1,0,0,-1,0,0,-1,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,0,-1,0,0,-1,0,0,-1,0,0,-1,0,0,-1,0,0,-1,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,0,-1,0,0,-1,0,0,-1,0,0,-1,0,0,-1,0,0,-1,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,0,-1,0,0,-1,0,0,-1,0,0,-1,0,0,-1,0,0,-1,0,-1,0,0,-1,0,0,-1,0,0,-1,0,0,-1,0,0,-1,0,0]);e.bufferData(e.ARRAY_BUFFER,t,e.STATIC_DRAW)}function setGeometry(e){for(var s,t=new Float32Array([0,0,0,0,150,0,30,0,0,0,150,0,30,150,0,30,0,0,30,0,0,30,30,0,100,0,0,30,30,0,100,30,0,100,0,0,30,60,0,30,90,0,67,60,0,30,90,0,67,90,0,67,60,0,0,0,30,30,0,30,0,150,30,0,150,30,30,0,30,30,150,30,30,0,30,100,0,30,30,30,30,30,30,30,100,0,30,100,30,30,30,60,30,67,60,30,30,90,30,30,90,30,67,60,30,67,90,30,0,0,0,100,0,0,100,0,30,0,0,0,100,0,30,0,0,30,100,0,0,100,30,0,100,30,30,100,0,0,100,30,30,100,0,30,30,30,0,30,30,30,100,30,30,30,30,0,100,30,30,100,30,0,30,30,0,30,60,30,30,30,30,30,30,0,30,60,0,30,60,30,30,60,0,67,60,30,30,60,30,30,60,0,67,60,0,67,60,30,67,60,0,67,90,30,67,60,30,67,60,0,67,90,0,67,90,30,30,90,0,30,90,30,67,90,30,30,90,0,67,90,30,67,90,0,30,90,0,30,150,30,30,90,30,30,90,0,30,150,0,30,150,30,0,150,0,0,150,30,30,150,30,0,150,0,30,150,30,30,150,0,0,0,0,0,0,30,0,150,30,0,0,0,0,150,30,0,150,0]),o=math.xRotation(Math.PI),o=math.translate(o,-50,-75,-15),n=0;n<t.length;n+=3)s=math.transformVector(o,[t[n+0],t[n+1],t[n+2],1]),t[n+0]=s[0],t[n+1]=s[1],t[n+2]=s[2];e.bufferData(e.ARRAY_BUFFER,t,e.STATIC_DRAW)}function Degree2Radian(e){return e*Math.PI/180}function createShader(e,t,n){var o,s=e.createShader(t);if(e.shaderSource(s,n),e.compileShader(s),o=e.getShaderParameter(s,e.COMPILE_STATUS),o)return s;console.log(e.getShaderInfoLog(s)),e.deleteShader(s)}function readTextFile(e){var t=new XMLHttpRequest,n="";return t.open("GET",e,!1),t.onreadystatechange=function(){t.readyState===4&&(t.status===200||t.status==0)&&(n=t.responseText)},t.send(null),n}function createProgram(e,t,n){var o,s=e.createProgram();if(e.attachShader(s,t),e.attachShader(s,n),e.linkProgram(s),o=e.getProgramParameter(s,e.LINK_STATUS),o)return s;console.log(e.getProgramInfoLog(s)),e.deleteProgram(s)}function drawScene(){gl.viewport(0,0,gl.canvas.width,gl.canvas.height),gl.clearColor(0,0,0,0),gl.clear(gl.COLOR_BUFFER_BIT|gl.DEPTH_BUFFER_BIT),gl.enable(gl.DEPTH_TEST),gl.enable(gl.CULL_FACE),gl.useProgram(program),gl.bindVertexArray(vao);var t,n,o,m=gl.canvas.clientWidth/gl.canvas.clientHeight,i=1,h=2e3,a=math.perspective(fieldOfViewRadians,m,i,h),r=[100,150,200],c=[0,35,0],l=[0,1,0],d=math.lookAt(r,c,l),u=math.inverse(d),e=math.multiply4x4(a,u),v=math.yRotate(e,fRotationRadians),s=math.yRotation(fRotationRadians),f=math.multiply4x4(e,s),p=math.inverse(s),g=math.transpose(p);gl.uniformMatrix4fv(worldViewProjectionLocation,!1,f),gl.uniformMatrix4fv(worldInverseTransposeLocation,!1,g),gl.uniform4fv(colorLocation,[.2,1,.2,1]),gl.uniform3fv(reverseLightDirectionLocation,math.normalize([.5,.7,1])),n=gl.TRIANGLES,t=0,o=16*6,gl.drawArrays(n,t,o)}var canvas=document.querySelector("#canvas"),vertexShaderPath,fragmentShaderPath,vertexShaderSource,fragmentShaderSource,vertexShader,fragmentShader,program,positionAttributeLocation,normalAttributeLocation,worldViewProjectionLocation,worldInverseTransposeLocation,colorLocation,reverseLightDirectionLocation,positionBuffer,vao,size,type,normalize,stride,offset,normalBuffer,fieldOfViewRadians,fRotationRadians,gl=canvas.getContext("webgl2");gl.enable(gl.CULL_FACE),gl.enable(gl.DEPTH_TEST),gl||console.log("OpenGl is not avaiable"),vertexShaderPath=canvas.dataset.vertexShader,fragmentShaderPath=canvas.dataset.fragmentShader,vertexShaderSource=readTextFile(vertexShaderPath),fragmentShaderSource=readTextFile(fragmentShaderPath),vertexShader=createShader(gl,gl.VERTEX_SHADER,vertexShaderSource),fragmentShader=createShader(gl,gl.FRAGMENT_SHADER,fragmentShaderSource),program=createProgram(gl,vertexShader,fragmentShader),positionAttributeLocation=gl.getAttribLocation(program,"a_position"),normalAttributeLocation=gl.getAttribLocation(program,"a_normal"),worldViewProjectionLocation=gl.getUniformLocation(program,"u_worldViewProjection"),worldInverseTransposeLocation=gl.getUniformLocation(program,"u_worldInverseTranspose"),colorLocation=gl.getUniformLocation(program,"u_color"),reverseLightDirectionLocation=gl.getUniformLocation(program,"u_reverseLightDirection"),positionBuffer=gl.createBuffer(),vao=gl.createVertexArray(),gl.bindVertexArray(vao),gl.enableVertexAttribArray(positionAttributeLocation),gl.bindBuffer(gl.ARRAY_BUFFER,positionBuffer),setGeometry(gl),size=3,type=gl.FLOAT,normalize=!1,stride=0,offset=0,gl.vertexAttribPointer(positionAttributeLocation,size,type,normalize,stride,offset),normalBuffer=gl.createBuffer(),gl.bindBuffer(gl.ARRAY_BUFFER,normalBuffer),setNormals(gl),gl.enableVertexAttribArray(normalAttributeLocation),size=3,type=gl.FLOAT,normalize=!1,stride=0,offset=0,gl.vertexAttribPointer(normalAttributeLocation,size,type,normalize,stride,offset),fieldOfViewRadians=Degree2Radian(60),fRotationRadians=0,drawScene(),slider_transform_y=document.querySelector("#transform-y"),slider_transform_y.addEventListener("input",function(){var e=parseInt(this.nextElementSibling.value);translation[1]=e,drawScene()}),slider_transform_x=document.querySelector("#transform-x"),slider_transform_x.addEventListener("input",function(){var e=parseInt(this.nextElementSibling.value);translation[0]=e,drawScene()}),slider_transform_z=document.querySelector("#transform-z"),slider_transform_z.addEventListener("input",function(){var e=parseInt(this.nextElementSibling.value);translation[2]=e,drawScene()}),slider_scale_x=document.querySelector("#scale-x"),slider_scale_x.addEventListener("input",function(){var e=parseFloat(this.nextElementSibling.value);scale[0]=e,drawScene()}),slider_scale_y=document.querySelector("#scale-y"),slider_scale_y.addEventListener("input",function(){var e=parseFloat(this.nextElementSibling.value);scale[1]=e,drawScene()}),slider_rotate_x=document.querySelector("#rotation-x"),slider_rotate_x.addEventListener("input",function(){var e=parseInt(this.nextElementSibling.value);rotation[0]=Degree2Radian(e),drawScene()}),slider_rotate_y=document.querySelector("#rotation-y"),slider_rotate_y.addEventListener("input",function(){var e=parseInt(this.nextElementSibling.value);fRotationRadians=Degree2Radian(e),drawScene()}),slider_rotate_z=document.querySelector("#rotation-z"),slider_rotate_z.addEventListener("input",function(){var e=parseInt(this.nextElementSibling.value);rotation[2]=Degree2Radian(e),drawScene()}),field_of_view=document.querySelector("#field-of-view"),field_of_view.addEventListener("input",function(){var e=parseInt(this.nextElementSibling.value);fieldOfView=Degree2Radian(e),drawScene()})