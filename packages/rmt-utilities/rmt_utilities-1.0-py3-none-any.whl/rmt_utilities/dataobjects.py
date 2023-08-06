"""
data classes for holding RMT outputs and computed observables
"""
import pandas as pd
import numpy as np
from pathlib import Path, PosixPath
from _io import TextIOWrapper


def convertpath(path):
    """
    Utility function for converting paths to PosixPath type. If path is already
    PosixPath, do nothing. If it is a str, convert to PosixPath.


    Note: type TextIOWrapper passes through unchanged as it is needed for several
    internal functions.
    """
    tt = type(path)
    if (tt == str):
        return Path(path)
    elif (tt == PosixPath or tt == TextIOWrapper):
        return path
    else:
        raise TypeError(f"The path supplied ({path}) is of type {tt}: please \
                        supply type str or PosixPath")


class Hfile():
    def __init__(self, path):
        self.path = convertpath(path)
        self.path = self.path / 'H'
        try:
            with open(self.path, 'rb') as f:
                self.rmatr = np.fromfile(f, dtype=float, count=4)[-1]
        except (FileNotFoundError, IndexError):
            print("Error reading H file: using default R-matrix boundary of 20 a.u.")
            self.rmatr = 20.0


class UnitError(NameError):
    def __init__(self, units, cls):
        message = f"""{units} is not a valid unit for {cls}.
To use custom units, use atomic units (select units='au') and apply scaling factors in postprocessing"""
        super().__init__(message)


class distribution(np.ndarray):
    """ storage and utilities for 2d polar representation of density/momentum distributions

    Provides method ``.plot()`` for displaying the data

    Parameters
    -----------
    path : pathlib.Path or str
        absolute or relative path to datafile
    rootcalc : rmtutil.RMTCalc
        RMT calculation from which the distribution file is derived
    rskip : int
        for momentum distributions, skip the first rskip a.u of space before
        transforming

    Attributes
    ----------
    path : pathlib.Path
        absolute or relative path to the source datafile
    theta : np.ndarray
        array containing the azimuthal angles for the 2-d polar distribution
        together with ``r`` forms a meshgrid for plotting the distribution
    r : np.ndarray
        array containing the radial grid points for the 2-d polar distribution.
        together with ``theta`` forms a meshgrid for plotting the distribution
    """
    def __new__(cls, path, rootcalc, rskip=0):
        # Input array is an already formed ndarray instance
        # We first cast to be our class type
        obj = np.asarray(np.loadtxt(path, unpack=True)).view(cls)
        obj.path = convertpath(path)
        obj.theta = 0
        obj.r = 0
        return obj

    def __array_finalize__(self, obj):
        # see InfoArray.__array_finalize__ for comments
        if obj is None:
            return
        self.theta = getattr(obj, 'theta', None)
        self.r = getattr(obj, 'r', None)

    def plot(self, normalise=False, log=False, rmax=None):
        """
        Plot the requested distribution in polar form with colourbar. Optionally
        normalise the yield, show on a log scale or limit the maximum radial
        value displayed.

        Note that the actual data is not modified- only the view expressed in
        the plot.

        Parameters
        -----------
        normalise : bool, default False
            normalise the distribution

        log : bool, default False
            show the distribution on a log scale

        rmax : float, default None
            limit the radial extent of the plot.


        Returns
        -------
        ax : matplotlib.axes.SubplotBase
            handle for axes holding the plotted distibution

        cbar : matplotlib.colorbar.Colorbar
            handle for colorbar object
        """
        import matplotlib.pyplot as plt
        from matplotlib import cm

        Psi = np.copy(self)
        cbar_label_info = []

        if normalise:
            Psi /= np.max(Psi)
            cbar_label_info.append('Normalised Scale')

        if log:
            Psi = -np.log10(Psi + 1e-10)
            cbar_label_info.append('(log scale, $10^{-x}$)')

        plt.figure(1, figsize=(8, 9))

        ax = plt.subplot(label="polar", polar=True)
        ax.set_theta_zero_location("E")

        levels = np.linspace(0.0, np.amax(Psi), 200)
        CS = plt.contourf(self.theta, self.r, Psi, levels, cmap=cm.jet)
        if rmax:
            ax.set_rmax(rmax)
        cbar = plt.colorbar(CS)
        cbar.set_label(' '.join(cbar_label_info))

        return ax, cbar


