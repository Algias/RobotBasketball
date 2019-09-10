#ifndef Intake_h
#define Intake_h

#include "Actuator.h"
#include "Sensor.h"

class Intake {
    public:
        Intake(int IntakeServoPin, int IntakeFeedbackPin);
        ~Intake();

        Actuator intakeServo;
        Sensor limitSwitch;
    private:

};

#endif