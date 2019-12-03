
#include "src/Drive.h"
#include "src/Intake.h"
#include "src/Launcher.h"
#include "src/PinDeclarations.h"
#include "src/Constants.h"
#include "src/Communication.h"
#include "src/Master.h"

// #define LOCAL
#define EXTERNAL_INPUT

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

// Construct the drive with the channels for the 4 wheels and pins for 4
// feedback
Drive _drive(pwm, FRONT_LEFT_WHEEL_EXPANSION_CHANNEL,
             FRONT_RIGHT_WHEEL_EXPANSION_CHANNEL,
             BACK_LEFT_WHEEL_EXPANSION_CHANNEL,
             BACK_RIGHT_WHEEL_EXPANSION_CHANNEL, FRONT_LEFT_WHEEL_FEEDBACK_PIN,
             FRONT_RIGHT_WHEEL_FEEDBACK_PIN, BACK_LEFT_WHEEL_FEEDBACK_PIN,
             BACK_RIGHT_WHEEL_FEEDBACK_PIN);
// Construct the launcher with channels for quadrature encoder input and i2c
// channel
Launcher _launcher(pwm, FLYWHEEL_EXPANSION_CHANNEL_A, FLYWHEEL_EXPANSION_CHANNEL_B, FLYWHEEL_FEEDBACK_CHANNEL_A,
                   FLYWHEEL_FEEDBACK_CHANNEL_B);
// Construct the intake with servo i2c channel and limit switch feedback
Intake _intake(pwm, INTAKE_SERVO_EXPANSION_CHANNEL, INTAKE_SERVO2_EXPANSION_CHANNEL, INTAKE_LIMIT_SWITCH_PIN);

Communication _comms(BLUETOOTH_TX, BLUETOOTH_RX);

Master _master;

void setup()
{
  //Set the servo enable pin as an output
  pinMode(SERVO_ENABLE_PIN, OUTPUT);
  //Set the debug pin as an output
  pinMode(DEBUG_PIN, OUTPUT);
  //Set the PWM generator logic enable as an output
  pinMode(SERVO_LOGIC_ENABLE, OUTPUT);
  //Pull the PWM generator logic output low
  digitalWrite(SERVO_LOGIC_ENABLE, LOW);
  //Set up the PWM generator
  pwm.begin();
  pwm.setPWMFreq(PWM_GENERATOR_FREQUENCY);
  //Wait for stabilization
  delay(100);
#ifdef EXTERNAL_INPUT
  _comms.initializeComms();
#endif
#ifdef LOCAL
  Serial.begin(9600);
#endif
  //Enable the power to the servos
  digitalWrite(SERVO_ENABLE_PIN, HIGH);
  _intake.setPosition(90);
  _drive.move(0, 0, 0);
  _launcher.setRPM(0);
}

#ifdef LOCAL
int driveSpeed = 0;
int launcherSpeed = 0;
#endif

