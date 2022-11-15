import os
import subprocess
import numpy as np
import matplotlib.pyplot as plt
from generate_lib import generateAirfoilNames

os.chdir("C:/Users/nicho/OneDrive/Documents/XFoil")

# DIR_CPWR = "Saved_cpwr_thickness1/"
# DIR_DUMP = "Saved_dump_thickness1/"

DIR_CPWR = "Saved_cpwr_maxchamber/"
DIR_DUMP = "Saved_dump_maxchamber/"


## INPUTS:
useAllAirfoils = False           # CHANGE

if useAllAirfoils:
    airfoil_names = generateAirfoilNames()
else:
    # airfoil_names = ['NACA1409', 'NACA1410', 'NACA1412', 'NACA1414', 'NACA1416', 'NACA1418', 'NACA1420', 'NACA1422', 'NACA1424', 'NACA1426']
    # airfoil_names = ["NACA0012"]

    airfoil_names = ["NACA1412", "NACA2412", "NACA3412", "NACA4412", "NACA5412", "NACA6412"]


cl = 0.576
chord = 0.136
Re = 90_550
isViscous = True              # TODO: Change to true
n_panelnodes = 300
n_iter = 300




def getOutputFileNameDUMP(airfoil_name: str) -> str:
    return f"{DIR_DUMP}dump_file_{airfoil_name}.txt"

def getOutputFileNameCPWR(airfoil_name: str) -> str:
    return f"{DIR_CPWR}cpwr_file_{airfoil_name}.txt"


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

        input_file.write("ITER {0}\n".format(n_iter))

        input_file.write(f"cl {cl}\n")
        input_file.write(f"DUMP {output_file_nameDUMP}\n")
        input_file.write(f"CPWR {output_file_nameCPWR}\n\n")

        input_file.write("\n\n")
        input_file.write("quit\n")


    # Running calculations in XFOIL
    subprocess.call("xfoil.exe < input_file.in", shell=True)

# """



# -------------------------------------------------------------------------------
## PLOTTING DATA


# Plotting y vs x (shape of aerofoil)
plt.figure()
for airfoil_name in airfoil_names:
    polar_data = np.loadtxt(getOutputFileNameCPWR(airfoil_name), skiprows=3)
    plt.plot(polar_data[:, 0], polar_data[:, 1], label=airfoil_name)

plt.title("Plot geometry of aerofoil - y Vs x")
plt.xlabel("x")
plt.ylabel("y")
plt.grid()
plt.legend()
plt.show()





# Plotting CPWR  -  Cp vs x/c     (LARGE NUMBER OF AEROFOILS)
plt.figure()
plt.gca().invert_yaxis()
plt.axhline(y=0, color='black', linestyle='-',)

for airfoil_name in airfoil_names:
    polar_data = np.loadtxt(getOutputFileNameCPWR(airfoil_name), skiprows=3)
    layer_boundary = np.argmax(polar_data[:, 1] < 0)                        # The 1st point that is for lower layer of airfoil

    plt.plot(polar_data[0:layer_boundary, 0]/chord, polar_data[0:layer_boundary, 2], label=airfoil_name)  # Plot upper layer of airfoil   # TODO: Is doing x/c correct?
    plt.plot(polar_data[layer_boundary:, 0]/chord, polar_data[layer_boundary:, 2], ':', color=plt.gca().lines[-1].get_color())

plt.title("Cp Vs x/c")
plt.xlabel("x/c")
plt.ylabel("Cp")
plt.grid()
plt.legend(loc='upper right', fontsize='x-small')
plt.show()



# """
# Plotting CPWR  -  Cp vs x     (SMALL NUMBER OF AEROFOILS)
plt.figure()
plt.gca().invert_yaxis()

for airfoil_name in airfoil_names:
    polar_data = np.loadtxt(getOutputFileNameCPWR(airfoil_name), skiprows=3)
    layer_boundary = np.argmax(polar_data[:, 1] < 0)                        # The 1st point that is for lower layer of airfoil

    plt.plot(polar_data[0:layer_boundary, 0]/chord, polar_data[0:layer_boundary, 2], label=f"upper-{airfoil_name}")  # Plot upper layer of airfoil   # TODO: Is doing x/c correct?
    plt.plot(polar_data[layer_boundary:, 0]/chord, polar_data[layer_boundary:, 2], ':', label=f"lower-{airfoil_name}")

plt.title("Cp Vs x/c")
plt.xlabel("x/c")
plt.ylabel("Cp")
plt.grid()
plt.legend()
plt.show()

# """


# --------------------------------------------------------------------------------------------------

# Plotting DUMP  -  Cf vs x      (LARGE NUMBER OF AEROFOILS)
plt.figure()
plt.axhline(y=0, color='black', linestyle='-', linewidth=0.5)

for airfoil_name in airfoil_names:
    polar_data = np.loadtxt(getOutputFileNameDUMP(airfoil_name), skiprows=1)
    layer_boundary = np.argmax(polar_data[:, 2] < 0)                        # The 1st point that is for lower layer of airfoil

    plt.plot(polar_data[0:layer_boundary, 1], polar_data[0:layer_boundary, 6], label=airfoil_name, linewidth=0.5)  # Plot upper layer of airfoil   # TODO: Is doing x/c correct?
    plt.plot(polar_data[layer_boundary:, 1], polar_data[layer_boundary:, 6], ':', color=plt.gca().lines[-1].get_color())

plt.xlim(0, 1)
plt.title("Cf Vs x")
plt.xlabel("x")
plt.ylabel("Cf")
plt.grid()
plt.legend(loc='upper right', fontsize='x-small')
plt.show()


# """
# Plotting DUMP  -  Cf vs x             # TODO: Lots more data in dump file to plot
for airfoil_name in airfoil_names:
    plt.figure()

    polar_data = np.loadtxt(getOutputFileNameDUMP(airfoil_name), skiprows=1)
    layer_boundary = np.argmax(polar_data[:, 2] < 0)                            # The 1st point that is for lower layer of airfoil

    plt.plot(polar_data[0:layer_boundary, 1], polar_data[0:layer_boundary, 6], label=f"upper-{airfoil_name}")       # Plot upper layer of airfoil
    plt.plot(polar_data[layer_boundary:, 1],  polar_data[layer_boundary:, 6],  label=f"lower-{airfoil_name}")       # Plot lower layer of airfoil

    plt.xlim(0, 1)
    plt.ylim(0, 0.1)
    plt.title(f"Cf Vs x - {airfoil_name}")
    plt.xlabel("x")
    plt.ylabel("Cf")
    plt.grid()
    plt.legend()
    plt.show()

# """

for airfoil_name in airfoil_names:
    with open(getOutputFileNameCPWR(airfoil_name)) as f:
        f.readline()                                    # Skip 1st line
        alpha = f.readline().split()[2]                 # From 2nd line, get alpha value for this cl
        print(f'{airfoil_name}  ->  Alpha = {alpha}')

# """

