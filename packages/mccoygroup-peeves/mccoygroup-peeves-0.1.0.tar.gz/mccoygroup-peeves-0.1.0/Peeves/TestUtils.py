"""
All of the utilities that are used in writing tests for Peeves
"""

from .Timer import Timer
import unittest, os, sys, argparse

__all__ = [
    "TestRunner",
    "DebugTests",
    "ValidationTests",
    "TimingTests",
    "TestManager",
    "DataGenerator",
    "load_tests",
    "validationTest",
    "debugTest",
    "dataGenTest",
    "timeitTest",
    "timingTest",
    "inactiveTest"
]

class TestManager:
    """
    Manages the run of the tests
    """

    log_file = "test_results.txt"
    log_results = False
    quiet_mode = False
    debug_tests = True
    validation_tests = False
    timing_tests = False
    data_gen_tests = False
    test_files = "All"
    test_name = None
    def __init__(self,
                 test_root=None, test_dir=None, test_data=None,
                 base_dir=None, start_dir=None,
                 test_pkg=None, test_data_ext="TestData",
                 log_file=None,
                 log_results=None,
                 quiet_mode=None,
                 debug_tests=None,
                 validation_tests=None,
                 timing_tests=None,
                 data_gen_tests=None,
                 test_files=None,
                 test_name=None
                 ):
        """
        :param test_root: the root package
        :type test_root:
        :param test_dir: the directory to load tests from (usually test_root/test_pkg)
        :type test_dir:
        :param test_data: the directory to load test data from (usually test_dir/test_data_ext)
        :type test_data:
        :param base_dir: the overall base directory to do imports from
        :type base_dir:
        :param start_dir: the directory to start test discovery from
        :type start_dir:
        :param test_pkg: the name of the python package that holds all the tests
        :type test_pkg:
        :param test_data_ext: the extension from test_dir to look for data in (usually TestData)
        :type test_data_ext:
        """
        self._base_dir = base_dir
        self._start_dir = start_dir
        self._test_root = test_root
        self._base_dir_use_default = base_dir is None
        self._test_dir = test_dir
        self._test_dir_use_default = test_dir is None
        self._test_data = test_data
        self._test_data_use_default = test_data is None
        self._test_pkg = test_pkg
        self._test_pkg_validated = False
        self.data_ext = test_data_ext

        if log_file is not None:
            self.log_file = log_file
        if log_results is not None:
            self.log_results = log_results
        if quiet_mode is not None:
            self.quiet_mode = quiet_mode
        if debug_tests is not None:
            self.debug_tests = debug_tests
        if validation_tests is not None:
            self.validation_tests = validation_tests
        if timing_tests is not None:
            self.timing_tests = timing_tests
        if data_gen_tests is not None:
            self.data_gen_tests = data_gen_tests
        if test_files is not None:
            self.test_files = test_files
        if test_name is not None:
            self.test_name = test_name
    @property
    def test_root(self):
        if self._test_root is None:
            try:
                test_root = [ a for a in sys.argv if os.path.isdir(a) ][0] # you can pass the directory to run the tests as the first sys.argv arg
            except IndexError:
                test_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # or we'll assume it's two dirs up from here
            sys.path.insert(0, test_root) # not sure exactly what this does... might want to be more targeted with it
            self._test_root = test_root
        return self._test_root
    @test_root.setter
    def test_root(self, root):
        self._test_root = root
        if self._base_dir_use_default:
            self._base_dir = None
        if self._test_dir_use_default:
            self._test_dir = None
        if self._test_data_use_default:
            self._test_data = None
    @property
    def base_dir(self):
        if self._base_dir is None:
            self._base_dir = self.test_root
        return self._base_dir
    @base_dir.setter
    def base_dir(self, d):
        self._base_dir = d
        if d is not None:
            self._base_dir_use_default = False
    @property
    def start_dir(self):
        if self._start_dir is None:
            return self.test_dir
        return self._start_dir
    @start_dir.setter
    def start_dir(self, d):
        self._start_dir = d
        if d is not None:
            self._start_dir_use_default = False
    @property
    def test_pkg(self):
        if not self._test_pkg_validated:
            root = self.test_root
            # TODO: find some way to check it to figure out how many . we need to go up...
            # for now we'll just leave it, though
            if self._test_pkg is None:
                self._test_pkg = "Tests"
            if "." not in self._test_pkg:
                self._test_pkg = "."*(len(__package__.split(".")) - 1) + self._test_pkg
                # a basic guess as to what'll get us to the right spot...
            self._test_pkg_validated = True
        return self._test_pkg
    @test_pkg.setter
    def test_pkg(self, pkg):
        self._test_pkg = pkg
        self._test_pkg_validated = False
    @property
    def test_dir(self):
        # the Tests package _must_ be in the parent repository
        if self._test_dir is None:
            self._test_dir = os.path.join(self.test_root, self.test_pkg.split(".")[-1])
            if not os.path.isdir(self._test_dir) and self.test_pkg[0] == ".":
                raise IOError(
                    "Peeves expects a '{}' package at {} to hold all the tests because I wrote it bad".format(
                        self.test_pkg,
                        self.test_root
                        )
                    )
        return self._test_dir
    @test_dir.setter
    def test_dir(self, d):
        self._test_dir = d
        if d is not None:
            self._test_dir_use_default = False
    @property
    def test_data_dir(self):
        if self._test_data is None:
            self._test_data = os.path.join(self.test_dir, self.data_ext)
        return self._test_data
    @test_data_dir.setter
    def test_data_dir(self, d):
        self._test_data = d
        if d is not None:
            self._test_data_use_default = False
    @classmethod
    def test_data(cls, filename):
        return os.path.join(cls().test_data_dir, filename)

    @classmethod
    def collect_run_args(cls):
        parser = argparse.ArgumentParser(description='Process test configurations')

        def parse_bool(s):
            if s in {"False", '0'}:
                return False
            else:
                return True

        parser.add_argument('-q', dest='quiet', metavar='-q',
                            type=bool, nargs='?', default=cls.quiet_mode,
                            help='whether to run the tests in quiet mode')
        parser.add_argument('-d', dest='debug', metavar='-d',
                            type=parse_bool, nargs='?', default=cls.debug_tests,
                            help='whether to run the debug tests')
        parser.add_argument('-v', dest='validate', metavar='-v',
                            type=parse_bool, nargs='?', default=cls.validation_tests,
                            help='whether to run the validation tests')
        parser.add_argument('-t', dest='timing', metavar='-t',
                            type=parse_bool, nargs='?', default=cls.timing_tests,
                            help='whether to run the timing tests')
        parser.add_argument('-g', dest='data_gen', metavar='-g',
                            type=parse_bool, nargs='?', default=cls.data_gen_tests,
                            help='whether to run the data generating tests')
        parser.add_argument('-l', dest='log', metavar='-l',
                            type=parse_bool, nargs='?', default=cls.log_results,
                            help='whether to log results')
        parser.add_argument('-L', dest='logfile', metavar='-L',
                            type=str, nargs='?', default=cls.log_file,
                            help='whether to log results')
        parser.add_argument('-f', dest='testfile', metavar='-f',
                            type=str, nargs='?', default=cls.test_files,
                            help='which tests to run')
        parser.add_argument('-n', dest='testname', metavar='-n',
                            type=str, nargs='?', default="",
                            help='name of specific test to run')
        args = parser.parse_args()

        return dict(
            quiet_mode=True if args.quiet is None else args.quiet,
            debug_tests=True if args.debug is None else args.debug,
            validation_tests=True if args.validate is None else args.validate,
            timing_tests=True if args.timing is None else args.timing,
            data_gen_tests=True if args.data_gen is None else args.data_gen,
            log_results=True if args.log is None else args.log,
            log_file=args.logfile,
            test_name=None if args.testname.lower().strip() == "" else args.testname,
            test_files='All' if args.testfile.lower() == "all" else args.testfile.split(",")
        )

    def get_log_file(self, log_results=None, log_file=None, syserr_redirect=True):
        log_results = self.log_results if log_results is None else log_results
        log_file = self.log_file if log_file is None else log_file
        if os.path.abspath(log_file) != log_file:
            log_file = os.path.join(self.test_dir, log_file)
        log_stream = self._stderr_wrap(open(log_file, "w") if log_results else sys.stderr, syserr_redirect=syserr_redirect)
        return log_stream
    class _stderr_wrap:
        def __init__(self, stream, syserr_redirect=True):
            self.stream = stream
            self.syserr_redirect = syserr_redirect
            self.stderr1 = None
            self.stdout1 = None
        def __enter__(self):
            self.stderr1 = sys.stderr
            sys.stderr = self.stream
            if self.syserr_redirect:
                self.stdout1 = sys.stdout
                sys.stdout = sys.stderr
            if hasattr(self.stream, '__enter__'):
                return self.stream.__enter__()
            else:
                return self.stream
        def __exit__(self, exc_type, exc_val, exc_tb):
            sys.stderr = self.stderr1
            self.stderr1 = None
            if self.syserr_redirect:
                sys.stdout = self.stdout1
                sys.stdout1 = None
            if hasattr(self.stream, '__exit__'):
                self.stream.__exit__(exc_type, exc_val, exc_tb)

    def run_tests(self, tag, test_set, runner, log_stream):
        print(
            "\n" + "-" * 70 + "\n" + "-" * 70 + "\n" +
            "Running {} Tests:\n".format(tag),
            file=log_stream
        )
        return runner.run(test_set)

    def get_test_types(self, debug=None, validate=None, timing=None, data_gen=None):
        tests = {}
        dt = DebugTests() # drain the stack even if unused
        if debug or (debug is None and self.debug_tests):
            tests["Debug"] = dt
        vt = ValidationTests()
        if validate or (validate is None and self.validation_tests):
            tests["Validation"] = vt
        tt = TimingTests()
        if timing or (timing is None and self.timing_tests):
            tests["Timing"] = tt
        dgt = DataGenTests()
        if data_gen or (data_gen is None and self.data_gen_tests):
            tests["DataGen"] = dgt
        return tests
    def _run(self,
             log_results=None, log_file=None, quiet=None,
             syserr_redirect=True
             ):
        TestManager.test_data_dir = self.test_data_dir
        with self.get_log_file(log_results=log_results, log_file=log_file, syserr_redirect=syserr_redirect) as log_stream:
            quiet = self.quiet_mode if quiet is None else quiet
            v_level = 1 if quiet else 2
            runner = TestRunner(stream=log_stream, verbosity=v_level)

            results = [
                self.run_tests(tag, tests, runner, log_stream)
                for tag, tests in self.get_test_types().items()
                ]
        test_status = not all(res.wasSuccessful() for res in results)
        return test_status

    def load_tests(self, start_dir=None, base_dir=None):
        if start_dir is None:
            start_dir = self.start_dir
        if base_dir is None:
            base_dir = self.base_dir

        sys.path.insert(0, base_dir)
        cur = ManagedTestLoader.manager
        try:
            ManagedTestLoader.manager = self
            unittest.defaultTestLoader.discover(
                start_dir,
                top_level_dir=base_dir
            )
        finally:
            ManagedTestLoader.manager = cur
    @classmethod
    def run(cls,
            exit=True, exit_code=None,
            syserr_redirect=True,
            cmd_line=False,
            **kwargs
            ):

        if cmd_line:
            kwargs = dict(cls.collect_run_args(), **kwargs)
        manager = cls(**kwargs)
        manager.load_tests()

        test_status = manager._run(syserr_redirect=syserr_redirect)
        if exit:
            sys.exit(test_status if exit_code is None else exit_code) #should kill everything...?
        return test_status


