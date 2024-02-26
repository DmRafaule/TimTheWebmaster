function makeZToWMatrix(e){return[1,0,0,0,0,1,0,0,0,0,1,e,0,0,0,1]}function setNormals(e){var t=new Float32Array([0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,-1,0,0,-1,0,0,-1,0,0,-1,0,0,-1,0,0,-1,0,0,-1,0,0,-1,0,0,-1,0,0,-1,0,0,-1,0,0,-1,0,0,-1,0,0,-1,0,0,-1,0,0,-1,0,0,-1,0,0,-1,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,0,-1,0,0,-1,0,0,-1,0,0,-1,0,0,-1,0,0,-1,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,0,-1,0,0,-1,0,0,-1,0,0,-1,0,0,-1,0,0,-1,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,0,-1,0,0,-1,0,0,-1,0,0,-1,0,0,-1,0,0,-1,0,-1,0,0,-1,0,0,-1,0,0,-1,0,0,-1,0,0,-1,0,0]);e.bufferData(e.ARRAY_BUFFER,t,e.STATIC_DRAW)}function setGeometry(e){for(var s,t=new Float32Array([0,0,0,0,150,0,30,0,0,0,150,0,30,150,0,30,0,0,30,0,0,30,30,0,100,0,0,30,30,0,100,30,0,100,0,0,30,60,0,30,90,0,67,60,0,30,90,0,67,90,0,67,60,0,0,0,30,30,0,30,0,150,30,0,150,30,30,0,30,30,150,30,30,0,30,100,0,30,30,30,30,30,30,30,100,0,30,100,30,30,30,60,30,67,60,30,30,90,30,30,90,30,67,60,30,67,90,30,0,0,0,100,0,0,100,0,30,0,0,0,100,0,30,0,0,30,100,0,0,100,30,0,100,30,30,100,0,0,100,30,30,100,0,30,30,30,0,30,30,30,100,30,30,30,30,0,100,30,30,100,30,0,30,30,0,30,60,30,30,30,30,30,30,0,30,60,0,30,60,30,30,60,0,67,60,30,30,60,30,30,60,0,67,60,0,67,60,30,67,60,0,67,90,30,67,60,30,67,60,0,67,90,0,67,90,30,30,90,0,30,90,30,67,90,30,30,90,0,67,90,30,67,90,0,30,90,0,30,150,30,30,90,30,30,90,0,30,150,0,30,150,30,0,150,0,0,150,30,30,150,30,0,150,0,30,150,30,30,150,0,0,0,0,0,0,30,0,150,30,0,0,0,0,150,30,0,150,0]),o=math.xRotation(Math.PI),o=math.translate(o,-50,-75,-15),n=0;n<t.length;n+=3)s=math.transformVector(o,[t[n+0],t[n+1],t[n+2],1]),t[n+0]=s[0],t[n+1]=s[1],t[n+2]=s[2];e.bufferData(e.ARRAY_BUFFER,t,e.STATIC_DRAW)}function Degree2Radian(e){return e*Math.PI/180}function createShader(e,t,n){var o,s=e.createShader(t);if(e.shaderSource(s,n),e.compileShader(s),o=e.getShaderParameter(s,e.COMPILE_STATUS),o)return s;console.log(e.getShaderInfoLog(s)),e.deleteShader(s)}function readTextFile(e){var t=new XMLHttpRequest,n="";return t.open("GET",e,!1),t.onreadystatechange=function(){t.readyState===4&&(t.status===200||t.status==0)&&(n=t.responseText)},t.send(null),n}function createProgram(e,t,n){var o,s=e.createProgram();if(e.attachShader(s,t),e.attachShader(s,n),e.linkProgram(s),o=e.getProgramParameter(s,e.LINK_STATUS),o)return s;console.log(e.getProgramInfoLog(s)),e.deleteProgram(s)}function drawScene(){gl.viewport(0,0,gl.canvas.width,gl.canvas.height),gl.clear(gl.COLOR_BUFFER_BIT|gl.DEPTH_BUFFER_BIT),gl.enable(gl.CULL_FACE),gl.enable(gl.DEPTH_TEST),gl.useProgram(program),gl.bindVertexArray(vao);var e,n,s,o,f=gl.canvas.clientWidth/gl.canvas.clientHeight,b=1,v=2e3,g=math.perspective(fieldOfViewRadians,f,b,v),i=[100,150,200],a=[0,35,0],r=[0,1,0],p=math.lookAt(i,a,r),l=math.inverse(p),d=math.multiply4x4(g,l),t=math.yRotation(fRotationRadians),u=math.multiply4x4(d,t),h=math.inverse(t),m=math.transpose(h);gl.uniformMatrix4fv(worldViewProjectionLocation,!1,u),gl.uniformMatrix4fv(worldInverseTransposeLocation,!1,m),gl.uniformMatrix4fv(worldLocation,!1,t),gl.uniform4fv(colorLocation,[.2,1,.2,1]);const c=[40,60,120];gl.uniform3fv(lightWorldPositionLocation,c),gl.uniform3fv(viewWorldPositionLocation,i),gl.uniform1f(shininessLocation,shininess),e=math.lookAt(c,a,r),e=math.multiply4x4(math.xRotation(lightRotationX),e),e=math.multiply4x4(math.yRotation(lightRotationY),e),lightDirection=[-e[8],-e[9],-e[10]],gl.uniform3fv(lightDirectionLocation,lightDirection),gl.uniform1f(innerLimitLocation,Math.cos(innerLimit)),gl.uniform1f(outerLimitLocation,Math.cos(outerLimit)),o=gl.TRIANGLES,s=0,n=16*6,gl.drawArrays(o,s,n)}var canvas=document.querySelector("#canvas"),vertexShaderPath,fragmentShaderPath,vertexShaderSource,fragmentShaderSource,vertexShader,fragmentShader,program,positionAttributeLocation,normalAttributeLocation,worldViewProjectionLocation,worldInverseTransposeLocation,colorLocation,reverseLightDirectionLocation,lightWorldPositionLocation,worldLocation,viewWorldPositionLocation,shininessLocation,lightColorLocation,specularColorLocation,lightDirectionLocation,innerLimitLocation,outerLimitLocation,positionBuffer,vao,size,type,normalize,stride,offset,normalBuffer,fieldOfViewRadians,fRotationRadians,shininess,lightRotationX,lightRotationY,lightDirection,innerLimit,outerLimit,gl=canvas.getContext("webgl2");gl.enable(gl.CULL_FACE),gl.enable(gl.DEPTH_TEST),gl||console.log("OpenGl is not avaiable"),vertexShaderPath=canvas.dataset.vertexShader,fragmentShaderPath=canvas.dataset.fragmentShader,vertexShaderSource=readTextFile(vertexShaderPath),fragmentShaderSource=readTextFile(fragmentShaderPath),vertexShader=createShader(gl,gl.VERTEX_SHADER,vertexShaderSource),fragmentShader=createShader(gl,gl.FRAGMENT_SHADER,fragmentShaderSource),program=createProgram(gl,vertexShader,fragmentShader),positionAttributeLocation=gl.getAttribLocation(program,"a_position"),normalAttributeLocation=gl.getAttribLocation(program,"a_normal"),worldViewProjectionLocation=gl.getUniformLocation(program,"u_worldViewProjection"),worldInverseTransposeLocation=gl.getUniformLocation(program,"u_worldInverseTranspose"),colorLocation=gl.getUniformLocation(program,"u_color"),reverseLightDirectionLocation=gl.getUniformLocation(program,"u_reverseLightDirection"),lightWorldPositionLocation=gl.getUniformLocation(program,"u_lightWorldPosition"),worldLocation=gl.getUniformLocation(program,"u_world"),viewWorldPositionLocation=gl.getUniformLocation(program,"u_viewWorldPosition"),shininessLocation=gl.getUniformLocation(program,"u_shininess"),lightColorLocation=gl.getUniformLocation(program,"u_lightColor"),specularColorLocation=gl.getUniformLocation(program,"u_specularColor"),lightDirectionLocation=gl.getUniformLocation(program,"u_lightDirection"),innerLimitLocation=gl.getUniformLocation(program,"u_innerLimit"),outerLimitLocation=gl.getUniformLocation(program,"u_outerLimit"),positionBuffer=gl.createBuffer(),vao=gl.createVertexArray(),gl.bindVertexArray(vao),gl.enableVertexAttribArray(positionAttributeLocation),gl.bindBuffer(gl.ARRAY_BUFFER,positionBuffer),setGeometry(gl),size=3,type=gl.FLOAT,normalize=!1,stride=0,offset=0,gl.vertexAttribPointer(positionAttributeLocation,size,type,normalize,stride,offset),normalBuffer=gl.createBuffer(),gl.bindBuffer(gl.ARRAY_BUFFER,normalBuffer),setNormals(gl),gl.enableVertexAttribArray(normalAttributeLocation),size=3,type=gl.FLOAT,normalize=!1,stride=0,offset=0,gl.vertexAttribPointer(normalAttributeLocation,size,type,normalize,stride,offset),fieldOfViewRadians=Degree2Radian(60),fRotationRadians=0,shininess=10,lightRotationX=0,lightRotationY=0,lightDirection=[0,0,1],innerLimit=Degree2Radian(10),outerLimit=Degree2Radian(20),drawScene(),slider_transform_y=document.querySelector("#transform-y"),slider_transform_y.addEventListener("input",function(){var e=parseInt(this.nextElementSibling.value);translation[1]=e,drawScene()}),slider_transform_x=document.querySelector("#transform-x"),slider_transform_x.addEventListener("input",function(){var e=parseInt(this.nextElementSibling.value);translation[0]=e,drawScene()}),slider_transform_z=document.querySelector("#transform-z"),slider_transform_z.addEventListener("input",function(){var e=parseInt(this.nextElementSibling.value);drawScene()}),slider_scale_x=document.querySelector("#scale-x"),slider_scale_x.parentElement.previousElementSibling.textContent="LightRotaionX",slider_scale_x.addEventListener("input",function(){var e=parseFloat(this.nextElementSibling.value);lightRotationX=e,drawScene()}),slider_scale_y=document.querySelector("#scale-y"),slider_scale_y.parentElement.previousElementSibling.textContent="LightRotaionY",slider_scale_y.addEventListener("input",function(){var e=parseFloat(this.nextElementSibling.value);lightRotationY=e,drawScene()}),slider_rotate_x=document.querySelector("#rotation-x"),slider_rotate_x.parentElement.previousElementSibling.textContent="Inner limmit",slider_rotate_x.addEventListener("input",function(){var e=parseInt(this.nextElementSibling.value);innerLimit=Degree2Radian(e),drawScene()}),slider_rotate_y=document.querySelector("#rotation-y"),slider_rotate_y.addEventListener("input",function(){var e=parseInt(this.nextElementSibling.value);fRotationRadians=Degree2Radian(e),drawScene()}),slider_rotate_z=document.querySelector("#rotation-z"),slider_rotate_z.parentElement.previousElementSibling.textContent="Outer limit",slider_rotate_z.addEventListener("input",function(){var e=parseInt(this.nextElementSibling.value);outerLimit=Degree2Radian(e),drawScene()})