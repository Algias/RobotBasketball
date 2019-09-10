#include "Drive.h"

//Constructor
Drive::Drive(int frontLeftWheelPin, 
                int frontRightWheelPin,
                int backLeftWheelPin,
                int backRightWheelPin,
                int frontLeftWheelFeedbackPin,
                int frontRightWheelFeedbackPin,
                int backLeftWheelFeedbackPin,
                int backRightWheelFeedbackPin) :
    frontLeftWheel(Actuator::OutputType::I2CExpansion, frontLeftWheelPin),
    frontLeftWheelFeedback(Sensor::InputType::PWM, frontLeftWheelFeedbackPin),
    frontRightWheel(Actuator::OutputType::I2CExpansion, frontRightWheelPin),
    frontRightWheelFeedback(Sensor::InputType::PWM,frontRightWheelFeedbackPin),
    backLeftWheel(Actuator::OutputType::I2CExpansion, backLeftWheelPin),
    backLeftWheelFeedback(Sensor::InputType::PWM,backLeftWheelFeedbackPin),
    backRightWheel(Actuator::OutputType::I2CExpansion, backRightWheelPin),
    backRightWheelFeedback(Sensor::InputType::PWM,backRightWheelFeedbackPin)
{
    //Set 0 commands for all
    frontLeftWheel.setCommandSpeed(0);
    frontRightWheel.setCommandSpeed(0);
    backLeftWheel.setCommandSpeed(0);
    backRightWheel.setCommandSpeed(0);
}
void Drive::move(float direction, float speed){
    //TODO Kinematics (Take direction & speed and parse into 4 wheel directions)
    
    
    //Set command outputs
    frontLeftWheel.setCommandSpeed(0);
    frontRightWheel.setCommandSpeed(0);
    backLeftWheel.setCommandSpeed(0);
    backRightWheel.setCommandSpeed(0);
}

Drive::~Drive(){}