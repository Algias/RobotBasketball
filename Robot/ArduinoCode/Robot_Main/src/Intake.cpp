#include "Intake.h"

//Constructor
Intake::Intake(int intakeServoPin, int intakeFeedbackPin):
    intakeServo(Actuator::OutputType::I2CExpansion,intakeServoPin),
    limitSwitch(Sensor::InputType::Digital, intakeFeedbackPin)
{
    
}

Intake::~Intake(){}