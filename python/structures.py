import numpy as np

from constants import NDATA
from crc16 import crc16
from ecc import encode8
from type_checking import auto_attr_check


@auto_attr_check
class Data(object):
    """Block on paper.

    addr np.uint32 - Offset of the block or special code
    data     bytes - Useful data. Max size constants.NDATA
    crc  np.uint16 - Cyclic redundancy of addr and data
    ecc      bytes - Reed-Solomon's error correction code 32 bytes
    """
    params = {
        "address": (np.uint32, None),
        "data": (bytes, None),
        "crc": (np.uint16, None),
        "ecc": (bytes, None),
    }

    def tobytes(self, with_crc=False, with_ecc=False):
        """Convert datastructure into bytes.

        :param with_crc: Include Cyclic redundancy
        :type  with_crc: bool
        :param with_ecc: Include error correction code
        :type  with_ecc: bool
        :rtype: bytes
        """
        out = (self.address or np.uint32(0)).tobytes()
        # data + 0 till end
        out += self.data or bytes() + bytes([0] * (NDATA - len(self.data or [])))
        if with_crc:
            out += (self.crc or np.uint16(0)).tobytes()
        if with_ecc:
            # ecc + 0 till end
            out += self.ecc or bytes() + bytes([0] * (32 - len(self.ecc or [])))
        return out

    def calc_crc(self):
        """Calculate cyclic redundancy of addr and data."""
        self.crc = crc16(self.tobytes()) ^ 0x55AA

    def calc_ecc(self):
        """Calculate Reed-Solomon's error correction code."""
        assert self.crc != None
        self.ecc = encode8(self.tobytes(with_crc=True))
