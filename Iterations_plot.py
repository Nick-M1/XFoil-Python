import argparse
import time

import yaml
import os
from subprocess import Popen
import numpy as np
import matplotlib.pyplot as plt




def getOutputFileName(airfoil_name: str) -> str:
    return f"polar_file_{airfoil_name}.txt"


def main(args: argparse.Namespace):

    # Open + read YAML config file
    with open('config.yaml', "r") as ymlfile:
        cfg: dict = yaml.safe_load(ymlfile)

    # Set directory to the dir of XFOIL
    os.chdir(cfg['setup']['xfoil_path'])


    # --------------------------------------------------------------------------
    # XFOIL input file writer

    for airfoil_name in args.aerofoil_names:

        output_file_name = getOutputFileName(airfoil_name)

        if args.delete_old and os.path.exists(output_file_name):
            os.remove(output_file_name)

        with open("input_file.in", 'w') as input_file:
            input_file.write(airfoil_name + '\n')

            input_file.write("PPAR\n")
            input_file.write(f"n {cfg['setup']['n_panelnodes']}\n\n\n")

            input_file.write("PANE\n")
            input_file.write("OPER\n")

            if cfg['variables']['Re'] >= 0:
                input_file.write(f"Visc {cfg['variables']['Re']}\n")

            input_file.write("PACC\n")
            input_file.write(f"{output_file_name}\n\n")

            if not args.delete_old:
                input_file.write("y\n\n")

            input_file.write(f"ITER {cfg['setup']['n_iter']}\n")
            input_file.write(f"ASeq {cfg['iterations']['alpha_i']} {cfg['iterations']['alpha_f']} {cfg['iterations']['alpha_step']}\n")

            input_file.write("\n\n")
            input_file.write("quit\n")


        # Running calculations in XFOIL
        Popen("xfoil.exe < input_file.in", shell=True)
        time.sleep(1.5)






if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument("-i", "--input_path", help="Path of frames directory", default="PART_1-Vids/Temp-frames/Seg-files")
    # parser.add_argument("-n", "--new_plot", help="wipes the ", default="PART_1-Vids/Outputs/output_vid.mp4")

    parser.add_argument('-o', '--delete_old', action='store_false', default=True,
                        help='If NOT FLAGGED (true), deletes any previously stored data for inputted aerofoils, else if FLAGGED (false), appends new data to this reviously stored data')

    parser.add_argument('-n', '--aerofoil_names', nargs='+', default=['NACA0012', 'NACA0013', 'NACA0014'],
                        help='NACA 4-digit aerofoils to test (in "NACAxxxx" form)')

    args = parser.parse_args()
    main(args)

    # print(args)


"""



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