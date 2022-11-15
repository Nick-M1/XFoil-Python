
from scipy.interpolate import make_interp_spline, BSpline

import os
import numpy as np
import matplotlib.pyplot as plt


# PLOT_TYPE = 'thickness1b'
# PLOT_TYPE = 'thickness2'
PLOT_TYPE = 'maxchamber'

CL_REQUIRED = 0.576



os.chdir(f"C:/Users/nicho/OneDrive/Documents/XFoil/Saved_polarfiles_{PLOT_TYPE}")
files_list = os.listdir()


def getNACA(file_name: str) -> str:
    return file_name[11:19]


def smooth_plot(x_original: np.ndarray, y_original: np.ndarray) -> (np.ndarray, np.ndarray):
    x_new = np.linspace(x_original[0], x_original[-1], 30)
    y_new = make_interp_spline(x_original, y_original, k=7)(x_new)
    return x_new, y_new


## PLOTTING DATA

# Plotting CL Vs alpha
plt.figure()
plt.axhline(y=CL_REQUIRED, color='tab:pink', linestyle='-.', label='Min cl Required')

plt.axhline(y=0, color='black', linewidth=0.5)
plt.axvline(x=0, color='black', linewidth=0.5)

for file_name in files_list:
    polar_data = np.loadtxt(file_name, skiprows=12)
    x_arr = polar_data[:, 0]
    y_arr = polar_data[:, 1]

    plt.plot(*smooth_plot(x_arr, y_arr), label=getNACA(file_name))

    # Display cl-max
    print(f'CL-max for "{getNACA(file_name)}"  => {np.max(y_arr)}')


plt.title("cl Vs Angle of attack - for different Aerofoils")
plt.xlabel("Angle of attack (deg)")
plt.ylabel("cl")
plt.grid()
plt.legend(loc='lower right', fontsize='x-small')
plt.show()


# Plotting CD Vs alpha
plt.figure()
plt.axhline(y=0, color='black', linewidth=0.5)
plt.axvline(x=0, color='black', linewidth=0.5)

for file_name in files_list:
    polar_data = np.loadtxt(file_name, skiprows=12)
    x_arr = polar_data[:, 0]
    y_arr = polar_data[:, 2]

    plt.plot(*smooth_plot(x_arr, y_arr), label=getNACA(file_name))


plt.title("cd Vs Angle of attack - for different Aerofoils")
plt.xlabel("Angle of attack (deg)")
plt.ylabel("cd")
plt.grid()
plt.legend(loc='lower right', fontsize='x-small')
plt.show()




# Plotting CL Vs CD
plt.figure(3)
plt.axhline(y=0, color='black', linewidth=0.5)
plt.axvline(x=0, color='black', linewidth=0.5)

for file_name in files_list:
    polar_data = np.loadtxt(file_name, skiprows=12)

    plt.plot(polar_data[:, 2], polar_data[:, 1], label=getNACA(file_name))


plt.axhline(y=CL_REQUIRED, color='tab:pink', linestyle='-.', label='Min cl Required')
plt.title("cl Vs cd - for different Aerofoils")
plt.xlabel("cd")
plt.ylabel("cl")
plt.grid()
plt.legend(loc='lower right', fontsize='x-small')
plt.show()