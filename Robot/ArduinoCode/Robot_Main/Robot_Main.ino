#include "src/Drive.h"
#include "src/Launcher.h"
#include "src/Intake.h"
#include "src/PinDeclarations.h"

Drive _drive(FRONT_LEFT_WHEEL_EXPANSION_CHANNEL, 
              FRONT_RIGHT_WHEEL_EXPANSION_CHANNEL,
              BACK_LEFT_WHEEL_EXPANSION_CHANNEL,
              BACK_RIGHT_WHEEL_EXPANSION_CHANNEL,
              FRONT_LEFT_WHEEL_FEEDBACK_PIN,
              FRONT_RIGHT_WHEEL_FEEDBACK_PIN,
              BACK_LEFT_WHEEL_FEEDBACK_PIN,
              BACK_RIGHT_WHEEL_FEEDBACK_PIN);

Launcher _launcher(FLYWHEEL_EXPANSION_CHANNEL,
                    FLYWHEEL_FEEDBACK_CHANNEL_A,
                    FLYWHEEL_FEEDBACK_CHANNEL_B);

Intake _intake(INTAKE_SERVO_EXPANSION_CHANNEL,
                INTAKE_LIMIT_SWITCH_PIN);

void setup() {
  // put your setup code here, to run once:

}

void loop() {
  // put your main code here, to run repeatedly:

}


/// High level logic:

//Communication
// Bluetooth parsing & listener 
//Drive control functions
// 4 PWM control + 4 feedback lines
//Intake/Launcher Control Functions
// 1 PWM control, 2 DIO Lines (Could be hardwired) + 2 Feedback lines