#ifndef Drive_h
#define Drive_h
#include "Actuator.h"
#include "Sensor.h"
class Drive {
    public:
        Drive(int frontLeftWheelPin, 
                int frontRightWheelPin,
                int backLeftWheelPin,
                int backRightWheelPin,
                int frontLeftWheelFeedbackPin,
                int frontRightWheelFeedbackPin,
                int backLeftWheelFeedbackPin,
                int backRightWheelFeedbackPin);
        ~Drive();

        Actuator frontLeftWheel;
        Sensor frontLeftWheelFeedback;
        Actuator frontRightWheel;
        Sensor frontRightWheelFeedback;
        Actuator backLeftWheel;
        Sensor backLeftWheelFeedback;
        Actuator backRightWheel;
        Sensor backRightWheelFeedback;

        void move(float direction, float speed);

    private:

};

#endif