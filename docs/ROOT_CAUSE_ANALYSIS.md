# Quality Assurance & Root Cause Analysis (RCA)

This document details the defect investigation, root cause determination, and remediation strategies for the Environmental Air Quality Monitor.

---

## Summary of Tracked Issues

| Issue ID | Domain | Severity | Investigation Technique | Status |
| :--- | :--- | :--- | :--- | :--- |
| **QA-001** | Sensor / Firmware | High | 5-Why Analysis | Resolved |
| **QA-002** | Bus / Interface | Critical | Ishikawa (Fishbone) Diagram | Resolved |
| **QA-003** | HMI / Debounce | Medium | 5-Why Analysis | Resolved |
| **QA-004** | Architecture | High | 5-Why Analysis | Resolved |

---

## 1. Issue QA-001: False Alarm on Power-Up (MQ-135 Warmup Cycle)

### Problem Description
Upon powering the device, the buzzer immediately sounds and the red alert LED activates, despite ambient air being clean. The alarm continues for 15–20 seconds before settling.

### 5-Why Investigation
1. **Why does the alarm trigger immediately on power-up?**  
   The analog reading from the MQ-135 sensor registers above 600 PPM, exceeding the critical threshold of 500 PPM.
2. **Why does the sensor output an elevated analog voltage in clean air?**  
   The internal tin dioxide ($SnO_2$) sensing element has not reached thermal equilibrium with the heater coil.
3. **Why does the firmware evaluate readings while the sensor is still heating?**  
   The initialization routine immediately starts comparing analog values against danger thresholds without checking sensor state.
4. **Why was no warmup delay or state check implemented?**  
   The initial software assumed sensor readings were valid instantaneously upon pin configuration.
5. **Root Cause:**  
   Missing non-blocking initialization stabilization state machine in firmware to discard burn-in transients.

### Corrective Action
- Introduce a 30-second non-blocking warmup timer during boot (`WARMUP_PERIOD_MS = 30000`).
- Display warmup countdown on LCD screen (`"Heating: 25s..."`).
- Inhibit acoustic alarm triggers until warmup flag clears.

---

## 2. Issue QA-002: I2C Display Communication Hang Under Noise

### Problem Description
Intermittent electrical noise causes the microcontroller execution to halt completely during LCD screen updates. Both serial telemetry and gas sampling stop until a hard manual reset is performed.

### Ishikawa (Fishbone) Diagram

```
Hardware & Bus                     Firmware Logic
  │                                   │
  ├─ Missing 4.7k pull-up resistors   ├─ Default blocking Wire library
  ├─ Long unshielded jumper wires     ├─ No I2C bus recovery routine
  │                                   │
  ├───────────────────────────────────┴───────────────── [ I2C Bus Lockup ]
  │                                   │
  ├─ Transient inductive kickback     ├─ Continuous LCD rewrites in loop
  ├─ Power rail voltage dips          ├─ Lack of hardware watchdog
  │                                   │
Electrical Noise                    Timing & Scheduling
```

### Root Cause
1. Hardware: Reliance on internal weak pull-ups (~30 kΩ) on SDA/SCL lines made the bus susceptible to capacitance and noise spikes.
2. Firmware: The standard `Wire` library lacked a bus timeout, causing an indefinite `while` loop block when a clock pulse was dropped.

### Corrective Action
- Add dedicated external 4.7 kΩ pull-up resistors to 5V rail.
- Enable software hardware recovery via `Wire.setWireTimeout(3000, true)` to auto-reset bus peripherals upon clock stretching timeout.

---

## 3. Issue QA-003: Button Bouncing on Alarm Silence Switch

### Problem Description
Pressing the silence pushbutton occasionally results in the buzzer briefly muting and then immediately reactivating, requiring multiple presses.

### 5-Why Investigation
1. **Why does the alarm mute and unmute with one physical press?**  
   The toggle variable switches state multiple times in rapid succession.
2. **Why does the variable toggle multiple times?**  
   The digital read evaluated the button state as pressed 3 to 6 times within 20 milliseconds.
3. **Why did the pin read multiple logic LOW states?**  
   Mechanical contacts inside the switch bounce physically upon closure.
4. **Why did the firmware react to each contact bounce?**  
   The button handling code read raw pin status every loop cycle without edge detection or a refractory delay.
5. **Root Cause:**  
   Absence of a temporal debounce filter in firmware.

### Corrective Action
- Implement software debounce with edge detection: require stable input state across a 50 ms window before accepting state transition.

---

## 4. Issue QA-004: Blocking `delay()` Stalls Real-Time Sensor Telemetry

### Problem Description
The system exhibits up to 2-3 seconds of lag when reacting to sudden toxic gas spikes, creating an unacceptable latency in hazardous environments.

### 5-Why Investigation
1. **Why is the response time to gas spikes delayed by up to 2 seconds?**  
   The main execution loop executes once every 2 seconds.
2. **Why is the loop cycle time 2000 milliseconds?**  
   A blocking `delay(2000)` was inserted at the end of the loop.
3. **Why was a 2-second delay added?**  
   The DHT22 temperature/humidity sensor specification requires a minimum of 2 seconds between consecutive read commands.
4. **Why was the entire loop delayed instead of just the DHT22 read?**  
   The code was written synchronously rather than decoupling tasks with distinct sampling intervals.
5. **Root Cause:**  
   Monolithic blocking architecture instead of multi-rate cooperative task scheduling.

### Corrective Action
- Refactor loop into a timestamp-based cooperative scheduler using `millis()`.
- Sample MQ-135 gas levels at 100 ms intervals.
- Sample DHT22 climate data at 2500 ms intervals.
- Update LCD screen at 500 ms intervals.
