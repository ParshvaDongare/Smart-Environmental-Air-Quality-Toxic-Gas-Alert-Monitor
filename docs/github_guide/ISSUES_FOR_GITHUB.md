# GitHub Issues: Copy-Paste Reference

Follow this guide to create the 5 QA issues in your GitHub repository.
Assign each issue to the Milestone **v1.0 Release** and add to your **Project Board**.

---

### Issue #1
- **Title:** `False alarm triggered on startup due to unheated MQ-135 sensor`
- **Labels:** `bug`, `hardware`
- **Milestone:** `v1.0 Release`
- **Description:**
```markdown
### Description
On cold boot, the MQ-135 analog output spikes above the critical 500 PPM threshold before the heating element reaches operating temperature, immediately sounding the buzzer and flashing the red LED in clean air.

### Expected Behavior
The system should have a warmup grace period (30 seconds) where acoustic alarms are inhibited until the sensor thermally stabilizes.

### Actual Behavior
Buzzer screams and red LED flashes for ~20-30 seconds immediately upon power-up.

### Steps to Reproduce
1. Disconnect power from the board for 2 minutes to cool the MQ-135.
2. Reconnect USB/DC power.
3. Observe immediate continuous buzzer triggering.

### Severity
High
```
- **Comment to post on Issue #1 (Root Cause Analysis):**
```markdown
### Root Cause Analysis (5-Why)
1. **Why did the alarm sound on power-up?** Because the MQ-135 analog reading exceeded 500 PPM.
2. **Why was the reading high in clean air?** The tin dioxide (SnO2) sensing element was cold and internal resistance had not stabilized.
3. **Why did the system evaluate uncalibrated readings?** The firmware immediately read analog pin A0 in setup/loop.
4. **Why was there no warmup check?** The sensor was treated as an instantaneous device without checking thermal burn-in.
5. **Root cause:** No startup stabilization grace period or non-blocking countdown state machine in firmware.

**Fix plan:** Implement a 30-second non-blocking warmup timer with live countdown on LCD and alarm muting.
```

---

### Issue #2
- **Title:** `Pin assignments and gas thresholds hard-coded as magic numbers`
- **Labels:** `enhancement`
- **Milestone:** `v1.0 Release`
- **Description:**
```markdown
### Description
Pin numbers (A0, 2, 4, 8, 9, 10), threshold values (500 PPM), and delay intervals are hard-coded directly as numeric literals throughout `Smart_Air_Quality_Monitor.ino`.

### Expected Behavior
All pin numbers, gas PPM safety thresholds, and timing parameters should be defined in a dedicated `Config.h` header using uppercase constant macros.

### Actual Behavior
Values are repeated across setup and loop, making calibration and maintenance error-prone.

### Steps to Reproduce
Open `src/Smart_Air_Quality_Monitor.ino` v1 and inspect lines with numeric pin and threshold parameters.

### Severity
Low
```
- **Comment to post on Issue #2 (Root Cause Analysis):**
```markdown
### Root Cause Analysis
**Cause:** The v1 prototype was written quickly to verify sensor readouts without establishing an embedded coding standard.
**Fix plan:** Extract all hardware pins, sensor calibration constants, and threshold constants into a separate `Config.h` header file.
```

---

