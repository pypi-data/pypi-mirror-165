"""
Reconstruct the channel population files in the data directory. For use when the
RMT calculation has been executed with binary_data_files = .true.
"""
from pathlib import Path
import errno
import os


def read_command_line():
    from argparse import ArgumentParser as AP
    parser = AP(prog='data_recon', usage="data_recon <path to popchn binary file")
    parser.add_argument('popchn', help="""path to the binary popchn file for
unpacking, defaults to any file called popchn.* in the current directory""",
                        nargs='?', default=None)

    return parser


def get_popchn_file(args):
    """if the command line argument points to a popchn file, return the path to
    that file. Otherwise if it points to a directory, look for popchn there, or
    if no argument has been supplied, find the popchn file in the current
    directory"""
    if (args.popchn):
        path = Path(args.popchn)
        if path.is_file():
            return path
        elif path.is_dir():
            return find_popchn_file(path)
        else:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT),
                                    path)
    else:
        path = Path("./")
        return find_popchn_file(path)


def find_popchn_file(dirname):
    """look in dirname for a file matching popchn.*, and return the path to that
    file"""
    f = list(dirname.glob('popchn.*'))
    if len(f) == 0:
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT),
                                dirname/'popchn.*')
    elif len(f) > 1:
        import warnings
        warnings.warn(UserWarning(
            f"""Multiple popchn,
Found more than one popchn file in {dirname}.
This could lead to unexpected or incorrect results. Please specify
the popchn file explicitly to avoid this warning"""))
        f.sort()
        return f[0]
    else:
        return f[0]


def recon():
    """get popchn file and unpack it"""
    from rmt_utilities.dataobjects import popdata
    file = get_popchn_file(read_command_line().parse_args())
    popdata(file, recon=True)


if __name__ == '__main__':
    recon()
