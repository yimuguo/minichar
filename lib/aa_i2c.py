import struct
import sys
if struct.calcsize("P") * 8 == 32:
    from lib.Aardvark.win32.aardvark_py import *
else:
    from lib.Aardvark.x64.aardvark_py import *


class AAReadWrite:
    length = 106
    bitrate = 400   # Khz
    bus_timeout = 150   # ms

    def __init__(self, port, i2c_add, pullup=False):
        if i2c_add is str:
            self.i2c_add = int(i2c_add, 16)
        self.pullup = pullup
        self.handle = aa_open(port)
        if self.handle <= 0:
            print "Unable to open Aardvark device on port %d" % port
            print "Error code = %d" % self.handle
            sys.exit()
        self.aa_init()

    def aa_init(self):

        # Ensure that the I2C subsystem is enabled
        aa_configure(self.handle, AA_CONFIG_SPI_I2C)
        
        # Enable the I2C bus pullup resistors (2.2k resistors).
        # This command is only effective on v2.0 hardware or greater.
        # The pullup resistors on the v1.02 hardware are enabled by default.
        if self.pullup is True:
            aa_i2c_pullup(self.handle, AA_I2C_PULLUP_BOTH)
        elif self.pullup is False:
            aa_i2c_pullup(self.handle, AA_I2C_PULLUP_NONE)
        
        # Power the EEPROM using the Aardvark adapter's power supply.
        # This command is only effective on v2.0 hardware or greater.
        # The power pins on the v1.02 hardware are not enabled by default.
        aa_target_power(self.handle, AA_TARGET_POWER_NONE)
        
        # Set the self.bitrate
        self.bitrate = aa_i2c_bitrate(self.handle, self.bitrate)
        print "Bitrate set to %d kHz" % self.bitrate
        
        # Set the bus lock timeout
        bus_timeout = aa_i2c_bus_timeout(self.handle, self.bus_timeout)
        print "Bus lock timeout set to %d ms" % bus_timeout

    def aa_write_i2c(self, str_addr, wrt_lst):
        # Write to the I2C EEPROM
        #
        # The AT24C02 EEPROM has 8 byte pages.  Data can written
        # in pages, to reduce the number of overall I2C transactions
        # executed through the Aardvark adapter.
        if str_addr is str:
            wrt_lst.insert(int(str_addr, 16), wrt_lst)
        for x in range(len(wrt_lst)):
            if wrt_lst[x] is str:
                wrt_lst[x] = int(x, 16)
            elif wrt_lst[x] is hex:
                wrt_lst[x] = int(wrt_lst)
        aa_i2c_write(self.handle, self.i2c_add, AA_I2C_NO_FLAGS, array('B', wrt_lst))
        aa_sleep_ms(10)
    
    def aa_read_i2c(self, str_addr):
        # Write the address
        aa_i2c_write(self.handle, self.i2c_add, AA_I2C_NO_STOP, array('B', [str_addr & 0xff]))
        (count, data_in) = aa_i2c_read(self.handle, self.i2c_add, AA_I2C_NO_FLAGS, self.length)
        if count < 0:
            print "error: %s" % aa_status_string(count)
            return
        elif count == 0:
            print "error: no bytes read"
            print "  are you sure you have the right slave address?"
            return
        elif count != self.length:
            print "error: read %d bytes (expected %d)" % (count, self.length)
        sys.stdout.write("\nData read from device:")
        for i in range(count):
            if (i & 0x0f) == 0:
                sys.stdout.write("\n%04x:  " % (self.i2c_add+i))
            sys.stdout.write("%02x " % (data_in[i] & 0xff))
            if ((i+1) & 0x07) == 0:
                sys.stdout.write(" ")
        # Dump the data to the screen
        return data_in
