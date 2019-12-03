#ifndef Launcher_h
#define Launcher_h
#include "Actuator.h"
#include "Sensor.h"
#include "FastPID.h"
#include "Constants.h"
class Launcher
{
public:
  Launcher(Adafruit_PWMServoDriver &pwm, byte flywheelDrivePinA, byte flywheelDrivePinB,
           byte flywheelEncoderA, byte flywheelEncoderB);
  ~Launcher();
  I2CActuator flywheel;
  PCIInput encoder;
  FastPID flywheelPID;

  void setRPM(int RPM);
  void readInputs();
  void writeOutputs();
  void process();

private:
  Adafruit_PWMServoDriver _pwm;
  const float flywheelPIDConstants[4] = {6.0, 0.5, 1.0, 20};
  int commandRPM = 0;
  int _rampRPM = 0;
};

#endif