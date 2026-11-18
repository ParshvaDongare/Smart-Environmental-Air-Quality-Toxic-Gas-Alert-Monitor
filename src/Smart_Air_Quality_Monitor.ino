/**
 * Project: Smart Environmental Air Quality & Toxic Gas Alert Monitor
 * Academic Year: 2026-2027 | Course: Project Management (2307476T)
 * Department of Electronics & Telecommunication Engineering
 * MIT Academy of Engineering, Pune
 *
 * Version: 1.0.0 (Initial Prototype Release)
 * Description: Basic implementation for reading MQ-135 gas sensor and DHT22,
 * displaying readings on 16x2 I2C LCD, and sounding an alarm when threshold is crossed.
 */

#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <DHT.h>
#include "Config.h"

// Initialize peripherals
LiquidCrystal_I2C lcd(0x27, 16, 2);
DHT dht(PIN_DHT22_DATA, DHT22);

bool alarmMuted = false;

void setup() {
  Serial.begin(9600);
  Serial.println(F("[BOOT] Initializing Air Quality Monitor v1.0.0..."));

  pinMode(PIN_BUTTON_MUTE, INPUT_PULLUP);
  pinMode(PIN_BUZZER, OUTPUT);
  pinMode(PIN_LED_RED, OUTPUT);
  pinMode(PIN_LED_GREEN, OUTPUT);

  // Initialize LCD
  Wire.begin();
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("Air Monitor v1.0");

  dht.begin();

  // Test buzzer on startup
  digitalWrite(PIN_BUZZER, HIGH);
  delay(100);
  digitalWrite(PIN_BUZZER, LOW);

  Serial.println(F("[BOOT] System initialization complete."));
}

void loop() {
  // Read MQ-135 Analog Sensor
  int rawADC = analogRead(PIN_MQ135_ANALOG);
  float voltage = rawADC * (VREF_VOLTAGE / ADC_MAX_VALUE);
  float ppm = (voltage / VREF_VOLTAGE) * 1000.0f; // Simplified linear approximation

  // Read DHT22
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  // Check Mute Button (Naive check without debouncing)
  if (digitalRead(PIN_BUTTON_MUTE) == LOW) {
    alarmMuted = !alarmMuted; // Toggle mute
    Serial.println(F("[BUTTON] Mute toggled!"));
  }

  // Serial Diagnostic Logging
  Serial.print(F("PPM: "));
  Serial.print(ppm);
  Serial.print(F(" | Temp: "));
  Serial.print(temperature);
  Serial.print(F("C | Humidity: "));
  Serial.print(humidity);
  Serial.print(F("% | Muted: "));
  Serial.println(alarmMuted ? "YES" : "NO");

  // Display on LCD
  lcd.setCursor(0, 0);
  lcd.print("PPM: ");
  lcd.print((int)ppm);
  lcd.print(" Gas: ");
  if (ppm > GAS_THRESHOLD_CRITICAL_PPM) {
    lcd.print("DANGER");
  } else {
    lcd.print("NORMAL");
  }

  lcd.setCursor(0, 1);
  lcd.print("T:");
  lcd.print((int)temperature);
  lcd.print("C H:");
  lcd.print((int)humidity);
  lcd.print("%   ");

  // Alarm actuation
  if (ppm > GAS_THRESHOLD_CRITICAL_PPM && !alarmMuted) {
    digitalWrite(PIN_BUZZER, HIGH);
    digitalWrite(PIN_LED_RED, HIGH);
    digitalWrite(PIN_LED_GREEN, LOW);
  } else {
    digitalWrite(PIN_BUZZER, LOW);
    digitalWrite(PIN_LED_RED, LOW);
    digitalWrite(PIN_LED_GREEN, HIGH);
  }

  // Blocking delay for DHT22 timing & LCD update
  delay(2000);
}
