import os
from subprocess import Popen
import numpy as np
import matplotlib.pyplot as plt
from generate_lib import *

os.chdir("C:/Users/nicho/OneDrive/Documents/XFoil")


## INPUTS:
useAllAirfoils = False           # CHANGE

if useAllAirfoils:
    airfoil_names = generateAirfoil_thickness()
else:
    # airfoil_names = ["NACA0012", "NACA1406", "NACA2412"]
    airfoil_names = ['NACA1409', 'NACA2409', 'NACA3409', 'NACA4409', 'NACA5409', 'NACA6409', 'NACA7409', 'NACA8409', 'NACA9409']


NEW_PLOT = True

alpha_i = -2
alpha_f = 20
alpha_step = 0.1           # TODO: Change to 0.25

cl_required = 0.576

Re = 90_550
viscous = False              # TODO: Change to true
n_panelnodes = 400
n_iter = 400


def getOutputFileName(airfoil_name: str) -> str:
    return f"polar_file_{airfoil_name}.txt"

# --------------------------------------------------------------------------
# XFOIL input file writer

# """



for airfoil_name in airfoil_names:

    output_file_name = getOutputFileName(airfoil_name)

    # print("\n\n\n", airfoil_name, output_file_name, "\n\n\n")

    if NEW_PLOT and os.path.exists(output_file_name):
        os.remove(output_file_name)


    with open("input_file.in", 'w') as input_file:
        input_file.write(airfoil_name + '\n')

        input_file.write("PPAR\n")
        input_file.write(f"n {n_panelnodes}\n\n\n")

        input_file.write("PANE\n")

        input_file.write("OPER\n")

        if viscous:
            input_file.write("Visc {0}\n".format(Re))

        input_file.write("PACC\n")
        input_file.write(f"{output_file_name}\n\n")

        if not NEW_PLOT:
            input_file.write("y\n\n")

        input_file.write("ITER {0}\n".format(n_iter))
        input_file.write("ASeq {0} {1} {2}\n".format(alpha_i, alpha_f, alpha_step))

        input_file.write("\n\n")
        input_file.write("quit\n")


    # Running calculations in XFOIL
    Popen("xfoil.exe < input_file.in", shell=True)

# """



# -------------------------------------------------------------------------------
## PLOTTING DATA

# Plotting CL Vs alpha
plt.figure()
for airfoil_name in airfoil_names:
    polar_data = np.loadtxt(getOutputFileName(airfoil_name), skiprows=12)
    plt.plot(polar_data[:, 0], polar_data[:, 1], label=airfoil_name)

plt.axhline(y=cl_required, color='tab:pink', linestyle='-.', label='Min CL Required')
plt.title("CL Vs Angle of attack")
plt.xlabel("Angle of attack (deg)")
plt.ylabel("CL")
plt.grid()
plt.legend()
plt.show()


# Plotting CD Vs alpha
plt.figure()
for airfoil_name in airfoil_names:
    polar_data = np.loadtxt(getOutputFileName(airfoil_name), skiprows=12)
    plt.plot(polar_data[:, 0], polar_data[:, 2], label=airfoil_name)

plt.title("CD Vs Angle of attack")
plt.xlabel("Angle of attack (deg)")
plt.ylabel("CD")
plt.grid()
plt.legend()
plt.show()


# Plotting CL Vs CD
plt.figure(3)
for airfoil_name in airfoil_names:
    polar_data = np.loadtxt(getOutputFileName(airfoil_name), skiprows=12)
    plt.plot(polar_data[:, 2], polar_data[:, 1], label=airfoil_name)

plt.axhline(y=cl_required, color='tab:pink', linestyle='-.', label='Min CL Required')
plt.title("CL Vs CD")
plt.xlabel("CD")
plt.ylabel("CL")
plt.grid()
plt.legend()
plt.show()

# """