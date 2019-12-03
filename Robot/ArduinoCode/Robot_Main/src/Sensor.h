#ifndef Sensor_h
#define Sensor_h

#include <Arduino.h>
#include <Wire.h>
#include <Ewma.h>
#include <EwmaT.h>
//#include "QuadratureEncoder.h"
#include "PinChangeInterrupt.h"

// Base class for sensor information
class Sensor
{
public:
  enum SensorMode
  {
    position,
    velocity
  };
  Sensor();
  SensorMode mode = position;
  virtual void readInput() = 0;
  int getValue();
  int getRaw();
  int getMapped();
  void setMappedScale(int scale);
  void mapValue();
  bool invert = false;
  bool longDelta = false;

protected:
  bool _error;
  int _rawValue;
  int _mappedValue = 0;
  int _differentialValue;
  int _prevValue;
  int _prevRawValue;
  int _value;
  Ewma myFilter;

  int _diff;
  int _mapScale;
  volatile int angle;

  unsigned long _currentTime;
  unsigned long _prevTime;
  unsigned long _deltaT;
};

// Inputs that are boolean (High / Low)
class DigitalInput : public Sensor
{
public:
  DigitalInput(byte pin);
  void readInput();

private:
  int _pin;
};

// Inputs that are cyclic PWM with a defined duty cycle
class PWMInput : public Sensor
{
public:
  PWMInput(byte pin);
  void readInput();
  //  Ewma filter;

private:
  int _pin;

  int unitsFC = 360;       // Units in a full circle
  int dutyScale = 1000;    // Scale duty cycle to 1/1000ths
  int dcMin = 29;          // Minimum duty cycle
  int dcMax = 971;         // Maximum duty cycle
  int q2min = unitsFC / 4; // For checking if in 1st quadrant
  int q3max = q2min * 3;   // For checking if in 4th quadrant
  int turns = 0;           // For tracking turns
  // dc is duty cycle, theta is 0 to 359 angle, thetaP is theta from previous
  // loop repetition, tHigh and tLow are the high and low signal times for
  // duty cycle calculations.
  long dc, tHigh, tLow;
  int theta, thetaP;
};

// Inputs that are read from analog channels
class AnalogInput : public Sensor
{
public:
  AnalogInput(byte pin);
  void readInput();

private:
  int _pin;
};

// Inputs that are digital but non cyclic that requires ISR
class PCIInput : public Sensor
{
public:
  PCIInput(byte pin);
  void readInput();
  static int rawCounter;
private:
  int _pin;
  static void interruptResponse();
  
};



class QuadratureInput : public Sensor
{
public:
  QuadratureInput(byte channelA, byte channelB);

  void readInput();

private:
  byte _channelA;
  byte _channelB;
  //Encoders _encoder;
};

#endif