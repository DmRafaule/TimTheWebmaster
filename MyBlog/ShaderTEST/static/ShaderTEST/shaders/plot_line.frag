#ifdef GL_ES
precision mediump float;
#endif

uniform vec2 u_resolution;
uniform vec2 u_mouse;
uniform float u_time;

#define PI 3.14159265359

float plot(vec2 st) {
	return smoothstep(0.005, 0.0, abs(st.y - st.x));
}

float curved_plot(vec2 st, float pct) {
	return smoothstep(pct - 0.005, pct, st.y) - smoothstep( pct, pct + 0.01, st.y);
}


void main() {
	vec2 st = gl_FragCoord.xy/u_resolution;

	float y = sqrt(st.x);
	y -= pow(st.x, 7.0);
	
	// Shading effect from black on left to white on right
	vec3 color = vec3(y);

	// Plot a line
	float pct = curved_plot(st, y);
	color = (1.0 - pct) * color + pct * vec3(1.0, 0.0, 0.0);

	gl_FragColor = vec4(color, 1.0);
}
