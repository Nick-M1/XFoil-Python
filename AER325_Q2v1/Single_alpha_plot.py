import os
import subprocess
import numpy as np
import matplotlib.pyplot as plt

os.chdir("C:/Users/nicho/OneDrive/Documents/XFoil")



## INPUTS:
# airfoil_names = ["NACA0012", "NACA1406", "NACA2412"]
airfoil_names = ["NACA0012", "NACA2412"]

alpha = 5

Re = 90_550
isViscous = True              # TODO: Change to true
n_panelnodes = 300




def getOutputFileNameDUMP(airfoil_name: str) -> str:
    return f"dump_file_{airfoil_name}.txt"

def getOutputFileNameCPWR(airfoil_name: str) -> str:
    return f"cpwr_file_{airfoil_name}.txt"


# --------------------------------------------------------------------------
# XFOIL input file writer

# """
for airfoil_name in airfoil_names:

    output_file_nameDUMP = getOutputFileNameDUMP(airfoil_name)
    output_file_nameCPWR = getOutputFileNameCPWR(airfoil_name)

    # print("\n\n\n", airfoil_name, output_file_name, "\n\n\n")         #TODO: ADD THIS TO A LOGGING FILE

    for output_file_name in (output_file_nameDUMP, output_file_nameCPWR):
        if os.path.exists(output_file_name):
            os.remove(output_file_name)

    with open("input_file.in", 'w') as input_file:
        # input_file.write("LOAD {0}.dat\n".format(airfoil_name))
        input_file.write(airfoil_name + '\n')

        input_file.write("PPAR\n")
        input_file.write("n\n")
        input_file.write(f"{n_panelnodes}\n\n\n")

        input_file.write("PANE\n")

        input_file.write("OPER\n")

        if isViscous:
            input_file.write("Visc {0}\n".format(Re))

        input_file.write(f"A {alpha}\n")
        input_file.write(f"DUMP {output_file_nameDUMP}\n")
        input_file.write(f"CPWR {output_file_nameCPWR}\n\n")

        input_file.write("\n\n")
        input_file.write("quit\n")


    # Running calculations in XFOIL
    subprocess.call("xfoil.exe < input_file.in", shell=True)

# """



# -------------------------------------------------------------------------------
## PLOTTING DATA

# Plotting CPWR  -  Cp vs x
plt.figure()
for airfoil_name in airfoil_names:
    polar_data = np.loadtxt(getOutputFileNameCPWR(airfoil_name), skiprows=3)
    plt.plot(polar_data[:, 0], polar_data[:, 1], label=airfoil_name)

plt.title("Plot geometry of aerofoil - Cp Vs x")
plt.xlabel("x")
plt.ylabel("Cp")
plt.grid()
plt.legend()
plt.show()


# Plotting DUMP  -  Cf vs x             # TODO: Lots more data in dump file to plot
for airfoil_name in airfoil_names:
    plt.figure()

    polar_data = np.loadtxt(getOutputFileNameDUMP(airfoil_name), skiprows=1)
    layer_boundary = np.argmax(polar_data[:, 2] < 0)                            # The 1st point that is for lower layer of airfoil

    plt.plot(polar_data[0:layer_boundary, 1], polar_data[0:layer_boundary, 6], label=f"upper-{airfoil_name}")       # Plot upper layer of airfoil
    plt.plot(polar_data[layer_boundary:, 1],  polar_data[layer_boundary:, 6],  label=f"lower-{airfoil_name}")       # Plot lower layer of airfoil


    plt.title("Cf Vs x")
    plt.xlabel("x")
    plt.ylabel("Cf")
    plt.grid()
    plt.legend()
    plt.show()

# """

