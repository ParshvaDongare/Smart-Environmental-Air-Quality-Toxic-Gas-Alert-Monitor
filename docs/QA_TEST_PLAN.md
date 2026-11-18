# Quality Assurance Test Plan & Verification Protocol

## 1. Test Environment
- **Target Device:** ATmega328P (Arduino Uno)
- **Clock Speed:** 16 MHz
- **Supply Voltage:** 5.0 V DC regulated
- **Test Instruments:** Digital Multimeter, 2-Channel USB Oscilloscope, Serial Monitor (9600 baud)

---

## 2. Test Execution Matrix

| Test Case ID | Feature Under Test | Test Input / Condition | Expected Result | Pass/Fail Criteria |
| :--- | :--- | :--- | :--- | :--- |
| **TC-01** | Power-on Warmup Grace | Cold start from 0V supply | LCD displays warmup countdown; buzzer remains silent during first 30 seconds. | Pass: 0 false alarms during boot phase. |
| **TC-02** | Gas Threshold Alert | Expose MQ-135 to calibration gas (>500 PPM) | Red LED illuminates, buzzer sounds within 150 ms of threshold crossing. | Pass: Trigger latency < 200 ms. |
| **TC-03** | Alarm Silence Button | Press silence switch during active alarm | Buzzer mutes immediately; red LED stays solid; status shows MUTED. | Pass: Single press reliably mutes without bouncing. |
| **TC-04** | I2C Bus Noise Recovery | Induce transient noise / clock stretch on SDA | Wire timeout triggers; MCU resumes execution without requiring hardware reset. | Pass: Loop does not lock up; auto-recovery < 5 ms. |
| **TC-05** | Multi-Rate Scheduling | Simultaneous sensor polling and LCD refresh | Gas sampled at 10 Hz; DHT22 sampled at 0.4 Hz; loop latency under 10 ms. | Pass: Zero blocking delays detected in main loop. |

---

## 3. Verification Execution Results
- **TC-01 Result:** PASS - 30-second countdown confirmed on LCD. Buzzer inhibited until timer elapsed.
- **TC-02 Result:** PASS - Fast alarm actuation observed with non-blocking polling.
- **TC-03 Result:** PASS - 50 ms debounce window eliminated multiple toggles over 50 test presses.
- **TC-04 Result:** PASS - `Wire.setWireTimeout(3000, true)` successfully prevented hang during bus glitch.
- **TC-05 Result:** PASS - Maximum loop execution time measured at 1.4 ms.
