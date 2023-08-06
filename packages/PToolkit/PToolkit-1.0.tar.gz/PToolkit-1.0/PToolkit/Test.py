import matplotlib.pyplot as plt
import numpy as np
from PToolkit import Plotter

P = Plotter()

fig, ax = plt.subplots()

P.Decimal_format_axis(ax)

x = np.linspace(0, 10, 10)
y = np.linspace(0, 10, 10)

P.Set_xlabel(ax, "T", "$\degree$")
P.Set_ylabel(ax, "R", "$\Omega$")

plt.errorbar(x, y, xerr=0.2, yerr=1)
#plt.show()


from PToolkit import Round_sigfig
to_round = np.array([1.52, 163, 1.7776, 1.98, 1090.897481242155221, 20.6])
sigfig = 2
rounded = Round_sigfig(to_round, sigfig)

print(rounded)

from PToolkit import Error_function
import sympy as sy

I, R = sy.symbols("I, R")
U = I*R

error = Error_function(U, [I, R])
