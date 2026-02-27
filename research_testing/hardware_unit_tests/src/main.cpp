#include <Arduino.h>

// ==========================
// Pin configuration
// ==========================

// Front Left Motor
#define FL_IN1 25
#define FL_IN2 26

// Front Right Motor
#define FR_IN1 27
#define FR_IN2 14

// Back Left Motor
#define BL_IN1 12
#define BL_IN2 13

// Back Right Motor
#define BR_IN1 32
#define BR_IN2 33

void setMotor(int in1, int in2, bool forward) {
  digitalWrite(in1, forward ? HIGH : LOW);
  digitalWrite(in2, forward ? LOW  : HIGH);
}

void stopAll() {
  digitalWrite(FL_IN1, LOW); digitalWrite(FL_IN2, LOW);
  digitalWrite(FR_IN1, LOW); digitalWrite(FR_IN2, LOW);
  digitalWrite(BL_IN1, LOW); digitalWrite(BL_IN2, LOW);
  digitalWrite(BR_IN1, LOW); digitalWrite(BR_IN2, LOW);
}

void setup() {
  pinMode(FL_IN1, OUTPUT); pinMode(FL_IN2, OUTPUT);
  pinMode(FR_IN1, OUTPUT); pinMode(FR_IN2, OUTPUT);
  pinMode(BL_IN1, OUTPUT); pinMode(BL_IN2, OUTPUT);
  pinMode(BR_IN1, OUTPUT); pinMode(BR_IN2, OUTPUT);
}

void loop() {
  // === เดินหน้า ===
  setMotor(FL_IN1, FL_IN2, true);
  setMotor(FR_IN1, FR_IN2, true);
  setMotor(BL_IN1, BL_IN2, true);
  setMotor(BR_IN1, BR_IN2, true);
  delay(500); stopAll(); delay(500);

  // === ถอยหลัง ===
  setMotor(FL_IN1, FL_IN2, false);
  setMotor(FR_IN1, FR_IN2, false);
  setMotor(BL_IN1, BL_IN2, false);
  setMotor(BR_IN1, BR_IN2, false);
  delay(500); stopAll(); delay(500);

  // === สไตรฟขวา ===
  setMotor(FL_IN1, FL_IN2, true);
  setMotor(FR_IN1, FR_IN2, false);
  setMotor(BL_IN1, BL_IN2, false);
  setMotor(BR_IN1, BR_IN2, true);
  delay(500); stopAll(); delay(500);

  // === สไตรฟซ้าย ===
  setMotor(FL_IN1, FL_IN2, false);
  setMotor(FR_IN1, FR_IN2, true);
  setMotor(BL_IN1, BL_IN2, true);
  setMotor(BR_IN1, BR_IN2, false);
  delay(500); stopAll(); delay(500);

  // === หมุนขวา ===
  setMotor(FL_IN1, FL_IN2, true);
  setMotor(FR_IN1, FR_IN2, false);
  setMotor(BL_IN1, BL_IN2, true);
  setMotor(BR_IN1, BR_IN2, false);
  delay(500); stopAll(); delay(500);

  // === หมุนซ้าย ===
  setMotor(FL_IN1, FL_IN2, false);
  setMotor(FR_IN1, FR_IN2, true);
  setMotor(BL_IN1, BL_IN2, false);
  setMotor(BR_IN1, BR_IN2, true);
  delay(500); stopAll(); delay(500);

  // === เฉียงหน้า-ขวา === (FL + BR forward)
  setMotor(FL_IN1, FL_IN2, true);
  setMotor(BR_IN1, BR_IN2, true);
  delay(500); stopAll(); delay(500);

  // === เฉียงหน้า-ซ้าย === (FR + BL forward)
  setMotor(FR_IN1, FR_IN2, true);
  setMotor(BL_IN1, BL_IN2, true);
  delay(500); stopAll(); delay(500);

  // === เฉียงหลัง-ขวา === (FR + BL backward)
  setMotor(FR_IN1, FR_IN2, false);
  setMotor(BL_IN1, BL_IN2, false);
  delay(500); stopAll(); delay(500);

  // === เฉียงหลัง-ซ้าย === (FL + BR backward)
  setMotor(FL_IN1, FL_IN2, false);
  setMotor(BR_IN1, BR_IN2, false);
  delay(500); stopAll(); delay(500);

  while (true) delay(1000); // หยุดลูปหลังทดสอบครบ
}