import psutil
import linecache
import tracemalloc
from ELKLogging.Infra.Enum import MemLevel

psutil.PROCFS_PATH = "/proc"


def display_top(snapshot, limit, key_type='lineno'):
    snapshot = snapshot.filter_traces((
        tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
        tracemalloc.Filter(False, "<unknown>"),
    ))
    top_stats = snapshot.statistics(key_type)
    print("Top %s lines" % limit)
    for index, stat in enumerate(top_stats[:limit], 1):
        frame = stat.traceback[0]
        print("#%s: %s:%s: %.1f KiB"
              % (index, frame.filename, frame.lineno, stat.size / 1024))
        line = linecache.getline(frame.filename, frame.lineno).strip()
        if line:
            print('    %s' % line)
    other = top_stats[limit:]
    if other:
        size = sum(stat.size for stat in other)
        print("%s other: %.1f KiB" % (len(other), size / 1024))
    total = sum(stat.size for stat in top_stats)
    print("Total allocated size: %.1f KiB" % (total / 1024))


class SystemMetricsCatcher:
    def __init__(self):
        pass

    @staticmethod
    def tracing_start():
        tracemalloc.stop()
        tracemalloc.start()

    @staticmethod
    def tracing_mem(display=False, limit=5, level=MemLevel.MB.value, length=2):
        first_size, first_peak = tracemalloc.get_traced_memory()
        peak = first_peak / pow(1024, level)

        if display:
            snapshot = tracemalloc.take_snapshot()
            display_top(snapshot, limit)
        return round(peak, length)

    @staticmethod
    def cpu_usage_percent():
        return psutil.cpu_percent()

    @staticmethod
    def mem_usage_percent():
        return psutil.virtual_memory().percent

    @staticmethod
    def mem_usage(level=MemLevel.GB.value):
        total = psutil.virtual_memory().total / pow(1024, level)
        used = psutil.virtual_memory().used / pow(1024, level)
        free = psutil.virtual_memory().free / pow(1024, level)

        return total, used, free
