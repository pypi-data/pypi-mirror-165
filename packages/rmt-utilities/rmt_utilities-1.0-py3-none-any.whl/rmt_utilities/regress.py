from rmt_utilities.rmtutil import RMTCalc
from pathlib import Path


class regress_report:
    """report on the agreement between two rmt calculations file by file"""

    def __init__(self, failList=[], passList=[], location=None):
        """
        Parameters
        ----------
        failList : list of tuples
            information on failed on pairs of files which do not agree to the
            necessary level of tolerance
            (filename, number of decimal places to which the two files agree)
        passList : list of tuples
            information on failed on pairs of files which agree to the necessary
            level of tolerance
            (filename, number of decimal places to which the two files agree)
        location : path or str
            location(directory) of the RMT calculation
        """
        self.fails = failList
        self.passes = passList
        self.dir = location

    def __bool__(self):
        return len(self.fails) == 0

    def __str__(self):
        """print the report"""
        return self.compileReport()

    def compileCalcs(self, listOfCalcs, agreeString):
        """expand tuples into a report about the agreement between pairs of
        files in two RMT calculations

        Parameters
        ----------
        listOfCalcs : list of tuples
            information on comparison of pairs of files
            (filename, number of decimal places to which the two files agree)
        agreeString : str
            either "Failing" or "Passing"
        """
        msg = [f"RMT calculation in: {str(self.dir)}", f"{agreeString} comparisons:", "=========="]
        for fname, dp in listOfCalcs:
            msg.append(f"{fname} agrees to {dp} decimal places")
        msg.append("")
        return msg

    def compileReport(self):
        """put together report on failing and passing file comparisons"""
        msg = []
        if (self.fails):
            msg += self.compileCalcs(self.fails, "Failing")
        if (self.passes):
            msg += self.compileCalcs(self.passes, "Passing")
        return "\n".join(msg)


class regressError(Exception):
    """Exception raised when two RMT calculations do not agree to the desired
    level of tolerance"""

    def __init__(self, report):
        msg = report.compileCalcs(report.fails, "Failing")
        self.message = "\n".join(msg)
        super().__init__(self.message)


class executionError(Exception):
    """Exception raised when an RMT calculation does not execute as expected"""

    def __init__(self, directory):
        self.message = f"""RMT calculation in {directory} failed to execute as
expected"""
        super().__init__(self.message)


class mpirunError(Exception):
    """Exception raised if mpirun is not available on the host system"""

    def __init__(self):
        self.message = """RMT regression testing requires a working mpi \
installation. Please provide the path to mpirun when setting up the tests"""
        super().__init__(self.message)


