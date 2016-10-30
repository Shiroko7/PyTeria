int capSensePin = 2;
int capSensePin2= 3;
int capSensePin3= 4;
int capSensePin4= 5;
int capSensePin5= 6;
int capSensePin6= 7;
int capSensePin7= 8;



int touchedCutoff = 60;

void setup(){
Serial.begin(9600);
}

void loop(){

if (readCapacitivePin(capSensePin) > touchedCutoff) {
Serial.print("TOCANDO1 \n");
}
if ( (millis() % 500) == 0){
}

///////////////////////
if (readCapacitivePin(capSensePin2) > touchedCutoff) {
Serial.print("TOCANDO2 \n");
}
if ( (millis() % 500) == 0){
}

if (readCapacitivePin(capSensePin3) > touchedCutoff){
  Serial.print("TOCANDO3 \n");
}
if ( (millis() % 500) == 0){
}

if (readCapacitivePin(capSensePin4) > touchedCutoff){
  Serial.print("TOCANDO4 \n");
}
if ( (millis() % 500) == 0){
}

if (readCapacitivePin(capSensePin5) > touchedCutoff){
  Serial.print("TOCANDO5 \n");
}
if ( (millis() % 500) == 0){
}

if (readCapacitivePin(capSensePin6) > touchedCutoff){
  Serial.print("TOCANDO6 \n");
}
if ( (millis() % 500) == 0){
}

if (readCapacitivePin(capSensePin7) > touchedCutoff){
  Serial.print("TOCANDO7 \n");
}

// Every 500 ms, print the value of the capacitive sensor
if ( (millis() % 500) == 0){
}
}


uint8_t readCapacitivePin(int pinToMeasure){

volatile uint8_t* port;
volatile uint8_t* ddr;
volatile uint8_t* pin;

byte bitmask;
if ((pinToMeasure >= 0) && (pinToMeasure <= 7)){
port = &PORTD;
ddr = &DDRD;
bitmask = 1 << pinToMeasure;
pin = &PIND;
}
if ((pinToMeasure > 7) && (pinToMeasure <= 13)){
port = &PORTB;
ddr = &DDRB;
bitmask = 1 << (pinToMeasure - 8);
pin = &PINB;
}
if ((pinToMeasure > 13) && (pinToMeasure <= 19)){
port = &PORTC;
ddr = &DDRC;
bitmask = 1 << (pinToMeasure - 13);
pin = &PINC;
}

*port &= ~(bitmask);
*ddr  |= bitmask;
delay(0);

*ddr &= ~(bitmask);

int cycles = 16000;
for(int i = 0; i < cycles; i++){
if (*pin & bitmask){
cycles = i;
break;
}
}

*port &= ~(bitmask);
*ddr  |= bitmask;

return cycles;
}
