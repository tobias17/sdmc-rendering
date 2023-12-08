#version 450 compatibility

layout(location = 0) out vec4 color_fs;
layout(location = 2) out vec4 light_color_fs;

void main() {
    color_fs = vec4(6.0/255.0, 230.0/255.0, 230.0/255.0, 1.0);

    light_color_fs = vec4(0);
}