class testcase():
    """
    Individual RMT regression test calculation

    Attributes
    ----------
    testdir : pathlib.Path
        root directory for RMT test calculation
            The directory structure should be
            testdir
            ├── inputs        # directory containing the input files
            ├── regress_run   # directory containing RMT output for comparison
    exec : str or pathlib.Path
        rmt executable
    mpiRun : str or pathlib.Path
        mpirun executable
    taskopt : str
        the command line option/flag for specifying the number of mpi tasks
        e.g. for mpirun taskopt = "-n", for srun, taskopt = "--ntasks"
    mpiopts : str
        any additional options to be passed to mpirun
    """

    def __init__(self, testdir, rmtexec, mpiRun, taskopt="-n", mpiopts=None):
        import os
        import errno

        if Path(testdir).is_dir():
            self.testdir = Path(testdir)
        else:
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), Path(testdir))
        if os.access(rmtexec, os.X_OK):
            self.exec = rmtexec
        else:
            raise PermissionError(
                errno.EPERM, os.strerror(errno.EPERM), Path(rmtexec))
        if not mpiRun or not os.access(mpiRun, os.X_OK):
            from shutil import which
            self.mpirun = which('mpirun')
        else:
            self.mpirun = mpiRun

        if not self.mpirun:
            raise mpirunError

        for required_directory in ['regress_run', 'inputs']:
            if not (self.testdir / required_directory).is_dir():

                raise FileNotFoundError(
                    errno.ENOENT, os.strerror(errno.ENOENT),
                    self.testdir / required_directory)

        self.target_results = RMTCalc(path=self.testdir/'regress_run')
        self.template = self.testdir / 'inputs'
        self.rundir = self.testdir / f'run_{self._UID()}'
        self.taskopt = taskopt
        self.mpiopts = mpiopts
        return

    def _UID(self):
        """generate a unique 10 digit ID for directory naming"""
        import random
        import string
        digits = string.digits
        return (''.join(random.choice(digits) for i in range(10)))

    def runTest(self, result_dict={}, key=None, tolerance=9):
        """ Run an RMT calculation and test against the expected output

        Parameters
        ----------
        result_dict : dictionary
            dictionary to contain the result of the test (needed for
            multiprocessing)
        key : str
            dictionary key for storing the result of the test. I.E the result of
            the test will be stored in result_dict[key]

        Returns
        -------
        Success : bool
            whether or not the calculation agrees with the expected output
        """

        calc = RMTCalc(path=self.rundir, template=self.template, rmtexec=self.exec)
        calcruns = calc.execute(rmtexec=self.exec, mpirun=self.mpirun,
                                taskopt=self.taskopt, mpiopts=self.mpiopts)
        if calcruns:
            agreement = calc.agreesWith(self.target_results, tolerance=tolerance)
            result_dict[key] = agreement
            if not agreement:
                raise regressError(agreement)
            else:
                return agreement
        else:
            result_dict[key] = "Calculation did not execute correctly"
            raise executionError(self.rundir)

    def cleanupdir(self):
        from subprocess import call
        call(["rm", "-rf", self.rundir])

    def mvdir(self, newname):
        """mv self.rundir to self.testdir/newname"""
        from subprocess import call
        if self.rundir.is_dir():
            target_dir = self.testdir/newname
            if target_dir.exists():
                call(["rm", "-rf", target_dir])
            call(["mv", self.rundir, target_dir])
        self.rundir = self.testdir/newname


class RMT_regression_tests:
    """
    Class for building RMT calculations and comparing with expected outputs.

    Should be able to read in a yaml file with information on each test case,
    build the test directories, execute the calculations and provide as its main
    output a True or False statement of whether or not the tests agree within a
    specified tolerance. Additionally, could provide a summary
    report of the level of agreement in each test calculation.

    TODO:
    [ ] possible: autogenerate yaml file based on available test calculations?
    [ ] re-engineer runTest so that it can be used with Assert as part of pytest
    [ ] handle the report differently (it can't be used by pytest) custom Error?

    taskopt : str
        the command line option/flag for specifying the number of mpi tasks
        e.g. for mpirun taskopt = "-n", for srun, taskopt = "--ntasks"
    mpiopts : str
        any additional options to be passed to mpirun
    """

    def __init__(self, testlist, rmtexec=None, mpiRun=None, taskopt="-n",
                 mpiopts=None, tolerance=9):
        import yaml
        try:
            with open(testlist, 'r') as stream:
                tests = (yaml.safe_load(stream))
        except FileNotFoundError:
            print(f'{testlist} cannot be found')
            return

        self.tests = []
        for test in tests:
            self.tests.append(testcase(tests[test], rmtexec, mpiRun, taskopt,
                                       mpiopts))

        return

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n < len(self.tests):
            result = self.tests[self.n]
            self.n += 1
            return result
        else:
            raise StopIteration

    def runAllTests(self):
        """run every RMT test calculation in self.tests"""
        import multiprocessing as mp

        allprocs = []
        manager = mp.Manager()
        results = manager.dict()

        for calc in self:
            try:
                p = mp.Process(target=calc.runTest, args=(results,
                                                          calc.testdir))
                p.start()
                allprocs.append(p)
            except Exception:
                pass

        for p in allprocs:
            p.join()
        return results

    def cleanup(self):
        """clean up (remove) all test directories"""
        for calc in self.tests:
            calc.cleanupdir()
