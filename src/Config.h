#ifndef CONFIG_H
#define CONFIG_H

// ============================================================================
// HARDWARE PIN DEFINITIONS
// ============================================================================
#define PIN_MQ135_ANALOG   A0
#define PIN_BUTTON_MUTE    2
#define PIN_DHT22_DATA     4
#define PIN_BUZZER         8
#define PIN_LED_RED        9
#define PIN_LED_GREEN      10

// ============================================================================
// SENSOR & THRESHOLD CONSTANTS
// ============================================================================
#define GAS_THRESHOLD_WARNING_PPM   350.0f
#define GAS_THRESHOLD_CRITICAL_PPM  500.0f
#define TEMP_THRESHOLD_HIGH_C       38.0f
#define HUMIDITY_THRESHOLD_HIGH_PCT 75.0f

// Sensor Calibration Constants
#define MQ135_RLOAD_KOHMS           10.0f
#define MQ135_R0_CLEAN_AIR          76.63f
#define ADC_MAX_VALUE               1023.0f
#define VREF_VOLTAGE                5.0f

// QA-001 Fix: Sensor Warmup & Stabilization Timing
#define MQ135_WARMUP_TIME_MS        30000UL // 30-second thermal stabilization window

// QA-003 Fix: Switch Debounce Timing Window
#define BUTTON_DEBOUNCE_DELAY_MS    50UL    // 50ms temporal refractory period

// QA-004 Fix: Non-Blocking Multi-Rate Task Scheduling Intervals
#define INTERVAL_GAS_SAMPLE_MS      100UL   // 10 Hz sampling for real-time gas alarm
#define INTERVAL_LCD_REFRESH_MS     500UL   // 2 Hz LCD display update
#define INTERVAL_DHT_SAMPLE_MS      2500UL  // 0.4 Hz DHT22 read (min 2.0s required)
#define INTERVAL_SERIAL_LOG_MS      1000UL  // 1 Hz telemetry logging

#endif // CONFIG_H
