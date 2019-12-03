#include "Communication.h"
Communication::Communication(byte Tx, byte Rx)
{
}

Communication::~Communication()
{
}
//Cyclically read data
void Communication::readComms()
{
    if (!Serial.available() && ((millis() - lastSendPacketTime) > WRITE_COMM_TIMEOUT_MILLIS))
    {
        Serial.println("G");
        // packet = "";
        // _packetEnd = false;
        // _packetStart = false;
        lastSendPacketTime = millis();
    }

    //Serial.println("Im in the >31 char");
    //Iterate through the characters
    while (Serial.available())
    {
        //Read character from buffer (and remove from buffer)
        char c = Serial.read();

        //If the packet has not started and we receive a ^
        if (!_packetStart && c == '^')
        {
            // digitalWrite(DEBUG_PIN, HIGH);
            _packetStart = true;
            _packetEnd = false;
            // Serial.println("Packet Begin");
            packet = "^";
        }
        //Packet has not started and not a ^
        else if (!_packetStart && c != '^')
        {
            //Jump to the beginning of the while loop
            Serial.println("Dead Char");
            continue;
        }
        //Packet has begun and is not finished
        else if (_packetStart && c != '\n')
        {
            // Serial.println("Good char");
            packet += c;
        }
        //finishing now
        else if (c == '\n')
        {
            // Serial.println("Finish packet");
            // digitalWrite(DEBUG_PIN, LOW);
            packet += c;
            _packetEnd = true;
            _packetStart = false;
            Serial.print("Packet: ");
            Serial.println(packet);

            break;
        }
        //packet += c;
        //Expects the following form:
        //^000000,00,00,00,00,00,00,00,00
    }

    // _packetEnd = true;
}
void Communication::writeComms()
{
    // Serial.println(_launcherV.value);
}

void Communication::initializeComms()
{
    Serial.begin(115200); // Start bluetooth serial at 9600
}

//Conver the ascii data to valid commands
void Communication::parseComms()
{
    //If the packet isn't ready, return
    if (!_packetEnd)
        return;
    //Verify packet integrity
    validatePacket();
    //If the packet is valid, start converting data
    if (validPacket)
    {
        // digitalWrite(DEBUG_PIN, !digitalRead(DEBUG_PIN));
        //Parse Header
        for (int i = 1; i < 5; i++)
            _header.str[i - 1] = (char)packet[i];

        _state.rawData = hexConvert(packet[5], packet[6]);

        _driveVx.rawData = hexConvert(packet[8], packet[9]);

        _driveVy.rawData = hexConvert(packet[11], packet[12]);

        _driveW.rawData = hexConvert(packet[14], packet[15]);

        _launcherV.rawData = hexConvert(packet[17], packet[18]);

        _intakeP.rawData = hexConvert(packet[20], packet[21]);

        _spare1.rawData = hexConvert(packet[23], packet[24]);

        _spare2.rawData = hexConvert(packet[26], packet[27]);

        _spare3.rawData = hexConvert(packet[29], packet[30]);

        if (debugCounter++ % 5 == 0)
        {
            String myTestString;
            myTestString += String(_header.value);
            myTestString += ",";
            myTestString += String(_state.value);
            myTestString += ",";
            myTestString += String(_driveVx.value);
            myTestString += ",";
            myTestString += String(_driveVy.value);
            myTestString += ",";
            myTestString += String(_driveW.value);
            myTestString += ",";
            myTestString += String(_launcherV.value);
            myTestString += ",";
            myTestString += String(_intakeP.value);
        }
        validPacket = false;
        packet = "";
    }
}

//Prepare a packet to send data
void Communication::packComms()
{
    //TODO: Prep packet to send back serially to the Master controler
}

//Verifies that the packet as valid data such as the commas in correct locations, start and end characters, and hex data
void Communication::validatePacket()
{
    //StartCharacter|Header|State|sep|drive vx|
    //sep|drive vy|sep|drive w|sep| launch speed|sep|
    //intake p |sep| spare 1|sep| spare 2|sep| spare 3| endchar
    // ^012301,01,01,01,01,01,01,01,01
    int packetLength = packet.length();
    // Validate packet
    if (packetLength != 0)
    {

        if (packetLength != 32)
        {
            validPacket = false;
            //Serial.print("Invalid Length: ");
            //Serial.println(packetLength);
        }
        else if (packet[0] != '^')
        {
            validPacket = false;
            //Serial.println("Invalid start");
        }
        else if (packet[7] != ',')
        {
            validPacket = false;
            //Serial.println("Invalid 1 comma");
        }
        else if (packet[10] != ',')
        {
            validPacket = false;
            //Serial.println("Invalid 2 comma");
        }
        else if (packet[13] != ',')
        {
            validPacket = false;
            //Serial.println("Invalid 3 comma");
        }
        else if (packet[16] != ',')
        {
            validPacket = false;
            //Serial.println("Invalid 4 comma");
        }
        else if (packet[19] != ',')
        {
            validPacket = false;
            //Serial.println("Invalid 5 comma");
        }
        else if (packet[22] != ',')
        {
            validPacket = false;
            //Serial.println("Invalid 6 comma");
        }
        else if (packet[25] != ',')
        {
            validPacket = false;
            //Serial.println("Invalid 7 comma");
        }
        else if (packet[28] != ',')
        {
            validPacket = false;
            //Serial.println("Invalid 8 comma");
        }
        else if (packet[31] != '\n')
        {
            validPacket = false;
            //Serial.println("Invalid end ");
        }
        else
        {
            validPacket = true;
            lastValidPacketTime = millis();
            //Serial.println("Valid Packet");
        }
    }
}

int Communication::getDriveVx()
{
    return _driveVx.value;
}

int Communication::getDriveVy()
{
    return _driveVy.value;
}

int Communication::getDriveW()
{
    return _driveW.value;
}

int Communication::getLauncher()
{
    return _launcherV.value;
}

int Communication::getIntake()
{
    return _intakeP.value;
}

bool Communication::checkTimeout()
{
    //Returns true if the packet has timed out
    // (AKA, have not received valid packet in more than COMM timeout in milliseconds)
    if ((millis() - lastValidPacketTime) > COMMUNICATION_TIMEOUT_MILLIS)
    {
        return true;
    }
    else
    {
        return false;
    }
}

//Takes two hex characters and converts it to binary data
signed char Communication::hexConvert(char Low, char High)
{
    //Initialize result
    signed char result = 0;
    //If the upper hex is > A, add 10 to the reuslt
    if (High >= 'A')
    {
        result = High - 'A' + 10;
    }
    //If the upper hex is a digit, add to the result
    else if (High >= '0')
    {
        result = High - '0';
    }
    //If the lower hex is a character, add ten and then shift the bits and add
    if (Low >= 'A')
    {
        result += ((Low - 'A' + 10) << 4);
    }
    //If the lower hex is a digit, shift the bits and add
    else if (Low >= '0')
    {
        result += ((Low - '0') << 4);
    }
    return result;
}