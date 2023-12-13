#version 450 compatibility

layout(location = 0) out vec4 color_fs;
layout(location = 2) out vec4 light_color_fs;

void main() {
    vec3 seg_map_color   = vec3(61.0/255.0, 230.0/255.0, 250.0/255.0);
    vec3 attn_mask_color = vec3( 0.0/255.0,   0.0/255.0,   4.0/255.0);

    color_fs = vec4(attn_mask_color, 1.0);

    light_color_fs = vec4(0);
}
