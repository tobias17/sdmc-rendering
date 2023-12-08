#version 450 compatibility

out vec4 vertex_color_vs;

void main() {
    vertex_color_vs = gl_Color;
    gl_Position = ftransform();
}