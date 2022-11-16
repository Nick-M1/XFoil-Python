from _utils import *
import argparse
import time
import yaml
import os
from subprocess import Popen



def main(args: argparse.Namespace):

    # Open + read YAML config file
    with open('config.yaml', "r") as ymlfile:
        cfg: dict = yaml.safe_load(ymlfile)

    # Set directory to the dir of XFOIL
    os.chdir(cfg['setup']['xfoil_path'])

    # Create output folder (if it doesn't already exist)
    if not os.path.isdir(cfg['setup']['polarfiles_dir']):
        os.mkdir(cfg['setup']['polarfiles_dir'])


    # --------------------------------------------------------------------------
    # XFOIL input file writer

    for airfoil_name in args.aerofoil_names:

        output_file_name = getOutputFileName(OutputFiles.POLAR, cfg['setup']['polarfiles_dir'])(airfoil_name)

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
            input_file.write(f"ASeq {cfg['sequence_variables']['alpha_i']} {cfg['sequence_variables']['alpha_f']} {cfg['sequence_variables']['alpha_step']}\n")

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
                        help='If NOT FLAGGED (true), deletes any previously stored data for inputted aerofoils, else if FLAGGED (false), appends new data to this previously stored data')

    parser.add_argument('-n', '--aerofoil_names', nargs='+', default=['NACA0012', 'NACA0013', 'NACA0014'],
                        help='NACA 4-digit aerofoils to test (in "NACAxxxx" form)')

    args = parser.parse_args()
    main(args)

    # print(args)