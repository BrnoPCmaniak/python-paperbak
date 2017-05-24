# Notes about code structure of `old_cpp`

- [x] `BZLIB` - unchanged bzip2/libbzip2 version 1.0.6
- [ ] `CRYPTO` - AES is in nasm assembler after recompile might work, SHA looks like pure c++ so after recompile might work _(as encryption is not crucial at the moment I took only brief look into theese two.)_
- [ ] `Controls.cpp` - UI logic - borland dependent
- [x] `Crc16.cpp` - [CRC-CCITT](https://en.wikipedia.org/wiki/Cyclic_redundancy_check) 16 bit Cyclic redundancy check - after removing win headers should work
- [ ] `Decoder.cpp` - **Nextdataprocessingstep** The main decoding logic, after removing GUI stuff can be used
- [x] `Ecc.cpp` - [Reed–Solomon error correction](https://en.wikipedia.org/wiki/Reed%E2%80%93Solomon_error_correction)
- [ ] `Fileproc.cpp`- Handling files + pages
- [ ] `Main.cpp` highly borderland dependent - Updating buttons setting up windows
- [ ] `Printer.cpp` - Printer UI + Drawing data into bitmap
- [ ] `Scanner.cpp` - Scanner UI + Load Bitmap
- [ ] `Service.cpp` - File related routines + Queue

# Useful links

* How to set file attributes in python http://stackoverflow.com/a/28519209/2629036 
