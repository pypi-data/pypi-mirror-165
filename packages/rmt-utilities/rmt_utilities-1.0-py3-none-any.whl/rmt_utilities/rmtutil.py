from rmt_utilities.dataobjects import DataFile
from rmt_utilities.atomicunits import eV, c
from pathlib import Path
from itertools import zip_longest
import numpy as np


class RMTCalc:
    """
    Primary data structure: holds all metadata for a given rmt calculation
    and provides methods ``.HHG()`` and ``.ATAS()`` for computing high harmonic spectra
    and attosecond transient absorption spectra respectivey.

    Parameters
    -----------
    path : path or str
        path to the rmt calculation directory (default = ".")
    target : str
        name of atomic/molecular target for calculation (default = None)
    description : str
        description of the rmt calculation (default = "RMT calculation")
    template : path or str
        path to the template directory containing rmt input to use for setup
    rmtexec : path or str
        path to the rmt executable to be used

    Attributes
    ----------
    path : path
        path to root directory of caculation
    conffile : path
        path to input.conf file used to drive RMT calculation
    config : dict
        dictionary containing input variables read from conffile
    datalist : list
        list of all files in the /data/ directory
    statelist : list
        list of all files in the /state/ directory
    expec_z : DataFile
        time-dependent dipole length
    expec_v : DataFile
        time-dependent dipole velocity
    field : DataFile
        time-depedent electric field
    length : Observable
        Harmonic spectrum computed from the dipole length
    velocity: Observable
        Harmonic spectrum computed from the dipole velocity
    """

    def __init__(self, path=".", target=None, description="RMT calculation",
                 template=None, rmtexec=None):
        self.path = Path(path).absolute()

        if template:
            self._buildFromTemplate(template, rmtexec)

        self.target = target
        self.description = description
        conffile = self.path / "input.conf"
        if conffile.is_file():
            self.conffile = conffile
            self.config = self._getConfig()
            self._suffix = self._getSuffix()
        else:
            self.conffile, self.config, self._suffix = None, {}, None
        self._buildFileLists()
        self.expec_z = None
        self.expec_v = None
        self.field = None

    def _buildFromTemplate(self, template, rmtexec):
        """Set up an RMT calculation with the necessary input files, executable
        and directories. The input is linked from the template directory, the
        executable linked from the provided rmtexec
        Parameters
        ==========
        template : str or pathlib.Path
            path to template directory containing input files
        rmtexec : str or pathlib.Path
            path to rmt executable
        """
        import os

        templatepath = Path(template).absolute()
        if not self.path.is_dir():
            os.mkdir(self.path)

        filestolink = list(templatepath.glob('*'))
        noexecutable = True
        if rmtexec:
            rmtexec = Path(rmtexec).absolute()
            if os.access(rmtexec, os.X_OK):
                if templatepath/'rmt.x' in filestolink:
                    filestolink.remove(templatepath/'rmt.x')
                filestolink.append(rmtexec)
                noexecutable = False
        else:
            if templatepath/'rmt.x' in filestolink:
                if os.access(templatepath/'rmt.x', os.X_OK):
                    noexecutable = False

        if noexecutable:
            print("no suitable rmt executable provided, templated calculation may be incomplete")

        for file in filestolink:
            if file.is_file():
                dest = self.path/file.parts[-1]
                dest.unlink(missing_ok=True)
                os.symlink(file, dest)

        filestomake = [self.path/f for f in ['ground', 'state', 'data']]
        for dest in filestomake:
            if dest.exists():
                if not dest.is_dir():
                    dest.unlink()
                    os.mkdir(dest)
            else:
                os.mkdir(dest)

        return not noexecutable

    def _buildFileLists(self):
        """populate the rootfiles, datalist and statelist attributes with lists
        of output files from the RMT calculation"""
        self.rootfiles = list(self.path.glob("pop*"))
        self.rootfiles += list(self.path.glob("expec*"))
        self.rootfiles += list(self.path.glob("EField*"))
        self.rootfiles.sort()
        if (self.path / "data").is_dir():
            self.datalist = list(self.path.glob("data/p*"))
            self.datalist.sort()
        else:
            self.datalist = []
        if (self.path / "state").is_dir():
            self.statelist = list(self.path.glob("state/p*"))
            self.statelist.sort()
        else:
            self.statelist = []
        return

    def __eq__(self, other):
        for fA, fB in zip_longest(self.rootfiles, other.rootfiles):
            try:
                fileA = DataFile(fA)
                fileB = DataFile(fB)
                if (fileA != fileB):
                    return False
            except Exception:
                return False
        return True

    def __ne__(self, other):
        return (not self == other)

    def _samefiles(self, other):
        for fA, fB in zip_longest(self.rootfiles + self.datalist, other.rootfiles + other.datalist):
            try:
                assert fA.parts[-1] == fB.parts[-1]
            except AttributeError:
                raise FileNotFoundError(f"Mismatch in files: {fA}, vs. {fB}")
            except AssertionError:
                raise IOError(f"Mismatch in files: {fA}, vs. {fB}")

    def agreesWith(self, other, tolerance=9):
        """
        Compare two RMT calculations to each other to ensure the computed data
        agrees to within `tolerance` significant figures. A.agreesWith(B,
        tolerance=9) will check that all pop and expec files in the root
        directory, and all pop files in the data directory agree to within 9
        decimal places. Information on the extent of agreement for each file
        is returned as part of the regression report.
        Parameters
        ==========
        other : RMTCalc
            the other RMTCalc object against which to compare this one
        tolerance : int (optional)
            number of decimal places to which to enforce agreement
        Returns
        =======
        regrep : regression_report
            information on the agreement between the output files in the calculation
        """
        from rmt_utilities.regress import regress_report

        self._samefiles(other)
        passList = []
        failList = []
        for fA, fB in zip_longest(self.rootfiles + self.datalist, other.rootfiles + other.datalist):
            try:
                fileA = DataFile(fA)
                fileB = DataFile(fB)
                fail = False
                for dp in range(min([2 * tolerance, 16])):
                    fileA.tolerance = dp
                    if fileA != fileB:
                        if dp <= tolerance:
                            failList.append((fA.parts[-1], dp-1))
                            fail = True
                        break
                if not fail:
                    passList.append((fA.parts[-1], dp-1))
            except Exception:
                raise IOError

        return regress_report(failList, passList, self.path)

    def _getConfig(self):
        import f90nml
        config = f90nml.read(self.conffile)["inputdata"]
        for item in config:
            f = config[item]
            config[item] = f
        try:
            num_out_pts = config['x_last_master'] + \
                config['x_last_others'] * (config['no_of_pes_to_use_outer'] - 1)
            config['num_out_pts'] = num_out_pts
        except KeyError:
            pass
        return config

    def _getSuffix(self):
        f = self.config["intensity"]
        if hasattr(f, "__len__"):
            inten = f[0]
        else:
            inten = f
        return self.config["version_root"] + str(int(1000 * (inten))).zfill(8)

    def _initExpecFiles(self, sols):
        varnames = ['expec_v', 'expec_z', 'field']
        if (self._suffix):
            filnames = [self.path / (f + self._suffix)
                        for f in ["expec_v_all.", "expec_z_all.", "EField."]]
        else:
            filnames = []
            for f in ["expec_v_all", "expec_z_all", "EField"]:
                allfiles = [x for x in self.rootfiles if f in x.stem]
                if allfiles:
                    filnames.append(allfiles[0])
                else:
                    filnames.append(None)

        for var, fil in zip(varnames, filnames):
            if fil in self.rootfiles:
                setattr(self, var, DataFile(fil, sols=sols))

    def _FFT(self, data, cutoff, pad):
        """Fourier transform and remove high energies"""
        df = data.FFT(pad=pad)
        lastindex = (min(df[df["Freq"] > cutoff].index.tolist()))
        df = df.truncate(after=lastindex - 1)

        return (df)

    def HHG(self, sols=None, cutoff=200 * eV, pad=1, phase=False):
        """Compute the high harmonic spectrum given by [a(w)]**2 where a is
        the Fourier transform of the dipole acceleration. The dipole data is
        read from the expec_z and expec_v files and the harmonic spectra in both
        length and velocity form is returned.

        Parameters
        ----------
        sols : list of str, optional
            list of which solutions (column headings) should be selected from
            the dipole files for processing
        cutoff : float, optional
            highest energy retained in the HHG spectra in atomic units. Default
            is 200eV (7.34 a.u)
        pad : int, optional
            pad factor used to improve resolution in Fourier Transform.
            Increases the length of the signal by factor ``pad`` and then rounds
            up to the nearest power of two. Default is 1.
        phase: bool, optional
            if True compute the harmonic phase, rather than the amplitude.

        Returns
        -------
        length   :  DataFrame holding the High Harmonic Spectrum computed from the
                    dipole length
        velocity :  DataFrame holding the High Harmonic Spectrum computed from the
                    dipole length
            Each DataFrame has a ``Freq`` column, containing the frequency axis, and
            then amplitudes (or phases) in columns matching those in the source data files
            (expec_z_all.<> and expec_v_all.<>) or a subset as selected with the
            ``sols`` parameter.
        """

        self._initExpecFiles(sols)
        if not (getattr(self, "expec_z") or getattr(self, "expec_v")):
            print(f"Failed to read expec_z or expec_v file from {self.path}")
            return None, None

        for name, key in zip(["length", "velocity"], ["expec_z", "expec_v"]):
            if getattr(self, key):
                data = getattr(self, key)
                df = self._FFT(data, cutoff=cutoff, pad=pad)
                for col in df.columns[1:]:
                    if phase:
                        Phase = np.angle(data.phasefactor * df[col])
                        df[col] = Phase
                    else:
                        amplitude = np.real(np.abs(df[col])**2)
                        amplitude = amplitude * df["Freq"]**data.scalefactor
                        df[col] = amplitude
                df.root = self.path
                setattr(self, name, df)
            else:
                setattr(self, name, None)
        return self.length, self.velocity

    def ATAS(self, sols=None, cutoff=200 * eV, pad=1):
        """Compute the transient absorption spectrum. which is proportional to
        the imaginary part of d(w)/E(w) where d(w) and E(w) are the Fourier
        transformed dipole and electric field data respectively. Data is read
        from the expec_z_all.<> and EField.<> files, and the absorption spectrum
        computed for each solution therein.

        Returns
        -------
        Observable
            DataFrame containing column "Freq" holding the frequencies, and then one
            column for each corresponding solution the expec_z_all file, giving
            the optical density as a function of frequency.
        """
        self._initExpecFiles(sols)
        if not (getattr(self, "expec_z") and getattr(self, "field")):
            print(f"Failed to read expec_z and field files from {self.path}")
            return None
        else:
            ddat = self._FFT(self.expec_z, cutoff=80 * eV, pad=8)
            Edat = self._FFT(self.field, cutoff=80 * eV, pad=8)
            for col in ddat.columns[1:]:
                rat = np.imag(ddat[col] / Edat[col])
                ddat[col] = 4 * np.pi * ddat["Freq"] * rat / c
            setattr(self, "TAS", ddat)
        self.TAS.root = self.path
        return (self.TAS)

    def _effective_cycles(self, sol_id=1, nphotons=1):
        """Calculate the total number of effective peak cycles by scaling the
        ramp cycles (assuming a sin^2 field)."""
        ramp = self._select_params(sol_id, 'periods_of_ramp_on')
        peak = self._select_params(sol_id, 'periods_of_pulse')
        peak -= 2*ramp
        effective_ratio = {1: 0.3750, 2: 0.27343750}
        eff_rat = effective_ratio[nphotons]

        return peak + 2.0 * ramp * eff_rat

    def _select_params(self, sol=1, param="intensity"):
        """Select a particular value for a given parameter from the calculation
        configuration. For calculations with multiple solutions (i.e. several
        different field configs in the same run), we can select the value for a
        particular solution from the list of values read from the config file

        Parameters
        ==========
        sol : int
            solution id
        param : str
            dictionary key for the parameter of interest

        Returns
        =======
        pvalue : int or float
            selected value from self.config[param]
        """

        pvalue = self.config[param]
        if hasattr(pvalue, '__len__'):
            pvalue = pvalue[sol-1]
        return pvalue

    def cross_sec(self, channel_list, sols=None, nphotons=1):
        """ Read the final populations for specific ionisation channels, and
        compute using information from the conffile the ionisation cross
        section.

        Parameters
        ==========
        channel_list : list of ints or str
            list of which channels should be included in the calculation
        sols : list of ints or str (optional)
            which RMTcalc solutions (field configurations) for which to compute
            the cross section
        nphotons : int
            number of photons for the ionisation pathway under investigation

        Returns
        =======
        cs : dict
            dictionary with a key for each RMTcalc solution and the computed
            cross section for that solution
        """
        from rmt_utilities.dataobjects import popdata

        if Path(f"{self.path}/data/popchn.{self._suffix}").absolute() in self.datalist:
            pop_path = self.path/"data"/f"popchn.{self._suffix}"
        else:
            pop_path = self.path/"data"

        allpops = popdata(pop_path)
        channel_list = [str(x).zfill(allpops.chandigits) for x in channel_list]
        if not sols:
            sols = [x for x in range(1, allpops.numsol+1)]
        else:
            sols = [int(x) for x in sols]
        solstrs = [str(x).zfill(4) for x in sols]

        cs = {}
        for sol, solstr in zip(sols, solstrs):
            intensity = self._select_params(sol, 'intensity')
            frequency = self._select_params(sol, 'frequency')
            cycles = self._effective_cycles(sol, nphotons=nphotons)
            cs[solstr] = allpops.cross_sec(solstr, channel_list, frequency,
                                           intensity, cycles, nphotons)

        return cs

    def execute(self, mpirun, rmtexec="./rmt.x", logfile="./log.out",
                taskopt="-n", mpiopts=None):
        """execute the RMT calculation using the provided input

        Parameters
        ==========
        mpirun : str or path
            path to mpirun executable
        rmtexec : str or path
            path to rmt executable, default ./rmt.x
        logfile : str or path
            path to logfile for stdout from RMT, default ./log.out
        taskopt : str
            the command line option/flag for specifying the number of mpi tasks
            e.g. for mpirun taskopt = "-n", for srun, taskopt = "--ntasks"
        mpiopts : str
            any additional options to be passed to mpirun

        Returns
        =======
        Success : bool
            True if calculation executed successfully
        """
        from subprocess import run, PIPE
        from os import environ

        mpiTasks = self.config["no_of_pes_to_use_inner"] \
            + self.config["no_of_pes_to_use_outer"]

        mpiTasks = str(mpiTasks)
        environ["disk_path"] = str(self.path)+"/"
        success = False
        cmd = [mpirun, taskopt, mpiTasks]
        if mpiopts:
            for opt in mpiopts.split(" "):
                cmd.append(opt)
        cmd.append(str(rmtexec))

        try:
            rmtrun = run(cmd, stdout=PIPE, universal_newlines=True)
            success = (rmtrun.returncode == 0)
        except Exception:
            print("RMT execution Failed")

        if success:
            with open(self.path/logfile, 'w') as f:
                for line in rmtrun.stdout:
                    f.write(line)
            self._buildFileLists()
        return success

#    def _attachMetaData(self, df):
#        """use the configuration file to associate calculation parameters with
#        specific columns in an output data structure"""
#        attlist = ["intensity",
#                   "frequency"]  # expand later with more attributes
#        for col in df.columns[1:]:
#             transforms "0001_z" into 0 for instance
#            attr_index = int(col[:4]) - 1
#            for att in attlist:
#                f = self.config[att]
#                f = f if isinstance(f, list) else [f]
#                setattr(df[col], att, f[attr_index])
