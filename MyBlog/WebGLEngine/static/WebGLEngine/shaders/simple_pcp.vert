#version 300 es

in vec4 a_position;
// model , view , and projection matrix 
in mat4 a_mvp;
in vec4 a_color;
in float a_pointSize;

out vec4 v_color;
 
void main() {
  gl_Position = a_mvp * a_position;
  gl_PointSize = a_pointSize;
  v_color = a_color;
}
