# Test Case Execution and Verification Logs

**Target:** Smart Environmental Air Quality & Toxic Gas Alert Monitor  
**Firmware Branch:** `main` (after merging fixes)  
**Tester:** QA Lead / Firmware Verification Team  

---

### Test Case Log 1: Warmup Countdown and False Alarm Ingestion (QA-001)
- **Input:** Apply 5V power from cold start.
- **Observed Serial Output:**
  ```text
  [BOOT] Starting Air Quality Monitor v1.1.0...
  [WARMUP] Remaining: 30s | Sensor output: 780 PPM (Ignored)
  [WARMUP] Remaining: 20s | Sensor output: 620 PPM (Ignored)
  [WARMUP] Remaining: 10s | Sensor output: 410 PPM (Ignored)
  [WARMUP] Complete. Sensor state: READY. Monitoring active.
  ```
- **Observed LCD Display:** `Warming: 28s...` followed by normal monitoring dashboard.
- **Acoustic Check:** 0 beep events detected during initial 30 seconds.
- **Verdict:** PASS

---

### Test Case Log 2: I2C Noise Recovery (QA-002)
- **Input:** Momentarily ground the SDA line to simulate bus interference.
- **Observed Behavior:**
  - Microcontroller detected SDA lockup.
  - Wire timeout routine triggered at 3000 µs limit.
  - Bus peripheral reset succeeded; LCD refreshed next cycle without freezing.
- **Verdict:** PASS

---

### Test Case Log 3: Tactile Switch Debouncing (QA-003)
- **Input:** 50 consecutive button presses with rapid actuations.
- **Measurement:** Oscilloscope recorded mechanical contact bounce lasting between 6 ms and 18 ms.
- **Observed Behavior:** Each physical press registered exactly once in firmware. State toggle count matched physical presses 50/50.
- **Verdict:** PASS

---

### Test Case Log 4: Non-Blocking Scheduler Timing Verification (QA-004)
- **Input:** Continuous execution under simulated gas surge.
- **Timing Benchmarks:**
  - Average `loop()` execution duration: 1.14 ms.
  - Worst-case `loop()` execution duration: 4.80 ms (during LCD update).
  - Gas alert trigger latency after threshold breach: 12 ms (previously ~2000 ms).
- **Verdict:** PASS