unsigned int i = 0;
void loop()
{
  // Read Inputs
  _drive.readInputs();
  _launcher.readInputs();
  _intake.readInputs();
#ifdef EXTERNAL_INPUT
  _comms.readComms();
#endif

  // Process
#ifdef EXTERNAL_INPUT
  _comms.parseComms();
  if (_comms.checkTimeout())
  {
    //If theres a timeout, disable servo power and set commands to default states
    //TODO: implement stops before disabling power
    digitalWrite(SERVO_ENABLE_PIN, LOW);
    _drive.move(0, 0, 0);
    _launcher.setRPM(0);
    _intake.setPosition(0);
  }
  else
  {
    //If there is no timeout, make sure the power is enabled and set commands
    digitalWrite(SERVO_ENABLE_PIN, HIGH);
    //Set the drive function to take Vx,Vy, and W from the comms
    _drive.move(_comms.getDriveVx(), _comms.getDriveVy(), _comms.getDriveW());
    //Set the command for the Launcher RPM
    _launcher.setRPM(_comms.getLauncher());
    //Set command from comms to intake
    _intake.setPosition(_comms.getIntake());
  }
#endif
  //Process subsystem controllers
  _drive.process();
  _launcher.process();
  _intake.process();
//Local Serial processing for wired control
#ifdef LOCAL
  //Serial Input Commands
  char incomingByte = Serial.read();
  if (i++ % 5 == 0)
  {
    Serial.print("Front Left: ");
    Serial.print(_drive.frontLeftWheelCmd);
    Serial.print(",");
    Serial.print(_drive.frontLeftWheeloutput);
    Serial.print(",");
    Serial.println(_drive.frontLeftWheelFeedback.getMapped());
    Serial.print("Front Right: ");
    Serial.print(_drive.frontRightWheelCmd);
    Serial.print(",");
    Serial.print(_drive.frontRightWheeloutput);
    Serial.print(",");
    Serial.println(_drive.frontRightWheelFeedback.getMapped());
    Serial.print("Back Left: ");
    Serial.print(_drive.backLeftWheelCmd);
    Serial.print(",");
    Serial.print(_drive.backLeftWheeloutput);
    Serial.print(",");
    Serial.println(_drive.backLeftWheelFeedback.getMapped());
    Serial.print("Back Right: ");
    Serial.print(_drive.backRightWheelCmd);
    Serial.print(",");
    Serial.print(_drive.backRightWheeloutput);
    Serial.print(",");
    Serial.println(_drive.backRightWheelFeedback.getMapped());

    // Serial.print(launcherSpeed);
    // Serial.print(" ");
    Serial.print(_launcher.flywheel.getCommandValue());
    Serial.print(" ");
    Serial.println(_launcher.encoder.getMapped());
  }
  switch (incomingByte)
  {
  //Forward
  case 'w':
    _drive.move(0, driveSpeed, 0);
    break;
  //Back
  case 's':
    _drive.move(0, -driveSpeed, 0);
    break;
  //Strafe Left
  case 'a':
    _drive.move(-driveSpeed, 0, 0);
    break;
  //Strafe Right
  case 'd':
    _drive.move(driveSpeed, 0, 0);
    break;
  //Increment Speed
  case ']':
    driveSpeed = constrain(driveSpeed + 10, 0, 100);
    break;
  //Decrement Speed
  case '[':
    driveSpeed = constrain(driveSpeed - 10, 0, 100);
    break;
  //Increase launcher speed
  case '.':
    launcherSpeed = constrain(launcherSpeed + 5, 0, 100);
    break;
  //Decrement launcher Speed
  case ',':
    launcherSpeed = constrain(launcherSpeed - 5, 0, 100);
    break;
  //Stop all
  case ' ':
    _drive.move(0, 0, 0);
    _launcher.setRPM(0);

    break;
  //Rotate Left
  case 'q':
    _drive.move(0, 0, driveSpeed);
    break;
  //Rotate Right
  case 'e':
    _drive.move(0, 0, -driveSpeed);
    break;
  case 'l':
    _launcher.setRPM(launcherSpeed);
    break;
  case 'i':
    _intake.setPosition(0);
    break;
  case 'm':
    _intake.setPosition(50);
    break;
  case 'k':
    _intake.setPosition(100);
    break;
  }
#endif

  _drive.writeOutputs();
  _launcher.writeOutputs();
  _intake.writeOutputs();
#ifdef EXTERNAL_INPUT
  _comms.writeComms();
  //Launcher Debug strings
  String myTestString;
  myTestString += String(map(_comms.getLauncher(), 0, 100, 0, _launcher.flywheel.getMaxJointVelocity()));
  myTestString += ",";
  myTestString += String(_launcher.encoder.getMapped());
  myTestString += ",";
  myTestString += String(_launcher.flywheel.getCommandValue());
  Serial.println(myTestString);

#endif
  //Clock cycler to verify loop timing (~ 20ms)
  digitalWrite(DEBUG_PIN, !digitalRead(DEBUG_PIN));
}
