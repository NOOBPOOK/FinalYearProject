# 🧠 Brain-Controlled Wheelchair

[![Python](https://img.shields.io/badge/Python-%2314354C.svg?style=for-the-badge\&logo=python\&logoColor=white)](https://www.python.org/)
[![Arduino](https://img.shields.io/badge/Arduino-%230097C1.svg?style=for-the-badge\&logo=arduino\&logoColor=white)](https://www.arduino.cc/)
[![EEG](https://img.shields.io/badge/EEG-%230077B5.svg?style=for-the-badge)]()
[![EOG](https://img.shields.io/badge/EOG-%2300A86B.svg?style=for-the-badge)]()
[![Bio Amp EXG Pill](https://img.shields.io/badge/Bio%20Amp-EXG%20Pill-%23736CED.svg?style=for-the-badge)](https://www.upsidedownlabs.tech/product-page/bio-amp-exg-pill)
[![IR Sensors](https://img.shields.io/badge/IR%20Obstacle%20Detection-%23C2185B.svg?style=for-the-badge)]()
[![FFT](https://img.shields.io/badge/Signal%20Processing-FFT-%23FFA500.svg?style=for-the-badge)]()
[![Circuit Design](https://img.shields.io/badge/Custom%20EEG%2FEOG%20Circuit-%239C27B0.svg?style=for-the-badge)]()

---

## 🚀 Project Overview

This project focuses on a **non-invasive, real-time brain-controlled wheelchair** that uses **EEG (brain)** and **EOG (eye movement)** signals. These bio-signals are processed through a **custom hardware circuit** and analyzed in real time using **FFT (Fast Fourier Transform)** to determine user intent such as moving forward or turning.

Additionally, **IR sensors** are integrated into the system to detect nearby obstacles, enhancing the safety of the user while navigating.

This system is ideal for patients with severe physical disabilities, allowing them to operate a wheelchair hands-free using just their mental focus and eye movements.

---

## ✨ Key Features

* 🧠 **Brain Signal Control (EEG):** Detects focus or blink via forehead electrodes.
* 👁️ **Eye Movement Detection (EOG):** Identifies left/right movement from muscle signals.
* ⚡ **Real-Time Signal Processing:** Uses FFT for analyzing frequency bands and thresholding logic.
* 🛑 **Obstacle Avoidance with IR Sensors:** Automatically stops if an object is detected in path.
* 🧰 **Custom Circuit Design:** Op-amp based amplifiers, filters (bandpass, notch), and protection circuits.
* 🛴 **Motorized Wheelchair Navigation:** Microcontroller sends movement commands based on detected intent.
* 🔄 **Live Feedback Loop:** Instant reaction based on serial input data from EEG/EOG signals.

---

## 🛠️ Tech Stack

### 🧠 Bio-Signal Acquisition

- [![Bio Amp EXG Pill](https://img.shields.io/badge/Bio%20Amp-EXG%20Pill-%23736CED.svg?style=for-the-badge)](https://www.upsidedownlabs.tech/product-page/bio-amp-exg-pill) Used for acquiring clean, low-noise EEG and EOG signals.
- **Electrodes:** Connected to Bio Amp EXG.
- **Amplification & Filtering:** Onboard instrumentation amplifiers with safety features.

### ⚙️ Processing & Control

* [![Arduino](https://img.shields.io/badge/Arduino-Uno-%230097C1.svg?style=for-the-badge\&logo=arduino)](https://www.arduino.cc/)
* [![Python](https://img.shields.io/badge/Python-Serial%20Comm-%2314354C.svg?style=for-the-badge\&logo=python)](https://python.org)
* **FFT (NumPy):** Signal transformation and analysis.
* **Threshold Logic:** Decision-making based on frequency band energy.
* **Motor Control:** L298N driver + DC motors.

### 🧱 Obstacle Detection

* [![IR](https://img.shields.io/badge/IR%20Sensor-IR%20Pair-%23C2185B.svg?style=for-the-badge)]() - Reflective IR sensors to detect obstacles in front.

---

## 📊 Signal Interpretation

| Signal Type | Trigger          | Frequency Range (Hz) | Action              |
| ----------- | ---------------- | -------------------- | ------------------- |
| EEG         | Blink/Focus      | \~10–13 Hz (Alpha)   | Move Forward / Stop |
| EOG         | Eye Left Motion  | Voltage spike        | Turn Left           |
| EOG         | Eye Right Motion | Voltage spike        | Turn Right          |
| IR Sensor   | Obstacle < 15cm  | Logic LOW            | Stop Wheelchair     |

---

## 🧪 Testing Results

| Scenario            | Expected Action | Actual Result |
| ------------------- | --------------- | ------------- |
| SLow Blink          | Stop            | ✅ Accurate    |
| Steady focus        | Move Forward    | ✅ Accurate    |
| Eye look left/right | Turn L/R        | ✅ Smooth      |
| Obstacle in path    | Auto-stop       | ✅ Reliable    |

---

## 🤝 Contributing

Have suggestions or want to collaborate?

📫 **Contact Me:**

* [LinkedIn – Vedant Shetye](https://www.linkedin.com/in/vedant-shetye-579016262/)
* [GitHub](https://[githu(https://github.com/NOOBPOOK))