TestCase = unittest.TestCase #just in case I want to change this up later
class DataGenerator:
    """Provides methods to generate relevant data for testing methods
    """

    seed = 15
    @classmethod
    def coords(cls, n=50):
        import numpy as np
        np.random.seed(cls.seed)
        return np.random.rand(n, 3)
    @classmethod
    def multicoords(cls, n=10, m=50):
        import numpy as np
        np.random.seed(cls.seed)
        return np.random.rand(n, m, 3)
    @classmethod
    def mats(cls, n=1):
        import numpy as np
        np.random.seed(cls.seed)
        return np.random.rand(n, 3, 3)
    @classmethod
    def vecs(cls, n=1):
        import numpy as np
        np.random.seed(cls.seed)
        return np.random.rand(n, 3)

    @classmethod
    def angles(cls, n=50, r=(0, 360), use_rad=False):
        import numpy as np
        np.random.seed(cls.seed)
        angles = np.random.uniform(*r, size=(n,))
        if use_rad:
            angles = np.rad2deg(angles)
        return angles
    @classmethod
    def dists(cls, n=50, minmax=(.5, 1.5)):
        import numpy as np
        np.random.seed(cls.seed)
        return np.random.uniform(*minmax, size=(n,))
    @classmethod
    def zmat(cls, ncoords=15, use_rad=False):
        import numpy as np
        np.random.seed(cls.seed)
        refs1 = np.sort(np.random.randint(0, ncoords, ncoords))
        refs2 = np.sort(np.random.randint(0, ncoords, ncoords))
        refs3 = np.sort(np.random.randint(0, ncoords, ncoords))
        ass = np.arange(0, ncoords)
        refs1 = np.amin(np.array((refs1, ass)), axis=0)
        refs2 = np.amin(np.array((refs2, ass)), axis=0)
        for i,rs in enumerate(zip(refs1, refs2)):
            r1, r2 = rs
            if i > 0 and r1 == r2:
                while r1 == r2:
                    r2 = (r2 + 1) % (i + 1)
                    # print(r1, r2, i)
                refs2[i] = r2
        refs3 = np.amin(np.array((refs3, ass)), axis=0)
        for i,rs in enumerate(zip(refs1, refs2, refs3)):
            r1, r2, r3 = rs
            if i > 1 and (r1 == r3 or r2 == r3):
                while (r1 == r3 or r2 == r3):
                    r3 = (r3 + 1) % (i + 1)
                refs3[i] = r3

        # raise Exception(np.array((refs1, refs1-refs2, refs1-refs3, refs2-refs3)))
        dists = DataGenerator.dists(ncoords)
        angles = DataGenerator.angles(ncoords, (0, 180), use_rad=use_rad)
        dihedrals = DataGenerator.angles(ncoords, (0, 360), use_rad=use_rad)

        return np.array([refs1+1, dists, refs2+1, angles, refs3+1, dihedrals ]).T
    @classmethod
    def zmats(cls, m=10, ncoords=15, use_rad=False):
        import numpy as np
        np.random.seed(cls.seed)
        return np.array([DataGenerator.zmat(ncoords, use_rad) for i in range(m)])