class density(distribution):
    """
    Storage and utilities for 2d polar representation of density distribution
    """
    def __new__(cls, path, rootcalc, rmatr=None, *args, **kwargs):
        obj = super().__new__(cls, path, rootcalc, *args, **kwargs)

        if rmatr is None:
            rmatr = Hfile(rootcalc.path).rmatr
        dR = rootcalc.config['deltar']
        Nr, Nphi = obj.shape
        zeniths = rmatr + dR * np.arange(0, Nr)
        phi = np.linspace(0, 360, num=Nphi)
        angle = np.radians(-phi)
        obj.theta, obj.r = np.meshgrid(angle, zeniths)
        return obj


class momentum(distribution):
    """
    Storage and utilities for 2d polar representation of momentum distribution
    """
    def __new__(cls, path, rootcalc, rskip=200, *args, **kwargs):
        obj = super().__new__(cls, path, rootcalc, rskip=rskip, *args, **kwargs)

        nskip = int(rskip / rootcalc.config['deltar'])
        Nt = rootcalc.config['num_out_pts'] - nskip

        dK = (2.0 * np.pi) / (rootcalc.config['deltar'] * Nt)
        Nr, Nphi = obj.shape
        zeniths = dK * np.arange(0, Nr)
        phi = np.linspace(0, 360, num=Nphi)
        angle = np.radians(-phi)
        obj.theta, obj.r = np.meshgrid(angle, zeniths)
        # Finally, we must return the newly created object:
        return obj


