import numpy as np
import matplotlib.pyplot as plt

dt = [0.4, 0.2, 0.1, 0.05, 0.025, 0.0125, 0.00625]
# energy error taken from main.py file after 3 minutes of sim time
energy_error = [0.028302646351876317, 0.024618196366020126, 0.02366087621323822, 0.023404138790676366, 0.02334194308382575, 0.02332734344297205, 0.02332146871721488]


model = np.poly1d(np.polyfit(dt, energy_error, 2))
polyline = np.linspace(0, 0.4, 100)
plt.scatter(dt, energy_error)
plt.xlabel("Time Step (s)")
plt.ylabel("Percentage error")
plt.title("Percentage energy error vs time step")
plt.plot(polyline, model(polyline), color="red")
plt.savefig("percentage_error_vs_time_step.png")
plt.show()

print(model)
