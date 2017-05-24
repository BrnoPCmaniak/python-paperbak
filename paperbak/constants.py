"""Constatns for python-paperbak."""

NDATA = 90  # Number of data bytes in a block
NDOT = 32  # Block X and Y size, dots

NGROUP = 5 # For NGROUP blocks (1..15), 1 recovery
NGROUPMIN = 2
NGROUPMAX = 10

# Special address
MAXSIZE = 0x0FFFFF80  # Maximal (theoretical) length of file
SUPERBLOCK = 0xFFFFFFFF  # Address of superblock
