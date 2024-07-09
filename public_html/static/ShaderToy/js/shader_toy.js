function GenerateUID(){return Math.random().toString(16).slice(2)}function SetToyStatus(e){var t=e.dataset.setedStatus,n=document.getElementById("render-status");n.innerText=t}var pause_shader_button=document.getElementById("pause_shader"),pause_render,resume_shader_button,resume_render,reload_shader_button,save_shader_button,remove_shader_buttons,upload_shader_buttons,saves_tab,upload_library_tab,toDefault_shader_button;pause_shader_button.addEventListener("click",function(){pause_render.select(),window.cancelAnimationFrame(toy.request_animation_id)}),pause_render=new ColoredRadioButton(".switch_action",pause_shader_button,"#f0bb29","#fff",SetToyStatus,pause_shader_button),resume_shader_button=document.getElementById("resume_shader"),resume_shader_button.addEventListener("click",function(){resume_render.select(),toy.request_animation_id=window.requestAnimationFrame(e=>toy.update(e,toy))}),resume_render=new ColoredRadioButton(".switch_action",resume_shader_button,"#84a8e3","#fff",SetToyStatus,resume_shader_button),reload_shader_button=document.getElementById("reload_shader"),reload_shader_button.addEventListener("click",function(){toy.clearLog(),toy.updateShaderProgram(),toy.updateUIElements(),toy.updateGeometry()});function SaveShaderAction(){for(var n,e=new Date,a=e.getDay()+"."+e.getMonth()+"."+e.getFullYear()+"-"+e.getHours()+":"+e.getMinutes()+":"+e.getSeconds()+":"+e.getMilliseconds(),s=GenerateUID(),o={buffers:[]},i={sizes:[]},t=0;t<toy.ui_elements.length;t++)n=!1,toy.ui_elements[t].buffer.constructor===Float32Array&&(n=!0),o.buffers.push({data:toy.ui_elements[t].buffer,is_raw:n}),i.sizes.push({data:toy.ui_elements[t].size});$.ajax({type:"POST",url:"save_shader/",data:{name:a,shader_id:s,fragment_src:toy.fragment_editor.getValue(),vertex_src:toy.vertex_editor.getValue(),default_geometry_data_indx:toy.default_geometry_data_indx,render_mode:toy.render_mode,bg:JSON.stringify(toy.bg),buffers:JSON.stringify(o),sizes:JSON.stringify(i)},headers:{"X-CSRFToken":csrftoken},mode:"same-origin",success:function(e){var t=document.getElementById("tab_body-8");t.insertAdjacentHTML("beforeend",e),document.getElementById("delete-"+s).addEventListener("click",RemoveShaderAction),document.getElementById("upload-"+s).addEventListener("click",UploadShaderAction)},error:function(){}})}save_shader_button=document.getElementById("save_shader"),save_shader_button.addEventListener("click",SaveShaderAction);function RemoveShaderAction(e){var t=e.target.attributes.value.nodeValue,n=document.getElementById(t);n.remove(),$.ajax({type:"POST",url:"remove_shader/",data:{shader_id:t},headers:{"X-CSRFToken":csrftoken},mode:"same-origin",success:function(){},error:function(){}})}remove_shader_buttons=document.querySelectorAll(".shader_remove_action"),remove_shader_buttons.forEach(e=>{e.addEventListener("click",RemoveShaderAction)});function UploadShaderAction(e){var t=e.target.attributes.value.nodeValue;$.ajax({type:"POST",url:"get_shader/",data:{shader_id:t},headers:{"X-CSRFToken":csrftoken},mode:"same-origin",success:function(e){toy.fragment_editor.setValue(e.fragment_src),toy.vertex_editor.setValue(e.vertex_src),toy.clearLog(),toy.updateShaderProgram(),toy.updateUIElements(),toy.updateGeometry(),toy.default_geometry_data_indx=e.dgd_indx,toy.render_mode=parseInt(e.render_mode);var t,n,o,i,s=JSON.parse(e.bg);toy.bg_color_btn.update(s),toy.updateBgColor(s[0],"r"),toy.updateBgColor(s[1],"g"),toy.updateBgColor(s[2],"b"),toy.updateBgColor(s[3],"a");for(n=JSON.parse(e.buffers),i=JSON.parse(e.sizes),t=0;t<toy.ui_elements.length;t++){if(n.buffers[t].is_raw){o=[];for(value in n.buffers[t].data)o.push(n.buffers[t].data[value]);toy.ui_elements[t].buffer=new Float32Array(o)}else toy.ui_elements[t].buffer=n.buffers[t].data;toy.ui_elements[t].size=i.sizes[t].data}toy.updateUIElements(),toy.updateGeometry()},error:function(){}})}upload_shader_buttons=document.querySelectorAll(".shader_upload_action"),upload_shader_buttons.forEach(e=>{e.addEventListener("click",UploadShaderAction)});function LoadSaves(){$.ajax({type:"POST",url:"load_shader/",headers:{"X-CSRFToken":csrftoken},mode:"same-origin",success:function(e){var t,n=document.getElementById("tab_body-8");n.insertAdjacentHTML("beforeend",e),t=n.querySelectorAll(".save_shader"),t.forEach(e=>{document.getElementById("delete-"+e.id).addEventListener("click",RemoveShaderAction),document.getElementById("upload-"+e.id).addEventListener("click",UploadShaderAction)})},error:function(){}})}saves_tab=document.getElementById("tab_button_for_save"),saves_tab.addEventListener("click",LoadSaves,{once:!0});function LoadLibrary(){$.ajax({type:"POST",url:"load_library/",headers:{"X-CSRFToken":csrftoken},mode:"same-origin",success:function(e){var t,n=document.getElementById("tab_body-5");n.insertAdjacentHTML("beforeend",e),t=n.querySelectorAll(".save_shader"),t.forEach(e=>{document.getElementById("delete-"+e.id).remove(),document.getElementById("upload-"+e.id).addEventListener("click",UploadShaderAction)})},error:function(){}})}upload_library_tab=document.getElementById("tab_button_for_lib"),upload_library_tab.addEventListener("click",LoadLibrary,{once:!0}),toDefault_shader_button=document.getElementById("toDefault_shader"),toDefault_shader_button.addEventListener("click",function(){toy.render_mode=toy.gl.TRIANGLES,toy.render_mode_btn.update(0),toy.bg=[1,1,1,1],toy.bg_color_btn.update(toy.bg),resume_render.select(),toy.setFromDefaultsShaderSrouceCode(),toy.updateShaderProgram(),toy.setFromDefaultsUIElements(),toy.updateGeometry()});function handleRawData(e,t){switch(e.tagName){case"INPUT":e.type=="number"?(this.size=parseInt(t),toy.updateShaderProgram(),toy.updateUIElements(),this.loc=toy.gl.getAttribLocation(toy.program,this.name),toy.updateGeometry()):toy.default_geometry_data_indx=parseInt(t);break;case"TEXTAREA":this.buffer=new Float32Array(t.split(",").map(e=>parseFloat(e))),toy.updateShaderProgram(),toy.updateUIElements(),this.loc=toy.gl.getAttribLocation(toy.program,this.name),toy.updateGeometry();break}}function handleFloat(e,t){this.buffer=parseFloat(t)}function handleInt(e,t){this.buffer=parseInt(t)}function handleBool(e,t){this.buffer=parseInt(t)}function handleFloatVector(e,t){var n=parseInt(e.dataset.vecIndx);this.buffer[n]=parseFloat(t)}function handleBoolVector(e,t){var n=parseInt(e.dataset.vecIndx);this.buffer[n]=parseInt(t)}function handleIntVector(e,t){var n=parseInt(e.dataset.vecIndx);this.buffer[n]=parseInt(t)}function handleMatrix(e,t){var n=parseInt(e.dataset.vecIndx);this.buffer[n]=parseFloat(t)}function resizeCanvasToDisplaySize(e,t){t=t||1;const n=e.clientWidth*t|0,s=e.clientHeight*t|0;return(e.width!==n||e.height!==s)&&(e.width=n,e.height=s,!0)}function onInputChange(){function e(e){e.forEach(e=>{var t=e.dataset.uiElementId;e.addEventListener("change",e=>{toy.ui_elements[t].handler(e.target,e.target.value)})})}function t(t){for(const n of t)if(n.addedNodes.length>0){const t=n.addedNodes[0].querySelectorAll(".input_el");e(t)}}const n=document.querySelectorAll(".toObserve"),s={childList:!0},o=new MutationObserver(t);n.forEach(e=>{o.observe(e,s)});const i=document.querySelectorAll(".input_el");e(i)}document.addEventListener("DOMContentLoaded",onInputChange);function UpdateMousePos(e){var t=e.target.getBoundingClientRect(),n=e.clientX-t.left,s=e.clientY-t.top;toy.mouse_pos[0]=n,toy.mouse_pos[1]=s}document.getElementById("canvas").onmousemove=UpdateMousePos;class ShaderToy{constructor(){window.onerror=this.log,this.start=0,this.default_geometry_data_indx=0,this.mouse_pos=[0,0],this.render_mode_btn=new RadioButton(".render_mode",this.updateRenderMode),this.pipeline_work_btn=new CheckBoxButton(".pipeline_work",this.updatePipelineCheck,this.updatePipelineUnCheck),this.bg_color_btn=new InputValueButton(".bg_color",this.updateBgColor),this.fragment_editor=ace.edit("fragment_editor"),this.fragment_editor.session.setMode("ace/mode/glsl"),this.vertex_editor=ace.edit("vertex_editor"),this.vertex_editor.session.setMode("ace/mode/glsl"),this.canvas=document.querySelector("#canvas"),this.gl=this.canvas.getContext("webgl2"),this.render_mode=this.gl.TRIANGLES,this.bg=[1,1,1,1],this.gl||this.log("OpenGl is not avaiable"),resume_render.select(),this.setFromDefaultsShaderSrouceCode(),this.updateShaderProgram(),this.setFromDefaultsUIElements(),this.updateGeometry()}setFromDefaultsShaderSrouceCode(){this.vertexShaderPath=this.canvas.dataset.vertexShader,this.fragmentShaderPath=this.canvas.dataset.fragmentShader,this.vertex_editor.setValue(this.readTextFile(this.vertexShaderPath)),this.fragment_editor.setValue(this.readTextFile(this.fragmentShaderPath))}updateShaderProgram(){this.fragment_source_code=this.fragment_editor.getValue(),this.vertex_source_code=this.vertex_editor.getValue(),this.vertexShader=this.createShader(this.gl,this.gl.VERTEX_SHADER,this.vertex_source_code),this.fragmentShader=this.createShader(this.gl,this.gl.FRAGMENT_SHADER,this.fragment_source_code),this.program=this.createProgram(this.gl,this.vertexShader,this.fragmentShader)}setFromDefaultsUIElements(){this.uTimeLoc=this.gl.getUniformLocation(this.program,"u_time"),this.uResolutionLoc=this.gl.getUniformLocation(this.program,"u_resolution"),this.uMousePosLoc=this.gl.getUniformLocation(this.program,"u_mouse"),this.uniforms=this.getUniforms,this.attributes=this.getAttributes,this.ui_elements=[],this.clearwebUIElements(),this.clearbuffUIElements();for(var e=0;e<this.attributes.length;e++)this.setUIElement(this.attributes[e]);for(e=0;e<this.uniforms.length;e++)this.setUIElement(this.uniforms[e]);for(e=0;e<this.ui_elements.length;e++)this.setbufferUIElement(this.ui_elements[e]),this.setwebUIElement(this.ui_elements[e]),this.setcallbacksUIElement(this.ui_elements[e])}updateUIElements(){this.uTimeLoc=this.gl.getUniformLocation(this.program,"u_time"),this.uResolutionLoc=this.gl.getUniformLocation(this.program,"u_resolution"),this.uMousePosLoc=this.gl.getUniformLocation(this.program,"u_mouse"),this.uniforms=this.getUniforms,this.attributes=this.getAttributes;var e,s,o,t=[],n=0;for(this.clearwebUIElements();n<this.attributes.length;n++)t.push({buffer:null,name:this.attributes[n].name,loc:this.attributes[n].loc,type_data:this.attributes[n].type}),this.setbufferUIElement(t[n]),this.setcallbacksUIElement(t[n]),o=t.length-1,t[n].id=o;for(e=0;e<this.uniforms.length;e++)t.push({buffer:null,name:this.uniforms[e].name,loc:this.uniforms[e].loc,type_data:this.uniforms[e].type}),this.setbufferUIElement(t[n]),this.setcallbacksUIElement(t[n]),o=t.length-1,t[n].id=o,n+=1;for(e=0;e<t.length;e++)for(s=0;s<this.ui_elements.length;s++)if(t[e].name==this.ui_elements[s].name){t[e].buffer=this.ui_elements[s].buffer,t[e].update=this.ui_elements[s].update,t[e].handler=this.ui_elements[s].handler,t[e].size=this.ui_elements[s].size;break}this.ui_elements=t;for(e=0;e<this.ui_elements.length;e++)this.setwebUIElement(this.ui_elements[e]),this.setcallbacksUIElement(this.ui_elements[e])}updateGeometry(){this.vao=this.gl.createVertexArray(),this.gl.bindVertexArray(this.vao);for(var t,n,s,o,i,a,e=0;e<this.attributes.length;e++)t=this.gl.createBuffer(),this.gl.bindBuffer(this.gl.ARRAY_BUFFER,t),this.gl.bufferData(this.gl.ARRAY_BUFFER,this.ui_elements[e].buffer,this.gl.STATIC_DRAW),this.gl.enableVertexAttribArray(this.ui_elements[e].loc),n=this.ui_elements[e].size,s=this.gl.FLOAT,o=!1,i=0,a=0,this.gl.vertexAttribPointer(this.ui_elements[e].loc,n,s,o,i,a)}updateRenderMode(e){switch(e){case"TRIANGLES":toy.render_mode=toy.gl.TRIANGLES;break;case"POINTS":toy.render_mode=toy.gl.POINTS;break;case"LINES":toy.render_mode=toy.gl.LINES;break;case"LINE_LOOP":toy.render_mode=toy.gl.LINE_LOOP;break;case"LINE_STRIP":toy.render_mode=toy.gl.LINE_STRIP;break;case"TRIANGLE_STRIP":toy.render_mode=toy.gl.TRIANGLE_STRIP;break;case"TRIANGLE_FAN":toy.render_mode=toy.gl.TRIANGLE_FAN;break}}updatePipelineUnCheck(e){switch(e){case"BLEND":toy.gl.disable(toy.gl.BLEND);break;case"CULL_FACE":toy.gl.disable(toy.gl.CULL_FACE);break;case"DEPTH_TEST":toy.gl.disable(toy.gl.DEPTH_TEST);break;case"DITHER":toy.gl.disable(toy.gl.DITHER);break;case"POLYGON_OFFSET_FILL":toy.gl.disable(toy.gl.POLYGON_OFFSET_FILL);break;case"SAMPLE_ALPHA_TO_COVERAGE":toy.gl.disable(toy.gl.SAMPLE_ALPHA_TO_COVERAGE);break;case"SAMPLE_COVERAGE":toy.gl.disable(toy.gl.SAMPLE_COVERAGE);break;case"SCISSOR_TEST":toy.gl.disable(toy.gl.SCISSOR_TEST);break;case"STENCIL_TEST":toy.gl.disable(toy.gl.STENCIL_TEST);break}}updatePipelineCheck(e){switch(e){case"BLEND":toy.gl.enable(toy.gl.BLEND);break;case"CULL_FACE":toy.gl.enable(toy.gl.CULL_FACE);break;case"DEPTH_TEST":toy.gl.enable(toy.gl.DEPTH_TEST);break;case"DITHER":toy.gl.enable(toy.gl.DITHER);break;case"POLYGON_OFFSET_FILL":toy.gl.enable(toy.gl.POLYGON_OFFSET_FILL);break;case"SAMPLE_ALPHA_TO_COVERAGE":toy.gl.enable(toy.gl.SAMPLE_ALPHA_TO_COVERAGE);break;case"SAMPLE_COVERAGE":toy.gl.enable(toy.gl.SAMPLE_COVERAGE);break;case"SCISSOR_TEST":toy.gl.enable(toy.gl.SCISSOR_TEST);break;case"STENCIL_TEST":toy.gl.enable(toy.gl.STENCIL_TEST);break}}updateBgColor(e,t){var n=parseFloat(e);switch(t){case"r":toy.bg[0]=n;break;case"g":toy.bg[1]=n;break;case"b":toy.bg[2]=n;break;case"a":toy.bg[3]=n;break}}isBuiltIn(e){const t=e.name;return t.startsWith("gl_")||t.startsWith("webgl_")}glEnum2String(e){if(typeof e!="string"){const t=[];for(const n in this.gl)this.gl[n]===e&&t.push(n);return t.length?t.join(" | "):`0x${e.toString(16)}`}return e}get getUniforms(){var e=[];const t=this.gl.getProgramParameter(this.program,this.gl.ACTIVE_UNIFORMS),n=[...Array(t).keys()],s=this.gl.getActiveUniforms(this.program,n,this.gl.UNIFORM_BLOCK_INDEX),o=this.gl.getActiveUniforms(this.program,n,this.gl.UNIFORM_OFFSET);for(let n=0;n<t;++n){const a=this.gl.getActiveUniform(this.program,n);if(this.isBuiltIn(a))continue;const{name:i,type:r,size:l}=a;if(i=="u_time"||i=="u_resolution"||i=="u_mouse")continue;const d=s[n],u=o[n],c=this.gl.getUniformLocation(this.program,i);e.push({loc:c,name:i,type:r})}return e}get getAttributes(){var e=[];const t=this.gl.getProgramParameter(this.program,this.gl.ACTIVE_ATTRIBUTES);for(let n=0;n<t;++n){const{name:s,type:i,size:a}=this.gl.getActiveAttrib(this.program,n),o=this.gl.getAttribLocation(this.program,s);e.push({loc:o,name:s,type:"RAW_DATA"})}return e}setUIElement(e){this.ui_elements.push({buffer:e.buffer,name:e.name,loc:e.loc,size:null,update:()=>{},handler:()=>{},type_data:e.type});var t=this.ui_elements.length-1;this.ui_elements[t].id=t}updateUIElement(e,t){this.ui_elements[t].name=e.name,this.ui_elements[t].loc=e.loc,this.ui_elements[t].type_data=e.type,this.ui_elements[t].id=t}clearwebUIElements(){var e=document.getElementById("tab_body-4"),t=e.querySelectorAll(".mat-type");t.forEach(e=>{e.remove()})}clearbuffUIElements(){this.ui_elements.length=0}setcallbacksUIElement(e){switch(this.glEnum2String(e.type_data)){case"RAW_DATA":e.handler=handleRawData,e.update=()=>{};break;case"FLOAT":e.handler=handleFloat,e.update=function(){toy.gl.uniform1f(e.loc,e.buffer)};break;case"BOOL":e.handler=handleBool,e.update=function(){toy.gl.uniform1i(e.loc,e.buffer)};break;case"INT":e.handler=handleInt,e.update=function(){toy.gl.uniform1i(e.loc,e.buffer)};break;case"FLOAT_VEC2":e.handler=handleFloatVector,e.update=function(){toy.gl.uniform2fv(e.loc,e.buffer)};break;case"FLOAT_VEC3":e.handler=handleFloatVector,e.update=function(){toy.gl.uniform3fv(e.loc,e.buffer)};break;case"FLOAT_VEC4":e.handler=handleFloatVector,e.update=function(){toy.gl.uniform4fv(e.loc,e.buffer)};break;case"BOOL_VEC2":e.handler=handleBoolVector,e.update=function(){toy.gl.uniform2iv(e.loc,e.buffer)};break;case"BOOL_VEC3":e.handler=handleBoolVector,e.update=function(){toy.gl.uniform3iv(e.loc,e.buffer)};break;case"BOOL_VEC4":e.handler=handleBoolVector,e.update=function(){toy.gl.uniform4iv(e.loc,e.buffer)};break;case"INT_VEC2":e.handler=handleIntVector,e.update=function(){toy.gl.uniform2iv(e.loc,e.buffer)};break;case"INT_VEC3":e.handler=handleIntVector,e.update=function(){toy.gl.uniform3iv(e.loc,e.buffer)};break;case"INT_VEC4":e.handler=handleIntVector,e.update=function(){toy.gl.uniform4iv(e.loc,e.buffer)};break;case"FLOAT_MAT2":e.handler=handleMatrix,e.update=function(){toy.gl.uniformMatrix2fv(e.loc,!1,e.buffer)};break;case"FLOAT_MAT3":e.handler=handleMatrix,e.update=function(){toy.gl.uniformMatrix3fv(e.loc,!1,e.buffer)};break;case"FLOAT_MAT4":e.handler=handleMatrix,e.update=function(){toy.gl.uniformMatrix4fv(e.loc,!1,e.buffer)};break}}setwebUIElement(e){var n,s,t="";switch(this.glEnum2String(e.type_data)){case"RAW_DATA":n=null,e.id==this.default_geometry_data_indx?n="checked":n="",t=`<fieldset class="mat-type">
	<legend>
		${e.name} | RAW_DATA	
	</legend>
	<div class="input_data column min_row_gap">
		<div class="row min_col_gap no_wrap">
			<p>step</p>
			<input data-ui-element-id="${e.id}" class="input_el" value="${e.size}" type="number" id="tentacles" name="tentacles" step="1"/>
		</div>
		<div class="row min_col_gap no_wrap">
			<p>is for geometry</p>
			<input data-ui-element-id="${e.id}" class="input_el" value="${e.id}" type="radio" name="geometry" ${n}/>
		</div>
		<hr>
		<textarea data-ui-element-id="${e.id}" class="input_el" name="about" id="">
${e.buffer}
		</textarea>
	</div>
</fieldset>`;break;case"FLOAT":t=`<fieldset class="mat-type">
	<legend>
		${e.name} | FLOAT
	</legend>
	<input data-ui-element-id="${e.id}" class="input_el" value="${e.buffer}" type="number" id="tentacles" name="tentacles" step="0.01"/>
</fieldset>`;break;case"BOOL":t=`<fieldset class="mat-type">
	<legend>
		${e.name} | BOOL 
	</legend>
	<input data-ui-element-id="${e.id}" class="input_el" value="${e.buffer}" min="0" max="1" type="number" id="tentacles" name="tentacles" step="1"/>
</fieldset>`;break;case"INT":t=`<fieldset class="mat-type">
	<legend>
		${e.name} | INT
	</legend>
	<input data-ui-element-id="${e.id}" class="input_el" value="${e.buffer}" type="number" id="tentacles" name="tentacles" step="1"/>
</fieldset>`;break;case"FLOAT_VEC2":t=`<fieldset class="mat-type">
	<legend>
		${e.name} | FLOAT VECTOR_2
	</legend>
	<div class="input_vector">
		<input data-ui-element-id="${e.id}" data-vec-indx="0" class="input_el" value="${e.buffer[0]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
		<input data-ui-element-id="${e.id}" data-vec-indx="1" class="input_el" value="${e.buffer[1]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
	</div>
</fieldset>`;break;case"FLOAT_VEC3":t=`<fieldset class="mat-type">
	<legend>
		${e.name} | FLOAT VECTOR_3
	</legend>
	<div class="input_vector">
		<input data-ui-element-id="${e.id}" data-vec-indx="0" class="input_el" value="${e.buffer[0]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
		<input data-ui-element-id="${e.id}" data-vec-indx="1" class="input_el" value="${e.buffer[1]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
		<input data-ui-element-id="${e.id}" data-vec-indx="2" class="input_el" value="${e.buffer[2]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
	</div>
</fieldset>`;break;case"FLOAT_VEC4":t=`<fieldset class="mat-type">
	<legend>
		${e.name} | FLOAT VECTOR_4
	</legend>
	<div class="input_vector">
		<input data-ui-element-id="${e.id}" data-vec-indx="0" class="input_el" value="${e.buffer[0]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
		<input data-ui-element-id="${e.id}" data-vec-indx="1" class="input_el" value="${e.buffer[1]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
		<input data-ui-element-id="${e.id}" data-vec-indx="2" class="input_el" value="${e.buffer[2]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
		<input data-ui-element-id="${e.id}" data-vec-indx="3" class="input_el" value="${e.buffer[3]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
	</div>
</fieldset>`;break;case"BOOL_VEC2":t=`<fieldset class="mat-type">
	<legend>
		${e.name} | BOOL VECTOR_2
	</legend>
	<div class="input_vector">
		<input data-ui-element-id="${e.id}" data-vec-indx="0" class="input_el" value="${e.buffer[0]}" min="0" max="1" type="number" id="tentacles" name="tentacles" step="1"/>
		<input data-ui-element-id="${e.id}" data-vec-indx="1" class="input_el" value="${e.buffer[1]}" min="0" max="1" type="number" id="tentacles" name="tentacles" step="1"/>
	</div>
</fieldset>`;break;case"BOOL_VEC3":t=`<fieldset class="mat-type">
	<legend>
		${e.name} | BOOL VECTOR_3
	</legend>
	<div class="input_vector">
		<input data-ui-element-id="${e.id}" data-vec-indx="0" class="input_el" value="${e.buffer[0]}" min="0" max="1" type="number" id="tentacles" name="tentacles" step="1"/>
		<input data-ui-element-id="${e.id}" data-vec-indx="1" class="input_el" value="${e.buffer[1]}" min="0" max="1" type="number" id="tentacles" name="tentacles" step="1"/>
		<input data-ui-element-id="${e.id}" data-vec-indx="2" class="input_el" value="${e.buffer[2]}" min="0" max="1" type="number" id="tentacles" name="tentacles" step="1"/>
	</div>
</fieldset>`;break;case"BOOL_VEC4":t=`<fieldset class="mat-type">
	<legend>
		${e.name} | BOOL VECTOR_4
	</legend>
	<div class="input_vector">
		<input data-ui-element-id="${e.id}" data-vec-indx="0" class="input_el" value="${e.buffer[0]}" min="0" max="1" type="number" id="tentacles" name="tentacles" step="1"/>
		<input data-ui-element-id="${e.id}" data-vec-indx="1" class="input_el" value="${e.buffer[1]}" min="0" max="1" type="number" id="tentacles" name="tentacles" step="1"/>
		<input data-ui-element-id="${e.id}" data-vec-indx="2" class="input_el" value="${e.buffer[2]}" min="0" max="1" type="number" id="tentacles" name="tentacles" step="1"/>
		<input data-ui-element-id="${e.id}" data-vec-indx="3" class="input_el" value="${e.buffer[3]}" min="0" max="1" type="number" id="tentacles" name="tentacles" step="1"/>
	</div>
</fieldset>`;break;case"INT_VEC2":t=`<fieldset class="mat-type">
	<legend>
		${e.name} | INT VECTOR_2
	</legend>
	<div class="input_vector">
		<input data-ui-element-id="${e.id}" data-vec-indx="0" class="input_el" value="${e.buffer[0]}" type="number" id="tentacles" name="tentacles" step="1"/>
		<input data-ui-element-id="${e.id}" data-vec-indx="1" class="input_el" value="${e.buffer[1]}" type="number" id="tentacles" name="tentacles" step="1"/>
	</div>
</fieldset>`;break;case"INT_VEC3":t=`<fieldset class="mat-type">
	<legend>
		${e.name} | INT VECTOR_3
	</legend>
	<div class="input_vector">
		<input data-ui-element-id="${e.id}" data-vec-indx="0" class="input_el" value="${e.buffer[0]}" type="number" id="tentacles" name="tentacles" step="1"/>
		<input data-ui-element-id="${e.id}" data-vec-indx="1" class="input_el" value="${e.buffer[1]}" type="number" id="tentacles" name="tentacles" step="1"/>
		<input data-ui-element-id="${e.id}" data-vec-indx="2" class="input_el" value="${e.buffer[2]}" type="number" id="tentacles" name="tentacles" step="1"/>
	</div>
</fieldset>`;break;case"INT_VEC4":t=`<fieldset class="mat-type">
	<legend>
		${e.name} | INT VECTOR_4
	</legend>
	<div class="input_vector">
		<input data-ui-element-id="${e.id}" data-vec-indx="0" class="input_el" value="${e.buffer[0]}" type="number" id="tentacles" name="tentacles" step="1"/>
		<input data-ui-element-id="${e.id}" data-vec-indx="1" class="input_el" value="${e.buffer[1]}" type="number" id="tentacles" name="tentacles" step="1"/>
		<input data-ui-element-id="${e.id}" data-vec-indx="2" class="input_el" value="${e.buffer[2]}" type="number" id="tentacles" name="tentacles" step="1"/>
		<input data-ui-element-id="${e.id}" data-vec-indx="3" class="input_el" value="${e.buffer[3]}" type="number" id="tentacles" name="tentacles" step="1"/>
	</div>
</fieldset>`;break;case"FLOAT_MAT2":t=`<fieldset class="mat-type">
						<legend>
							${e.name} | MATRIX_2x2
						</legend>
						<div class="input_matrix">
							<div class="input_vector">
								<input data-ui-element-id="${e.id}" data-vec-indx="0" class="input_el" value="${e.buffer[0]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
								<input data-ui-element-id="${e.id}" data-vec-indx="1" class="input_el" value="${e.buffer[1]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
							</div>
							<div class="input_vector">
								<input data-ui-element-id="${e.id}" data-vec-indx="2" class="input_el" value="${e.buffer[2]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
								<input data-ui-element-id="${e.id}" data-vec-indx="3" class="input_el" value="${e.buffer[3]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
							</div>
						</div>
					</fieldset>`;break;case"FLOAT_MAT3":t=`<fieldset class="mat-type">
						<legend>
							${e.name} | MATRIX_3x3
						</legend>
						<div class="input_matrix">
							<div class="input_vector">
								<input data-ui-element-id="${e.id}" data-vec-indx="0" class="input_el" value="${e.buffer[0]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
								<input data-ui-element-id="${e.id}" data-vec-indx="1" class="input_el" value="${e.buffer[1]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
								<input data-ui-element-id="${e.id}" data-vec-indx="2" class="input_el" value="${e.buffer[2]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
							</div>
							<div class="input_vector">
								<input data-ui-element-id="${e.id}" data-vec-indx="3" class="input_el" value="${e.buffer[3]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
								<input data-ui-element-id="${e.id}" data-vec-indx="4" class="input_el" value="${e.buffer[4]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
								<input data-ui-element-id="${e.id}" data-vec-indx="5" class="input_el" value="${e.buffer[5]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
							</div>
							<div class="input_vector">
								<input data-ui-element-id="${e.id}" data-vec-indx="6" class="input_el" value="${e.buffer[6]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
								<input data-ui-element-id="${e.id}" data-vec-indx="7" class="input_el" value="${e.buffer[7]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
								<input data-ui-element-id="${e.id}" data-vec-indx="8" class="input_el" value="${e.buffer[8]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
							</div>
						</div>
					</fieldset>`;break;case"FLOAT_MAT4":t=`<fieldset class="mat-type">
						<legend>
							${e.name} | MATRIX_4x4
						</legend>
						<div class="input_matrix">
							<div class="input_vector">
								<input data-ui-element-id="${e.id}" data-vec-indx="0" class="input_el" value="${e.buffer[0]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
								<input data-ui-element-id="${e.id}" data-vec-indx="1" class="input_el" value="${e.buffer[1]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
								<input data-ui-element-id="${e.id}" data-vec-indx="2" class="input_el" value="${e.buffer[2]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
								<input data-ui-element-id="${e.id}" data-vec-indx="3" class="input_el" value="${e.buffer[3]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
							</div>
							<div class="input_vector">
								<input data-ui-element-id="${e.id}" data-vec-indx="4" class="input_el" value="${e.buffer[4]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
								<input data-ui-element-id="${e.id}" data-vec-indx="5" class="input_el" value="${e.buffer[5]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
								<input data-ui-element-id="${e.id}" data-vec-indx="6" class="input_el" value="${e.buffer[6]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
								<input data-ui-element-id="${e.id}" data-vec-indx="7" class="input_el" value="${e.buffer[7]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
							</div>
							<div class="input_vector">
								<input data-ui-element-id="${e.id}" data-vec-indx="8" class="input_el" value="${e.buffer[8]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
								<input data-ui-element-id="${e.id}" data-vec-indx="9" class="input_el" value="${e.buffer[9]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
								<input data-ui-element-id="${e.id}" data-vec-indx="10" class="input_el" value="${e.buffer[10]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
								<input data-ui-element-id="${e.id}" data-vec-indx="11" class="input_el" value="${e.buffer[11]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
							</div>
							<div class="input_vector">
								<input data-ui-element-id="${e.id}" data-vec-indx="12" class="input_el" value="${e.buffer[12]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
								<input data-ui-element-id="${e.id}" data-vec-indx="13" class="input_el" value="${e.buffer[13]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
								<input data-ui-element-id="${e.id}" data-vec-indx="14" class="input_el" value="${e.buffer[14]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
								<input data-ui-element-id="${e.id}" data-vec-indx="15" class="input_el" value="${e.buffer[15]}" type="number" id="tentacles" name="tentacles" step="0.01"/>
							</div>
						</div>
					</fieldset>`;break}s=document.getElementById("tab_body-4"),s.insertAdjacentHTML("beforeend",t)}setbufferUIElement(e,t){var n=t||this.glEnum2String(e.type_data);switch(n){case"RAW_DATA":e.buffer=new Float32Array([-1,1,1,1,-1,-1,-1,-1,1,1,1,-1]),e.size=2;break;case"FLOAT":e.buffer=1;break;case"BOOL":e.buffer=!0;break;case"INT":e.buffer=1;break;case"FLOAT_VEC2":e.buffer=[1,1];break;case"FLOAT_VEC3":e.buffer=[1,1,1];break;case"FLOAT_VEC4":e.buffer=[1,1,1,1];break;case"BOOL_VEC2":e.buffer=[0,0];break;case"BOOL_VEC3":e.buffer=[0,0,0];break;case"BOOL_VEC4":e.buffer=[0,0,0,0];break;case"INT_VEC2":e.buffer=[1,1];break;case"INT_VEC3":e.buffer=[1,1,1];break;case"INT_VEC4":e.buffer=[1,1,1,1];break;case"FLOAT_MAT2":e.buffer=[1,0,0,1];break;case"FLOAT_MAT3":e.buffer=[1,0,0,0,1,0,0,0,1];break;case"FLOAT_MAT4":e.buffer=[1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1];break}}createProgram(e,t,n){var o,s=e.createProgram();if(e.attachShader(s,t),e.attachShader(s,n),e.linkProgram(s),o=e.getProgramParameter(s,e.LINK_STATUS),o)return s;this.log(e.getProgramInfoLog(s)),e.deleteProgram(s)}createShader(e,t,n){var o,s=e.createShader(t);if(e.shaderSource(s,n),e.compileShader(s),o=e.getShaderParameter(s,e.COMPILE_STATUS),o)return s;this.log(e.getShaderInfoLog(s)),e.deleteShader(s)}readTextFile(e){var t=new XMLHttpRequest,n="";return t.open("GET",e,!1),t.onreadystatechange=function(){t.readyState===4&&(t.status===200||t.status==0)&&(n=t.responseText)},t.send(null),n}log(e){var t,n,s=document.getElementById("tab_button_for_err");s.style.display="flex",t=document.getElementById("tab_body-7"),n=`
<div class="logs_and_erros">${e}</div>`,t.insertAdjacentHTML("beforeend",n)}clearLog(){var e,t=document.getElementById("tab_button_for_err");t.style.display="none",e=document.getElementById("tab_body-7"),e.innerHTML=""}update(e,t){e*=.001,t.deltaTime=e-t.start,t.start=e,resizeCanvasToDisplaySize(t.canvas),t.gl.viewport(0,0,t.gl.canvas.width,t.gl.canvas.height),t.gl.clearColor(t.bg[0],t.bg[1],t.bg[2],t.bg[3]),t.gl.clear(t.gl.COLOR_BUFFER_BIT|t.gl.DEPTH_BUFFER_BIT),t.gl.useProgram(t.program),t.gl.bindVertexArray(t.vao);for(var n=0;n<t.ui_elements.length;n++)t.ui_elements[n].update();t.gl.uniform1f(t.uTimeLoc,e),t.gl.uniform2fv(t.uResolutionLoc,[t.gl.canvas.width,t.gl.canvas.height]),t.gl.uniform2fv(t.uMousePosLoc,t.mouse_pos),t.draw(e),t.request_animation_id=window.requestAnimationFrame(e=>this.update(e,t))}draw(){var e=this.render_mode,t=0,n=this.ui_elements[this.default_geometry_data_indx].buffer.length/this.ui_elements[this.default_geometry_data_indx].size;this.gl.drawArrays(e,t,n)}run(){this.request_animation_id=window.requestAnimationFrame(e=>this.update(e,this))}}let toy=new ShaderToy;toy.run()