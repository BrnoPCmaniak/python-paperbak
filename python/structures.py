import numpy as np

from constants import NDATA, SUPERBLOCK
from crc16 import crc16
from dtypes import FileTime
from ecc import encode8
from type_checking import auto_attr_check


@auto_attr_check
class Data(object):
    """Block on paper.

    Structure:
    address np.uint32 - Offset of the block or special code
    data        bytes - Useful data. Max size constants.NDATA
    crc     np.uint16 - Cyclic redundancy of addr and data
    ecc         bytes - Reed-Solomon's error correction code 32 bytes

    Extra attributes:
    dt       np.dtype - dtype for parsing structure
    """
    params = {
        "address": np.uint32,
        "data": bytes,
        "crc": np.uint16,
        "ecc": bytes,
    }
    dt = np.dtype([("address", np.uint32, 1), ("data", np.uint8, 90),
                   ("crc", np.uint16, 1), ("ecc", np.uint8, 32)])

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

    @classmethod
    def frombytes(cls, bytes_):
        """Parse structure from bytes."""
        d = cls()
        parsed = np.frombuffer(bytes_, dtype=cls.dt)[0]
        d.address = parsed["address"]
        d.data = bytes(list(parsed["data"]))
        d.crc = parsed["crc"]
        d.ecc = bytes(list(parsed["ecc"]))
        return d


@auto_attr_check
class SuperData(object):
    """Identification block on paper.

    Structure:
    address   np.uint32 - Expecting SUPERBLOCK
    datasize  np.uint32 - Size of (compressed) data
    pagesize  np.uint32 - Size of (compressed) data on page
    origsize  np.uint32 - Size of original (uncompressed) data
    mode       np.uint8 - Special mode bits, set of PBM_xxx
    attributes np.uint8 - Basic file attributes
    page      np.uint16 - Actual page (1-based)
    modified   FileTime - Time of last file modification
    filecrc   np.uint16 - CRC of compressed decrypted file
    name            str - File name - may have all 64 chars
    crc       np.uint16 - Cyclic redundancy of previous fields
    ecc        np.uint8 - Reed-Solomon's error correction code 32 bytes

    Extra attributes:
    pbm_compressed bool(False) - Paper backup is compressed
    pbm_encrypted  bool(False) - Paper backup is encrypted
    """
    address = np.uint32(SUPERBLOCK)
    params = {
        "address": False,
        "datasize": np.uint32,
        "pagesize": np.uint32,
        "origsize": np.uint32,
        "pbm_compressed": (bool, False, False),
        "pbm_encrypted": (bool, False, False),
        "attributes": np.uint8,
        "page": np.uint16,
        "modified": FileTime,
        "filecrc": np.uint16,
        "name": str,
        "crc": np.uint16,
        "ecc": bytes,
    }
    PBM_COMPRESSED = 0x01
    PBM_ENCRYPTED = 0x02

    @property
    def mode(self):
        """Return byte of PBM_*** flags."""
        out = np.uint8(0)
        if self.pbm_encrypted:
            out |= self.PBM_ENCRYPTED
        if self.pbm_compressed:
            out |= self.PBM_COMPRESSED
        return out

    def tobytes(self, with_crc=False, with_ecc=False):
        out = self.address.tobytes()
        out += (self.datasize or np.uint32(0)).tobytes()
        out += (self.pagesize or np.uint32(0)).tobytes()
        out += (self.origsize or np.uint32(0)).tobytes()
        out += self.mode.tobytes()
        out += (self.attributes or np.uint8(0)).tobytes()
        out += (self.page or np.uint16(0)).tobytes()
        out += (self.modified or FileTime(0)).tobytes()
        out += (self.filecrc or np.uint16(0)).tobytes()
        # name + 0 till end of field
        name_bytes = bytes(self.name or "", encoding="utf8")
        out += name_bytes + bytes([0] * (64 - len(name_bytes)))
        if with_crc:
            out += (self.crc or np.uint16(0)).tobytes()
        if with_ecc:
            out += self.ecc or bytes() + bytes([0] * (32 - len(self.ecc or [])))
        return out

    def calc_crc(self):
        """Calculate cyclic redundancy of addr and data."""
        self.crc = crc16(self.tobytes()) ^ 0x55AA

    def calc_ecc(self):
        """Calculate Reed-Solomon's error correction code."""
        assert self.crc != None
        self.ecc = encode8(self.tobytes(with_crc=True))
