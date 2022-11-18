import subprocess

# FOR SINGLE:
# For help
# subprocess.run('python Single_calc.py -h')
# subprocess.run('python Single_plot.py -h')

# For calculation
subprocess.run('python Single_calc.py -t cl -v 0.5 -n NACA1418')
# subprocess.run('python Single_calc.py -r 90000 -t cl -v 0.5 -n NACA1416 NACA1417')
# subprocess.run('python Single_calc.py -r 90000 -t alpha -v 5.0 -n NACA1416 NACA1417')

# For plotting
# subprocess.run('python Single_plot.py')
# subprocess.run('python Single_plot.py -n NACA1418')
# subprocess.run('python Single_plot.py -n NACA1416 NACA1417')


# ===============================================================================


# FOR SEQUENCE:
# For help
# subprocess.run('python Sequence_calc.py -h')
# subprocess.run('python Sequence_plot.py -h')

# For calculation
# subprocess.run('python Sequence_calc.py -r 90000 -n NACA1418')
# subprocess.run('python Sequence_calc.py -r 90000 -o -n NACA1416 NACA1417')
# subprocess.run('python Sequence_calc.py -r 90000 -n NACA1416 NACA1417')

# For plotting
# subprocess.run('python Sequence_plot.py')
# subprocess.run('python Sequence_plot.py -n NACA1418')
# subprocess.run('python Sequence_plot.py -n NACA1416 NACA1417')
