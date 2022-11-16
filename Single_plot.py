import argparse
import time
from _utils import *

import yaml
import os
from subprocess import Popen
import numpy as np
import matplotlib.pyplot as plt



def restricted_float(x):
    try:
        x = float(x)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{x} not a floating-point literal")
    return x

def outputfile_to_NACA(output_file: str) -> str:
    return output_file[10: 18]


def main(args: argparse.Namespace):

    # Open + read YAML config file
    with open('config.yaml', "r") as ymlfile:
        cfg: dict = yaml.safe_load(ymlfile)

    # Set directory to the dir of XFOIL
    os.chdir(cfg['setup']['xfoil_path'])

    # Create separate output folders for DUMP & CPWR (if it doesn't already exist)
    for output_type in ('dump_dir', 'cpwr_dir'):
        if not os.path.isdir(cfg['setup'][output_type]):
            os.mkdir(cfg['setup'][output_type])

    # Create alias for _helper in getOutputFileName(), for DUMP & CPWR
    getOutputFileNameDUMP = getOutputFileName(OutputFiles.DUMP, cfg['setup']['dump_dir'])
    getOutputFileNameCPWR = getOutputFileName(OutputFiles.CPWR, cfg['setup']['cpwr_dir'])

    # Map each 'NACAxxxx' from args.aerofoil_names to a tuple with its name '.txt' path, for DUMP & CPWR
    if args.aerofoil_names:
        # If aerofoil_names given in arg, use these
        zipped_namesDUMP: list[tuple[str, str]] = [(name, getOutputFileNameDUMP(name)) for name in args.aerofoil_names]
        zipped_namesCPWR: list[tuple[str, str]] = [(name, getOutputFileNameCPWR(name)) for name in args.aerofoil_names]

    else:
        # If this arg is left empty, plot every aerofoil data in the DUMP & CPWR dirs
        files_list = os.listdir(cfg['setup']['dump_dir'])
        zipped_namesDUMP: list[tuple[str, str]] =\
            [(outputfile_to_NACA(filename), f"{cfg['setup']['dump_dir']}{filename}") for filename in files_list]

        files_list = os.listdir(cfg['setup']['cpwr_dir'])
        zipped_namesCPWR: list[tuple[str, str]] =\
            [(outputfile_to_NACA(filename), f"{cfg['setup']['cpwr_dir']}{filename}") for filename in files_list]



    # --------------------------------------------------------------------------
    # XFOIL PLOTTING

    # Plotting CPWR  -  Cp vs x/c
    plt.figure()
    plt.gca().invert_yaxis()
    plt.axhline(y=0, color='black', linestyle='-', )

    for naca_name, file_name in zipped_namesCPWR:
        polar_data = np.loadtxt(file_name, skiprows=3)

        # Find 1st point that is for lower layer of airfoil
        layer_boundary = np.argmax(polar_data[:, 1] < 0)

        # Plot upper surface of aerofoil (as solid line)
        plt.plot(polar_data[0:layer_boundary, 0] / cfg['single_variables']['chord'], polar_data[0:layer_boundary, 2],
                 label=naca_name)

        # Plot lower surface of aerofoil (as dashed line)
        plt.plot(polar_data[layer_boundary:, 0] / cfg['single_variables']['chord'], polar_data[layer_boundary:, 2], ':',
                 color=plt.gca().lines[-1].get_color())

    plt.title("Cp Vs x/c")
    plt.xlabel("x/c")
    plt.ylabel("Cp")
    plt.grid()
    plt.legend(loc='upper right', fontsize='x-small')
    plt.show()


    # --------------------------------------------------------------------------------------------------
    # Plotting DUMP  -  Cf vs x
    for naca_name, file_name in zipped_namesDUMP:
        plt.figure()
        polar_data = np.loadtxt(file_name, skiprows=1)

        # The 1st point that is for lower layer of airfoil
        layer_boundary = np.argmax(polar_data[:, 2] < 0)

        # Plot upper surface of aerofoil
        plt.plot(polar_data[0:layer_boundary, 1], polar_data[0:layer_boundary, 6], label=f"upper-{naca_name}")

        # Plot lower surface of aerofoil
        plt.plot(polar_data[layer_boundary:, 1], polar_data[layer_boundary:, 6], label=f"lower-{naca_name}")

        plt.xlim(0, 1)
        plt.ylim(0, 0.1)
        plt.title(f"Cf Vs x - {naca_name}")
        plt.xlabel("x")
        plt.ylabel("Cf")
        plt.grid()
        plt.legend()
        plt.show()






if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument("-i", "--input_path", help="Path of frames directory", default="PART_1-Vids/Temp-frames/Seg-files")
    # parser.add_argument("-n", "--new_plot", help="wipes the ", default="PART_1-Vids/Outputs/output_vid.mp4")

    parser.add_argument('-n', '--aerofoil_names', nargs='+', default=[],
                        help='NACA 4-digit aerofoils to test (in "NACAxxxx" form)')

    args = parser.parse_args()
    # print(args)
    main(args)
