# About this project

![alt text](https://github.com/GCorreia3/Gravity-Simulation/blob/master/gravitysim2.png?raw=true)
![alt text](https://github.com/GCorreia3/Gravity-Simulation/blob/master/GraphingBinary.png?raw=true)

For my schools independent project, I chose to study how to simulate binary systems and how blackholes emit gravitational waves.
This project is an N-body gravity simulation using Newtons gravity and leapfrog integration.
The emission of gravitational waves is simulated by reducing the stored energy of orbiting bodies and thus the distance between the bodies decreases.
Thus the project explores the binary systems until they merge and I have created a real time graph from scratch to plot the separation over time.
I use a custom vector class instead of numpy to learn more about classes and how to write methods in classes.

Produces a result similar to the observed gravitational events from the LIGO.
For example, set the two masses to be 29 and 36 solar masses with a distance of 90km.
The official LIGO data shows that the time to merge should be 0.2s and the simulation gets around 0.22s ish which is roughly 10% off.

The error of the Simulation is second order with respect to the time step.

Completed Summer 2023
Did some error analysis in 2026
- Shows the simulation errors are second order with respect to time as the plot is a quadratic
- The errors are very low after 3 minuts with being around 0.02%

![alt text](https://github.com/GCorreia3/Gravity-Simulation/blob/master/percentage_error_vs_time_step.png?raw=true)

## Goals:

Completed: Create a gravitational attraction between two objects

Completed: add many objects and allow the ability to spawn objects

Completed: allow for spawned objects to have their velocity chosen by the mouse cursor and thus outline a predicted trajectory

Completed: Vector arrow class

Completed: Vector arrows for force and velocity

Completed: Spawn binary interface - allows you to modify values during runtime

Completed: Orbital decay due to gravitational waves
- make it look visually nice
- Find energy of object in binary system
- Use equation to reduce the power of the binary system due to gravitational waves
- Graph the distace/ other info over time for binary system
