import numpy as np

from PToolkit import Round_sigfig
to_round = np.array([1.52, 163, 1.7776, 1.98, 1090.897481242155221, 20.6])
sigfig = 2
rounded = Round_sigfig(to_round, sigfig)

print(rounded)