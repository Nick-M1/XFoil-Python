from _utils import *
import argparse
import yaml
import os
import numpy as np
import matplotlib.pyplot as plt


def main(args: argparse.Namespace):
    # Open + read YAML config file
    with open('config.yaml', "r") as ymlfile:
        cfg: dict = yaml.safe_load(ymlfile)

    # Set directory to the dir of XFOIL
    os.chdir(cfg['setup']['xfoil_path'])

    # Get alias for helper of getOutputFileName()
    getOutputFileName_ = getOutputFileName(OutputFiles.POLAR, cfg['setup']['polarfiles_dir'])

    # Map each 'NACAxxxx' from args.aerofoil_names to a tuple with its name '.txt' path
    zipped_names: list[tuple[str, str]] = [(name, getOutputFileName_(name)) for name in args.aerofoil_names]

    # --------------------------------------------------------------------------
    # XFOIL PLOTTING

    # Plotting CL Vs alpha
    plt.figure()
    plt.axhline(y=cfg['variables']['cl_required'], color='tab:pink', linestyle='-.', label='Min cl Required')

    plt.axhline(y=0, color='black', linewidth=0.5)
    plt.axvline(x=0, color='black', linewidth=0.5)

    for naca_name, file_name in zipped_names:
        polar_data = np.loadtxt(file_name, skiprows=12)
        x_arr = polar_data[:, 0]
        y_arr = polar_data[:, 1]

        plt.plot(*smooth_plot(x_arr, y_arr), label=naca_name)

        # Display cl-max
        print(f'CL-max for "{naca_name}"  => {np.max(y_arr)}')

    plt.title("cl Vs Angle of attack - for different Aerofoils")
    plt.xlabel("Angle of attack (deg)")
    plt.ylabel("cl")
    plt.grid()
    plt.legend(loc='lower right', fontsize='x-small')
    plt.show()


    # --------------------------------------------------------------------------
    # Plotting CD Vs alpha
    plt.figure()
    plt.axhline(y=0, color='black', linewidth=0.5)
    plt.axvline(x=0, color='black', linewidth=0.5)

    for naca_name, file_name in zipped_names:
        polar_data = np.loadtxt(file_name, skiprows=12)
        x_arr = polar_data[:, 0]
        y_arr = polar_data[:, 2]

        plt.plot(*smooth_plot(x_arr, y_arr), label=naca_name)

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

    for naca_name, file_name in zipped_names:
        polar_data = np.loadtxt(file_name, skiprows=12)

        plt.plot(polar_data[:, 2], polar_data[:, 1], label=naca_name)

    plt.axhline(y=cfg['variables']['cl_required'], color='tab:pink', linestyle='-.', label='Min cl Required')
    plt.title("cl Vs cd - for different Aerofoils")
    plt.xlabel("cd")
    plt.ylabel("cl")
    plt.grid()
    plt.legend(loc='lower right', fontsize='x-small')
    plt.show()






if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-n', '--aerofoil_names', nargs='+', default=['NACA0012', 'NACA0013', 'NACA0014'],
                        help='NACA 4-digit aerofoils to test (in "NACAxxxx" form)')

    args = parser.parse_args()
    main(args)

