from enum import Enum
from typing import Callable

import numpy as np
from scipy.interpolate import make_interp_spline


class OutputFiles(Enum):
    POLAR = 'polar_file'
    DUMP = 'dump_file'
    CPWR = 'cpwr_file'


# Gets output '.txt' file name, from the 'NACAxxxx' name
def getOutputFileName(file_type: OutputFiles, path_dir: str) -> Callable[[str], str]:
    def _helper(airfoil_name: str) -> str:
        return f"{path_dir}{file_type.value}_{airfoil_name}.txt"
    return _helper


# Given x & y axis, smooths lines and returns new x & y axis
def smooth_plot(x_original: np.ndarray, y_original: np.ndarray) -> (np.ndarray, np.ndarray):
    x_new = np.linspace(x_original[0], x_original[-1], 30)
    y_new = make_interp_spline(x_original, y_original, k=7)(x_new)
    return x_new, y_new