class Observable(pd.DataFrame):
    """ DataFrame plus routines for observables

    Provides methods ``.write()`` ``.plot()`` for storing and displaying data
    respectively.
    """

    def __init__(self, root=".", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.root = Path(root)

    def truncate(self, *args, **kwargs):
        """Truncate an observable (DataFrame), retaining the class definition"""
        return Observable(root=self.root, data=super().truncate(*args, **kwargs))

    def write(self, fname, units="eV"):
        """
        Write the observable data to separate output files: one for each
        column.  The output files will be named

        ``self.root/fname_column``

        where ``self.root`` is the location of the RMT calculation, ``fname`` is the
        provided filename prefix, and ``column`` is the column heading in the DataFrame

        optionally scale the x-axis data for different units: "eV" (default) or
        "au".
        """

        if units == "eV":
            from rmt_utilities.atomicunits import eV
            xscale = 1.0 / eV
        elif units == "au":
            xscale = 1.0
        else:
            raise UnitError(units=units, cls=type(self))
        c1 = self.columns[0]
        tmpdf = self.copy()
        tmpdf[c1] = xscale * tmpdf[c1]
        for col in self.columns[1:]:
            filename = fname + col
            opf = self.root / filename
            with open(opf, "w") as f:
                tmpdf.to_csv(f, columns=[c1, col],
                             sep=" ", index=False, header=None)

    def plot(self, units="eV", *args, **kwargs):
        """ Plot the columns of the dataframe using the first column as the x
        axis.
        """
        if units == "eV":
            from rmt_utilities.atomicunits import eV
            xscale = 1.0 / eV
        elif units == "au":
            xscale = 1.0
        else:
            raise UnitError(units=units, cls=type(self))
        c1 = self.columns[0]
        tmpdf = self.copy()
        tmpdf[c1] = xscale * tmpdf[c1]
        ax = tmpdf.plot(0, tmpdf.columns[1:], *args, **kwargs)
        ax.set_xlabel(f"Frequency ({units})")
        ax.set_ylabel("Amplitude (arb. units)")
        return ax


class Data(pd.DataFrame):
    """DataFrame plus additional methods.

    Provides method ``.FFT()`` for Fourier transforming the sanitised (zero-padded
    and windowed) data.

    Parameters
    -----------
    data : Pandas DataFrame
    """

    def __init__(self, data, sols=None, *args, **kwargs):
        super().__init__(data)

    def __bool__(self):
        """returns True"""
        return True

    def FFT(self, blackman=True, pad=1):
        """Apply a blackman window to all data columns, take fourier transform
        of the windowed input data, return DataFrame with transformed data

        Parameters
        ----------
        blackman : bool, optional
            Apply blackman window to data before Fourier Transforming
        pad : int, optional
            prepad the data with zeros before transforming: increases the length
            of the signal by factor ``pad`` and then rounds up to the nearest
            power of two
        """
        df = Observable()
        for col in self.columns[1:]:
            ydat = np.array(self[col])
            if blackman:
                ydat = np.blackman(len(ydat)) * ydat
            if pad:
                ydat = self._pad_with_zeros(ydat, factor=pad)
            Y = (np.fft.fft(ydat))[:len(ydat) // 2]
            df[col] = Y
        X = np.arange(len(Y)) * (((np.pi) / len(Y)) / self.xstep)
        df.insert(0, "Freq", X)

        return df

    def _pad_with_zeros(self, ydat, factor=8):
        """pad ydat with zeros so that the length of ydat is a power of 2 and
        at least factor times the length of ydat on input."""

        pot = 2  # power of two
        while pot < (factor * len(ydat)):
            pot *= 2
        numzeros = pot - len(ydat)
        return np.concatenate([np.zeros(numzeros), np.transpose(ydat)])


class DataFile(Data):
    """DataFile with metadata from RMT output file

    Parameters
    -----------
    path : pathlib.Path or str
        absolute or relative path to datafile
    sols : list of str
        list of which solutions (column headings) to extract from data files.
        E.G ["0001_x", "0001_y"]

    Attributes
    ----------
    path : pathlib.Path
        absolute or relative path to the source datafile
    name : str
        name of the datafile
    xstep : float
        spacing between successive values in the first column of datafile
    len : int
        number of elements in each column of the datafile
    """

    def __init__(self, path, sols=None, *args, **kwargs):
        super().__init__(self._harvest(path, sols=sols))
        self.path = convertpath(path)
        self.name = self.path.parts[-1]
        self.xstep = self[self.columns[0]][1] - self[self.columns[0]][0]
        self.len = len(self)
        self.tolerance = 9  # number of decimal places to check agreement between calculations
        if self.name.startswith("expec_v_all"):
            self.phasefactor = -1j
            self.scalefactor = 2
        else:
            self.phasefactor = 1.0
            self.scalefactor = 4

    def _harvest(self, path, sols):
        """ Given the name of a file to read, harvest will read the data, return
        the column headers, and the (multicolumn) data as a numpy ndarray"""
        with open(path, 'r') as f:
            toprow = f.readline()
            try:
                float(toprow.split()[0])  # check to see if top row is headers
            except ValueError:  # top row is headers
                head = 0
            else:  # no column headings
                head = None

        df = pd.read_csv(path, delim_whitespace=True, header=head)

        if sols:
            cols = [df.columns[0]]
            for sol in sols:
                cols.extend([c for c in df.columns if c == sol])
            df = df[cols]

        return df

    def __eq__(self, other):
        """ checks equivalence between self and other up to tolerance.
        First check to see if the dataframes are identical. Then if not, checks
        to see if they are sufficiently close. This is faster in the first
        check, and then in the second allows for relatively large differences in
        very small numbers"""
        if self.round(self.tolerance).equals(other.round(self.tolerance)):
            return True
        else:
            tol = 10**-self.tolerance
            return np.allclose(self, other, atol=tol)

    def __ne__(self, other):
        return (not self == other)


class popdata():
    """
    handle population data (in the /data directory) for an RMT calculation

    provides methods for reading the binary popchn file output by an RMT
    calculation run with binary_data_files option.

    Can unpack the binary data file into its constituent popL files (i.e. one
    file per channel) using popdata(<path to popchn>, recon=True)

    Alternatively can store all the population data in a pandas dataFrame (one
    for each field configuration/solution (numsols in RMT calculation)) with the
    resulting dataFrames held in a dictionary, popdata.alldfs {'0001' :
    pd.DataFrame, '0002' : pd.DataFrame, ...} Each column in the DataFrame
    represents an individual channel

    TODO:
    [ ] attach column metadata to DataFrame
    [ ] implement methods for computing cross sections
    [ ] testing!!!
    """

    def __init__(self, popfile=None, recon=False):
        if popfile:
            self.path = convertpath(popfile)
            if self.path.is_file():
                if recon:
                    self._data_recon()
                else:
                    self._initialise_data()
            elif self.path.is_dir():
                flist = list(set(self.path.glob("p*")) -
                             set(self.path.glob("pop_GS*")) -
                             set(self.path.glob("popchn*")))
                flist.sort()
                self._read_formatted_files(flist)
            else:
                print("failed to compile population data")

    def _get_channelID(self, fname):
        """given an RMT pop file name, extract the channel id"""
        prefixes = ['popL0', 'popL', 'ppL', 'pL', 'p']
        fname = str(fname.parts[-1]).split(".")[0]
        for prefix in prefixes:
            if prefix in fname:
                num = fname.replace(prefix, "")
                return int(num)

    def _build_fname(self, channel_id):
        """reproduce RMT's naming convention for the pop files."""

        prefix = ['popL0', 'popL', 'ppL', 'pL', 'p']
        sel = len(str(channel_id)) - 1
        newname = f'{prefix[sel]}{channel_id}'
        fname = Path(str(self.path).replace('popchn', newname))

        return fname

    def _ColumnHeader(self):
        """reproduce RMT's column headers"""
        ll = [("{0:20}".format("Time"))]
        ll.extend(['{: 05}'.format(x)+16*" " for x in range(1, self.numsol+1)])
        ll.append("\n")
        return " ".join(ll)

    def _data_recon(self):
        """ convert binary popchn.* file into individual, formatted popL###
        files, one for each channel"""
        data = self._read_binary_data()
        for chan in range(self.nchan):
            chandat = []
            for check in range(self.checkpt):
                for rec in range(self.nrec):
                    for sol in range(self.numsol):
                        chandat.append(data[check][sol][chan][rec])
            chandat = np.array(chandat)
            chandat = chandat.reshape((self.nrec*self.checkpt, self.numsol))

            self._write_recon_data(chandat, chan)

    def _write_recon_data(self, chandat, chan):
        "write individual channel pop data to file"
        fname = self._build_fname(chan+1)
        try:
            fmtstring = "{:.15E} "
            fstring = ""
            for x in range(self.numsol+1):
                fstring += fmtstring
            fstring += "\n"
            with open(fname, 'w+') as opf:
                opf.write(self._ColumnHeader())
                for tim, dat in zip(self.times, chandat):
                    opf.write(fstring.format(tim, *dat))

        except Exception as e:
            print('unable to write to file {}'.format(fname))
            raise e

    def _read_binary_data(self):
        """read in the data from the binary popchn file, output by RMT"""

        try:
            self.nchan, self.nrec, self.checkpt, self.numsol, self.steps = \
                np.fromfile(self.path, dtype=np.int32, count=5)

            cnt = self.nchan * self.nrec * self.checkpt * self.numsol
            self.deltat = np.fromfile(self.path, dtype=np.float64, count=1, offset=20)[0]

            data = np.fromfile(self.path, dtype=np.float64, count=cnt, offset=28)
            results = data.reshape((self.checkpt, self.numsol, self.nchan, self.nrec))

            stride = self.deltat * self.steps
            NoTimeSteps = self.checkpt * self.nrec
            self.times = np.array([self.deltat + i*stride for i in range(NoTimeSteps)])

            return results
        except Exception:
            return None

    def _initialise_data(self):
        """read in data and reformat into dictionary of pandas DataFrames, one
        for each solution"""

        from math import ceil
        self.alldfs = {}
        results = self._read_binary_data()

        if results is not None:
            self.chandigits = ceil(np.log10(self.nchan + 1))
            soldigits = 4  # rmt uses 4 digit solution indices
            for sol in range(self.numsol):
                solstr = str(sol+1).zfill(soldigits)
                df = pd.DataFrame()
                for chan in range(self.nchan):
                    chandat = []
                    chanstr = str(chan+1).zfill(self.chandigits)
                    for check in range(self.checkpt):
                        for rec in range(self.nrec):
                            chandat.append(results[check][sol][chan][rec])
                    df[chanstr] = np.array(chandat)
                self.alldfs[solstr] = df
        return results is not None

    def _read_formatted_files(self, files):
        """read individual pop files and store each data in dictionary of
        DataFrames, one for each solution"""
        from math import ceil

        self.nchan = len(files)

        self.chandigits = ceil(np.log10(self.nchan + 1))
        dfs = {}
        for fname in files:
            chan = self._get_channelID(fname)
            chanstr = str(chan).zfill(self.chandigits)
            dfs[chanstr] = pd.read_csv(fname, delim_whitespace=True)

        tmpdf = dfs[list(dfs.keys())[0]]
        self.numsol = len(tmpdf.columns) - 1

        self.alldfs = {}
        soldigits = 4  # rmt uses 4 digit solution indices
        for sol in range(self.numsol):
            solstr = str(sol+1).zfill(soldigits)
            soldf = {}
            for chan in dfs:
                df = dfs[chan]
                soldf[chan] = df[solstr].values
            self.alldfs[solstr] = pd.DataFrame(soldf)

    def cross_sec(self, sol, channel_list, frequency, intensity, cycles, nphotons):
        from rmt_utilities.atomicunits import alpha, I0, a0, t0
        pop = self.alldfs[sol]

        t1 = (8 * np.pi * alpha * frequency) ** nphotons
        t2 = (I0*10**(-14)/(intensity))**(nphotons)
        t3 = a0 ** (2 * nphotons)
        t4 = t0 ** (nphotons - 1)
        total_yield = 0
        for chan in channel_list:
            total_yield += pop[chan].values[-1]
        rate = (total_yield * frequency) / (cycles * 2 * np.pi)
        return 1e22 * t1 * t2 * t3 * t4 * rate
