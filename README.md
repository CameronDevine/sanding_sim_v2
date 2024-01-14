# Sanding Sim V2

![Sanding Sim V2 screenshot](down.png)

This repository contains a the source code for a sanding simulator used for human robot interaction experiments. The program was used as part of my Ph.D. research, specifically Chapter 7:

Cameron Devine. [_Material Removal Control for Teleoperated Robotic Sanding_](https://www.proquest.com/docview/2769193626). University of Washington, 2022.

This code uses [Panda3D](https://www.panda3d.org/) for rendering and [MR Sim](https://github.com/CameronDevine/mr_sim) for simulating the material removed via sanding.

### Installation

Before running the simulator, install the dependencies using

```bash
pip install -r requirements.txt
```

### Running

Before running the simulator, make sure that a Sony DualShock 4 or similar controller is connected, then run

```bash
python experiment.py
```