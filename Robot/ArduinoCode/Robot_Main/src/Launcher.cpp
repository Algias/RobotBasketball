#include "Launcher.h"

//Constructor
Launcher::Launcher(int flywheelDrivePin, int flywheelEncoderPinA, int flywheelEncoderPinB): 
    flywheel(Actuator::OutputType::I2CExpansion, flywheelDrivePin),
    encoder(Sensor::InputType::Quadrature, flywheelEncoderPinA, flywheelEncoderPinB)
{
    
}

Launcher::~Launcher(){}