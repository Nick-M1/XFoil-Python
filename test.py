import subprocess

# subprocess.run('python Iterations_plot.py -o -n NACA1416 NACA1417')

# subprocess.run('python Iterations_plot.py -n NACA1416 NACA1417')

# subprocess.run('python Iterations_plot.py -n NACA1416')





# subprocess.run('python Single_plot.py -t cl -v 5.0 -n NACA1416 NACA1417')
subprocess.run('python Single_plot.py -t alpha -v -5.0 -n NACA1416 NACA1417')
