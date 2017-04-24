import numpy as np

import datetime

class FileTime(np.uint64):
    EPOCH_DIFF = 11644473600 # number of seconds between 1.1.1601 and 1.1.1970
    N100_NSEC_IN_SEC = 10000000 # number of 100 nanosecond intervals in second

    def __new__(cls, value):
        if isinstance(value, datetime.datetime):
            value = (round(value.timestamp()) + cls.EPOCH_DIFF)*cls.N100_NSEC_IN_SEC
        return super().__new__(cls, value)

    def get_timestamp(self):
        return datetime.datetime.fromtimestamp((self/self.N100_NSEC_IN_SEC)-self.EPOCH_DIFF)