### Issue #3
- **Title:** `I2C bus lockup and MCU freeze under electrical noise`
- **Labels:** `bug`, `hardware`
- **Milestone:** `v1.0 Release`
- **Description:**
```markdown
### Description
When the buzzer sounds simultaneously with LCD display updates, electrical noise causes the I2C bus to hang indefinitely on SDA, freezing microcontroller execution.

### Expected Behavior
The I2C driver should timeout after a set period and auto-recover the bus rather than hanging the system.

### Actual Behavior
The entire system stops responding; serial telemetry freezes and gas levels are no longer monitored until manual hardware reset.

### Steps to Reproduce
1. Trigger rapid LCD rewrites while activating the active piezo buzzer.
2. Observe microcontroller hang on `Wire` communication.

### Severity
Critical
```
- **Comment to post on Issue #3 (Root Cause Analysis):**
```markdown
### Root Cause Analysis (Ishikawa / 5-Why)
1. **Why did the system lock up?** The CPU was trapped in an infinite `while` loop waiting for I2C ACK.
2. **Why was ACK dropped?** Electrical noise and bus capacitance from jumper wires caused missing clock transitions.
3. **Why did noise corrupt the lines?** Missing external 4.7k pull-up resistors (relying on weak internal ~30k pull-ups).
4. **Why didn't the firmware recover?** Default Arduino `Wire.h` lacked bus timeout protection.
5. **Root cause:** Missing hardware pull-ups combined with unbounded blocking I2C transactions in firmware.

**Fix plan:** Add external 4.7k pull-ups and enable `Wire.setWireTimeout(3000, true)` for automatic peripheral recovery.
```

---

### Issue #4
- **Title:** `Mechanical switch contact bounce causing double-toggle on mute button`
- **Labels:** `bug`, `hardware`
- **Milestone:** `v1.0 Release`
- **Description:**
```markdown
### Description
Pressing the tactile pushbutton on pin D2 to silence an active alarm frequently causes the alarm to mute and immediately unmute due to switch contact bouncing.

### Expected Behavior
A single physical button press should toggle the alarm mute state exactly once.

### Actual Behavior
Button reads LOW 4 to 8 times within 15 milliseconds, causing erratic toggling.

### Steps to Reproduce
Press the mute button firmly while the alarm is sounding and observe erratic mute status on serial monitor.

### Severity
Medium
```
- **Comment to post on Issue #4 (Root Cause Analysis):**
```markdown
### Root Cause Analysis (5-Why)
1. **Why did the mute toggle multiple times?** The digital read evaluated the button as pressed multiple times in one press.
2. **Why were multiple LOW states detected?** Mechanical metal contacts vibrate and bounce upon closing.
3. **Why did firmware respond to each bounce?** Pin was read directly in the loop without a debouncing algorithm.
4. **Why was debounce omitted?** Prototype assumed ideal digital logic from a mechanical tactile switch.
5. **Root cause:** Absence of temporal software debouncing filter with state-change hysteresis.

**Fix plan:** Implement a non-blocking 50 ms debounce refractory timer with confirmed falling-edge detection.
```

---

### Issue #5
- **Title:** `Blocking delay() calls prevent multitasking and real-time gas alarm`
- **Labels:** `bug`, `enhancement`
- **Milestone:** `v1.0 Release`
- **Description:**
```markdown
### Description
The firmware uses `delay(2000)` to throttle DHT22 reads and LCD refreshes. During this 2-second block, the CPU cannot sample the MQ-135 sensor, process serial commands, or read the mute button.

### Expected Behavior
Gas sensor sampling should occur at 10 Hz (100 ms) continuously so hazardous gas surges trigger alarms within 150 ms.

### Actual Behavior
Worst-case alarm response latency is 2000-2500 ms, presenting a safety hazard.

### Steps to Reproduce
Expose the sensor to calibration gas during a delay cycle; note the 2-second lag before the buzzer sounds.

### Severity
High
```
- **Comment to post on Issue #5 (Root Cause Analysis):**
```markdown
### Root Cause Analysis (5-Why)
1. **Why is gas alert response sluggish?** The main loop is stalled inside `delay(2000)`.
2. **Why was delay(2000) added?** DHT22 sensor requires 2 seconds between consecutive read requests.
3. **Why was the entire loop delayed?** Code was written synchronously as a single sequential loop.
4. **Why wasn't non-blocking timing used?** The initial prototype prioritized quick verification over responsiveness.
5. **Root cause:** Monolithic blocking architecture without multi-rate cooperative task scheduling.

**Fix plan:** Refactor main loop into non-blocking cooperative scheduler using `millis()`, decoupling gas sampling (100ms), LCD refresh (500ms), and DHT22 sampling (2500ms).
```
