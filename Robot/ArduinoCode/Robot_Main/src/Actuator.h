#ifndef Actuator_h
#define Actuator_h

#include "Adafruit_PWMServoDriver.h"

// Base actuator class, abstract & cannot be instantiated
class Actuator
{
public:
  bool OutputEnable = false;

  virtual void setCommandValue(int cmd) = 0;
  virtual void writeOutput() = 0;
  int getCommandValue();
  int getMaxJointVelocity();
  void setMaxJointVelocity(int MaxJointVelocity);
  int getMinJointVelocity();
  void setMinJointVelocity(int MinJointVelocity);
  void setCenterJoint(int);
  bool invert = false;

protected:
  int _cmdValue;
  int _currentPosition;
  int _maxJointVelocity = 100;
  int _minJointVelocity = -100;
  int _centerJoint = 0;
  bool _error;
};

// Implementation for Abstract Actuator based on PCA9685 I2C communications
class I2CActuator : public Actuator
{
public:
  I2CActuator(Adafruit_PWMServoDriver &pwm, byte channel);
  I2CActuator(Adafruit_PWMServoDriver &pwm, byte channel, byte channel_extra);

  void setCommandValue(int cmd);
  void writeOutput();
  void setMinMaxCenterDeadband(int, int, int, int);

private:
  Adafruit_PWMServoDriver _pwm;
  int _channel;
  int _channel_extra = -1;
  int _maxOutput = 370;
  int _minOutput = 260;
  int _centerOutput = 400;
  int _centerDeadband = 30;
  uint16_t _cmdOutput;
};

// Implementation for Abstract Actuator based on PWM outputs
class PWMActuator : public Actuator
{
public:
  PWMActuator(byte pin);

  void setCommandValue(int cmd);
  void writeOutput();

private:
  unsigned int _pin;
  int _maxOutput = 255;
  int _minOutput = 0;
  int _cmdOutput;
};

// Implementation for abstract actuaator based on a boolean Digital output
class DigitalActuator : public Actuator
{
public:
  DigitalActuator(byte pin);
  void writeOutput();
  void setCommandValue(int cmd);

private:
  byte _pin;
  int _maxOutput = 1;
  int _minOutput = 0;
  int _cmdOutput;
};

#endif