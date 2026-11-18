/**
 * Project: Smart Environmental Air Quality & Toxic Gas Alert Monitor
 * Version: 1.1.0 (QA & Reliability Hardened Release)
 * Description: Non-blocking cooperative scheduler for MQ-135 gas sensor,
 * DHT22 environmental monitoring, debounced HMI, and I2C LCD alert management.
 */

#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <DHT.h>
#include "Config.h"

// Peripheral Instances
LiquidCrystal_I2C lcd(0x27, 16, 2);
DHT dht(PIN_DHT22_DATA, DHT22);

// System State
bool alarmMuted = false;
bool sensorReady = false;
unsigned long bootTimestamp = 0;

// Button Debounce State Variables (QA-003 Fix)
int lastButtonReading = HIGH;
int stableButtonState = HIGH;
unsigned long lastDebounceTimestamp = 0;

// Cooperative Task Scheduling Timestamps (QA-004 Fix)
unsigned long lastGasSampleTimestamp = 0;
unsigned long lastDhtSampleTimestamp = 0;
unsigned long lastLcdRefreshTimestamp = 0;
unsigned long lastSerialLogTimestamp = 0;

// Current Sensor Values Cache
float cachedPpm = 0.0f;
float cachedTemperature = 0.0f;
float cachedHumidity = 0.0f;

void setup() {
  Serial.begin(9600);
  Serial.println(F("[BOOT] Initializing Air Quality Monitor v1.1.0..."));

  pinMode(PIN_BUTTON_MUTE, INPUT_PULLUP);
  pinMode(PIN_BUZZER, OUTPUT);
  pinMode(PIN_LED_RED, OUTPUT);
  pinMode(PIN_LED_GREEN, OUTPUT);

  // Initialize LCD with I2C bus lockup protection (QA-002 Fix)
  Wire.begin();
  #if defined(WIRE_HAS_TIMEOUT)
  Wire.setWireTimeout(3000, true); // 3000 us timeout with peripheral auto-recovery
  #endif
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("Air Monitor v1.1");
  lcd.setCursor(0, 1);
  lcd.print("Initializing...");

  dht.begin();

  // Test acoustic/visual alarms on power-up
  digitalWrite(PIN_BUZZER, HIGH);
  digitalWrite(PIN_LED_RED, HIGH);
  digitalWrite(PIN_LED_GREEN, HIGH);
  delay(150);
  digitalWrite(PIN_BUZZER, LOW);
  digitalWrite(PIN_LED_RED, LOW);
  digitalWrite(PIN_LED_GREEN, LOW);

  bootTimestamp = millis();
  Serial.println(F("[BOOT] Initialization complete. Entering sensor warmup mode."));
}

