import shutil
import time
from datetime import datetime
from typing import Callable


def timeit(func: Callable) -> Callable:
    """A decorator for functions, add execution time of a function as an additional return value.

    Use as @timeit just above your function definition.

    Args:
        func: A callable, could be any function.

    Returns:
        A wrapped function (callable) with one additional return value.
        Execution time (number of seconds) (int) is returned as the first return
        value. Any return values of the origial function is returned as the
        second value.

    Raises:
        None
    """

    def wrapped_function(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        elapsed: float = time.time() - start_time
        return elapsed, result

    return wrapped_function


def timeitprint(func: Callable) -> Callable:
    """A decorator for functions, prints execution time of a function as the side effect.

    Use as @timeitprint just above your function definition.

    Args:
        func: A callable, could be any function.

    Returns:
        A wrapped function (callable) that is identicial to the origial function
        with additional side effect: it prints the execution time to stdout.

    Raises:
        None
    """

    def wrapped_function(*args, **kwargs):
        time_start = time.time()
        result = func(*args, **kwargs)
        time_elapsed = time.time() - time_start

        hours, minutes = 0, 0

        if time_elapsed >= 3600:
            hours = int(time_elapsed // 3600)
            time_elapsed = time_elapsed - hours * 3600
        if time_elapsed >= 60:
            minutes = int(time_elapsed // 60)
            time_elapsed = time_elapsed - minutes * 60
        seconds = round(time_elapsed, 3)
        func_name = func.__name__
        try:
            terminal_width = shutil.get_terminal_size().columns
        except:
            terminal_width = 50

        if hours:
            msg = f" Func '{func_name}' finished in {hours} hrs, {minutes} mins, {int(seconds)} secs "
            print("{:=^{width}}\n".format(msg, width=terminal_width))
        elif minutes:
            msg = " Func '{}' finished in {} mins, {:.2f} secs ".format(
                func_name, minutes, seconds
            )
            print("{:=^{width}}\n".format(msg, width=terminal_width))
        else:
            msg = " Func '{}' finished in {:.10f} secs ".format(func_name, seconds)
            print("{:=^{width}}\n".format(msg, width=terminal_width))

        return result

    return wrapped_function


def timestamp_seconds() -> str:
    """Returns a 15-char string timestamp formatted as: {YYYYMMDD}T{HHMMSS}."""

    # '2015-01-01T12:30:59'
    now = str(datetime.now().isoformat(sep="T", timespec="seconds"))
    ts: str = ""
    for i in now:
        if i not in (" ", "-", ":"):
            ts += i
    return ts


def timestamp_milliseconds() -> str:
    """Returns a 19-char string timestamp formatted as: YYYYMMDD-HHMMSS-sss."""

    # '2015-01-01T12:30:59.000'
    now = str(datetime.now().isoformat(sep="T", timespec="milliseconds"))
    ts: str = ""
    for i in now:
        if i in ("T", "."):
            ts += "-"
        elif i not in (" ", ":", "-"):
            ts += i
    return ts


def timestamp_microseconds() -> str:
    """Returns a 22-char string timestamp formatted as: YYYYMMDD-HHMMSS-ffffff."""

    # '2015-01-01T12:30:59.000000'
    now = str(datetime.now().isoformat(sep="T", timespec="microseconds"))

    ts: str = ""
    for i in now:
        if i in ("T", "."):
            ts += "-"
        elif i not in (" ", ":", "-"):
            ts += i
    return ts


if __name__ == "__main__":
    ...

    @timeitprint
    def compute() -> None:
        a = 1000000
        for i in range(100000000):
            a -= 1
            b = a
        return

    compute()
