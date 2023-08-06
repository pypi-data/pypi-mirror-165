def read_command_line(objectstring='requested'):
    from argparse import ArgumentParser as AP
    parser = AP()
    parser.add_argument('files', nargs="*",
                        help="optional list of directories containing rmt\
                        calculations",
                        default=["."])
    parser.add_argument('-x', '--x', help='transform the  x component of the dipole',
                        action='store_true', default=False)
    parser.add_argument('-y', '--y', help='transform the y component of the dipole',
                        action='store_true', default=False)
    parser.add_argument('-z', '--z', help='transform the z component of the dipole',
                        action='store_true', default=False)
    parser.add_argument('-p', '--plot', help=f"show a plot of {objectstring} spectrum",
                        action='store_true', default=False)
    parser.add_argument('-o', '--output', action='store_true',
                        help=f'output the {objectstring} spectra to text files',
                        default=False)
    parser.add_argument('--pad_factor',
                        help='number of zeros to pad data with during calculations\
                        involving Fourier transforms i.e. pad signal up to length 2^n)',
                        type=int, default=8)
    parser.add_argument('-s', '--solutions_list',
                        help='list of solutions on which to operate, defaults to all solutions', default=None)
    parser.add_argument('-u', '--units',
                        help='units to use on the x-axis, "eV" or "au"', default="eV")

    return parser


def get_command_line(objectstring='requested'):
    parser = read_command_line(objectstring)
    args = parser.parse_args()
# If no dimension specified, operate on z.
    if not (args.x or args.y or args.z):
        args.z = True
# If no output/plot is specified, output to file
    if not args.plot and not args.output:
        args.output = True
    return args
