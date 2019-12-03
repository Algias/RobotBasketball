#ifndef Communication_h
#define Communication_h

#include <Arduino.h>
#include "Constants.h"
#include "PinDeclarations.h"
class Communication
{
public:
    Communication(byte Tx, byte Rx);
    ~Communication();

    void initializeComms();

    void readComms();

    void writeComms();

    void parseComms();

    void packComms();

    int getDriveVx();

    int getDriveVy();

    int getDriveW();

    int getLauncher();

    int getIntake();

    bool checkTimeout();

    //bool PacketTimedOut = false;

private:
    union Header {
        char str[4];
        byte bytes[4];
        long value;
    };
    union Cmd_State {
        byte rawData;
        signed char value;
    };
    union intData {
        byte rawData;
        signed char value;
    };
    Header _header;
    Cmd_State _state;
    intData _driveVx;
    intData _driveVy;
    intData _driveW;
    intData _launcherV;
    intData _intakeP;
    intData _spare1;
    intData _spare2;
    intData _spare3;

    void validatePacket();
    bool validPacket = false;
    String packet = "";
    int debugCounter = 0;

    int _packetCounter = 0;

    bool _packetStart = false;
    bool _packetEnd = false;
    int _counter = 0;

    long lastValidPacketTime;
    long lastSendPacketTime;

    signed char hexConvert(char Low, char High);
};

#endif