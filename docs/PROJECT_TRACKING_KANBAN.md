# Project Planning & Milestone Tracking

## Project Management Methodology: Agile / Kanban
The project workflow follows an iterative QA development cycle tracked across four continuous phases:
1. **Backlog:** Requirements definition, schematic capture, and initial prototype design.
2. **In Progress:** Feature branching, firmware development, and circuit breadboarding.
3. **QA Review & RCA:** Defect identification, 5-Why analysis, test plan execution.
4. **Done:** Branch integration, regression verification, and technical documentation.

---

## Sprint Task Board

| Task ID | Work Item Description | Owner | Priority | Target Milestone | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TSK-101** | Hardware BOM selection and pin mapping | Hardware Lead | High | Sprint 1 (Foundations) | Done |
| **TSK-102** | Initial prototype firmware (`v1.0.0`) | Firmware Eng | High | Sprint 1 (Foundations) | Done |
| **TSK-103** | Setup GitHub repository and issue templates | QA Lead | Medium | Sprint 1 (Foundations) | Done |
| **TSK-104** | Fix Issue QA-001 (Warmup stabilization timer) | Firmware Eng | High | Sprint 2 (Bug Fixes) | Done |
| **TSK-105** | Fix Issue QA-002 (I2C bus timeout & pull-ups) | Hardware/FW | Critical | Sprint 2 (Bug Fixes) | Done |
| **TSK-106** | Fix Issue QA-003 (Switch debounce filter) | Firmware Eng | Medium | Sprint 2 (Bug Fixes) | Done |
| **TSK-107** | Fix Issue QA-004 (Non-blocking cooperative FSM) | Firmware Eng | High | Sprint 2 (Bug Fixes) | Done |
| **TSK-108** | End-to-end test execution & validation log | QA Lead | High | Sprint 3 (Validation) | Done |
| **TSK-109** | Final project report and documentation | Project Manager| High | Sprint 3 (Validation) | Done |

---

## Release Milestones
- **Milestone v1.0.0 (Alpha Prototype):** Baseline hardware connections and basic sensor reading with synchronous loop.
- **Milestone v1.1.0 (QA & Reliability Release):** Remediation of bus locks, debounce errors, false startup alarms, and transition to non-blocking scheduling.
- **Milestone v1.2.0 (Final Academic Submission):** Completed verification protocol, academic report, and reproducible test matrices.
