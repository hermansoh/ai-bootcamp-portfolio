# Live Demo Script

## Opening

“MechaMentor helps students and junior engineers investigate faults systematically. It does not claim to inspect or diagnose equipment with certainty.”

## Demo 1 — Embedded system

- System: Embedded system / microcontroller
- Experience: Beginner
- Symptom: The board powers on, but firmware does not start and the debugger cannot connect.
- Observations: Power LED is on. Reset pin measures low. USB cable works elsewhere.
- Recent changes: Firmware target changed and an external sensor was rewired.
- Constraints: Low-voltage bench tests only.

Point out the safety section, ranked causes, expected observations, and escalation guidance.

## Demo 2 — Motor system

- System: Motor and drive system
- Experience: Intermediate
- Symptom: The motor starts but stops after two seconds under load.
- Observations: Driver fault LED turns on. Supply falls from 24 V to 20 V. Motor is warm.
- Recent changes: Mechanical load increased.
- Constraints: Do not exceed 2 A. Guard must remain installed.

Point out supply sag, overcurrent, thermal protection, load, and wiring hypotheses.
