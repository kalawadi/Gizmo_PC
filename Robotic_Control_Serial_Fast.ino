
/*

This code has been modified from the original code "BraccioSerialArduino" by Khulood Alawadi
by removing Serial.println in order to make the robotic arm move faster.

*/

#include <Braccio.h>
#include <Servo.h>

Servo base;
Servo shoulder;
Servo elbow;
Servo wrist_rot;
Servo wrist_ver;
Servo gripper;

int stepDelay = 10;
  // the position recieved from the serial (current command)
int m1 = 90;
int m2 = 45;
int m3 = 180;
int m4 = 180;
int m5 = 90;
int m6 = 10;

/*
  // the actual position (past) 
int m1p = 90;
int m2p = 45;
int m3p = 180;
int m4p = 180;
int m5p = 90;
int m6p = 10;
*/

char inData[25];
bool isRead = false;
int index = 0;

void setup() {

  Braccio.begin();
  Serial.begin(9600);
}

void loop() {

  readSerialStr();
  //Braccio.ServoMovement(stepDelay, m1, m2, m3, m4, m5, m6);

  // When receive a new value and 'if' statement is required

  base.write(m1); 
  shoulder.write(m2);
  elbow.write(m3);
  wrist_rot.write(m4);
  wrist_ver.write(m5);
  gripper.write(m6); 
  delay(100);
  
}

void readSerialStr() {

  if (Serial.available() > 0) {
    
    char incomingByte = Serial.read();
    while (incomingByte != '\n' && isDigit(incomingByte)) {
      isRead = true;
      delay(100);
      inData[index] = incomingByte;
      index++;
      incomingByte = Serial.read();
    }
    inData[index] = '\0';
  }

  if (isRead) {
    char m1_char[4];
    char m2_char[4];
    char m3_char[4];
    char m4_char[4];
    char m5_char[4];
    char m6_char[4];

    m1_char[0] = inData[0];
    m1_char[1] = inData[1];
    m1_char[2] = inData[2];
    m1_char[3] = '\0';
    m2_char[0] = inData[3];
    m2_char[1] = inData[4];
    m2_char[2] = inData[5];
    m2_char[3] = '\0';
    m3_char[0] = inData[6];
    m3_char[1] = inData[7];
    m3_char[2] = inData[8];
    m3_char[3] = '\0';
    m4_char[0] = inData[9];
    m4_char[1] = inData[10];
    m4_char[2] = inData[11];
    m4_char[3] = '\0';
    m5_char[0] = inData[12];
    m5_char[1] = inData[13];
    m5_char[2] = inData[14];
    m5_char[3] = '\0';
    m6_char[0] = inData[15];
    m6_char[1] = inData[16];
    m6_char[2] = inData[17];
    m6_char[3] = '\0';

    m1 = atoi(m1_char);
    m2 = atoi(m2_char);
    m3 = atoi(m3_char);
    m4 = atoi(m4_char);
    m5 = atoi(m5_char);
    m6 = atoi(m6_char);

    isRead = false;
    index = 0;
  }

}
