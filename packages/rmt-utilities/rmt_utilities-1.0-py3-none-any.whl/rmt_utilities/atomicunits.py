"""
some standard units and conversions for use in rmtutil
"""

eV = 0.036749322175655
fs = 41.341374575751
ryd = 0.500000000000
c = 137.036
I0 = 3.509*10**16
a0 = 0.5291772083e-10
t0 = 2.4188843265e-17
alpha = 0.007297353


def au2eV(x):
    """convert atomic units of energy to eV"""
    return x * 27.211386245988
