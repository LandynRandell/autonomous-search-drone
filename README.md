# Autonomous Search Drone (Independent Project)
A drone linked with a ground control station (GCS), built for search-and-rescue, by Landyn Randell, a senior at the Alabama School of Math and Science.

## Background
- This project extends GPS autonomy code originally built with a team during [Drone-First-Responder-Research-Fellows-USA](https://github.com/LandynRandell/Drone-First-Responder-Research-Fellows-USA), a mentored research project through the University of South Alabama. I'm now continuing the work independently.
- Very fascinated with rescue support through an engineering lens

## What this does
- Takes user-submitted perimeter values and sweeps the area in a lawnmower-like pattern
- Uses arrival-confirmed waypoint sequencing so the drone completes each leg before moving to the next

## Demo
Here's the sweep pattern running in SITL simulation:

![sweep demo](Search_and_rescue_drone_project.gif)

## Tools used
Python | pymavlink | ArduCopter

## Status
Active

## Team
Independent research, currently solo

## Goal
Build a physical model and attach object detection with a thermal camera to find heat signatures, aiding search-and-rescue operations

## Challenges
- Debugged a subtle sweep-pattern bug where waypoints were changing north and east/west position simultaneously, causing diagonal flight instead of a clean row-by-row sweep
- Fixed a self-terminating process issue in the dev environment where a cleanup script was matching and killing its own parent shell

## How to run it
Requires ArduPilot SITL installed in WSL2. Launch SITL and the mission script using the VS Code tasks in `.vscode/tasks.json`, then run the mission file to start the sweep.

---
Landyn Randell | [GitHub](https://github.com/LandynRandell)
