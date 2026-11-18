# Activity Report: GitHub-Based QA Documentation and Problem Solving

**Project Title:** Smart Environmental Air Quality & Toxic Gas Alert Monitor  
**Target Domain:** Embedded Systems & Cross-Domain IoT  
**Target Platform:** ATmega328P (Arduino Uno) & Sensor Suite  

---

## Pre-Reflection of Activity
Collaborative version control platforms like GitHub fundamentally elevate embedded and electronics engineering by transforming disparate hardware designs, schematics, and firmware source files into an auditable, transparent single source of truth. In cross-domain hardware-software projects, defects often arise at the boundary between physical components and software drivers (such as sensor warmups, bus noise, and mechanical switch bouncing). 

Utilizing structured issue trackers, issue templates, and commit-linked branch workflows enables cross-functional teams to isolate defects, track severity, link fixes directly to code changes via Pull Requests, and maintain full traceability from initial bug report to physical bench testing.

---

## Section A: GitHub Repository Link & Structure

- **Repository Link:** https://github.com/ParshvaDongare/Smart-Environmental-Air-Quality-Toxic-Gas-Alert-Monitor  
- **Local Workspace:** `D:\PM_PRJ`
- **Default Branch:** `main`
- **Active Release Tag:** `v1.1.0`

### Repository Tree
```text
D:\PM_PRJ\
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md             # Defect reporting template
│   │   └── qa_hardware_issue.md      # Hardware & electrical QA template
│   └── PULL_REQUEST_TEMPLATE.md      # Pull request review & verification template
├── docs/
│   ├── HARDWARE_SCHEMATIC_AND_BOM.md # Circuit schematic, pinouts, and bill of materials
│   ├── QA_TEST_PLAN.md               # QA test matrices and pass/fail criteria
│   ├── ROOT_CAUSE_ANALYSIS.md        # 5-Why and Fishbone RCA for all issues
│   └── PROJECT_TRACKING_KANBAN.md    # Agile sprint tasks and milestone tracking
├── src/
│   ├── Config.h                      # Pin definitions, calibration parameters, intervals
│   └── Smart_Air_Quality_Monitor.ino # Main non-blocking Arduino firmware
├── test/
│   └── test_cases.md                 # Verification test execution logs
├── README.md                         # Comprehensive project documentation
└── PROJECT_ACTIVITY_REPORT.md        # Formal academic submission report
```

---

## Section B: Brief Description of Code

The firmware (`src/Smart_Air_Quality_Monitor.ino` and `src/Config.h`) implements a **non-blocking cooperative task scheduler** to monitor environmental air quality and handle real-time emergency alerting.

### Core Modules and Functionality:
1. **Sensor Warmup State Machine (QA-001):** On power-up, an internal timer prevents false alarm triggers by enforcing a 30-second thermal stabilization period for the MQ-135 sensor heater, while presenting a real-time countdown on the 16x2 LCD.
2. **I2C Bus Lockup Protection (QA-002):** Configures `Wire.setWireTimeout(3000, true)` to detect bus clock-stretching hangs caused by electrical noise, resetting the peripheral automatically without locking up the MCU.
3. **Temporal Switch Debounce Filter (QA-003):** Implements a 50 ms non-blocking refractory window and edge-transition detector for the alarm mute switch, eliminating contact bounce errors.
4. **Cooperative Multi-Rate Task Scheduler (QA-004):** Replaces all blocking `delay()` functions with timestamp comparisons (`millis()`), decoupling tasks across rates:
   - Gas Sensor Sampling: **10 Hz (100 ms)** for rapid hazard detection.
   - LCD Screen Refresh: **2 Hz (500 ms)** for smooth user interface updates.
   - Climate Sampling: **0.4 Hz (2500 ms)** conforming to DHT22 timing limits.
   - Telemetry Output: **1 Hz (1000 ms)** for serial logging.

---

## Section C: QA Issues Logged & Root Cause Analysis

A total of four high-impact defects across hardware, interface, firmware, and architecture domains were identified, triaged, and resolved.

### Issue 1: QA-001 (High Severity)
- **Title:** False Threshold Alarm Triggered During MQ-135 Pre-Heat Cycle
- **Domain:** Sensor Physical Layer & Firmware Startup
- **Root Cause Method:** **5-Why Analysis**
  1. *Why did the alarm trigger immediately on power-on?* Analog reading exceeded 600 PPM in clean air.
  2. *Why did the sensor report elevated PPM?* The internal SnO2 element had not reached its 300°C operating temperature.
  3. *Why did firmware evaluate unheated sensor output?* The setup code immediately entered threshold comparison mode.
  4. *Why was no warmup grace period implemented?* Prototype treated MQ-135 as an instantaneous sensor.
  5. *Root Cause:* Absence of an initialization stabilization state machine to discard burn-in transients.
- **Resolution:** Implemented 30-second non-blocking warmup timer with visual LCD countdown and acoustic mute.