void loop() {
  unsigned long currentMillis = millis();

  // ==========================================================================
  // TASK 1: Tactile Switch Debounce & HMI Event Processing (Continuous, <1ms)
  // ==========================================================================
  int currentReading = digitalRead(PIN_BUTTON_MUTE);
  if (currentReading != lastButtonReading) {
    lastDebounceTimestamp = currentMillis;
  }
  if ((currentMillis - lastDebounceTimestamp) > BUTTON_DEBOUNCE_DELAY_MS) {
    if (currentReading != stableButtonState) {
      stableButtonState = currentReading;
      if (stableButtonState == LOW) { // Valid falling-edge trigger
        alarmMuted = !alarmMuted;
        Serial.print(F("[HMI] Mute state toggled: "));
        Serial.println(alarmMuted ? F("MUTED") : F("UNMUTED"));
      }
    }
  }
  lastButtonReading = currentReading;

  // ==========================================================================
  // TASK 2: Sensor Warmup & Stabilization Check (QA-001 Fix)
  // ==========================================================================
  if (!sensorReady) {
    unsigned long elapsed = currentMillis - bootTimestamp;
    if (elapsed >= MQ135_WARMUP_TIME_MS) {
      sensorReady = true;
      Serial.println(F("[WARMUP] Stabilization complete. Active monitoring started."));
    } else {
      if (currentMillis - lastLcdRefreshTimestamp >= INTERVAL_LCD_REFRESH_MS) {
        lastLcdRefreshTimestamp = currentMillis;
        int secondsLeft = (MQ135_WARMUP_TIME_MS - elapsed) / 1000;
        lcd.setCursor(0, 0);
        lcd.print("Sensor Warming  ");
        lcd.setCursor(0, 1);
        lcd.print("Wait: ");
        lcd.print(secondsLeft);
        lcd.print("s       ");
        digitalWrite(PIN_BUZZER, LOW);
        digitalWrite(PIN_LED_RED, LOW);
        digitalWrite(PIN_LED_GREEN, (secondsLeft % 2 == 0) ? HIGH : LOW);
      }
      return; // Skip active monitoring while heating
    }
  }

  // ==========================================================================
  // TASK 3: High-Frequency Gas Sampling & Alarm Actuation (10 Hz, 100ms)
  // ==========================================================================
  if (currentMillis - lastGasSampleTimestamp >= INTERVAL_GAS_SAMPLE_MS) {
    lastGasSampleTimestamp = currentMillis;

    int rawADC = analogRead(PIN_MQ135_ANALOG);
    float voltage = rawADC * (VREF_VOLTAGE / ADC_MAX_VALUE);
    cachedPpm = (voltage / VREF_VOLTAGE) * 1000.0f;

    // Instantaneous Alarm Logic
    if (cachedPpm > GAS_THRESHOLD_CRITICAL_PPM && !alarmMuted) {
      digitalWrite(PIN_BUZZER, HIGH);
      digitalWrite(PIN_LED_RED, HIGH);
      digitalWrite(PIN_LED_GREEN, LOW);
    } else if (cachedPpm > GAS_THRESHOLD_WARNING_PPM) {
      digitalWrite(PIN_BUZZER, LOW);
      digitalWrite(PIN_LED_RED, HIGH);
      digitalWrite(PIN_LED_GREEN, HIGH);
    } else {
      digitalWrite(PIN_BUZZER, LOW);
      digitalWrite(PIN_LED_RED, LOW);
      digitalWrite(PIN_LED_GREEN, HIGH);
    }
  }

  // ==========================================================================
  // TASK 4: Environmental Climate Sampling (0.4 Hz, 2500ms)
  // ==========================================================================
  if (currentMillis - lastDhtSampleTimestamp >= INTERVAL_DHT_SAMPLE_MS) {
    lastDhtSampleTimestamp = currentMillis;
    float h = dht.readHumidity();
    float t = dht.readTemperature();
    if (!isnan(h) && !isnan(t)) {
      cachedHumidity = h;
      cachedTemperature = t;
    }
  }

  // ==========================================================================
  // TASK 5: LCD Display Dashboard Refresh (2 Hz, 500ms)
  // ==========================================================================
  if (currentMillis - lastLcdRefreshTimestamp >= INTERVAL_LCD_REFRESH_MS) {
    lastLcdRefreshTimestamp = currentMillis;

    lcd.setCursor(0, 0);
    lcd.print("PPM:");
    lcd.print((int)cachedPpm);
    lcd.print(" ");
    if (cachedPpm > GAS_THRESHOLD_CRITICAL_PPM) {
      lcd.print(alarmMuted ? "DANG[M]" : "DANGER ");
    } else if (cachedPpm > GAS_THRESHOLD_WARNING_PPM) {
      lcd.print("WARN   ");
    } else {
      lcd.print("SAFE   ");
    }

    lcd.setCursor(0, 1);
    lcd.print("T:");
    lcd.print((int)cachedTemperature);
    lcd.print("C H:");
    lcd.print((int)cachedHumidity);
    lcd.print("%   ");
  }

  // ==========================================================================
  // TASK 6: Diagnostic Telemetry Serial Output (1 Hz, 1000ms)
  // ==========================================================================
  if (currentMillis - lastSerialLogTimestamp >= INTERVAL_SERIAL_LOG_MS) {
    lastSerialLogTimestamp = currentMillis;
    Serial.print(F("Time: "));
    Serial.print(currentMillis / 1000);
    Serial.print(F("s | PPM: "));
    Serial.print(cachedPpm);
    Serial.print(F(" | Temp: "));
    Serial.print(cachedTemperature);
    Serial.print(F("C | Humidity: "));
    Serial.print(cachedHumidity);
    Serial.print(F("% | Muted: "));
    Serial.println(alarmMuted ? F("YES") : F("NO"));
  }
}
