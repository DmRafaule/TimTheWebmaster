#ifdef GL_ES
precision mediump float;
#endif

attribute vec4 a_position;
 
uniform mat4 u_matrix;
 
void main() {
  // Умножаем координату на матрицу
  gl_Position = u_matrix * a_position;
}