class ManagedTestSuite(unittest.TestSuite):
    """
    A funky subclass of `TestSuite`
    that drains a stack of tests on initialization so that
    tests can be added to a global queue that is exhausted
    when called
    """
    stack = None
    def __init__(self):
        super().__init__(self.stack)
        type(self).stack = []
    @classmethod
    def queueTest(cls, test):
        cls.stack.append(test)

class DebugTests(ManagedTestSuite):
    """The set of fast tests in the test suite"""
    stack = []
class ValidationTests(ManagedTestSuite):
    """The set of slow tests in the test suite"""
    stack = []
class TimingTests(ManagedTestSuite):
    """The set of timing tests in the test suite"""
    stack = []
class InactiveTests(ManagedTestSuite):
    """The set of inactive tests in the test suite"""
    stack = []
class DataGenTests(ManagedTestSuite):
    """The set of tests in the test suite that exist to generate artefacts"""
    stack = []

def timingTest(fn):
    """
    A decorator that sets up a test to be added to the set of timing tests
    """
    timer = Timer()(fn)
    def Timing(*args, **kwargs):
        return timer(*args, **kwargs)
    return Timing
def timeitTest(**kwargs):
    """
    A decorator that sets up a test to be added to the set of timing tests
    using `timeit`
    """
    timer = Timer(**kwargs)
    def wrap(fn):
        inner_fn = timer(fn)
        def Timing(*args, **kwargs):
            return inner_fn(*args, **kwargs)
        return Timing
    return wrap

