import bz2
import datetime
import os
from stat import (
    FILE_ATTRIBUTE_ARCHIVE, FILE_ATTRIBUTE_HIDDEN, FILE_ATTRIBUTE_NORMAL, FILE_ATTRIBUTE_READONLY,
    FILE_ATTRIBUTE_SYSTEM)

from paperbak.constants import MAXSIZE, NDATA, NDOT, NGROUP, NGROUPMAX, NGROUPMIN
from paperbak.crc16 import crc16
from paperbak.structures import SuperData


class FilePrinter:

    # Print parameters
    compressed = False  # is the file compressed
    compression_level = 1  # level of bzip compression
    encrypted = False  # is the file encrypted
    printheader = False  # should we print header
    printborder = False  # should we print border or something??
    redundancy = NGROUP  # NGROUP Redundancy (NGROUPMIN..NGROUPMAX)

    # Filemetadata
    attributes = FILE_ATTRIBUTE_NORMAL  # windows only attributes
    mtime = datetime.utcfromtimestamp(0)  # date of modification
    origsize = 0  # original (uncompressed) file size in bytes
    datasize = 0  # Size of (compressed) data
    alignedsize = 0  # Data size aligned to next 16 bytes
    filecrc = None  # 16-bit CRC of (packed) data

    # page size
    resx = 300  # resolution, dpi (default 300)
    resy = 300  # resolution, dpi (default 300)
    in_hundredths_of_milimeters = False  # False => INTHOUSANDTHSOFINCHES units of papersize
    papersizex = 8270  # default A4 size (210x292 mm)
    papersizey = 11690  # default A4 size (210x292 mm)
    width = None  # Page width, pixels
    height = None  # Page height, pixels
    extratop = 0  # Height of title line, pixels
    extrabottom = 0  # Height of info line, pixels
    printable_width = None  # printable area in the pixels of printer's resolution
    printable_height = None  # printable area in the pixels of printer's resolution

    # margins
    printborder = False  # Print border around bitmap
    border = None  # Border around the data grid, pixels
    bordertop = 0  # Top page border, pixels
    borderleft = 0  # Left page border, pixels
    borderright = 0  # Right page border, pixels
    borderbottom = 0  # Bottom page border, pixels
    have_margins = False  # Does have page set margins?
    margintop = 0  # Top printer page margin
    marginleft = 0  # Left printer page margin
    marginright = 0  # Right printer page margin
    marginbottom = 0  # Bottom printer page margin

    # dot
    dpi = 200  # Dot raster, dots per inch
    dpipercent = 70  # Dot size, percent of dpi

    # blocks
    ny = None  # Number of blocks in y axis
    nx = None  # Number of blocks in x axis
    pagesize = None  # Size of (compressed) data on page

    # File
    data = None
    superdata = None

    path = None  # path to file
    name = None  # name of file

    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path)
        if len(self.name) > 64:
            raise ValueError("Name is too long.")

    def get_file_info(self):
        """Get metadtata of file.

        Metadata:
        * Attributes
        * Time of last modification
        * Size

        https://github.com/BrnoPCmaniak/python-paperbak/blob/dfba2a395bfeec4dafe9566afa4eb96c68771423/old_cpp/Printer.cpp#L276-L297  #NOQA
        """
        result = os.stat(self.path)
        self.attributes = getattr(result, "st_file_attributes", FILE_ATTRIBUTE_NORMAL)
        self.mtime = datetime.utcfromtimestamp(result.st_mtime)
        self.origsize = result.st_size
        if self.origsize > MAXSIZE:
            raise ValueError("File is too big.")

    def compress_data(self):
        """Compress the file data by bzip2.

        https://github.com/BrnoPCmaniak/python-paperbak/blob/dfba2a395bfeec4dafe9566afa4eb96c68771423/old_cpp/Printer.cpp#L325-L429  #NOQA
        """
        self.data = bz2.compress(self.data, compresslevel=self.compression_level)
        self.datasize = len(self.data)

    def calc_filecrc(self):
        self.filecrc = crc16(self.data)

    def make_superdata(self):
        """Prepare superdata block.

        https://github.com/BrnoPCmaniak/python-paperbak/blob/dfba2a395bfeec4dafe9566afa4eb96c68771423/old_cpp/Printer.cpp#L510-L531  #NOQA
        """
        self.superdata = SuperData()
        self.superdata.datasize = self.alignedsize
        self.superdata.origsize = self.origsize
        self.superdata.pbm_compressed = self.compressed
        self.superdata.pbm_encrypted = self.encrypted
        self.superdata.attributes = self.attributes & (
            FILE_ATTRIBUTE_READONLY | FILE_ATTRIBUTE_HIDDEN | FILE_ATTRIBUTE_SYSTEM |
            FILE_ATTRIBUTE_ARCHIVE | FILE_ATTRIBUTE_NORMAL)
        self.superdata.modified = self.mtime
        self.superdata.filecrc = self.filecrc
        if self.encrypted:
            if len(self.name) > 31:
                raise ValueError("Name can be only 31 characters long if encryption is enabled.")
            # don't overwrite the salt and iv
            self.superdata.name = self.name + "\0" * (32 - len(self.name)) + self.superdata.name
        else:
            self.superdata.name = self.name

    def calc_page_size(self):
        """Calculate the page size in px from printer resolution.

        https://github.com/BrnoPCmaniak/python-paperbak/blob/dfba2a395bfeec4dafe9566afa4eb96c68771423/old_cpp/Printer.cpp#L630-L635  #NOQA
        """
        if self.in_hundredths_of_milimeters:
            self.width = self.pagesizex * self.resx / 2540
            self.height = self.papersizey * self.resy / 2540
        else:
            self.width = self.pagesizex * self.resx / 1000
            self.height = self.papersizey * self.resy / 1000

    def calc_borders(self):
        """Calculate page borders in the pixels of printer's resolution.

        https://github.com/BrnoPCmaniak/python-paperbak/blob/dfba2a395bfeec4dafe9566afa4eb96c68771423/old_cpp/Printer.cpp#L646-L660  #NOQA
        """
        if self.have_margins:
            if self.in_hundredths_of_milimeters:
                self.borderleft = self.marginleft * self.resx / 2540
                self.borderright = self.marginright * self.resx / 2540
                self.bordertop = self.margintop * self.resy / 2540
                self.borderbottom = self.marginbottom * self.resy / 2540
            else:
                self.borderleft = self.marginleft * self.resx / 1000
                self.borderright = self.marginright * self.resx / 1000
                self.bordertop = self.margintop * self.resy / 1000
                self.borderbottom = self.marginbottom * self.resy / 1000
        else:
            self.borderleft = self.resx  # In original code there is no "/2" dunno why
            self.borderright = self.resx / 2
            self.bordertop = self.resy / 2
            self.borderbottom = self.resy / 2

    def calc_printable_area(self):
        """Calculate size of printable area, in the pixels of printer's resolution.

        https://github.com/BrnoPCmaniak/python-paperbak/blob/dfba2a395bfeec4dafe9566afa4eb96c68771423/old_cpp/Printer.cpp#L661-L665  #NOQA
        """
        self.printable_width = self.width - (self.borderleft + self.borderright)
        self.printable_height = self.height - \
            (self.bordertop + self.borderbottom + self.extratop + self.extrabottom)

    def calc_dot_size(self):
        """Calculate data point raster and size of point.

        Calculate data point raster (dx,dy) and size of the point (px,py) in the
        pixels of printer's resolution. Note that pixels, at least in theory, may
        be non-rectangular.

        https://github.com/BrnoPCmaniak/python-paperbak/blob/dfba2a395bfeec4dafe9566afa4eb96c68771423/old_cpp/Printer.cpp#L666-L672  #NOQA
        """

        self.dx = max(self.resx / self.dpi, 2)
        self.px = max((self.dx * self.dotpercent) / 100, 1)
        self.dy = max(self.resy / self.dpi, 2)
        self.py = max((self.dy * self.dotpercent) / 100, 1)

    def calc_border(self):
        """Calculate width of the border around the data grid.

        https://github.com/BrnoPCmaniak/python-paperbak/blob/dfba2a395bfeec4dafe9566afa4eb96c68771423/old_cpp/Printer.cpp#L673-L679  #NOQA
        """
        self.border = self.sx * 16 if self.printborder else 0

    def calc_number_of_blocks(self):
        """Calculate the number of data blocks that fit onto the single page.

        Single page must contain at least redundancy data blocks plus 1 recovery checksum,
        and redundancy+1 superblocks with name and size of the data. Data and recovery blocks
        should be placed into different columns.

        https://github.com/BrnoPCmaniak/python-paperbak/blob/dfba2a395bfeec4dafe9566afa4eb96c68771423/old_cpp/Printer.cpp#L680-L689  #NOQA
        """
        self.nx = (self.printable_width - self.px - 2 * self.border) / \
            (NDOT * self.dx + 3 * self.dx)
        self.ny = (self.printable_height - self.py - 2 * self.border) / \
            (NDOT * self.dy + 3 * self.dy)
        if self.nx < self.redundancy + 1 or self.ny < 3 or \
                self.nx * self.ny < 2 * self.redundancy + 2:
            raise ValueError("Printable area is too small, reduce borders or block size.")

    def calc_bitmap_size(self):
        """Calculate final size of the bitmap where to draw the image.

        https://github.com/BrnoPCmaniak/python-paperbak/blob/dfba2a395bfeec4dafe9566afa4eb96c68771423/old_cpp/Printer.cpp#L690-L692  #NOQA
        """
        self.bitmap_width = (self.nx * (NDOT + 3) * self.dx +
                             self.px + 2 * self.border + 3) & 0xFFFFFFFC
        self.bitmap_height = self.ny * (NDOT + 3) * self.dy + self.py + 2 * self.border

    def calc_data_page_size(self):
        """Calculate the total size of useful data, bytes, that fits onto the page.

        For each redundancy blocks, I create one recovery block. For each chain, I
        create one superblock that contains file name and size, plus at least one
        superblock at the end of the page.

        https://github.com/BrnoPCmaniak/python-paperbak/blob/dfba2a395bfeec4dafe9566afa4eb96c68771423/old_cpp/Printer.cpp#L730-L736  #NOQA
        """
        self.pagesize = ((self.nx * self.ny - self.redundancy - 2) /
                         (self.redundancy + 1)) * self.redundancy * NDATA
        self.superdata.pagesize = self.pagesize

    def print_file(self, out_path):
        if not NGROUPMIN <= self.redundancy <= NGROUPMAX:
            raise ValueError("Redundancy is too big or too small.")

        self.get_file_info()

        with open(self.path, "rb") as file:
            self.data = file.read()

        if self.origsize != len(self.data):
            self.origsize = len(self.data)
            # TODO: Log warning.

        if self.compressed:
            self.compress_data()
        else:
            self.datasize = self.origsize

        # Align size of (compressed) data to next 16-byte border. Note that bzip2
        # doesn't mind if data passed to decompressor is longer than expected.
        # https://github.com/BrnoPCmaniak/python-paperbak/blob/dfba2a395bfeec4dafe9566afa4eb96c68771423/old_cpp/Printer.cpp#L415-L420  #NOQA
        self.alignedsize = (self.datasize + 15) & 0xFFFFFFF0
        self.data = self.data + bytes(self.alignedsize)

        # TODO: encryption
        # https://github.com/BrnoPCmaniak/python-paperbak/blob/dfba2a395bfeec4dafe9566afa4eb96c68771423/old_cpp/Printer.cpp#L431-L498  #NOQA
        if self.encrypted:
            raise NotImplemented("Encryption is not implemented yet.")

        self.calc_filecrc()
        self.make_superdata()
        self.calc_page_size()
        # TODO: Calculate height of title and info lines on the paper. If printheader or printborder
        # https://github.com/BrnoPCmaniak/python-paperbak/blob/dfba2a395bfeec4dafe9566afa4eb96c68771423/old_cpp/Printer.cpp#L584-L616  #NOQA
        self.calc_borders()
        self.calc_printable_area()
        self.calc_dot_size()
        self.calc_border()
        self.calc_number_of_blocks()
