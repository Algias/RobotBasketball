#include "Actuator.h"

int Actuator::getCommandValue() { return _cmdValue; }

int Actuator::getMaxJointVelocity() { return _maxJointVelocity; }
void Actuator::setMaxJointVelocity(int maxVelocityValue) { _maxJointVelocity = maxVelocityValue; }

int Actuator::getMinJointVelocity() { return _minJointVelocity; }
void Actuator::setMinJointVelocity(int minVelocityValue) { _minJointVelocity = minVelocityValue; }
void Actuator::setCenterJoint(int center)
{
  _centerJoint = center;
}
//I2C Actuator Constructor
I2CActuator::I2CActuator(Adafruit_PWMServoDriver &pwm, byte channel)
    : _pwm(pwm)
{
  _channel = channel;
}

I2CActuator::I2CActuator(Adafruit_PWMServoDriver &pwm, byte channel, byte channel_extra) : _pwm(pwm)
{
  _channel = channel;
  _channel_extra = channel_extra;
}

//I2C actuator command value setter
void I2CActuator::setCommandValue(int cmd)
{
  _cmdValue = cmd;
  //Command is less than the center (IE -40 < 0), map from min to center
  if (_cmdValue < _centerJoint)
  {
    _cmdOutput = map(_cmdValue, _minJointVelocity, _centerJoint, _minOutput, _centerOutput - _centerDeadband);
  }
  //Command is greater than center (40 > 0), map from center to max
  else if (_cmdValue > _centerJoint)
  {
    _cmdOutput = map(_cmdValue, _centerJoint, _maxJointVelocity, _centerOutput + _centerDeadband, _maxOutput);
  }
  //If we are commanding center, go to center
  else
  {
    _cmdOutput = _centerOutput;
  }
}
//I2C actuator output implementation
void I2CActuator::writeOutput()
{
  _pwm.setPin(_channel, _cmdOutput);
  if (_channel_extra >= 0)
  {
    _pwm.setPin(_channel_extra, 0);
  }
}

void I2CActuator::setMinMaxCenterDeadband(int min, int max, int Center, int Deadband)
{
  _maxOutput = max;
  _minOutput = min;
  _centerDeadband = Deadband;
  _centerOutput = Center;
}

//PWM-based actuator constructor
PWMActuator::PWMActuator(byte pin)
{
  _pin = pin;
  pinMode(pin, OUTPUT);
}

void PWMActuator::setCommandValue(int cmd)
{
  _cmdValue = cmd;

  _cmdOutput =
      map(cmd, _minJointVelocity, _maxJointVelocity, _minOutput, _maxOutput);
}

void PWMActuator::writeOutput() { analogWrite(_pin, _cmdOutput); }
//Digital actuator constructor
DigitalActuator ::DigitalActuator(byte pin)
{
  _pin = pin;
  pinMode(pin, OUTPUT);
}

void DigitalActuator ::setCommandValue(int cmd)
{
  if (cmd == 0)
  {
    _cmdValue = HIGH;
    _cmdOutput = HIGH;
  }
  else
  {
    _cmdValue = LOW;
    _cmdOutput = HIGH;
  }
}
void DigitalActuator::writeOutput()
{
  digitalWrite(_pin, _cmdOutput);
}