/*

En este proyecto usamos un piezoelectrico como sensor

*/

// declaramos las constantes para el uso de los pines
const int pinPiezo = A0;
const int pinPiezo1 = A1;
const int pinPiezo2 = A2;
const int pinPiezo3 = A3;
const int pinPiezo4 = A4;
const int pinPiezo5 =  A5;    // piezo conectado al pin analogico  0

// declaramos una constante con el valor del umbral
const int umbral   = 10;    // valor umbral para detectar un golpe

// declaramos las variables para los valores de lectura y estdo del led
int lecturaSensor = 0;       // variable para gaurdar el valor del sensor
int lecturaSensor1 = 0;
int lecturaSensor2 = 0;
int lecturaSensor3 = 0;
int lecturaSensor4 = 0;
int lecturaSensor5 = 0;

void setup() {
	Serial.begin(9600);        // inicializamos la comunicacion serial
}

void loop() {
	// leemos el valor del sensor en lecturaSensor
	lecturaSensor = analogRead(pinPiezo);
	lecturaSensor1 = analogRead(pinPiezo1);
	lecturaSensor2 = analogRead(pinPiezo2);
	lecturaSensor3 = analogRead(pinPiezo3);
	lecturaSensor4 = analogRead(pinPiezo4);
	lecturaSensor5 = analogRead(pinPiezo5);
	// si el valor del sensor es mayor que el umbral
	if (lecturaSensor >= umbral) {
	// Y mandamos un "Golpe!!" a la computadora por el serial
		Serial.print("TOCANDO1,");
		Serial.println(lecturaSensor);
	}
	if (lecturaSensor1 >= umbral){
		Serial.print("TOCANDO2,");
		Serial.println(lecturaSensor1);
	}
	if (lecturaSensor2 >= umbral){
		Serial.print("TOCANDO3,");
		Serial.println(lecturaSensor2);
	}
	if (lecturaSensor3 >= umbral){
		Serial.print("TOCANDO4,");
		Serial.println(lecutasensor3);
	}
	if (lecturaSensor4 >= umbral){
		Serial.print("TOCANDO5,");
		Serial.println(lecturaSensor4);
	}
	if (lecturaSensor5 >= umbral){
		Serial.print("TOCANDO6,");
		Serial.println(lecturaSensor5);
	}
}
