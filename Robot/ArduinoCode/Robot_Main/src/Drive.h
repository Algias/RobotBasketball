#ifndef Drive_h
#define Drive_h
#include "Actuator.h"
#include "Sensor.h"
#include "FastPID.h"
#include "Constants.h"

class Drive
{
public:
  Drive(Adafruit_PWMServoDriver &pwm, byte frontLeftWheelPin,
        byte frontRightWheelPin, byte backLeftWheelPin, byte backRightWheelPin,
        byte frontLeftWheelFeedbackPin, byte frontRightWheelFeedbackPin,
        byte backLeftWheelFeedbackPin, byte backRightWheelFeedbackPin);
  ~Drive();

  I2CActuator frontLeftWheel;
  PWMInput frontLeftWheelFeedback;
  FastPID frontLeftWheelPID;

  I2CActuator frontRightWheel;
  PWMInput frontRightWheelFeedback;
  FastPID frontRightWheelPID;

  I2CActuator backLeftWheel;
  PWMInput backLeftWheelFeedback;
  FastPID backLeftWheelPID;

  I2CActuator backRightWheel;
  PWMInput backRightWheelFeedback;
  FastPID backRightWheelPID;

  bool ManualMode = false;

  void move(int vtx, int vty, int w);

  void readInputs();

  void writeOutputs();

  void process();

  bool controllerEnabled = false;

  int frontLeftWheeloutput;
  int frontRightWheeloutput;
  int backLeftWheeloutput;
  int backRightWheeloutput;

  int frontRightWheelCmd;
  int frontLeftWheelCmd;
  int backLeftWheelCmd;
  int backRightWheelCmd;

private:
  Adafruit_PWMServoDriver _pwm;
  const float frontLeftWheelPIDValues[4] = {1.0, 0.0, 0.0, 20};
  const float frontRightWheelPIDValues[4] = {1.0, 0.0, 0.0, 20};
  const float backLeftWheelPIDValues[4] = {1.0, 0.0, 0.0, 20};
  const float backRightWheelPIDValues[4] = {1.0, 0.0, 0.0, 20};
  unsigned int _stabalizedDriveCounter = 0;
};

#endif