### Issue 2: QA-002 (Critical Severity)
- **Title:** I2C Bus Lockup (SDA Held Low) and System Freeze Under Noise
- **Domain:** Hardware Bus & Communication Protocol
- **Root Cause Method:** **Ishikawa (Fishbone) Diagram**
  - *Hardware:* Missing external 4.7 kΩ pull-up resistors on SDA/SCL lines (relied on weak internal pull-ups).
  - *Firmware:* Default Arduino Wire library lacked timeout, causing indefinite `while(!TWCR)` loop hang.
  - *Environment:* Inductive kickback from buzzer activation and unshielded breadboard wiring.
- **Resolution:** Added 4.7 kΩ external pull-ups and configured `Wire.setWireTimeout(3000, true)` for automatic peripheral recovery.

### Issue 3: QA-003 (Medium Severity)
- **Title:** Mechanical Contact Bounce Causing Double-Toggle on Alarm Silence Switch
- **Domain:** Hardware HMI & Input Signal Conditioning
- **Root Cause Method:** **5-Why Analysis**
  1. *Why did the alarm mute and unmute with one press?* Toggle variable switched state multiple times.
  2. *Why did it switch multiple times?* Pin read LOW 4 to 8 times within 15 milliseconds.
  3. *Why did multiple transitions occur?* Mechanical switch contacts physically bounced on closure.
  4. *Why did software register every bounce?* Polling code checked instantaneous pin level every cycle.
  5. *Root Cause:* Lack of a temporal debounce filter and edge-detection logic.
- **Resolution:** Added 50 ms software debounce window with confirmed falling-edge state detection.

### Issue 4: QA-004 (High Severity)
- **Title:** Blocking `delay(2000)` Calls Causing Sluggish Response to Sudden Gas Spikes
- **Domain:** Firmware Architecture & Real-Time Scheduling
- **Root Cause Method:** **5-Why Analysis**
  1. *Why did gas alerts take over 2 seconds to sound?* The loop execution was throttled to 0.5 Hz.
  2. *Why was the loop throttled?* A blocking `delay(2000)` was placed at the end of `loop()`.
  3. *Why was the delay inserted?* DHT22 requires a 2-second interval between consecutive read requests.
  4. *Why was the entire loop delayed instead of the sensor task?* Monolithic procedural programming style.
  5. *Root Cause:* Synchronous blocking execution rather than a multi-rate cooperative scheduler.
- **Resolution:** Refactored into a timestamp-based cooperative scheduler; gas reaction latency decreased from 2000 ms to <15 ms.

---

## Section D: Collaboration & Git Workflow Summary

The project enforced an industry-standard Git collaboration lifecycle:
1. **Repository Structure:** Established standard templates in `.github/ISSUE_TEMPLATE` and `.github/PULL_REQUEST_TEMPLATE.md`.
2. **Feature Branching:** Every QA issue was developed and verified in isolation on dedicated branches:
   - Branch `fix/qa-001-sensor-warmup` (PR #1)
   - Branch `fix/qa-002-i2c-timeout` (PR #2)
   - Branch `fix/qa-003-button-debounce` (PR #3)
   - Branch `fix/qa-004-nonblocking-fsm` (PR #4)
3. **Commit Traceability:** Merge commits explicitly referenced issue numbers (e.g., `Fixes #1`), ensuring end-to-end traceability from defect identification to merged code.

---

## Section E: Learning Outcomes
1. **Cross-Domain QA Mindset:** Learned that embedded system failures are rarely purely software bugs; addressing electrical noise, sensor physical behavior, and mechanical bouncing requires co-design between hardware mitigation and software safeguards.
2. **Defect Root Cause Analysis:** Gained practical mastery of 5-Why analysis and Ishikawa fishbone modeling to avoid applying superficial "band-aid" fixes.
3. **Collaborative Version Control:** Experienced how branching, pull requests, issue templates, and commit linking establish an indisputable audit trail for quality assurance and compliance.
4. **Real-Time Systems Architecture:** Mastered non-blocking task scheduling in microcontrollers, decoupling multi-rate sensor acquisitions to achieve low-latency hazard response.

---

## Section F: Project Planning and Tracking

The project followed an Agile Kanban tracking workflow (`docs/PROJECT_TRACKING_KANBAN.md`) organized across three delivery sprints:

| Sprint | Goal | Key Deliverables | Status |
| :--- | :--- | :--- | :--- |
| **Sprint 1: Architecture & Prototype** | Baseline prototype setup | Circuit BOM, initial firmware v1.0.0, Git repository setup | Complete |
| **Sprint 2: QA Triaging & Bug Fixes** | RCA and defect remediation | PR #1 (Warmup), PR #2 (I2C), PR #3 (Debounce), PR #4 (FSM) | Complete |
| **Sprint 3: Validation & Reporting** | System test execution | Test execution matrices, oscilloscope logs, formal report | Complete |

---

## Post-Reflection of Activity
Adopting GitHub as the collaborative project management tool streamlined the entire defect resolution lifecycle. Rather than relying on unstructured notes or ad-hoc debugging, the issue tracker provided a structured medium to articulate failure symptoms, document root cause investigations, and link code solutions directly to verification tests. 

This methodology significantly reduced regression risks and ensured that every hardware and firmware modification was deliberate, verifiable, and documented for peer review.
