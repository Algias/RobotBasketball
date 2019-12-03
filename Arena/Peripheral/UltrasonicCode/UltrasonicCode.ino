
//#include <LiquidCrystal_I2C.h>/
#include <Wire.h>  // Comes with Arduino IDE
#define echoPin 7 // Echo Pin
#define trigPin 8 // Trigger Pin

long duration, distance; // Duration used to calculate distance
int sensorCounter = 0;   // counter for the number of button presses
int lastsensorDistance = 0;
int setCounter = 20;
int incomingByte;

long lastScoreTime = 0;

void setup() {
  Serial.begin (9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void loop() {

  /* The following trigPin/echoPin cycle is used to determine the
    distance of the nearest object by bouncing soundwaves off of it. */
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);

  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);

  //Calculate the distance (in cm) based on the speed of sound.
  distance = duration / 58.2;

  if (((distance - lastsensorDistance) > 100 || lastsensorDistance < 4) && (millis() - lastScoreTime) > 1000) {
    sensorCounter++;
    Serial.println("1");
    lastScoreTime = millis();
  }
  //    Serial.print("Distance: ");
  //Serial.print(sensorCounter);
  //Serial.print(",");
  //Serial.println(distance);
  delay(5);

  lastsensorDistance = distance;

}
