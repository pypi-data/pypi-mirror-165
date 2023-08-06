"""
Utility for comparing two RMT calculations to ensure the computed data agrees to
within a specified tolerance.
"""


def read_command_line():
    from argparse import ArgumentParser as AP
    parser = AP()
    parser.add_argument('fileA',
                        help="directory containing first rmt\
                        calculation for comparison")
    parser.add_argument('fileB',
                        help="directory containing first rmt\
                        calculation for comparison")
    parser.add_argument('-t', '--tolerance', help="optional tolerance (number \
                        of decimal places to which agreement is required, \
                        default = 9", type=int, default=9)
    parser.add_argument('-q', '--quiet', help="quiet mode: only report \
                        whether the files agree or not", action='store_true')
    return parser


def main():
    compare(read_command_line().parse_args())


def compare(args):
    import rmt_utilities.rmtutil as ru
    fA = ru.RMTCalc(args.fileA)
    fB = ru.RMTCalc(args.fileB)
    agree = fA.agreesWith(fB, args.tolerance)
    if not args.quiet:
        print(agree)
    if not agree:
        import sys
        sys.exit("Calculations do not agree to desired tolerance")
    return True


if __name__ == "__main__":
    main()
