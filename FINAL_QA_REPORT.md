# GitHub-Based QA Documentation and Problem Solving
### Case study: Smart Environmental Air Quality & Toxic Gas Alert Monitor using Arduino

**Name –** Parshva Dongare  
**PRN –** [Your PRN]  
**Class –** BTech E&TC (Div: C)  

---

## A. GitHub Repository Link

**Repository:** https://github.com/ParshvaDongare/Smart-Environmental-Air-Quality-Toxic-Gas-Alert-Monitor  
**Pull request:** https://github.com/ParshvaDongare/Smart-Environmental-Air-Quality-Toxic-Gas-Alert-Monitor/pull/6  
**Project board:** Air Quality Monitor QA Tracker (GitHub Projects)  

The repository was created with a README and an MIT licence, with Issues and Projects enabled.

*(Figure 1: Repository home page)*  
`[Insert Screenshot: Figure 1 - Repository home page showing files, README preview, and About section]`

---

## B. Brief Description of Code

The project monitors environmental hazardous gases (CO, Ammonia, Smoke, CO2) using an MQ-135 sensor and climate parameters (temperature and humidity) using a DHT22 sensor interfaced with an Arduino Uno. Telemetry is displayed on a 16x2 I2C LCD, and safety alerts are signaled via a piezo buzzer and status LEDs. 

It was developed in two versions so that real quality problems could be found, logged on GitHub, and fixed.

### Version 1 (initial commit)
A basic sketch using hard-coded pin and threshold values and blocking `delay()` calls, with no warmup delay, no switch debounce, no I2C bus recovery, and a default README.

```cpp
// Smart_Air_Quality_Monitor.ino (v1 excerpt)
void setup() {
  pinMode(2, INPUT_PULLUP);
  pinMode(8, OUTPUT);
  Wire.begin();
  lcd.init();
  dht.begin();
}

void loop() {
  int rawADC = analogRead(A0);
  float ppm = (rawADC * 5.0 / 1023.0) * 200.0;
  if (digitalRead(2) == LOW) { alarmMuted = !alarmMuted; }
  if (ppm > 500 && !alarmMuted) { digitalWrite(8, HIGH); }
  else { digitalWrite(8, LOW); }
  delay(2000); // Blocking delay halts execution
}
```

*(Figure 2: Smart_Air_Quality_Monitor.ino v1 committed to the main branch)*  
`[Insert Screenshot: Figure 2 - v1 code viewed on GitHub main branch]`

---

### Version 2 (after QA fixes)
Named constants in `Config.h` replace magic numbers, a non-blocking `millis()` scheduler replaces `delay()`, a 30-second sensor warmup countdown prevents false power-on alarms, a 50 ms software debounce stabilizes the alarm mute switch, I2C bus timeout protection prevents MCU hangs, and serial diagnostic messages (at 9600 baud) allow real-time telemetry verification. The README now includes complete component specifications, wiring diagrams, upload steps, and verification logs.

```cpp
// Smart_Air_Quality_Monitor.ino (v2 excerpt)
void loop() {
  unsigned long currentMillis = millis();

  // Task 1: Non-blocking button debounce (50ms refractory filter)
  int reading = digitalRead(PIN_BUTTON_MUTE);
  if (reading != lastButtonReading) { lastDebounceTimestamp = currentMillis; }
  if ((currentMillis - lastDebounceTimestamp) > BUTTON_DEBOUNCE_DELAY_MS) {
    if (reading != stableButtonState) {
      stableButtonState = reading;
      if (stableButtonState == LOW) { alarmMuted = !alarmMuted; }
    }
  }
  lastButtonReading = reading;

  // Task 2: High-frequency gas sampling (10 Hz / 100ms)
  if (currentMillis - lastGasSampleTimestamp >= INTERVAL_GAS_SAMPLE_MS) {
    lastGasSampleTimestamp = currentMillis;
    sampleGasAndActuateAlarm();
  }

  // Task 3: Display dashboard refresh (2 Hz / 500ms)
  if (currentMillis - lastLcdRefreshTimestamp >= INTERVAL_LCD_REFRESH_MS) {
    lastLcdRefreshTimestamp = currentMillis;
    refreshLcdDashboard();
  }
}
```

