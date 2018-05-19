#include <Wire.h>
#include <Servo.h>

Servo servo11;
Servo servo10;
Servo servo09;
Servo servo08;
Servo servo07;

const int IN_11 = 6;
const int IN_10 = 5;
const int IN_09 = 4;
const int IN_08 = 3;
const int IN_07 = 2;

#define SLAVE_ADDRESS 0x04
int number = 0;

void setup() {
  pinMode(13, OUTPUT);
  Serial.begin(9600); // start serial for output
  // initialize i2c as slave
  Wire.begin(SLAVE_ADDRESS);

  // define callbacks for i2c communication
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);

  Serial.begin(9600);
  servo11.attach(11);
  servo10.attach(10);
  servo09.attach(9);
  servo08.attach(8);
  servo07.attach(7);
}

// callback for received data
void receiveData(int byteCount) {

  while (Wire.available()) {
    number = Wire.read();
    digitalWrite(13, !digitalRead(13));
  }
}

// callback for sending data
void sendData() {
  Wire.write(number);
}

//int wingMicros = 1000;

void loop() {
  //delay(1000);
//  unsigned long sig = pulseIn(IN_11, HIGH);
//  sig = (sig == 0)? 1500 : sig;
//  servo11.writeMicroseconds(sig);
//  sig = pulseIn(IN_10, HIGH);
//  sig = (sig == 0)? 1500 : sig;
//  servo10.writeMicroseconds(sig);
//  sig = pulseIn(IN_09, HIGH);
//  sig = (sig == 0)? 1500 : sig;
//  servo09.writeMicroseconds(sig);
//  sig = pulseIn(IN_08, HIGH);
//  sig = (sig == 0)? 1500 : sig;
//  servo08.writeMicroseconds(sig);
  unsigned long sig = pulseIn(IN_07, HIGH);
  unsigned long sig2 = pulseIn(IN_07, LOW);
  sig = (sig == 0)? 1500 : sig;
  Serial.print(sig2);
  Serial.print(" ");
  Serial.println(sig);
  servo07.writeMicroseconds(sig);
//  wingMicros += 100;
//  if (wingMicros == 2000) wingMicros = 1000;
  
}


