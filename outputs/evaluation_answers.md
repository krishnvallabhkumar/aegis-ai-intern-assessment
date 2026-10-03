# Aegis Evaluation Questions — Evidence-backed Answers

## 1. What must be true before starting the Hydraulic Power Unit?
Before starting the HPU, verify hydraulic fluid is within the normal sight-glass band, IV-21 is OPEN, the emergency-stop circuit is RESET, and the maintenance access panel is installed/closed. Then POWER ON, press START, and verify the applicable pressure setpoint.

**Evidence:** F01, F02, F03, F04

## 2. What is the current normal operating pressure for the HPU, and under what conditions does that apply?
For software revision 3.2 and later, normal HPU discharge pressure is 200 bar. Before revision 3.2 it was 180 bar with PS-04.

**Evidence:** F05, F07

## 3. What does alarm A17 indicate, and what are its possible causes?
A17 is Hydraulic Pressure Low; possible causes are IV-21 closed/partially closed, low hydraulic fluid, or invalid pressure-sensor signal.

**Evidence:** F10, F11

## 4. Is PS-04 the same component as PS-04A?
No. PS-04 and PS-04A are different sensor revisions; PS-04 is superseded by PS-04A effective software revision 3.2.

**Evidence:** F08

## 5. Which document introduced the change from PS-04 to PS-04A?
ECN-1042 introduced the PS-04 → PS-04A change.

**Evidence:** F08, F09

## 6. Which components connect directly to the HCS controller, according to the hydraulic schematic?
PS-04A and IV-21 have the direct purple control/signal connections to PLC-03 shown in the hydraulic schematic.

**Evidence:** F06

## 7. What action is required if alarm A17 persists for more than 10 seconds?
If A17 persists for more than 10 seconds, execute Shutdown Procedure 4.7: close IV-21, confirm pressure decay, POWER OFF, tag out per LOTO, then troubleshoot.

**Evidence:** F12, F13

## 8. Under what circumstances must the controller not be reset?
Do not reset PLC-03 while hydraulic pressure is above 50 bar; reset is permitted only below 50 bar.

**Evidence:** F14

## 9. What was the operating pressure threshold before software revision 3.2, and what changed it?
Before software revision 3.2 the normal pressure was 180 bar. ECN-1042 changed it to 200 bar alongside the PS-04 → PS-04A replacement.

**Evidence:** F07, F09

## 10. Which alarm is associated with a pressure sensor reading below 150 bar?
A17 (Hydraulic Pressure Low), for pressure below 150 bar.

**Evidence:** F10, F16

## 11. According to the component register, what is the location of the isolation valve IV-21?
IV-21 is located in the Hydraulic Module.

**Evidence:** F20

## 12. Does the training slide deck introduce any component or alarm not found in the manuals?
Yes. The training excerpt introduces an Auxiliary Reservoir as a Line 4/5-specific configuration detail not covered in the standard Operator Manual; it does not introduce a new alarm.

**Evidence:** F23, F24

## 13. What sensor ID appears on the diagnostics screenshot, and does it match a known component?
The diagnostics screenshot shows P.S.04-A, which is a printed-label variant of known component PS-04A.

**Evidence:** F22

## 14. Per the revision history, when did software revision 3.2 take effect, and what changed alongside it?
Software revision 3.2 took effect on 2025-09-30; it replaced PS-04 with PS-04A and changed normal pressure from 180 to 200 bar.

**Evidence:** F18, F19

## 15. What does sensor_ps04a_threshold_bar in the configuration export correspond to in the operator manual's terminology?
sensor_ps04a_threshold_bar = 200 maps to the 200-bar normal HPU discharge pressure/setpoint for software revision 3.2 and later.

**Evidence:** F15, F25

## 16. Does the 200 bar threshold apply to all Aegis HCS units, or only some?
The 200-bar threshold applies to software revision 3.2 and later, not to all revisions; earlier revisions use 180 bar.

**Evidence:** F05, F07, F08

## 17. Is PS-04 the same as PS-40?
No. PS-40 is a different pressure sensor in the coolant loop on Skid B and is unrelated to the HPU discharge circuit.

**Evidence:** F21

## 18. What was the pressure limit before revision 3.2?
180 bar.

**Evidence:** F07

## 19. What is the maximum continuous operating temperature of PS-04A?
Not determinable from the supplied package; no maximum continuous operating temperature for PS-04A is specified.

**Evidence:** F27

## 20. What is the calibration interval for the electrical system diagram's voltage sensor?
Not determinable from the supplied package; no voltage-sensor calibration interval is specified.

**Evidence:** F26

## 21. Who approved engineering bulletin ECN-1058?
Not determinable from the supplied package; ECN-1058 is marked Released but names no approver.

**Evidence:** F28

## 22. What is the mean time between failures for the isolation valve IV-21?
Not determinable from the supplied package; no MTBF for IV-21 is provided.

**Evidence:** F29

## 23. Is the Aegis Series-7 HCS compatible with a 3-phase 400V supply?
The package does not establish compatibility with 3-phase 400V. It documents a 480V incoming disconnect and gives no 400V compatibility statement.

**Evidence:** F30, F31
