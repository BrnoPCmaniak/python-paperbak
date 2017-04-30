import numpy as np

from paperbak.constants import NDATA, SUPERBLOCK
from paperbak.crc16 import crc16
from paperbak.dtypes import FileTime
from paperbak.ecc import encode8
from paperbak.type_checking import auto_attr_check


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

    def tobytes(self, with_crc=True, with_ecc=True):
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
        self.crc = crc16(self.tobytes(False, False)) ^ 0x55AA

    def calc_ecc(self):
        """Calculate Reed-Solomon's error correction code."""
        assert self.crc != None, "CRC not calculated yet."
        self.ecc = encode8(self.tobytes(with_ecc=False))

    @classmethod
    def frombytes(cls, bytes_):
        """Parse structure from bytes."""
        d = cls()
        parsed = np.frombuffer(bytes_, dtype=cls.dt)[0]
        d.address = parsed["address"]
        d.data = bytes(parsed["data"])
        d.crc = parsed["crc"]
        d.ecc = bytes(parsed["ecc"])
        return d

    def __eq__(self, other):
        return self.address == other.address and self.data == other.data and self.crc == other.crc \
            and self.ecc == other.ecc


@auto_attr_check
class SuperData(object):
    """Identification block on paper.

    Structure:
    address   np.uint32 - Expecting SUPERBLOCK
    datasize  np.uint32 - Size of (compressed) data
    pagesize  np.uint32 - Size of (compressed) data on page
    origsize  np.uint32 - Size of original (uncompressed) data
    mode       np.uint8 - Special mode bits, set of PBM_xxx
    attributes np.uint8 - Basic windows file attributes. If current system is not Windows this
                          should be set to FILE_ATTRIBUTE_NORMAL 0x80
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
    PBM_COMPRESSED = 0x01
    PBM_ENCRYPTED = 0x02
    FILE_ATTRIBUTE_NORMAL = 0x80


    address = np.uint32(SUPERBLOCK)
    params = {
        "address": False,
        "datasize": np.uint32,
        "pagesize": np.uint32,
        "origsize": np.uint32,
        "pbm_compressed": (bool, False, False),
        "pbm_encrypted": (bool, False, False),
        "attributes": (np.uint8, np.uint8(FILE_ATTRIBUTE_NORMAL)),
        "page": np.uint16,
        "modified": FileTime,
        "filecrc": np.uint16,
        "name": str,
        "crc": np.uint16,
        "ecc": bytes,
    }

    dt = np.dtype([
        ("address", np.uint32, 1), ("datasize", np.uint32, 1), ("pagesize", np.uint32, 1),
        ("origsize", np.uint32, 1), ("mode", np.uint8, 1), ("attributes", np.uint8, 1),
        ("page", np.uint16, 1), ("modified", FileTime, 1), ("filecrc", np.uint16, 1),
        ("name", np.uint8, 64), ("crc", np.uint16, 1), ("ecc", np.uint8, 32)])

    @property
    def mode(self):
        """Return byte of PBM_*** flags."""
        out = np.uint8(0)
        if self.pbm_encrypted:
            out |= np.uint8(self.PBM_ENCRYPTED)
        if self.pbm_compressed:
            out |= np.uint8(self.PBM_COMPRESSED)
        return out

    def tobytes(self, with_crc=True, with_ecc=True):
        """Convert datastructure into bytes.

        :param with_crc: Include Cyclic redundancy
        :type  with_crc: bool
        :param with_ecc: Include error correction code
        :type  with_ecc: bool
        :rtype: bytes
        """
        out = self.address.tobytes()
        out += (self.datasize or np.uint32(0)).tobytes()
        out += (self.pagesize or np.uint32(0)).tobytes()
        out += (self.origsize or np.uint32(0)).tobytes()
        out += self.mode.tobytes()
        out += (self.attributes or np.uint8(self.FILE_ATTRIBUTE_NORMAL)).tobytes()
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
        self.crc = crc16(self.tobytes(False, False)) ^ 0x55AA

    def calc_ecc(self):
        """Calculate Reed-Solomon's error correction code."""
        assert self.crc != None, "CRC not calculated yet."
        self.ecc = encode8(self.tobytes(with_ecc=False))

    @classmethod
    def frombytes(cls, bytes_):
        """Parse structure from bytes."""
        d = cls()
        parsed = np.frombuffer(bytes_, dtype=cls.dt)[0]
        assert d.address == parsed["address"], "Adress of superdata doesn't match."
        d.datasize = parsed["datasize"]
        d.pagesize = parsed["pagesize"]
        d.origsize = parsed["origsize"]
        d.pbm_compressed = (
            parsed["mode"] & np.uint8(cls.PBM_COMPRESSED) == np.uint8(cls.PBM_COMPRESSED))
        d.pbm_encrypted = (
            parsed["mode"] & np.uint8(cls.PBM_ENCRYPTED) == np.uint8(cls.PBM_ENCRYPTED))
        d.attributes = parsed["attributes"]
        d.page = parsed["page"]
        d.modified = parsed["modified"]
        d.filecrc = parsed["filecrc"]
        d.name = bytes(parsed["name"]).decode("utf8").strip("\x00")
        d.crc = parsed["crc"]
        d.ecc = bytes(parsed["ecc"])
        return d

    def __eq__(self, other):
        return (
            self.address == other.address and self.datasize == other.datasize and
            self.pagesize == other.pagesize and self.origsize == other.origsize and
            self.mode == other.mode and self.attributes == other.attributes and
            self.page == other.page and self.modified == other.modified and
            self.filecrc == other.filecrc and self.name == other.name and self.crc == other.crc and
            self.ecc == other.ecc
        )
