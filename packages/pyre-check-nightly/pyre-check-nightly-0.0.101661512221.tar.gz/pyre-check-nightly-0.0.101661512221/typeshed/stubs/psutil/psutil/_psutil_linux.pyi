from typing import Any

DUPLEX_FULL: int
DUPLEX_HALF: int
DUPLEX_UNKNOWN: int
version: int

def disk_partitions(*args, **kwargs) -> Any: ...
def linux_sysinfo(*args, **kwargs) -> Any: ...
def net_if_duplex_speed(*args, **kwargs) -> Any: ...
def proc_cpu_affinity_get(*args, **kwargs) -> Any: ...
def proc_cpu_affinity_set(*args, **kwargs) -> Any: ...
def proc_ioprio_get(*args, **kwargs) -> Any: ...
def proc_ioprio_set(*args, **kwargs) -> Any: ...
def users(*args, **kwargs) -> Any: ...
