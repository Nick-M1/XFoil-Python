import argparse
import time
from _utils import *

import yaml
import os
from subprocess import Popen


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

    # Create alias for _helper in getOutputFileName() for DUMP & CPWR
    getOutputFileNameDUMP = getOutputFileName(OutputFiles.DUMP, cfg['setup']['dump_dir'])
    getOutputFileNameCPWR = getOutputFileName(OutputFiles.CPWR, cfg['setup']['cpwr_dir'])


    # --------------------------------------------------------------------------
    # XFOIL input file writer

    for airfoil_name in args.aerofoil_names:

        output_file_nameDUMP = getOutputFileNameDUMP(airfoil_name)
        output_file_nameCPWR = getOutputFileNameCPWR(airfoil_name)

        for output_file_name in (output_file_nameDUMP, output_file_nameCPWR):
            if os.path.exists(output_file_name):
                os.remove(output_file_name)

        with open("input_file.in", 'w') as input_file:
            input_file.write(airfoil_name + '\n')

            input_file.write("PPAR\n")
            input_file.write(f"n {cfg['setup']['n_panelnodes']}\n\n\n")

            input_file.write("PANE\n")
            input_file.write("OPER\n")

            if args.reynolds_num >= 0:
                input_file.write(f"Visc {args.reynolds_num}\n")

            input_file.write(f"ITER {cfg['setup']['n_iter']}\n")

            input_file.write(f"{args.input_type} {args.input_value}\n")
            input_file.write(f"DUMP {output_file_nameDUMP}\n")
            input_file.write(f"CPWR {output_file_nameCPWR}\n\n")

            input_file.write("\n\n")
            input_file.write("quit\n")


        # Running calculations in XFOIL
        Popen("xfoil.exe < input_file.in", shell=True)
        time.sleep(1.5)






if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-r", "--reynolds_num", type=restricted_integer, default=-1,
                        help="Value of Reynolds Number as integer (-1 for inviscid flow)")

    parser.add_argument("-t", "--input_type", type=str, help="Calculate based off cl or alpha", required=True, choices=['cl', 'alpha'])
    parser.add_argument("-v", "--input_value", type=restricted_float, help="Value of cl or alpha", required=True)

    parser.add_argument('-o', '--delete_old', action='store_false', default=True,
                        help='If NOT FLAGGED (true), deletes any previously stored data for inputted aerofoils, else if FLAGGED (false), appends new data to this reviously stored data')

    parser.add_argument('-n', '--aerofoil_names', nargs='+', default=['NACA0012', 'NACA0013', 'NACA0014'],
                        help='NACA 4-digit aerofoils to test (in "NACAxxxx" form)')

    args = parser.parse_args()
    main(args)

    # print(args)
