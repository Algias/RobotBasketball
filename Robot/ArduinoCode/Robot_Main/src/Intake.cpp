#include "Intake.h"

// Constructor
Intake::Intake(Adafruit_PWMServoDriver &pwm, byte intakeServoPin, byte intakeServoPin2,
               byte intakeFeedbackPin)
    : _pwm(pwm), intakeServo(pwm, intakeServoPin),
      intakeServo2(pwm, intakeServoPin2),
      limitSwitch(intakeFeedbackPin)
{

  intakeServo.setMinJointVelocity(180);
  intakeServo.setMaxJointVelocity(0);
  intakeServo.setMinMaxCenterDeadband(200, 450, 325, 0);
  intakeServo.setCenterJoint(90);
  intakeServo2.setMinJointVelocity(0);
  intakeServo2.setMaxJointVelocity(180);
  intakeServo2.setMinMaxCenterDeadband(190, 430, 290, 0);
  intakeServo2.setCenterJoint(90);
}

Intake::~Intake() {}

void Intake::readInputs()
{
  limitSwitch.readInput();
}

void Intake::writeOutputs()
{
  intakeServo.writeOutput();
  intakeServo2.writeOutput();
}

void Intake::process()
{
}

void Intake::setPosition(int position)
{
  position = map(position, 0, 100, 0, 180);
  intakeServo.setCommandValue(position);
  intakeServo2.setCommandValue(position);
}