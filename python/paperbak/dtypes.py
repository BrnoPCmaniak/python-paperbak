import numpy as np

from datetime import datetime, timezone

class FileTime(np.uint64):
    """Windows 64bit FileTime.

    Number of 100 nanosecond intervals from 1.1.1601.

    You can enter UTC datetime into constructor to create FileTime.
    """
    EPOCH_DIFF = 11644473600 # number of seconds between 1.1.1601 and 1.1.1970
    N100_NSEC_IN_SEC = 10000000 # number of 100 nanosecond intervals in second

    def __new__(cls, value):
        if isinstance(value, datetime):
            value = (round(value.timestamp()) + cls.EPOCH_DIFF)*cls.N100_NSEC_IN_SEC
        return super().__new__(cls, value)

    def get_datetime(self):
        """Convert windows FileTime into utc datetime."""
        return (datetime.utcfromtimestamp((self/self.N100_NSEC_IN_SEC)-self.EPOCH_DIFF)
                        .replace(tzinfo=timezone.utc))
