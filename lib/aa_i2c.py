#!/bin/env python
import struct
import sys
if struct.calcsize("P") * 8 == 32:
    from lib.Aardvark.win32.aardvark_py import *
else:
    from lib.Aardvark.x64.aardvark_py import *
# CONSTANTS
BUS_TIMEOUT = 150  # ms
PAGE_SIZE = 8
# ==========================================================================
# FUNCTIONS
# ==========================================================================


def vc5_write_i2c(handle, device, addr, length, zero):
    # Write to the I2C EEPROM
    #
    # The AT24C02 EEPROM has 8 byte pages.  Data can written
    # in pages, to reduce the number of overall I2C transactions
    # executed through the Aardvark adapter.
    n = 0
    while (n < length):
        data_out = array('B', [0 for i in range(1 + PAGE_SIZE)])

        # Fill the packet with data
        data_out[0] = addr & 0xff
        # Assemble a page of data
        i = 1
        while 1:
            if not (zero): data_out[i] = n & 0xff
            addr = addr + 1
            n += 1
            i = i + 1
            if not (n < length and (addr & (PAGE_SIZE - 1))): break
        # Truncate the array to the exact data size
        del data_out[i:]
        # Write the address and data
        aa_i2c_write(handle, device, AA_I2C_NO_FLAGS, data_out)
        aa_sleep_ms(10)


def vc5_read_i2c(handle, device, addr, length):
    # Write the address
    aa_i2c_write(handle, device, AA_I2C_NO_STOP, array('B', [addr & 0xff]))
    (count, data_in) = aa_i2c_read(handle, device, AA_I2C_NO_FLAGS, length)
    if (count < 0):
        print "error: %s" % aa_status_string(count)
        return
    elif (count == 0):
        print "error: no bytes read"
        print "  are you sure you have the right slave address?"
        return
    elif (count != length):
        print "error: read %d bytes (expected %d)" % (count, length)
    # Dump the data to the screen
    sys.stdout.write("\nData read from device:")
    return data_in
