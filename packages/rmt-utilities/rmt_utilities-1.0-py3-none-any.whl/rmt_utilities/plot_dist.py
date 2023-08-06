from rmt_utilities.reform_cli import get_command_line
from rmt_utilities.rmtutil import RMTCalc
from rmt_utilities.dataobjects import momentum, density
import matplotlib.pyplot as plt


def main(objectstring='requested distribution'):
    args = get_command_line(objectstring)
    plot_dist(args, objectstring)


def plot_dist(args, objectstring):
    calc = RMTCalc(args.dir)
    if not calc.config:
        raise IOError("no input file found. please specify the parent directory \
containing the input.conf file with the -d option")

    if objectstring == 'momentum distribution':
        Psi = momentum(args.file, calc, rskip=args.rskip)
    elif objectstring == 'electron density':
        Psi = density(args.file, calc, rmatr=args.rmatr)

    ax, _ = Psi.plot(normalise=args.normalise_bar, log=args.log_scale, rmax=args.rmax)

    if args.output:
        plt.savefig(args.output)
    if args.plot:
        plt.show()

    return ax


def plot_mom():
    main('momentum distribution')


def plot_den():
    main('electron density')


if __name__ == '__main__':
    pass
