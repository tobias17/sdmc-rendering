#version 120

varying vec2 TexCoords;

uniform sampler2D texture;

void main(){
    gl_FragData[0] = texture2D(texture, TexCoords);
}