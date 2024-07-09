#version 300 es

in vec4 a_position;
// model , view , and projection matrix 
in mat4 a_mvp;
in vec4 a_color;
in float a_pointSize;

in vec2 a_texCoord; 
out vec2 v_texCoord;
 
void main() {
  gl_Position = a_mvp * a_position;
  gl_PointSize = a_pointSize;
  v_texCoord = a_texCoord;
}
