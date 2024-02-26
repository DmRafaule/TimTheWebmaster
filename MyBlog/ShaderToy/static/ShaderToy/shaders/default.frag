#version 300 es

precision mediump float;
uniform float f;
uniform vec2 v2;
uniform vec3 v3;

in vec3 v_color;
out vec4 outColor;

void main() {
  vec3 res1 = vec3(1.0*f,v2.x,v3.y) * v_color;
  outColor = vec4(res1,1.0);
}
