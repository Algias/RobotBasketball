#ifndef Sensor_h
#define Sensor_h

class Sensor {
    public:
    enum InputType {Digital, Analog, PWM, I2CExpansion, Quadrature};
        Sensor(InputType inputType, int pin);
        Sensor(InputType inputType, int pinA, int pinB);
        ~Sensor();
    private:
        int _pin;
        float _currentValueRaw;
        float _currentValueMapped;
        bool _error;

};

#endif