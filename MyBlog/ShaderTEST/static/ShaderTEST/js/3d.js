  // Указываем атрибуту, как получать данные от positionBuffer (ARRAY_BUFFER)
  var size = 3;          // 3 компоненты на итерацию
  var type = gl.FLOAT;    // наши данные - 32-битные числа с плавающей точкой
  var normalize = false;  // не нормализовать данные
  var stride = 0;         // 0 = перемещаться на size * sizeof(type) каждую итерацию для получения следующего положения
  var offset = 0;         // начинать с начала буфера
  gl.vertexAttribPointer(
      positionAttributeLocation, size, type, normalize, stride, offset);
 
  ...
 
// Заполняем текущий буфер ARRAY_BUFFER.
// Передаём значения, описывающие букву 'F'.
function setGeometry(gl) {
  gl.bufferData(
      gl.ARRAY_BUFFER,
      new Float32Array([
          // вертикальный столб
            0,   0,  0,
           30,   0,  0,
            0, 150,  0,
            0, 150,  0,
           30,   0,  0,
           30, 150,  0,
 
          // верхняя перекладина
           30,   0,  0,
          100,   0,  0,
           30,  30,  0,
           30,  30,  0,
          100,   0,  0,
          100,  30,  0,
 
          // перекладина посередине
           30,  60,  0,
           67,  60,  0,
           30,  90,  0,
           30,  90,  0,
           67,  60,  0,
           67,  90,  0]),
      gl.STATIC_DRAW);
}
var m4 = {
translation: function(tx, ty, tz) {
return [
   1,  0,  0,  0,
   0,  1,  0,  0,
   0,  0,  1,  0,
   tx, ty, tz, 1,
];
},

xRotation: function(angleInRadians) {
var c = Math.cos(angleInRadians);
var s = Math.sin(angleInRadians);

return [
  1, 0, 0, 0,
  0, c, s, 0,
  0, -s, c, 0,
  0, 0, 0, 1,
];
},

yRotation: function(angleInRadians) {
var c = Math.cos(angleInRadians);
var s = Math.sin(angleInRadians);

return [
  c, 0, -s, 0,
  0, 1, 0, 0,
  s, 0, c, 0,
  0, 0, 0, 1,
];
},

zRotation: function(angleInRadians) {
var c = Math.cos(angleInRadians);
var s = Math.sin(angleInRadians);

return [
   c, s, 0, 0,
  -s, c, 0, 0,
   0, 0, 1, 0,
   0, 0, 0, 1,
];
},

scaling: function(sx, sy, sz) {
return [
  sx, 0,  0,  0,
  0, sy,  0,  0,
  0,  0, sz,  0,
  0,  0,  0,  1,
];
},
};
