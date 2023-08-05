import enum
import sys
from typing_extensions import Literal

LOG_THRESHOLD_FOR_CONNLOST_WRITES: Literal[5]
ACCEPT_RETRY_DELAY: Literal[1]
DEBUG_STACK_DEPTH: Literal[10]
SSL_HANDSHAKE_TIMEOUT: float
SENDFILE_FALLBACK_READBUFFER_SIZE: Literal[262144]
if sys.version_info >= (3, 11):
    SSL_SHUTDOWN_TIMEOUT: float
    FLOW_CONTROL_HIGH_WATER_SSL_READ: Literal[256]
    FLOW_CONTROL_HIGH_WATER_SSL_WRITE: Literal[512]

class _SendfileMode(enum.Enum):
    UNSUPPORTED: int
    TRY_NATIVE: int
    FALLBACK: int
