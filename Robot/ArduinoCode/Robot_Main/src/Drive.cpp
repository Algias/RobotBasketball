#include "Drive.h"

// Constructor
Drive::Drive(Adafruit_PWMServoDriver &pwm, byte frontLeftWheelPin,
             byte frontRightWheelPin, byte backLeftWheelPin,
             byte backRightWheelPin, byte frontLeftWheelFeedbackPin,
             byte frontRightWheelFeedbackPin, byte backLeftWheelFeedbackPin,
             byte backRightWheelFeedbackPin)
    : _pwm(pwm), frontLeftWheel(pwm, frontLeftWheelPin),
      frontLeftWheelFeedback(frontLeftWheelFeedbackPin),
      frontRightWheel(pwm, frontRightWheelPin),
      frontRightWheelFeedback(frontRightWheelFeedbackPin),
      backLeftWheel(pwm, backLeftWheelPin),
      backLeftWheelFeedback(backLeftWheelFeedbackPin),
      backRightWheel(pwm, backRightWheelPin),
      backRightWheelFeedback(backRightWheelFeedbackPin),
      frontLeftWheelPID(frontLeftWheelPIDValues[0], frontLeftWheelPIDValues[1], frontLeftWheelPIDValues[2], frontLeftWheelPIDValues[3]),
      frontRightWheelPID(frontRightWheelPIDValues[0], frontRightWheelPIDValues[1], frontRightWheelPIDValues[2], frontRightWheelPIDValues[3], 16, true),
      backLeftWheelPID(backLeftWheelPIDValues[0], backLeftWheelPIDValues[1], backLeftWheelPIDValues[2], backLeftWheelPIDValues[3]),
      backRightWheelPID(backRightWheelPIDValues[0], backRightWheelPIDValues[1], backRightWheelPIDValues[2], backRightWheelPIDValues[3])
{

  // Set 0 commands for all
  frontLeftWheel.setCommandValue(0);
  frontRightWheel.setCommandValue(0);
  backLeftWheel.setCommandValue(0);
  backRightWheel.setCommandValue(0);

  frontLeftWheelFeedback.mode = Sensor::SensorMode::velocity;
  frontLeftWheelFeedback.setMappedScale(DRIVE_FRONT_LEFT_SENSOR_SCALE);
  frontLeftWheel.setMinJointVelocity(DRIVE_MIN_RPM);
  frontLeftWheel.setMaxJointVelocity(DRIVE_MAX_RPM);
  frontLeftWheel.setMinMaxCenterDeadband(DRIVE_MIN_OUTPUT, DRIVE_MAX_OUTPUT, DRIVE_ZERO_CENTER, DRIVE_ZERO_DEADBAND_RANGE);
  frontLeftWheelPID.setOutputRange(DRIVE_MIN_RPM, DRIVE_MAX_RPM);
  frontLeftWheelPID.setCoefficients(frontLeftWheelPIDValues[0], frontLeftWheelPIDValues[1], frontLeftWheelPIDValues[2], frontLeftWheelPIDValues[3]);

  frontRightWheelFeedback.mode = Sensor::SensorMode::velocity;
  frontRightWheelFeedback.setMappedScale(DRIVE_FRONT_RIGHT_SENSOR_SCALE);
  frontRightWheel.setMinJointVelocity(DRIVE_MIN_RPM);
  frontRightWheel.setMaxJointVelocity(DRIVE_MAX_RPM);
  frontRightWheel.setMinMaxCenterDeadband(DRIVE_MIN_OUTPUT, DRIVE_MAX_OUTPUT, DRIVE_ZERO_CENTER, DRIVE_ZERO_DEADBAND_RANGE);
  frontRightWheelPID.setOutputRange(DRIVE_MIN_RPM, DRIVE_MAX_RPM);
  frontRightWheelPID.setCoefficients(frontRightWheelPIDValues[0], frontRightWheelPIDValues[1], frontRightWheelPIDValues[2], frontRightWheelPIDValues[3]);
  frontRightWheelPID.setOutputConfig(16, true);

  frontRightWheelFeedback.invert = false;

  backRightWheelFeedback.mode = Sensor::SensorMode::velocity;
  backRightWheelFeedback.setMappedScale(DRIVE_BACK_RIGHT_SENSOR_SCALE);
  backRightWheel.setMinJointVelocity(DRIVE_MIN_RPM);
  backRightWheel.setMaxJointVelocity(DRIVE_MAX_RPM);
  backRightWheel.setMinMaxCenterDeadband(DRIVE_MIN_OUTPUT, DRIVE_MAX_OUTPUT, DRIVE_ZERO_CENTER, DRIVE_ZERO_DEADBAND_RANGE);
  backRightWheelPID.setOutputRange(DRIVE_MIN_RPM, DRIVE_MAX_RPM);
  backRightWheelPID.setCoefficients(backRightWheelPIDValues[0], backRightWheelPIDValues[1], backRightWheelPIDValues[2], backRightWheelPIDValues[3]);

  backLeftWheelFeedback.mode = Sensor::SensorMode::velocity;
  backLeftWheelFeedback.setMappedScale(DRIVE_BACK_LEFT_SENSOR_SCALE);
  backLeftWheel.setMinJointVelocity(DRIVE_MIN_RPM);
  backLeftWheel.setMaxJointVelocity(DRIVE_MAX_RPM);
  backLeftWheel.setMinMaxCenterDeadband(DRIVE_MIN_OUTPUT, DRIVE_MAX_OUTPUT, DRIVE_ZERO_CENTER, DRIVE_ZERO_DEADBAND_RANGE);
  backLeftWheelPID.setOutputRange(DRIVE_MIN_RPM, DRIVE_MAX_RPM);
  backLeftWheelPID.setCoefficients(backLeftWheelPIDValues[0], backLeftWheelPIDValues[1], backLeftWheelPIDValues[2], backLeftWheelPIDValues[3]);
}
void Drive::move(int vtx, int vty, int w)
{

  vtx = constrain(vtx, -100, 100);
  vty = constrain(vty, -100, 100);
  w = constrain(w * .225, -100, 100);

  //r1 = (.707*L, .707*L) front right
  //r2 = (-.707L, .707L) front left
  //r3 = (-.707L, -.707L) back left
  //r4 = (.707L, -.707L) back right

  //v = vtranslational + w x r, vx = vtx - w . ry, vy = vty + w . rx
  // vw = vparallel = v.u = -.707 vx + .707 vy

  float vx1 = vtx - w * DRIVE_VECTOR_SCALE * DRIVE_SIZE; // front right
  float vy1 = vty + w * DRIVE_VECTOR_SCALE * DRIVE_SIZE;

  float vx2 = vtx - w * DRIVE_VECTOR_SCALE * DRIVE_SIZE; // front left
  float vy2 = vty + w * -DRIVE_VECTOR_SCALE * DRIVE_SIZE;

  float vx3 = vtx - w * -DRIVE_VECTOR_SCALE * DRIVE_SIZE; // back left
  float vy3 = vty + w * -DRIVE_VECTOR_SCALE * DRIVE_SIZE;

  float vx4 = vtx - w * -DRIVE_VECTOR_SCALE * DRIVE_SIZE; // back right
  float vy4 = vty + w * DRIVE_VECTOR_SCALE * DRIVE_SIZE;

  frontRightWheelCmd = DRIVE_VECTOR_SCALE * vx1 - DRIVE_VECTOR_SCALE * vy1;
  frontRightWheelCmd = map(frontRightWheelCmd, -71, 71, DRIVE_MIN_RPM, DRIVE_MAX_RPM);
  frontLeftWheelCmd = DRIVE_VECTOR_SCALE * vx2 + DRIVE_VECTOR_SCALE * vy2;
  frontLeftWheelCmd = map(frontLeftWheelCmd, -71, 71, DRIVE_MIN_RPM, DRIVE_MAX_RPM);
  backLeftWheelCmd = -DRIVE_VECTOR_SCALE * vx3 + DRIVE_VECTOR_SCALE * vy3;
  backLeftWheelCmd = map(backLeftWheelCmd, -71, 71, DRIVE_MIN_RPM, DRIVE_MAX_RPM);
  backRightWheelCmd = -DRIVE_VECTOR_SCALE * vx4 - DRIVE_VECTOR_SCALE * vy4;
  backRightWheelCmd = map(backRightWheelCmd, -71, 71, DRIVE_MIN_RPM, DRIVE_MAX_RPM);
}

