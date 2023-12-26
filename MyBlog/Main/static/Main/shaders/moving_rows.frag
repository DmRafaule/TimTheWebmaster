#ifdef GL_ES
precision mediump float;
#endif

uniform vec2 u_resolution;
uniform vec2 u_mouse;
uniform float u_time;

float random (in float x) {
    return fract(sin(x)*1e4);
}

float random (in vec2 st) {
    return fract(tan(dot(st.xy, vec2(1.9898,78.233)))* 44233.5453123);
}

float pattern(vec2 st, vec2 v, float t) {
    vec2 p = floor(st+v);
    return step(t, random(100. - p)+random(p.y)* 0.3 );
}

void main() {
    vec2 st = gl_FragCoord.xy/u_resolution.xy;
    st.x *= u_resolution.x/u_resolution.y;

    vec2 grid = vec2(200.0,200.);
    st *= grid;

    vec2 ipos = floor(st);  // integer
    vec2 fpos = fract(st);  // fraction

    vec2 vel = vec2(u_time * 0.1  * max(grid.x,grid.y)); // time
    vel *= vec2(0.0,1.0) * random(1.0+ipos.x); // direction

    // Assign a random value base on the integer coord
    vec2 offset = vec2(0.1,0.);

    vec3 color = vec3(0.);
    color.r = pattern(st+offset,vel,0.4);
    color.g = pattern(st,vel,0.4);
    color.b = pattern(st-offset,vel,0.4);

    // Margins
    color *= step(0.01,fpos.y);

    gl_FragColor = vec4(color,0.004*st.y);
}
