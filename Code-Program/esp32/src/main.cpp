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

// ==========================
// PWM configuration
// ==========================
const int PWM_FREQ       = 5000;  // 5 kHz PWM
const int PWM_RESOLUTION = 8;     // 8-bit (0–255)

// Channels for each IN1/IN2 pair
enum {
  CH_FL_F = 0, CH_FL_R,
  CH_FR_F, CH_FR_R,
  CH_BL_F, CH_BL_R,
  CH_BR_F, CH_BR_R
};

// Last commanded wheel PWMs (–255…+255)
int fl_pwm = 0, fr_pwm = 0, bl_pwm = 0, br_pwm = 0;

/**
 * Map percent input (–100…+100) to PWM:
 *   pct ==  0   →   0
 *   pct == +1   → +140
 *   pct == +100 → +255
 *   pct == –1   → –140
 *   pct == –100 → –255
 */
int percentToPwm(int pct) {
  if (pct > 0) {
    // map [1..100] → [140..255]
    return map(pct, 1, 100, 140, 255);
  } else if (pct < 0) {
    // map [–1..–100] → [–140..–255]
    // map() needs increasing ranges, so flip:
    int absPct = -pct;
    int pwm    = map(absPct, 1, 100, 140, 255);
    return -pwm;
  }
  // pct == 0
  return 0;
}

// Drive a single motor: chF = forward channel, chR = reverse channel
void driveMotor(int chF, int chR, int pwm) {
  if (pwm >= 0) {
    ledcWrite(chF, pwm);
    ledcWrite(chR, 0);
  } else {
    ledcWrite(chF, 0);
    ledcWrite(chR, -pwm);
  }
}

void setup() {
  Serial.begin(115200);
  while (!Serial) { delay(10); }
  Serial.println("ESP32 Wheel Sync with Deadzone Mapping Ready");

  // Configure pins as outputs
  pinMode(FL_IN1, OUTPUT); pinMode(FL_IN2, OUTPUT);
  pinMode(FR_IN1, OUTPUT); pinMode(FR_IN2, OUTPUT);
  pinMode(BL_IN1, OUTPUT); pinMode(BL_IN2, OUTPUT);
  pinMode(BR_IN1, OUTPUT); pinMode(BR_IN2, OUTPUT);

  // Attach each pin to a PWM channel
  ledcSetup(CH_FL_F, PWM_FREQ, PWM_RESOLUTION); ledcAttachPin(FL_IN1, CH_FL_F);
  ledcSetup(CH_FL_R, PWM_FREQ, PWM_RESOLUTION); ledcAttachPin(FL_IN2, CH_FL_R);

  ledcSetup(CH_FR_F, PWM_FREQ, PWM_RESOLUTION); ledcAttachPin(FR_IN1, CH_FR_F);
  ledcSetup(CH_FR_R, PWM_FREQ, PWM_RESOLUTION); ledcAttachPin(FR_IN2, CH_FR_R);

  ledcSetup(CH_BL_F, PWM_FREQ, PWM_RESOLUTION); ledcAttachPin(BL_IN1, CH_BL_F);
  ledcSetup(CH_BL_R, PWM_FREQ, PWM_RESOLUTION); ledcAttachPin(BL_IN2, CH_BL_R);

  ledcSetup(CH_BR_F, PWM_FREQ, PWM_RESOLUTION); ledcAttachPin(BR_IN1, CH_BR_F);
  ledcSetup(CH_BR_R, PWM_FREQ, PWM_RESOLUTION); ledcAttachPin(BR_IN2, CH_BR_R);
}

void loop() {
  // Read a line if available
  if (Serial.available()) {
    String line = Serial.readStringUntil('\n');
    line.trim();
    if (line.length() > 0) {
      int p0, p1, p2, p3;
      int n = sscanf(line.c_str(), "%d,%d,%d,%d", &p0, &p1, &p2, &p3);
      if (n == 4) {
        fl_pwm = percentToPwm(p0);
        fr_pwm = percentToPwm(p1);
        bl_pwm = percentToPwm(p2);
        br_pwm = percentToPwm(p3);
        Serial.printf(
          "Rx %%: [%d, %d, %d, %d] → PWM: [FL=%d, FR=%d, BL=%d, BR=%d]\n",
          p0, p1, p2, p3, fl_pwm, fr_pwm, bl_pwm, br_pwm
        );
      } else {
        Serial.println("! parse error");
      }
    }
  }

  // Re-apply last PWM values at 100 Hz
  driveMotor(CH_FL_F, CH_FL_R, fl_pwm);
  driveMotor(CH_FR_F, CH_FR_R, fr_pwm);
  driveMotor(CH_BL_F, CH_BL_R, bl_pwm);
  driveMotor(CH_BR_F, CH_BR_R, br_pwm);

  delay(10);
}
