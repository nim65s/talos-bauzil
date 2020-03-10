# Package Talos-bauzil

This package is a project to simulate Talos in the Bauzil room of LAAS-CNRS, Toulouse, France.

## What's needed ?

This package needs:
 * `robotpkg-talos-data`: to install, see [this guide](http://robotpkg.openrobots.org/debian.html)
 * `ROS`
 * `Gazebo` with a modern build:
   * For Ubuntu 16.04: `Gazebo` version 7.14.0 or newer
   * For Ubuntu 18.04: `Gazebo` version 9.4.0 or newer
 * `Python 2.7` (not tested with `Python 3`)
---
## How to use

> If you do not want to use the GPU acceleration, replace `gpu="true"` by `gpu="false"` in the line 155 of `urdf/head/head_ouster.urdf.xacro`.  
> N.B.: This modification may degrade the simulation.

### For Ubuntu 16.04

This package is not usable on Ubuntu 16.04 yet.

### For Ubuntu 18.04

You can start the simulation with
```bash
python <path_to_package>script/start_talos_gazebo.py
```

### Examples

Below is an example of the data obtained with the simulator.
![example of simulation data](./example/example.png)