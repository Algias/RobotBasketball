#ifndef Actuator_h
#define Actuator_h

class Actuator
{
    public:
        enum OutputType {Digital, Analog, PWM, I2CExpansion};
        Actuator(OutputType outputType, int pin);
        ~Actuator();

        bool OutputEnable = false;

        void setCommandSpeed(int speed);
        void getCommandSpeed();
        int getActualSpeed();
    private:
        int _pin;
        int _currentVelocity;
        int _currentPosition;
        int _maxVelocity;
        int _minVelocity;
        bool _error;
};
#endif