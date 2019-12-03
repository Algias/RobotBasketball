#include "Sensor.h"

Sensor::Sensor() : myFilter(0.10) {}

int Sensor::getValue()
{
  return _value;
}

int Sensor::getRaw()
{
  return _rawValue;
}

int Sensor::getMapped()
{
  return _mappedValue;
}

void Sensor::setMappedScale(int scale)
{
  _mapScale = scale;
}

void Sensor::mapValue()
{
  //If we are in velocity mode, take the current value and find the discrete derivative of it for velocity
  if (mode == velocity)
  {
    _currentTime = millis();
    _deltaT = _currentTime - _prevTime;
    if (longDelta && _deltaT < 35)
    {
      return;
    }
    int diff = _rawValue - _prevRawValue;

    //Filter out the noisy 1/2 value changes
    // if (abs(diff) == 1 || abs(diff) == 2)
    //   diff = 0;
    if (invert)
      diff *= -1;
    _mappedValue = (int)(((long)diff * (long)_mapScale) / (long)_deltaT);
    //Filter the rest of the derivative noise
    _mappedValue = myFilter.filter(_mappedValue);
    _prevTime = _currentTime;
    _prevRawValue = _rawValue;
  }
}

DigitalInput::DigitalInput(byte pin) : Sensor()
{
  _pin = pin;
}

void DigitalInput::readInput()
{
  _rawValue = digitalRead(_pin);
}

PWMInput::PWMInput(byte pin)
{
  _pin = pin;
  pinMode(pin, INPUT);

  // Measure feedback signal high/low times.
  tLow = pulseIn(_pin, LOW, 5000);   // Measure low time
  tHigh = pulseIn(_pin, HIGH, 5000); // Measure high time

  // Calcualte initial duty cycle and angle.
  dc = (dutyScale * tHigh) / (tHigh + tLow);
  theta = (unitsFC - 1) - ((dc - dcMin) * unitsFC) / (dcMax - dcMin + 1);
  //theta = filter.filter(theta);
  thetaP = theta;
  // theta = filter.filter(theta);
}

void PWMInput::readInput()
{

  // Measure high and low times, making sure to only take valid cycle
  // times (a high and a low on opposite sides of the 0/359 boundary
  // will not be valid.
  long tCycle = 0; // Clear cycle time

  tHigh = pulseIn(_pin, HIGH, 5000); // Measure time high
  tLow = pulseIn(_pin, LOW, 5000);   // Measure time low
  tCycle = tHigh + tLow;
  if ((tCycle < 1000) || (tCycle > 1200)) // If cycle time invalid
    return;

  dc = (dutyScale * tHigh) / tCycle; // Calculate duty cycle

  // This gives a theta increasing int the
  // counterclockwise direction.
  theta = (unitsFC - 1) - // Calculate angle
          ((dc - dcMin) * unitsFC) / (dcMax - dcMin + 1);

  if (theta < 0) // Keep theta valid
    theta = 0;
  else if (theta > (unitsFC - 1))
    theta = unitsFC - 1;

  // If transition from quadrant 4 to
  // quadrant 1, increase turns count.
  if ((theta < q2min) && (thetaP > q3max))
    turns++;
  // If transition from quadrant 1 to
  // quadrant 4, decrease turns count.
  else if ((thetaP < q2min) && (theta > q3max))
    turns--;

  // Construct the angle measurement from the turns count and
  // current theta value.
  if (turns >= 0)
    angle = (turns * unitsFC) + theta;
  else if (turns < 0)
    angle = ((turns + 1) * unitsFC) - (unitsFC - theta);

  thetaP = theta; // Theta previous for next rep
  _rawValue = angle;
  //_value = angle;
}

AnalogInput::AnalogInput(byte pin)
{
  _pin = pin;
  pinMode(pin, INPUT);
}

void AnalogInput::readInput()
{
  _rawValue = analogRead(_pin);
}

static int PCIInput::rawCounter;

static void PCIInput::interruptResponse()
{
  // _rawValue++;
  PCIInput::rawCounter++;
}

PCIInput::PCIInput(byte pin)
{
  _pin = pin;
  pinMode(pin, INPUT_PULLUP);
  // Attach the new PinChangeInterrupt and enable event function below
  attachPCINT(digitalPinToPCINT(_pin), PCIInput::interruptResponse, RISING);
}

void PCIInput::readInput()
{

  _rawValue = rawCounter;
}

QuadratureInput::QuadratureInput(byte channelA, byte channelB) // : _encoder(channelA, channelB)
{
  _channelA = channelA;
  pinMode(channelA, INPUT);
  _channelB = channelB;
  pinMode(channelB, INPUT);
}

void QuadratureInput::readInput()
{
  //_rawValue = _encoder.getEncoderCount();
}