void Drive::readInputs()
{
  frontLeftWheelFeedback.readInput();
  frontRightWheelFeedback.readInput();
  backLeftWheelFeedback.readInput();
  backRightWheelFeedback.readInput();
}

void Drive::process()
{
  frontLeftWheelFeedback.mapValue();
  frontRightWheelFeedback.mapValue();
  backLeftWheelFeedback.mapValue();
  backRightWheelFeedback.mapValue();

  if (_stabalizedDriveCounter < 100)
  {
    frontLeftWheel.setCommandValue(0);
    frontRightWheel.setCommandValue(0);
    backLeftWheel.setCommandValue(0);
    backRightWheel.setCommandValue(0);
    _stabalizedDriveCounter++;
    return;
  }
  if (!ManualMode)
  {
    const int tolerance = 2;
    frontLeftWheeloutput = frontLeftWheelPID.step(frontLeftWheelCmd, frontLeftWheelFeedback.getMapped());
    // if (abs(frontLeftWheeloutput) > tolerance)
    frontLeftWheeloutput += frontLeftWheelCmd;
    frontRightWheeloutput = frontRightWheelPID.step(frontRightWheelCmd, frontRightWheelFeedback.getMapped());
    // if (abs(frontRightWheeloutput) > tolerance)
    frontRightWheeloutput += frontRightWheelCmd;
    backLeftWheeloutput = backLeftWheelPID.step(backLeftWheelCmd, backLeftWheelFeedback.getMapped());
    // if (abs(backLeftWheeloutput) > tolerance)
    backLeftWheeloutput += backLeftWheelCmd;
    backRightWheeloutput = backRightWheelPID.step(backRightWheelCmd, backRightWheelFeedback.getMapped());
    // if (abs(backRightWheeloutput) > tolerance)
    backRightWheeloutput += backRightWheelCmd;
    if (abs(frontLeftWheeloutput) > tolerance || frontLeftWheeloutput == 0)
      frontLeftWheel.setCommandValue(frontLeftWheeloutput);
    if (abs(frontRightWheeloutput) > tolerance || frontRightWheeloutput == 0)
      frontRightWheel.setCommandValue(frontRightWheeloutput);
    if (abs(backLeftWheeloutput) > tolerance || backLeftWheeloutput == 0)
      backLeftWheel.setCommandValue(backLeftWheeloutput);
    if (abs(backRightWheeloutput) > tolerance || backRightWheeloutput == 0)
      backRightWheel.setCommandValue(backRightWheeloutput);
  }
  else
  {
    frontRightWheeloutput = frontRightWheelCmd;
    frontLeftWheeloutput = frontLeftWheelCmd;
    backRightWheeloutput = backRightWheelCmd;
    backLeftWheeloutput = backLeftWheelCmd;
    frontLeftWheel.setCommandValue(frontLeftWheelCmd);
    frontRightWheel.setCommandValue(frontRightWheelCmd);
    backLeftWheel.setCommandValue(backLeftWheelCmd);
    backRightWheel.setCommandValue(backRightWheelCmd);
  }
}

void Drive::writeOutputs()
{
  frontLeftWheel.writeOutput();
  frontRightWheel.writeOutput();
  backLeftWheel.writeOutput();
  backRightWheel.writeOutput();
}

Drive::~Drive() {}