

// Hello LoRa - ABP TTN Packet Sender (Multi-Channel)
// Tutorial Link: https://learn.adafruit.com/the-things-network-for-feather/using-a-feather-32u4
//
// Adafruit invests time and resources providing this open source code.
// Please support Adafruit and open source hardware by purchasing
// products from Adafruit!
//
// Copyright 2015, 2016 Ideetron B.V.
//
// Modified by Brent Rubell for Adafruit Industries, 2018
/************************** Configuration ***********************************/

#include <CayenneLPP.h>
#include <TinyLoRa.h>
#include <SPI.h>

// Visit your thethingsnetwork.org device console
// to create an account, or if you need your session keys.

// Network Session Key (MSB)
uint8_t NwkSkey[16] = { 0xAE, 0x25, 0xE7, 0x2C, 0xD0, 0x38, 0xBD, 0x3F, 0x72, 0xE3, 0x92, 0x30, 0xBC, 0x83, 0xFF, 0xBF };

// Application Session Key (MSB)
uint8_t AppSkey[16] = { 0x4B, 0x6B, 0x61, 0xD9, 0x8E, 0xDE, 0x12, 0x15, 0x58, 0x40, 0x1D, 0x54, 0x52, 0x28, 0xAC, 0x19 };

// Device Address (MSB)
uint8_t DevAddr[4] = {0x26, 0x06, 0x17, 0x73 };

CayenneLPP lpp(51);

/************************** Example Begins Here ***********************************/

// How many times data transfer should occur, in seconds
const unsigned int sendInterval = 30;


// Pinout for Whisper Node LoRa
TinyLoRa lora = TinyLoRa(2, 10, 7);

void setup()
{
  delay(2000);
  Serial.begin(9600);
  while (! Serial);
  
  // Initialize pin LED_BUILTIN as an output
  pinMode(9, OUTPUT);
  
  // Initialize LoRa
  Serial.print("Starting LoRa...");
  // define multi-channel sending
  lora.setChannel(MULTI);
  // set datarate
  lora.setDatarate(SF7BW125);
  if(!lora.begin())
  {
    Serial.println("Failed");
    Serial.println("Check your radio");
    while(true);
  }

  // Optional set transmit power. If not set default is +17 dBm.
  // Valid options are: -80, 1 to 17, 20 (dBm).
  // For safe operation in 20dBm: your antenna must be 3:1 VWSR or better
  // and respect the 1% duty cycle.

  // lora.setPower(17);

  Serial.println("OK");
}

void loop()
{
  Serial.println("Sending LoRa Data...");
  
  lpp.reset();
//  lpp.addTemperature(1, 21.3);
//  lpp.addBarometricPressure(2, 1073.21);
//  lpp.addGPS(3, 52.37365, 4.88650, 2);
// Analogue goes from -320 to +320
  //lpp.addAnalogOutput(1, -320.12);
  //lpp.addLuminosity(2, 64000); //#
//  lpp.addAnalogOutput(2, -620.45f);
//  lpp.addAnalogOutput(2, 255.0);
//  lpp.addAnalogOutput(3, 500.2);
  lpp.addPresence(1, 1);
  
  //lora.sendData(loraData, sizeof(loraData), lora.frameCounter);
  lora.sendData(lpp.getBuffer(), lpp.getSize(), lora.frameCounter);
  
  // Optionally set the Frame Port (1 to 255)
  // uint8_t framePort = 1;
  // lora.sendData(loraData, sizeof(loraData), lora.frameCounter, framePort);
  
  Serial.print("Frame Counter: ");Serial.println(lora.frameCounter);
  lora.frameCounter++;

  // blink LED to indicate packet sent
  digitalWrite(9, HIGH);
  delay(1000);
  digitalWrite(9, LOW);
  
  Serial.println("delaying...");
  delay(sendInterval * 1000);
}
