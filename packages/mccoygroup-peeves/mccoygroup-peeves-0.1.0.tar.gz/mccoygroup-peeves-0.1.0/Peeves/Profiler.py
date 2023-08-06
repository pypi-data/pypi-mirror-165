
# import sys, os, numpy as np, itertools as ip
import cProfile, pstats, io, abc

__all__ = [
    "BlockProfiler"
]

class AbstractBlockProfiler:
    def __init__(self, name="Profiled Block", inactive=False, print_res=True, logger=None):
        self.name = name
        self.print_res = print_res
        self.inactive = inactive
        self.logger = logger

    @abc.abstractmethod
    def start_profiler(self):
        raise NotImplementedError("abstract class")
    def __enter__(self):
        if not self.inactive:
            self.start_profiler()

    @abc.abstractmethod
    def stop_profiler(self):
        raise NotImplementedError("abstract class")
    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.inactive:
            self.stop_profiler()
            if self.print_res:
                self.print_profile()
    @abc.abstractmethod
    def format_profile(self):
        raise NotImplementedError("abstract class")
    def print_profile(self):
        msg = "In block {}:\n\n{}".format(self.name, self.format_profile())
        if isinstance(self.print_res, str) and self.print_res == 'raise':
            raise ValueError(msg)
        elif self.logger is None:
            if hasattr(self.print_res, 'write'):
                print(msg, file=self.print_res)
            else:
                print(msg)
        else:
            self.logger.log_print(msg)


class PyinstrumentBlockProfiler(AbstractBlockProfiler):

    def __init__(self, name="Profiled Block", inactive=False, print_res=True, logger=None):
        from pyinstrument import Profiler
        super().__init__(name=name, print_res=print_res, inactive=inactive, logger=logger)
        self.profiler = Profiler()

    def start_profiler(self):
        self.profiler.start()

    def stop_profiler(self):
        self.profiler.stop()

    def format_profile(self):
        return self.profiler.output_text(unicode=True, color=True)

class CProfileBlockProfiler(AbstractBlockProfiler):
    """
    Simple class to profile a block of code
    """

    def __init__(self,
                 name="Profile Block",
                 print_res=True,
                 inactive=False,
                 strip_dirs=None,
                 sort_by='cumulative',
                 num_lines=50,
                 filter=None,
                 logger=None
                 ):
        """
        :param name: name of profiled block
        :type name: str
        :param strip_dirs: directory paths to strip from report
        :type strip_dirs: None | Iterable[str]
        """

        super().__init__(name=name, print_res=print_res, inactive=inactive, logger=logger)
        self.strip_dirs = strip_dirs
        self.sort_by = sort_by
        self.num_lines = num_lines
        self.filter = filter
        self.pr = None

    def start_profiler(self):
        self.pr = cProfile.Profile()
        self.pr.enable()

    def stop_profiler(self):
        self.pr.disable()
        s = io.StringIO()
        sortby = self.sort_by
        ps = pstats.Stats(self.pr, stream=s).sort_stats(sortby)
        filt = [self.num_lines]
        if self.filter is not None:
            if isinstance(self.filter, (int, float, str)):
                filter = [self.filter]
            else:
                filter = list(self.filter)
            filt = filter + filt
        ps.print_stats(*filt)
        self.stat_block = s.getvalue()
        s.close()

    def format_profile(self):
        stat_block = self.stat_block
        strip_dirs = self.strip_dirs
        if strip_dirs is not None:
            for d in self.strip_dirs:
                stat_block = stat_block.replace(d, "")
        return stat_block


def BlockProfiler(name="Profiled Block", print_res=True, mode=None, inactive=False, **kwargs):
    """
    Dispatcher to the various BlockProfiler subclasses
    """

    if mode == None:
        try:
            profiler = PyinstrumentBlockProfiler(name=name, print_res=print_res, inactive=inactive, **kwargs)
        except ImportError:
            profiler = CProfileBlockProfiler(name=name, print_res=print_res, inactive=inactive, **kwargs)
    elif mode == "deterministic":
        profiler = CProfileBlockProfiler(name=name, print_res=print_res, inactive=inactive, **kwargs)
    else:
        profiler = PyinstrumentBlockProfiler(name=name, print_res=print_res, inactive=inactive, **kwargs)


    return profiler