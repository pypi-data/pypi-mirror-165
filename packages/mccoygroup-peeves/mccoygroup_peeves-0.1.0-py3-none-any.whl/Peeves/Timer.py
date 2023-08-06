"""Provides a little timer for testing

"""
import timeit, functools, time, sys
from collections import deque

__all__ = ["Timer"]

class Timer:

    tag_printing_times = {}
    def __init__(self, tag = None, file = sys.stderr, rounding = 5, print_times = 1, number = 1, **kw):
        self.kw = kw
        self.number = number
        self.file = file
        self.tag = tag
        self.rounding = rounding
        self.checkpoints = deque()
        self.print_times = print_times
        self.laps = []

    def get_time_list(self, time_elapsed):
        run_time = [0, 0, time_elapsed]
        if run_time[2] > 60:
            run_time[1] = int(run_time[2] / 60)
            run_time[2] = run_time[2] % 60
            if run_time[1] > 60:
                run_time[0] = int(run_time[1] / 60)
                run_time[1] = run_time[1] % 60
        return run_time

    def start(self):
        self.checkpoints.append(time.time())

    def stop(self):
        t = time.time()
        cp = self.checkpoints.pop()
        return t - cp

    def log(self):
        t = time.time()
        self.laps.append([self.checkpoints[-1], t])

    def __enter__(self):
        self.start()
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        time_elapsed = self.stop()
        self.print_timing(time_elapsed)

    def format_timing(self, time_elapsed, tag = None, steps = None):
        run_time = self.get_time_list(time_elapsed)
        if tag is None:
            tag = self.tag
        if steps is None:
            steps = self.number
        run_time_averaged = self.get_time_list(time_elapsed / steps)
        return "{0}: took {1[0]}:{1[1]}:{1[2]} per loop with {2[0]}:{2[1]}:{2[2]} overall".format(
            tag,
            [ round(x, self.rounding) for x in run_time_averaged],
            [ round(x, self.rounding) for x in run_time ]
        )

    def print_timing(self, time_elapsed, tag = None, steps = None):
        if tag is None:
            tag = self.tag
        if tag not in self.tag_printing_times:
            self.tag_printing_times[tag] = 0
        if self.tag_printing_times[tag] < self.print_times:
            print(self.format_timing(time_elapsed, tag = tag, steps = steps), file = self.file)
            self.tag_printing_times[tag] += 1

    def __call__(self, fn): # for use as a decorator
        @functools.wraps(fn)
        def timed_fn(*args, **kwargs):
            func = fn
            val = None
            time_elapsed = timeit.timeit("val = func(*args, **kwargs)", globals = locals(), **self.kw)
            self.print_timing(time_elapsed, tag = func.__name__)
            return val
        return timed_fn