*(Figure 3: Smart_Air_Quality_Monitor.ino v2 on the fix/improve-code-and-docs branch)*  
`[Insert Screenshot: Figure 3 - v2 code viewed on fix branch showing non-blocking scheduling]`

*(Figure 4: Updated README with components, wiring, and test results)*  
`[Insert Screenshot: Figure 4 - Rendered GitHub README page showing hardware table and diagrams]`

---

### Circuit Connection Details

| From (Arduino Pin) | To (Peripheral Component) | Purpose |
| :--- | :--- | :--- |
| **Pin A0** | MQ-135 Analog Output (AOUT) | Analog gas concentration voltage signal |
| **Pin A4** | LCD I2C SDA (with 4.7kΩ pull-up to 5V) | Serial Data communication line |
| **Pin A5** | LCD I2C SCL (with 4.7kΩ pull-up to 5V) | Serial Clock synchronization line |
| **Pin D2** | Momentary Pushbutton to GND | Alarm mute and display toggle switch |
| **Pin D4** | DHT22 Data Pin (with 10kΩ pull-up) | Bi-directional single-bus climate data |
| **Pin D8** | Active Piezo Buzzer Positive Pin | Acoustic emergency hazard alarm |
| **Pin D9** | Red LED Anode (via 220Ω resistor) | Optical hazard indicator |
| **Pin D10**| Green LED Anode (via 220Ω resistor) | Optical safe/normal status indicator |
| **5V Rail**| VCC of MQ-135, DHT22, LCD, Buzzer | Regulated sensor & peripheral power |
| **GND** | Common Ground of all components | System common reference ground |

---

## C. QA Issues Logged

Five issues were logged using GitHub Issues. Each has a description, expected and actual behaviour, steps to reproduce, a severity, labels, and a root cause analysis comment.

| # | Issue Title | Type | Severity | Labels |
| :-: | :--- | :--- | :---: | :--- |
| **1** | False alarm triggered on startup due to unheated MQ-135 sensor | Hardware / Firmware | High | `bug`, `hardware` |
| **2** | Pin assignments and gas thresholds hard-coded (magic numbers) | Code quality | Low | `enhancement` |
| **3** | I2C bus lockup and MCU freeze under electrical noise | Interface / Bus | Critical | `bug`, `hardware` |
| **4** | Mechanical switch contact bounce causing double-toggle on mute | Hardware / HMI | Medium | `bug`, `hardware` |
| **5** | Blocking delay() calls prevent multitasking and real-time gas alarm | Design / Architecture| High | `bug`, `enhancement` |

---

### Custom Labels
Labels (`bug`, `hardware`, `enhancement`, `testing`, `documentation`) were used to categorise the issues.

*(Figure 5: Labels used to categorise issues)*  
`[Insert Screenshot: Figure 5 - GitHub repository Labels page showing custom color-coded labels]`

---

### Root Cause Analysis

**Issue #1 (5-Why):** The alarm triggers on power-up because the MQ-135 reading exceeds 500 PPM; the reading is high in clean air because the internal tin dioxide ($SnO_2$) heater has not reached thermal equilibrium (300°C); the firmware evaluated readings immediately in `setup()`; the code assumed sensor output was valid instantaneously; there was no hardware checklist in the template. **Root cause:** No startup stabilization grace period or non-blocking countdown state machine in firmware.

**Issue #3 (5-Why & Ishikawa):** The CPU locks up inside `Wire.h` because it waits indefinitely for an ACK pulse; the pulse was corrupted by electrical noise from the active buzzer and long breadboard jumpers; missing external 4.7kΩ pull-up resistors on SDA/SCL lines made the bus susceptible to noise; the default `Wire` library lacked timeout protection. **Root cause:** Missing hardware pull-ups combined with unbounded blocking I2C transactions in firmware.

