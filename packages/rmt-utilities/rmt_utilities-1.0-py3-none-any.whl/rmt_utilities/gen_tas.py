"""
Utility for generating absorption spectra from RMT output.

Physics
=======

Following `[1] <https://doi.org/10.1103/PhysRevA.83.013419>`_ and
`[2] <https://doi.org/10.1088/0953-4075/49/6/062003>`_, it can be shown that the
transient absorption spectrum :math:`\\sigma(\\omega)` is given by

.. math::
    \\sigma (\\omega) = 4\\pi\\alpha\\omega \\; \\mathrm{Im}
    \\bigg[\\frac{\\mathbf{d}(\\omega)}{\\mathbf{\\epsilon}(\\omega)}\\bigg]

where :math:`\\alpha` is the fine-structure constant, :math:`\\omega` is the
photon energy, and :math:`\\mathbf{d}(\\omega)` and
:math:`\\mathbf{\\epsilon}(\\omega)`
are the Fourier transforms of the time-dependent expectation value of the
dipole operator :math:`\\mathbf{d}(t)` and electric field of the driving laser
:math:`\\mathbf{\\epsilon}(t)` respectively.

The transient absorption spectrum can therefore be calculated from the
time-dependent dipole expectation and electric field from RMT.
"""
from rmt_utilities.rmtutil import RMTCalc
from rmt_utilities.dipole_cli import get_command_line
import matplotlib.pyplot as plt


def main():
    get_tas_spectrum(get_command_line('absorption'))


def get_tas_spectrum(args):
    for f in args.files:
        calc = RMTCalc(f)
        if calc.ATAS() is not None:
            ax = calc.TAS.plot(units=args.units)
            if args.plot:
                plt.show()
            if args.output:
                calc.TAS.write(fname="TAS_", units=args.units)

    return ax


if __name__ == "__main__":
    main()
