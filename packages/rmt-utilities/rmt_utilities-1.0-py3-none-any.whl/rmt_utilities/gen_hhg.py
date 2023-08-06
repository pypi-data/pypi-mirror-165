"""
Utility for generating harmonic spectra from RMT outputs.

Physics
=======

Fundamentally, light is produced by accelerated charges, and in the cases
considered by RMT, the charge in question is the dipole.


`We may show that <https://doi.org/10.1103/PhysRevA.86.053420>`_ the
electric field produced by an oscillating dipole is

.. math::
    E(t) \\propto \\mathbf{\\ddot{d}}(t) =
    \\frac{d^2}{dt^2}\\langle\\Psi(t)|\\mathbf{z}|\\Psi(t)\\rangle,

where :math:`\\mathbf{\\ddot{d}}(t)` is the time-dependent expectation value of the dipole
acceleration, :math:`\\mathbf{z}` is the position operator and :math:`\\Psi(t)` is
the wavefunction.  Then, the power spectrum of the emitted radiation is given,
up to a proportionality constant,  by :math:`|\\mathbf{\\ddot{d}}(\\omega)|^2`- the
Fourier transform of :math:`\\mathbf{\\ddot{d}}(t)` squared.  The dipole
acceleration :math:`\\mathbf{\\ddot{d}}` cannot however be computed easily (except
in simple cases such as `atomic helium
<https://doi.org/10.1103/PhysRevA.86.053420>`_) as this quantity is
prohibitively sensitive to the description of atomic structure at very small
radial distances. Instead, the relationships between acceleration, velocity and
displacement can be exploited to express the harmonic spectrum in terms of the
the dipole velocity and/or length.

Thus in RMT calculations the harmonic spectrum is calculated from the
time-dependent expectation value of the dipole operator :math:`\\mathbf{D}`:

.. math:: \\mathbf{d}(t) =  \\langle \\Psi(t) | \\mathbf{D} | \\Psi(t)\\rangle,

and of the dipole velocity operator :math:`\\mathbf{\\dot{D}}`,

.. math:: \\dot{\\mathbf{d}} (t) =  \\langle \\Psi(t) | \\mathbf{\\dot{D}} | \\Psi(t)\\rangle.

The harmonic spectrum is then given by

.. math::
    S(\\omega) \\quad = \\quad \\omega^4 | \\mathbf{d}(\\omega)|^2 \\quad=
    \\quad \\omega^2 | \\mathbf{\\dot{d}}(\\omega)|^2,

where :math:`\\omega` is the photon energy and :math:`\\mathbf{d}(\\omega)` and
:math:`\\mathbf{\\dot{d}}(\\omega)` are the Fourier transforms of :math:`\\mathbf{d}(t)`
and :math:`\\mathbf{\\dot{d}}(t)` respectively. Consistency between the length and
velocity form spectra is used a test of the accuracy of the RMT calculations.

"""
from rmt_utilities.rmtutil import RMTCalc
from rmt_utilities.dipole_cli import get_command_line
import matplotlib.pyplot as plt


def main():
    args = get_command_line('harmonic')
    get_hhg_spectrum(args)


def get_hhg_spectrum(args):
    for f in args.files:
        calc = RMTCalc(f)
        l, v = calc.HHG()
        ax = plt.axes(label='figure')
        if l is not None:
            ax = calc.length.plot(units=args.units, logy=True, ax=ax,
                                  label=[f"{x}_l" for x in
                                         calc.length.columns[1:]])
        if v is not None:
            ax = calc.velocity.plot(units=args.units, logy=True, ax=ax,
                                    label=[f"{x}_v" for x in
                                           calc.velocity.columns[1:]])
        if args.plot:
            plt.show()
        if args.output:
            if l is not None:
                calc.length.write(fname="Harm_len_", units=args.units)
            if v is not None:
                calc.velocity.write(fname="Harm_vel_", units=args.units)
    return ax


if __name__ == "__main__":
    main()
