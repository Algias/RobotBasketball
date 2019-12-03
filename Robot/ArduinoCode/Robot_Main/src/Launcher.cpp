#include "Launcher.h"

// Constructor
Launcher::Launcher(Adafruit_PWMServoDriver &pwm, byte flywheelDrivePinA, byte flywheelDrivePinB,
                   byte flywheelEncoderPinA, byte flywheelEncoderPinB)
    : _pwm(pwm), flywheel(pwm, flywheelDrivePinA, flywheelDrivePinB),
      encoder(flywheelEncoderPinA),
      flywheelPID(flywheelPIDConstants[0], flywheelPIDConstants[1], flywheelPIDConstants[2], flywheelPIDConstants[3])
{
  encoder.mode = Sensor::SensorMode::velocity;
  encoder.setMappedScale(LAUNCHER_SENSOR_SCALE);
  encoder.longDelta = true;
  flywheelPID.setOutputRange(LAUNCHER_MIN_RPM, LAUNCHER_MAX_RPM);
  flywheel.setMinJointVelocity(LAUNCHER_MIN_RPM);
  flywheel.setMaxJointVelocity(LAUNCHER_MAX_RPM);
  flywheel.setCenterJoint(LAUNCHER_JOINT_CENTER);
  flywheel.setMinMaxCenterDeadband(LAUNCHER_MIN, LAUNCHER_MAX, LAUNCHER_CENTER, 0);
  flywheelPID.setCoefficients(flywheelPIDConstants[0], flywheelPIDConstants[1], flywheelPIDConstants[2], flywheelPIDConstants[3]);
}

void Launcher::readInputs() { encoder.readInput(); }

void Launcher::writeOutputs()
{

  flywheel.writeOutput();
}

void Launcher::process()
{
  encoder.mapValue();
  int mapped = encoder.getMapped();
  int macroError = commandRPM - mapped;
  int tempOutput = 0;
  //Linear ramp by 50 every loop cycle time, currently ignored
  if (macroError > 500)
  {
    _rampRPM = mapped + 300;
    tempOutput = _rampRPM;
  }
  else if (macroError > 150)
  {
    _rampRPM = mapped + 150;
    tempOutput = _rampRPM;
  }
  else
  {
    tempOutput = commandRPM;
  }

  //PID controller
  int output = flywheelPID.step(commandRPM, encoder.getMapped());
  //Feed forward
  // if (output != 0)
  //   output += 200;
  flywheel.setCommandValue(output);
}

void Launcher::setRPM(int RPM)
{
  //Map the RPM from 0 to 100 to the speed of the flywheel (0 to 3200ish)
  commandRPM = map(RPM, 0, 100, flywheel.getMinJointVelocity(), flywheel.getMaxJointVelocity());
}

Launcher::~Launcher() {}