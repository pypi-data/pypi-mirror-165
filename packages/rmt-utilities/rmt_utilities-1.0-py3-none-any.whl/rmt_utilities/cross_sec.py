"""
Utility for estimating ionisation cross sections from RMT calculations. The CS
is computed in barns and printed to screen for each solution. This method of
calculating the cross section is very approximate, and is based on the final
state populations in the named ionisation channels. Thus you must check that the
population is stable there, and that the correct channels are provided as
arguments to cross_sec.
"""


def read_command_line():
    from argparse import ArgumentParser as AP
    parser = AP()
    parser.add_argument('files', nargs="*",
                        help="optional list of directories containing rmt\
                        calculations",
                        default=["."])
    parser.add_argument('-n', '--nphotons', help='number of photons (1 or 2)',
                        type=int, default=1)
    parser.add_argument('-c', '--channels', help='list of channels to include',
                        nargs='*', default=['1'])
    parser.add_argument('-s', '--sols',
                        help='list of solutions to process, defaults to all',
                        nargs='*', default=None)
    return parser


def main(args):
    from rmt_utilities.rmtutil import RMTCalc
    for file in args.files:
        calc = RMTCalc(file)
        print(f"{file}: ", calc.cross_sec(args.channels,
                                          args.sols,
                                          args.nphotons))


if __name__ == '__main__':
    main(read_command_line().parse_args())
