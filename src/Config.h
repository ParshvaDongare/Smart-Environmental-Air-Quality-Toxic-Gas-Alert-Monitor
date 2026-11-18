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

#endif // CONFIG_H
