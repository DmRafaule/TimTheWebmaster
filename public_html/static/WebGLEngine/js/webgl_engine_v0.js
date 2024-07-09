class DI{constructor(e){var t,n,s,o,i,a,r={threshold:.01},c=new IntersectionObserver(e=>{for(const t of e)t.isIntersecting?this.request_animation_id=requestAnimationFrame(e=>this.Scene(e,this)):cancelAnimationFrame(this.request_animation_id)},r);c.observe(e),this.curr=null,this.attributes={},this.uniforms={},this.primitives=[],this.context=e.getContext("webgl2"),this.context||console.log("OpenGl is not avaiable"),this.context.enable(this.context.CULL_FACE),this.context.enable(this.context.DEPTH_TEST),t=e.dataset.vertexShader,n=e.dataset.fragmentShader,s=U.readTextFile(t),o=U.readTextFile(n),i=U.createShader(this.context,this.context.VERTEX_SHADER,s),a=U.createShader(this.context,this.context.FRAGMENT_SHADER,o),this.program=U.createProgram(this.context,i,a)}get gl(){return this.context}SetContext(e){this.context=e}SetProgram(e){this.program=e}SetUniform(e){this.uniforms[e]=this.context.getUniformLocation(this.program,e)}SetAttribute(e){this.attributes[e]=this.context.getAttribLocation(this.program,e)}StartVAO(e,t){var n=this.context.createVertexArray();this.curr=this.primitives.length,this.context.bindVertexArray(n),this.primitives.push({vao:n,P:[],mode:t,vertices:e.vertices,indices:e.indices,num_indices:e.num_indices,matrices:null,matrixData:null,matrixBuffer:null,numInstances:null})}SetPrimitive(e={}){e.pos=e.pos||[0,0,0],e.color=e.color||[.2,.2,.2,1],e.scale=e.scale||[1,1,1],e.rotate=e.rotate||[0,0,0],e.rotateAngle=e.rotateAngle||0,e.animation=e.animation||function(){},this.primitives[this.curr].numInstances++,this.primitives[this.curr].P.push(e);var t,n,s,o,i,a,r=this.context.createBuffer();this.context.bindBuffer(this.context.ARRAY_BUFFER,r),this.context.enableVertexAttribArray(this.attributes.a_position),t=3,n=this.context.FLOAT,s=!1,o=0,i=0,this.context.vertexAttribPointer(this.attributes.a_position,t,n,s,o,i),this.context.bufferData(this.context.ARRAY_BUFFER,this.primitives[this.curr].vertices,this.context.STATIC_DRAW),a=this.context.createBuffer(),this.context.bindBuffer(this.context.ELEMENT_ARRAY_BUFFER,a),this.context.bufferData(this.context.ELEMENT_ARRAY_BUFFER,this.primitives[this.curr].indices,this.context.STATIC_DRAW)}EndVAO(){var e,t,n,s,i,o=16;this.primitives[this.curr].matrixData=new Float32Array(this.primitives[this.curr].numInstances*o),this.primitives[this.curr].matrices=[];for(let e=0;e<this.primitives[this.curr].numInstances;++e){const t=e*o*4,n=o;this.primitives[this.curr].matrices.push(new Float32Array(this.primitives[this.curr].matrixData.buffer,t,n))}this.primitives[this.curr].matrixBuffer=this.context.createBuffer(),this.context.bindBuffer(this.context.ARRAY_BUFFER,this.primitives[this.curr].matrixBuffer),this.context.bufferData(this.context.ARRAY_BUFFER,this.primitives[this.curr].matrixData.byteLength,this.context.STATIC_DRAW);for(let n=4*16,e=0;e<4;++e){const t=this.attributes.a_mvp+e;this.context.enableVertexAttribArray(t);const s=e*16;this.context.vertexAttribPointer(t,4,this.context.FLOAT,!1,n,s),this.context.vertexAttribDivisor(t,1)}const a=this.context.createBuffer();for(t=new Float32Array(this.primitives[this.curr].numInstances*4),e=0;e<this.primitives[this.curr].numInstances;e++)n=this.primitives[this.curr].P[e].color,t[0+4*e]=n[0],t[1+4*e]=n[1],t[2+4*e]=n[2],t[3+4*e]=n[3];this.context.bindBuffer(this.context.ARRAY_BUFFER,a),this.context.bufferData(this.context.ARRAY_BUFFER,t,this.context.STATIC_DRAW),this.context.enableVertexAttribArray(this.attributes.a_color),this.context.vertexAttribPointer(this.attributes.a_color,4,this.context.FLOAT,!1,0,0),this.context.vertexAttribDivisor(this.attributes.a_color,1);for(i=this.context.createBuffer(),s=new Float32Array(this.primitives[this.curr].numInstances*1),e=0;e<this.primitives[this.curr].numInstances;e++)s[e]=this.primitives[this.curr].P[e].point_size;this.context.bindBuffer(this.context.ARRAY_BUFFER,i),this.context.bufferData(this.context.ARRAY_BUFFER,s,this.context.STATIC_DRAW),this.context.enableVertexAttribArray(this.attributes.a_pointSize),this.context.vertexAttribPointer(this.attributes.a_pointSize,1,this.context.FLOAT,!1,0,0),this.context.vertexAttribDivisor(this.attributes.a_pointSize,1)}Scene(e,t){e*=.001;var n=e-start;start=e,U.resizeCanvasToDisplaySize(t.gl.canvas),t.gl.viewport(0,0,t.gl.canvas.clientWidth,t.gl.canvas.clientHeight),t.gl.clearColor(0,0,0,0),t.gl.clear(t.gl.COLOR_BUFFER_BIT|t.gl.DEPTH_BUFFER_BIT),t.Draw(e),t.request_animation_id=requestAnimationFrame(e=>this.Scene(e,t))}Draw(e){this.context.useProgram(this.program);for(var n,s,o,i,t=0;t<this.primitives.length;t++)this.context.bindVertexArray(this.primitives[t].vao),n=this.context.canvas.clientWidth/this.context.canvas.clientHeight,s=M.perspective(fieldOfViewRadians,n,zNear,zFar),o=M.translation(cameraPosition[0],cameraPosition[1],cameraPosition[2]),i=M.multiplyM(s,o),this.primitives[t].matrices.forEach((n,s)=>{M.identity(n);var o,a,r,l,d,u,h,m,c=this.primitives[t].P[s].pos,f=M.translation(c[0],c[1],c[2]);M.multiplyM(n,f,n),l=this.primitives[t].P[s].rotateAngle,o=this.primitives[t].P[s].rotate,a=M.Degree2Radian(l),d=M.xRotation(a*o[0]),M.multiplyM(n,d,n),u=M.yRotation(a*o[1]),M.multiplyM(n,u,n),h=M.zRotation(a*o[2]),M.multiplyM(n,h,n),r=this.primitives[t].P[s].scale,m=M.scaling(r[0],r[1],r[2]),M.multiplyM(n,m,n),this.primitives[t].P[s].animation(e,n,s,this.primitives[t].P[s].animation_args),M.multiplyM(i,n,n)}),this.context.bindBuffer(this.context.ARRAY_BUFFER,this.primitives[t].matrixBuffer),this.context.bufferSubData(this.context.ARRAY_BUFFER,0,this.primitives[t].matrixData),this.context.drawElementsInstanced(this.primitives[t].mode,this.primitives[t].num_indices,this.context.UNSIGNED_SHORT,0,this.primitives[t].numInstances)}}var M={identity:function(e){return e=e||new Float32Array(16),e[0]=1,e[1]=0,e[2]=0,e[3]=0,e[4]=0,e[5]=1,e[6]=0,e[7]=0,e[8]=0,e[9]=0,e[10]=1,e[11]=0,e[12]=0,e[13]=0,e[14]=0,e[15]=1,e},perspective:function(e,t,n,s){var o=Math.tan(Math.PI*.5-.5*e),i=1/(n-s);return[o/t,0,0,0,0,o,0,0,0,0,(n+s)*i,-1,0,0,n*s*i*2,0]},orthographic:function(e,t,n,s,o,i){return[2/(t-e),0,0,0,0,2/(s-n),0,0,0,0,2/(o-i),0,(e+t)/(e-t),(n+s)/(n-s),(o+i)/(o-i),1]},inverse:function(e){var s=e[0*4+0],v=e[0*4+1],c=e[0*4+2],m=e[0*4+3],i=e[1*4+0],d=e[1*4+1],r=e[1*4+2],a=e[1*4+3],n=e[2*4+0],l=e[2*4+1],u=e[2*4+2],h=e[2*4+3],o=e[3*4+0],f=e[3*4+1],p=e[3*4+2],g=e[3*4+3],B=u*g,O=p*h,F=r*g,y=p*a,_=r*h,w=u*a,b=c*g,x=p*m,C=c*h,E=u*m,k=c*a,A=r*m,S=n*f,M=o*l,j=i*f,T=o*d,z=i*l,D=n*d,N=s*f,L=o*v,R=s*l,P=n*v,H=s*d,I=i*v,U=B*d+y*l+_*f-(O*d+F*l+w*f),V=O*v+b*l+E*f-(B*v+x*l+C*f),$=F*v+x*d+k*f-(y*v+b*d+A*f),W=w*v+C*d+A*l-(_*v+E*d+k*l),t=1/(s*U+i*V+n*$+o*W);return[t*U,t*V,t*$,t*W,t*(O*i+F*n+w*o-(B*i+y*n+_*o)),t*(B*s+x*n+C*o-(O*s+b*n+E*o)),t*(y*s+b*i+A*o-(F*s+x*i+k*o)),t*(_*s+E*i+k*n-(w*s+C*i+A*n)),t*(S*a+T*h+z*g-(M*a+j*h+D*g)),t*(M*m+N*h+P*g-(S*m+L*h+R*g)),t*(j*m+L*a+H*g-(T*m+N*a+I*g)),t*(D*m+R*a+I*h-(z*m+P*a+H*h)),t*(j*u+D*p+M*r-(z*p+S*r+T*u)),t*(R*p+S*c+L*u-(N*u+P*p+M*c)),t*(N*r+I*p+T*c-(H*p+j*c+L*r)),t*(H*u+z*c+P*r-(R*r+I*u+D*c))]},multiplyM:function(e,t,n){var s=e[0*4+0],o=e[0*4+1],i=e[0*4+2],a=e[0*4+3],r=e[1*4+0],c=e[1*4+1],l=e[1*4+2],d=e[1*4+3],u=e[2*4+0],h=e[2*4+1],m=e[2*4+2],f=e[2*4+3],p=e[3*4+0],g=e[3*4+1],v=e[3*4+2],b=e[3*4+3],j=t[0*4+0],y=t[0*4+1],_=t[0*4+2],w=t[0*4+3],O=t[1*4+0],x=t[1*4+1],C=t[1*4+2],E=t[1*4+3],k=t[2*4+0],A=t[2*4+1],S=t[2*4+2],M=t[2*4+3],F=t[3*4+0],T=t[3*4+1],z=t[3*4+2],D=t[3*4+3];return n=n||new Float32Array(16),n[0]=j*s+y*r+_*u+w*p,n[1]=j*o+y*c+_*h+w*g,n[2]=j*i+y*l+_*m+w*v,n[3]=j*a+y*d+_*f+w*b,n[4]=O*s+x*r+C*u+E*p,n[5]=O*o+x*c+C*h+E*g,n[6]=O*i+x*l+C*m+E*v,n[7]=O*a+x*d+C*f+E*b,n[8]=k*s+A*r+S*u+M*p,n[9]=k*o+A*c+S*h+M*g,n[10]=k*i+A*l+S*m+M*v,n[11]=k*a+A*d+S*f+M*b,n[12]=F*s+T*r+z*u+D*p,n[13]=F*o+T*c+z*h+D*g,n[14]=F*i+T*l+z*m+D*v,n[15]=F*a+T*d+z*f+D*b,n},translation:function(e,t,n){return[1,0,0,0,0,1,0,0,0,0,1,0,e,t,n,1]},xRotation:function(e){var t=Math.cos(e),n=Math.sin(e);return[1,0,0,0,0,t,n,0,0,-n,t,0,0,0,0,1]},yRotation:function(e){var t=Math.cos(e),n=Math.sin(e);return[t,0,-n,0,0,1,0,0,n,0,t,0,0,0,0,1]},zRotation:function(e){var t=Math.cos(e),n=Math.sin(e);return[t,n,0,0,-n,t,0,0,0,0,1,0,0,0,0,1]},scaling:function(e,t,n){return[e,0,0,0,0,t,0,0,0,0,n,0,0,0,0,1]},multiplyV:function(e,t,n){n=n||new Float32Array(4);for(var s,o=0;o<4;++o){n[o]=0;for(s=0;s<4;++s)n[o]+=e[s]*t[s*4+o]}return n},transpose:function(e){return[e[0],e[4],e[8],e[12],e[1],e[5],e[9],e[13],e[2],e[6],e[10],e[14],e[3],e[7],e[11],e[15]]},cross:function(e,t){return[e[1]*t[2]-e[2]*t[1],e[2]*t[0]-e[0]*t[2],e[0]*t[1]-e[1]*t[0]]},subtractV:function(e,t){return[e[0]-t[0],e[1]-t[1],e[2]-t[2]]},normalize:function(e){var t=Math.sqrt(e[0]*e[0]+e[1]*e[1]+e[2]*e[2]);return t>1e-5?[e[0]/t,e[1]/t,e[2]/t]:[0,0,0]},Degree2Radian:function(e){return e*Math.PI/180}},A={rotate_around_x_axis:function(e,t,n){var s=M.xRotation(e*(.1+.1*n));M.multiplyM(t,s,t)},rotate_around_y_axis:function(e,t,n){var s=M.yRotation(e*(.1+.1*n));M.multiplyM(t,s,t)},rotate_around_z_axis:function(e,t,n){var s=M.zRotation(e*(.1+.1*n));M.multiplyM(t,s,t)},rotate_around_pointA:function(e,t,n,s){var r=[0,0,0],o=s.speed,i=s.direction,a=M.translation(Math.sin(e)*o*i[0],Math.cos(e)*o*i[1],Math.sin(e)*o*i[1]);M.multiplyM(t,a,t)},move_to:function(e,t,n,s){var o=s.speed,i=s.direction,a=M.translation(e*o*i[0],e*o*i[1],e*o*i[2]);M.multiplyM(t,a,t)}},U={resizeCanvasToDisplaySize:function(e,t){t=t||1;const n=e.clientWidth*t|0,s=e.clientHeight*t|0;return(e.width!==n||e.height!==s)&&(e.width=n,e.height=s,!0)},getRndInteger:function(e,t){return Math.floor(Math.random()*(t-e+1))+e},getRndVec:function(e,t){return[U.getRndInteger(e,t),U.getRndInteger(e,t),U.getRndInteger(e,t)]},createShader:function(e,t,n){var o,s=e.createShader(t);if(e.shaderSource(s,n),e.compileShader(s),o=e.getShaderParameter(s,e.COMPILE_STATUS),o)return s;console.log(e.getShaderInfoLog(s)),e.deleteShader(s)},readTextFile:function(e){var t=new XMLHttpRequest,n="";return t.open("GET",e,!1),t.onreadystatechange=function(){t.readyState===4&&(t.status===200||t.status==0)&&(n=t.responseText)},t.send(null),n},createProgram:function(e,t,n){var o,s=e.createProgram();if(e.attachShader(s,t),e.attachShader(s,n),e.linkProgram(s),o=e.getProgramParameter(s,e.LINK_STATUS),o)return s;console.log(e.getProgramInfoLog(s)),e.deleteProgram(s)}},primitives={e_point:{vertices:new Float32Array([0,0,0]),indices:new Uint16Array([0]),num_indices:1},e_tetrahedron:{vertices:new Float32Array([1,1,1,-1,1,-1,1,-1,-1,-1,-1,1]),indices:new Uint16Array([0,3,2,2,0,1,1,2,3,3,1,0]),num_indices:12},e_cube:{vertices:new Float32Array([1,1,1,-1,1,1,-1,1,-1,1,1,-1,1,-1,1,-1,-1,1,-1,-1,-1,1,-1,-1]),indices:new Uint16Array([0,1,2,0,2,3,0,3,4,3,7,4,0,4,1,1,4,5,1,5,2,2,6,5,2,7,3,2,6,7,6,4,5,6,7,4]),num_indices:36},e_arrow:{vertices:new Float32Array([1,2,1,2,0,1,1,0,1,-1,2,1,-1,0,1,-2,0,1,0,-1,1,1,2,-1,2,0,-1,1,0,-1,-1,2,-1,-1,0,-1,-2,0,-1,0,-1,-1]),indices:new Uint16Array([6,5,1,4,3,0,4,0,2,13,12,8,11,10,7,11,0,9,6,5,12,6,12,13,6,1,8,6,8,13,5,4,11,5,11,12,2,9,8,2,8,1,2,0,7,2,7,9,3,10,7,3,7,0,4,3,10,4,10,11]),num_indices:60},e_quad:{vertices:new Float32Array([1,1,0,-1,1,0,1,-1,0,-1,-1,0]),indices:new Uint16Array([0,1,2,2,3,1]),num_indices:6},e_triangle:{vertices:new Float32Array([0,1,0,-1,-1,0,1,-1,0]),indices:new Uint16Array([0,1,2]),num_indices:3},a_cube:{vertices:new Float32Array([-1,-1,-1,-1,-1,1,-1,1,1,1,1,-1,-1,-1,-1,-1,1,-1,1,-1,1,-1,-1,-1,1,-1,-1,1,1,-1,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,1,1,-1,1,-1,1,-1,1,-1,-1,1,-1,-1,-1,-1,1,1,-1,-1,1,1,-1,1,1,1,1,1,-1,-1,1,1,-1,1,-1,-1,1,1,1,1,-1,1,1,1,1,1,1,-1,-1,1,-1,1,1,1,-1,1,-1,-1,1,1,1,1,1,-1,1,1,1,-1,1]),normals:new Float32Array([-1,0,0,-1,0,0,-1,0,0,0,0,-1,0,0,-1,0,0,-1,0,-1,0,0,-1,0,0,-1,0,0,0,-1,0,0,-1,0,0,-1,-1,0,0,-1,0,0,-1,0,0,0,-1,0,0,-1,0,0,-1,0,0,0,1,0,0,1,0,0,1,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,0,1,0,0,1,0,0,1])}}