def inactiveTest(fn):
    """
    A decorator that sets up a test to be added to the set of inactive tests
    """
    def Inactive(*args, **kwargs):
        return fn(*args, **kwargs)
    Inactive.__og_name__ = fn.__name__
    return Inactive

def debugTest(fn):
    """
    A decorator that sets up a test to be added to the set of debug tests
    """
    def Debug(*args, **kwargs):
        return fn(*args, **kwargs)
    Debug.__og_name__ = fn.__name__
    return Debug

def dataGenTest(fn):
    """
    A decorator that sets up a test to be added to the set of data generation tests
    """
    def DataGen(*args, **kwargs):
        return fn(*args, **kwargs)
    DataGen.__og_name__ = fn.__name__
    return DataGen

def validationTest(fn):
    """
    A decorator that sets up a test to be added to the set of validation tests
    """
    def Validation(*args, **kwargs):
        return fn(*args, **kwargs)
    Validation.__og_name__ = fn.__name__
    return Validation

def TestRunner(**kw):
    if not "resultclass" in kw:
        kw["resultclass"] = unittest.TextTestResult
    if not "verbosity" in kw:
        kw["verbosity"] = 2
    return unittest.TextTestRunner(**kw)

_test_loader_map = {
    "Debug" : DebugTests,
    "Validation": ValidationTests,
    "Timing" : TimingTests,
    "Inactive" : InactiveTests,
    "DataGen": DataGenTests
}
class ManagedTestLoader:
    manager = None
    @classmethod
    def load_tests(cls, loader, tests, pattern):
        from itertools import chain

        pkgs = cls.manager.test_files
        names = cls.manager.test_name
        if isinstance(names, str):
            names = names.split(",")

        test_packages = None if pkgs == "All" else set(pkgs)
        if test_packages is None:
            tests = list(chain(*((t for t in suite) for suite in tests)))
        else:
            def _get_suite_name(suite):
                for test in suite:
                    return type(test).__module__.split(".")[-1]
            tests_named = {_get_suite_name(suite):suite for suite in tests}
            tests = []
            for k in tests_named:
                if k in test_packages:
                    tests.extend(tests_named[k])

        for test in tests:
            method = getattr(test, test._testMethodName)
            ttt = method.__name__
            try:
                og = method.__og_name__
            except AttributeError:
                og = ttt
            og = og.split("test_")[-1]

            if names is not None:
                if og in names:
                    for suite in _test_loader_map.values():
                        suite.queueTest(test)
            else:
                if ttt not in _test_loader_map:
                    ttt = "Debug"
                suite = _test_loader_map[ttt]
                suite.queueTest(test)
        #
        # return _test_loader_map.values()

load_tests = ManagedTestLoader.load_tests
