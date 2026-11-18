# Hardware Schematic and Bill of Materials (BOM)

## Project Title
**Smart Environmental Air Quality & Toxic Gas Alert Monitor**

## Hardware Architecture Overview
The system is built around the **ATmega328P (Arduino Uno / Nano)** microcontroller, interfaced with environmental sensors, human-machine interface (HMI) peripherals, and acoustic/visual alert systems.

```
+-------------------------------------------------------------+
|                      Arduino Uno (ATmega328P)               |
|                                                             |
|   [A0] <--- MQ-135 Gas Sensor (Analog Analog PPM Out)       |
|   [D2] <--- Pushbutton (Alarm Silence / Units Toggle)       |
|   [D4] <--- DHT22 (Temp & Relative Humidity One-Wire)       |
|   [D8] ---> Piezo Active Buzzer Driver                      |
|   [D9] ---> Alert Status LED (Red)                          |
|  [D10] ---> Normal Status LED (Green)                       |
|   [A4] <==> I2C SDA (16x2 LCD with PCF8574 Backpack)        |
|   [A5] <==> I2C SCL (16x2 LCD with PCF8574 Backpack)        |
|  [5V]  ---> Sensor & Display Power Rail                      |
|  [GND] ---> Common Ground Rail                              |
+-------------------------------------------------------------+
```

---

## Bill of Materials (BOM)

| Item # | Component Description | Quantity | Interface / Pin | Operating Voltage | Purpose / Function |
| :---: | :--- | :---: | :--- | :---: | :--- |
| 1 | Arduino Uno R3 (ATmega328P) | 1 | MCU Mainboard | 5V (USB / DC Jack) | Central processing & timing coordinator |
| 2 | MQ-135 Air Quality / Gas Sensor | 1 | Analog Pin A0 | 5V (~150mA heater) | Detects CO2, Ammonia, NOx, Alcohol, Benzene, Smoke |
| 3 | DHT22 (AM2302) Digital Sensor | 1 | Digital Pin D4 | 3.3V - 5V | Temperature (-40°C to 80°C) & Humidity (0-100% RH) |
| 4 | 16x2 LCD with I2C Backpack (PCF8574) | 1 | I2C (SDA=A4, SCL=A5) | 5V | Real-time parameter and diagnostic display |
| 5 | Active 5V Piezo Buzzer | 1 | Digital Pin D8 | 5V | Audible alarm when gas threshold is exceeded |
| 6 | 5mm Diffused LEDs (Red & Green) | 2 | Digital Pins D9, D10 | 5V (via 220Ω resistor)| Visual status indicators (Safe / Danger) |
| 7 | Momentary Tactile Pushbutton (12mm) | 1 | Digital Pin D2 | 5V (via pull-up) | Alarm silence and display unit toggle |
| 8 | Pull-Up Resistors (4.7 kΩ) | 2 | SDA / SCL to 5V | N/A | I2C bus signal integrity and rise-time stabilization |
| 9 | Current Limiting Resistors (220 Ω) | 2 | D9, D10 to LEDs | N/A | LED forward current protection |
| 10 | Decoupling Capacitors (100nF + 10µF) | 2 | 5V to GND power rail | 5V - 16V | Suppress inductive switching spikes & voltage ripple |
| 11 | Solderless Breadboard & Jumpers | 1 set | Power & Bus rails | N/A | Prototype interconnection |

---

## Pin Connection Matrix

| Arduino Pin | Peripheral Connected | Type | Notes |
| :--- | :--- | :--- | :--- |
| **A0** | MQ-135 (AOUT) | Analog Input | Voltage proportional to gas concentration |
| **A4** | LCD I2C SDA | I2C Data | Hardware I2C data line (requires 4.7kΩ pull-up) |
| **A5** | LCD I2C SCL | I2C Clock | Hardware I2C clock line (requires 4.7kΩ pull-up) |
| **D2** | Alarm Silence Button | Digital Input (Pull-up) | Trigger for alarm mute and display mode switch |
| **D4** | DHT22 Data Pin | Bi-directional Digital | Single-bus timing protocol with 10kΩ pull-up |
| **D8** | Active Buzzer | Digital Output | High = Alarm Tone, Low = Mute |
| **D9** | Red LED (Hazard) | Digital Output | Flashes when PPM > Threshold or sensor fault |
| **D10** | Green LED (Normal) | Digital Output | Solid when environmental parameters are safe |
| **5V** | System VCC | Power Output | Sensor heating elements and logic power |
| **GND** | System GND | Ground | Common reference ground |

---

## Electrical Characteristics & Operating Safety Limits
- **Supply Voltage:** 5.0V ± 0.25V DC
- **Total Peak Current Consumption:** ~280mA (MQ-135 Heater: 150mA, LCD Backlight: 25mA, Buzzer: 30mA, Arduino MCU: 45mA, LEDs: 30mA).
- **Recommended Power Source:** Dedicated 5V 1A external DC adapter (to prevent USB port brownout resets during heater startup).
