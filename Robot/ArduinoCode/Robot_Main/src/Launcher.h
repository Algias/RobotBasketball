#ifndef Launcher_h
#define Launcher_h
#include "Actuator.h"
#include "Sensor.h"
class Launcher {
    public:
        Launcher(int flywheelDrivePin, int flywheelEncoderA, int flywheelEncoderB);
        ~Launcher();
        Actuator flywheel;
        Sensor encoder;
    private:

};

#endif