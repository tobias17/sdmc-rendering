#version 120

varying vec2 TexCoords;

uniform sampler2D colortex0;

void main(){
    gl_FragData[0] = vec4(texture2D(colortex0, TexCoords).rgb, 1.0f);
}