**Issues #2, #4, #5:** A short cause and fix plan was recorded for each (no coding standard established initially, mechanical contact bounce on tactile switches not filtered, and synchronous procedural design blocking the main CPU loop).

*(Figure 6: Issue #1 with labels and 5-Why root cause comment)*  
`[Insert Screenshot: Figure 6 - Issue #1 page on GitHub showing title, description, labels, and 5-Why comment]`

*(Figure 7: Issue #2: hard-coded values, with cause and fix plan)*  
`[Insert Screenshot: Figure 7 - Issue #2 page on GitHub showing description and resolution plan]`

*(Figure 8: Issue #3 with 5-Why root cause comment)*  
`[Insert Screenshot: Figure 8 - Issue #3 page on GitHub showing I2C lockup analysis]`

*(Figure 9: Issue #4 with 5-Why root cause comment)*  
`[Insert Screenshot: Figure 9 - Issue #4 page on GitHub showing switch debounce analysis]`

*(Figure 10: Issue #5 with 5-Why root cause comment)*  
`[Insert Screenshot: Figure 10 - Issue #5 page on GitHub showing blocking delay analysis]`

---

### Resolution Log
After the pull request was merged, all five issues closed automatically through the `Fixes #n` references.

*(Figure 11: All five issues closed after the merge)*  
`[Insert Screenshot: Figure 11 - GitHub Issues page filtered by 'is:issue is:closed' showing all 5 issues closed]`

---

## D. Collaboration Summary

GitHub features used: Issues, Labels, Branches, Commits, Pull Requests with review comments, Milestones, and Projects.

### 1. Branching
The branch `fix/improve-code-and-docs` was created from `main` so that `main` stayed stable while the fixes were developed.

*(Figure 12: New branch created from main)*  
`[Insert Screenshot: Figure 12 - GitHub branch creation dropdown showing fix/improve-code-and-docs]`

*(Figure 13: Branches page showing main and the fix branch)*  
`[Insert Screenshot: Figure 13 - GitHub Branches page displaying active branches]`

---

### 2. Pull Request
Pull request #6, *"Fix QA issues: improve code, non-blocking scheduler, and documentation (v2)"*, contained the bugfix commits and referenced `Fixes #1 to #5`. GitHub linked each issue to the pull request automatically.

*(Figure 14: Pull request #6: description, linked issues and commits)*  
`[Insert Screenshot: Figure 14 - Pull Request #6 overview showing linked issues #1-#5 and commit list]`

---

### 3. Review and Discussion
This was an individual activity and no external reviewer was available, so a self-review was carried out. A line comment on `Smart_Air_Quality_Monitor.ino` confirmed that `millis()` replaces `delay()` so the loop is no longer blocked, the conversation was resolved, and a self-review and test summary was posted on the pull request.

*(Figure 15: Line comment on the code change in the pull request)*  
`[Insert Screenshot: Figure 15 - Files Changed tab showing inline review comment on millis() implementation]`

*(Figure 16: Self-review and test summary; no merge conflicts)*  
`[Insert Screenshot: Figure 16 - PR conversation page showing posted test summary and green merge button]`

---

### 4. Merge
Pull request #6 was merged into `main` using a merge commit.

*(Figure 17: Pull request merged and closed)*  
`[Insert Screenshot: Figure 17 - PR page showing purple 'Merged' badge and merge commit hash]`

After the merge, the fix branch was deleted and only `main` remained.

*(Figure 18: Branch deleted after the merge)*  
`[Insert Screenshot: Figure 18 - Notice showing fix/improve-code-and-docs branch deleted]`

*(Figure 19: Only the main branch remains)*  
`[Insert Screenshot: Figure 19 - Branches page showing default main branch]`

---

### 5. Commit History

| Commit Hash | Commit Message | Purpose |
| :--- | :--- | :--- |
| `6cde1ff` | `feat: initial prototype of air quality monitor and project docs` | Repository setup and v1 code |
| `a5b4edb` | `docs: add QA test plan, root cause analysis, and project tracking` | QA documentation and test matrices |
| `ce6f752` | `fix(firmware): resolve QA-001 false alarm during MQ-135 warmup cycle` | Fixes #1 (Sensor warmup timer) |
| `99b967b` | `fix(driver): configure I2C wire timeout and peripheral auto-recovery` | Fixes #3 (I2C bus lockup) |
| `abe5547` | `fix(input): implement 50ms software debounce for mute switch` | Fixes #4 (Button debounce) |
| `b84649f` | `refactor(core): replace blocking delays with cooperative non-blocking FSM`| Fixes #2, #5 (Config constants & FSM) |
| `a2934ee` | `Merge pull request #6 from fix/improve-code-and-docs` | Merge into main and auto-close issues |

*(Figure 20: Commit history on the main branch)*  
`[Insert Screenshot: Figure 20 - GitHub Commits tab on main branch showing complete commit trail]`

---

## E. Learning Outcome

- **GitHub Issues** give complete traceability from an observed defect, to its root cause, to the exact commit and line of code that resolved it.
- **Branches and pull requests** keep the main production branch stable and ensure all modifications are reviewable before integration.
- Writing **`Fixes #n`** in the pull request description closes issues automatically upon merge and establishes an audit-ready resolution log.
- The **5-Why method and Ishikawa diagrams** showed that defects frequently stem from missing process standards, unhandled physical sensor characteristics, and electrical noise rather than simple coding typos.
- In embedded systems projects, **hardware documentation** (such as external pull-up resistors, decoupling capacitors, and wiring tables) is just as critical as the software logic.
- **Milestones and Project Boards** make sprint progress transparent and visible to all project stakeholders.

### Pre-Reflection
Collaborative platforms like GitHub improve transparency and traceability by keeping every defect report, technical discussion, and code fix organized in a single centralized platform.

### Post-Reflection
GitHub transformed an ad-hoc debugging process into a structured engineering workflow. Linking commits directly to issue tickets made each solution verifiable, and the pull request workflow established a repeatable standard for code review and regression prevention.

---

## F. Report Upload

This report is exported as a PDF with embedded screenshots and uploaded to Moodle for the Project Management course.

---

## G. Project Planning and Tracking

### Plan and Status

| Task | Target Date | Status |
| :--- | :---: | :---: |
| Repository setup and v1 prototype code | Day 1 | Done |
| Log 5 QA issues with 5-Why root cause analysis | Day 1 | Done |
| Develop fixes on branch, update Config.h and README, open PR | Day 2 | Done |
| Perform code self-review, execute test cases, merge and close issues | Day 2 | Done |
| Configure Milestone, Project board, and finalize formal report | Day 2 | Done |

---

### Milestone: v1.0 Release
All 5 issues were assigned to the milestone **"v1.0 Release"**. It shows 100% complete with 0 open and 5 closed issues.

*(Figure 21: Milestone v1.0 Release at 100%)*  
`[Insert Screenshot: Figure 21 - GitHub Milestones tab showing v1.0 Release at 100% complete]`

---

### Project Board: Air Quality Monitor QA Tracker
A GitHub Projects board with **Todo**, **In Progress**, and **Done** columns tracks the project tasks. Issues #1 to #5 and Pull Request #6 are organized in the **Done** column.

*(Figure 22: Project board with all items in Done)*  
`[Insert Screenshot: Figure 22 - GitHub Project Kanban board showing all cards in the Done column]`

---

## Conclusion
Using GitHub for an embedded IoT project demonstrated how issue tracking, root cause analysis (5-Why and Fishbone), feature branching, pull requests, milestones, and project boards support rigorous quality assurance and engineering discipline. All five logged issues were systematically analyzed, remediated, verified, and closed with a complete trail of evidence.
