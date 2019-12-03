#ifndef Intake_h
#define Intake_h

#include "Actuator.h"
#include "Sensor.h"
#include "Constants.h"
class Intake
{
public:
  Intake(Adafruit_PWMServoDriver &pwm, byte IntakeServoPin, byte IntakeServoPin2,
         byte IntakeFeedbackPin);
  ~Intake();

  I2CActuator intakeServo;
  I2CActuator intakeServo2;
  DigitalInput limitSwitch;
  void readInputs();
  void writeOutputs();
  void process();

  void setPosition(int position);

private:
  Adafruit_PWMServoDriver &_pwm;
};

#endif