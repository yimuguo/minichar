from lib.vc5_summary import VC5Get
from lib.aa_i2c import *
# ===================Read Specific Summary File From Input==================
file_input = sys.argv[0]
vc5 = VC5Get(file_input, 1, True)

# ==========================================================================
# I2C R/W MAIN PROGRAM
# ==========================================================================
port = 0
bitrate = 400
device = 0x6a
addr = 00
length = 106

handle = aa_open(port)
if (handle <= 0):
    print "Unable to open Aardvark device on port %d" % port
    print "Error code = %d" % handle
    sys.exit()

# Ensure that the I2C subsystem is enabled
aa_configure(handle, AA_CONFIG_SPI_I2C)

# Enable the I2C bus pullup resistors (2.2k resistors).
# This command is only effective on v2.0 hardware or greater.
# The pullup resistors on the v1.02 hardware are enabled by default.
aa_i2c_pullup(handle, AA_I2C_PULLUP_NONE)

# Power the EEPROM using the Aardvark adapter's power supply.
# This command is only effective on v2.0 hardware or greater.
# The power pins on the v1.02 hardware are not enabled by default.
aa_target_power(handle, AA_TARGET_POWER_NONE)

# Set the bitrate
bitrate = aa_i2c_bitrate(handle, bitrate)
print "Bitrate set to %d kHz" % bitrate

# Set the bus lock timeout
bus_timeout = aa_i2c_bus_timeout(handle, BUS_TIMEOUT)
print "Bus lock timeout set to %d ms" % bus_timeout

# Perform the operation
vc5_read = vc5_read_i2c(handle, device, addr, length)
print vc5_read
# Close the device
aa_close(handle)
