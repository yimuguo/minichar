import struct
import sys
from array import array, ArrayType

# ==========================================================================
AA_API_VERSION = 0x050a  # v5.10
AA_REQ_SW_VERSION = 0x050a  # v5.10


# ==========================================================================
# HELPER FUNCTIONS
# ==========================================================================
def array_u08(n): return array('B', '\0' * n)


def array_u16(n): return array('H', '\0\0' * n)


def array_u32(n): return array('I', '\0\0\0\0' * n)


def array_u64(n): return array('K', '\0\0\0\0\0\0\0\0' * n)


def array_s08(n): return array('b', '\0' * n)


def array_s16(n): return array('h', '\0\0' * n)


def array_s32(n): return array('i', '\0\0\0\0' * n)


def array_s64(n): return array('L', '\0\0\0\0\0\0\0\0' * n)


def array_f32(n): return array('f', '\0\0\0\0' * n)


def array_f64(n): return array('d', '\0\0\0\0\0\0\0\0' * n)


try:
    import lib.Aardvark.x64.aardvark as api
except ImportError, ex1:
    import imp
    import platform
    # ext = platform.system() in ('Windows', 'Microsoft') and '.dll' or '.so'
    ext = '.dll'
    try:
        if struct.calcsize("P") * 8 == 32:
            api = imp.load_dynamic('aardvark', '.\\lib\\Aardvark\\win32\\aardvark' + ext)
        else:
            api = imp.load_dynamic('aardvark', '.\\lib\\Aardvark\\x64\\aardvark' + ext)
    except ImportError, ex2:
        import_err_msg = 'Error importing aardvark%s\n' % ext
        import_err_msg += '  Architecture of aardvark%s may be wrong\n' % ext
        import_err_msg += '%s\n%s' % (ex1, ex2)
        raise ImportError(import_err_msg)

AA_SW_VERSION = api.py_version() & 0xffff
AA_REQ_API_VERSION = (api.py_version() >> 16) & 0xffff
AA_LIBRARY_LOADED = \
    ((AA_SW_VERSION >= AA_REQ_SW_VERSION) and
     (AA_API_VERSION >= AA_REQ_API_VERSION))
AA_INCOMPATIBLE_LIBRARY = -4

# Configure the I2C pullup resistors.
# This is only supported on hardware versions >= 2.00
AA_I2C_PULLUP_NONE = 0x00
AA_I2C_PULLUP_BOTH = 0x03
AA_I2C_PULLUP_QUERY = 0x80


def aa_i2c_pullup(aardvark, pullup_mask):
    """usage: int return = aa_i2c_pullup(aardvark, u08 pullup_mask)"""

    if not AA_LIBRARY_LOADED: return AA_INCOMPATIBLE_LIBRARY
    # Call API function
    return api.py_aa_i2c_pullup(aardvark, pullup_mask)


# Configure the target power pins.
# This is only supported on hardware versions >= 2.00
AA_TARGET_POWER_NONE = 0x00
AA_TARGET_POWER_BOTH = 0x03
AA_TARGET_POWER_QUERY = 0x80


def aa_target_power(aardvark, power_mask):
    """usage: int return = aa_target_power(Aardvark aardvark, u08 power_mask)"""

    if not AA_LIBRARY_LOADED: return AA_INCOMPATIBLE_LIBRARY
    # Call API function
    return api.py_aa_target_power(aardvark, power_mask)


# Sleep for the specified number of milliseconds
# Accuracy depends on the operating system scheduler
# Returns the number of milliseconds slept
def aa_sleep_ms(milliseconds):
    """usage: u32 return = aa_sleep_ms(u32 milliseconds)"""

    if not AA_LIBRARY_LOADED: return AA_INCOMPATIBLE_LIBRARY
    # Call API function
    return api.py_aa_sleep_ms(milliseconds)


# Set the I2C bit rate in kilohertz.  If a zero is passed as the
# bitrate, the bitrate is unchanged and the current bitrate is
# returned.
def aa_i2c_bitrate(aardvark, bitrate_khz):
    """usage: int return = aa_i2c_bitrate(Aardvark aardvark, int bitrate_khz)"""

    if not AA_LIBRARY_LOADED: return AA_INCOMPATIBLE_LIBRARY
    # Call API function
    return api.py_aa_i2c_bitrate(aardvark, bitrate_khz)


# Read a stream of bytes from the I2C slave device.
def aa_i2c_read(aardvark, slave_addr, flags, data_in):
    """usage: (int return, u08[] data_in) = aa_i2c_read(Aardvark aardvark, u16 slave_addr,
    AardvarkI2cFlags flags, u08[] data_in)

    All arrays can be passed into the API as an ArrayType object or as
    a tuple (array, length), where array is an ArrayType object and
    length is an integer.  The user-specified length would then serve
    as the length argument to the API funtion (please refer to the
    product datasheet).  If only the array is provided, the array's
    intrinsic length is used as the argument to the underlying API
    function.

    Additionally, for arrays that are filled by the API function, an
    integer can be passed in place of the array argument and the API
    will automatically create an array of that length.  All output
    arrays, whether passed in or generated, are passed back in the
    returned tuple."""

    if not AA_LIBRARY_LOADED: return AA_INCOMPATIBLE_LIBRARY
    # data_in pre-processing
    __data_in = isinstance(data_in, int)
    if __data_in:
        (data_in, num_bytes) = (array_u08(data_in), data_in)
    else:
        (data_in, num_bytes) = isinstance(data_in, ArrayType) and (data_in, len(data_in)) or (
        data_in[0], min(len(data_in[0]), int(data_in[1])))
        if data_in.typecode != 'B':
            raise TypeError("type for 'data_in' must be array('B')")
    # Call API function
    (_ret_) = api.py_aa_i2c_read(aardvark, slave_addr, flags, num_bytes, data_in)
    # data_in post-processing
    if __data_in: del data_in[max(0, min(_ret_, len(data_in))):]
    return (_ret_, data_in)


# Write a stream of bytes to the I2C slave device.
def aa_i2c_write(aardvark, slave_addr, flags, data_out):
    """usage: int return = aa_i2c_write(Aardvark aardvark, u16 slave_addr, AardvarkI2cFlags flags, u08[] data_out)

    All arrays can be passed into the API as an ArrayType object or as
    a tuple (array, length), where array is an ArrayType object and
    length is an integer.  The user-specified length would then serve
    as the length argument to the API funtion (please refer to the
    product datasheet).  If only the array is provided, the array's
    intrinsic length is used as the argument to the underlying API
    function."""

    if not AA_LIBRARY_LOADED: return AA_INCOMPATIBLE_LIBRARY
    # data_out pre-processing
    (data_out, num_bytes) = isinstance(data_out, ArrayType) and (data_out, len(data_out)) or (
    data_out[0], min(len(data_out[0]), int(data_out[1])))
    if data_out.typecode != 'B':
        raise TypeError("type for 'data_out' must be array('B')")
    # Call API function
    return api.py_aa_i2c_write(aardvark, slave_addr, flags, num_bytes, data_out)


def aa_open(port_number):
    """usage: Aardvark return = aa_open(int port_number)"""

    if not AA_LIBRARY_LOADED: return AA_INCOMPATIBLE_LIBRARY
    # Call API function
    return api.py_aa_open(port_number)


# Close the Aardvark port.
def aa_close(aardvark):
    """usage: int return = aa_close(Aardvark aardvark)"""

    if not AA_LIBRARY_LOADED: return AA_INCOMPATIBLE_LIBRARY
    # Call API function
    return api.py_aa_close(aardvark)


# Configure the device by enabling/disabling I2C, SPI, and
# GPIO functions.
# enum AardvarkConfig
AA_CONFIG_GPIO_ONLY = 0x00
AA_CONFIG_SPI_GPIO = 0x01
AA_CONFIG_GPIO_I2C = 0x02
AA_CONFIG_SPI_I2C = 0x03
AA_CONFIG_QUERY = 0x80

AA_CONFIG_SPI_MASK = 0x00000001
AA_CONFIG_I2C_MASK = 0x00000002


def aa_configure(aardvark, config):
    """usage: int return = aa_configure(Aardvark aardvark, AardvarkConfig config)
    :param aardvark: device object
    :param config: int ty """

    if not AA_LIBRARY_LOADED: return AA_INCOMPATIBLE_LIBRARY
    # Call API function
    return api.py_aa_configure(aardvark, config)


def aa_status_string(status):
    """usage: str return = aa_status_string(int status)"""

    if not AA_LIBRARY_LOADED: return AA_INCOMPATIBLE_LIBRARY
    # Call API function
    return api.py_aa_status_string(status)


# ==========================================================================
# I2C API
# ==========================================================================
# Free the I2C bus.
def aa_i2c_free_bus(aardvark):
    """usage: int return = aa_i2c_free_bus(Aardvark aardvark)
    :param aardvark: device object"""

    if not AA_LIBRARY_LOADED: return AA_INCOMPATIBLE_LIBRARY
    # Call API function
    return api.py_aa_i2c_free_bus(aardvark)


# Set the bus lock timeout.  If a zero is passed as the timeout,
# the timeout is unchanged and the current timeout is returned.
def aa_i2c_bus_timeout(aardvark, timeout_ms):
    """usage: int return = aa_i2c_bus_timeout(Aardvark aardvark, u16 timeout_ms)
    :param aardvark: device object
    :param timeout_ms: int unit(ms)"""

    if not AA_LIBRARY_LOADED: return AA_INCOMPATIBLE_LIBRARY
    # Call API function
    return api.py_aa_i2c_bus_timeout(aardvark, timeout_ms)


# enum AardvarkI2cFlags
AA_I2C_NO_FLAGS = 0x00
AA_I2C_10_BIT_ADDR = 0x01
AA_I2C_COMBINED_FMT = 0x02
AA_I2C_NO_STOP = 0x04
AA_I2C_SIZED_READ = 0x10
AA_I2C_SIZED_READ_EXTRA1 = 0x20


class AAReadWrite(object):
    length = 106
    bitrate = 400  # Khz
    bus_timeout = 150  # ms

    def __init__(self, port, i2c_add, pullup=False):
        if type(i2c_add) is str:
            self.i2c_add = int(i2c_add, 16)
            if self.i2c_add | 1000000 > 127:
                print("Aardvark Only use 7bit I2C address rather than 8bit\n"
                      "e.g. D4 is 0x6a")
        elif type(i2c_add) is int:
            self.i2c_add = i2c_add
        self.pullup = pullup
        self.handle = aa_open(port)
        if self.handle <= 0:
            print("Unable to open Aardvark device on port %d" % port)
            print("Error code = %d" % self.handle)
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
        # Write to the I2C Memory
        if type(str_addr) is str:
            wrt_lst.insert(0, int(str_addr, 16))
        elif type(str_addr) is int:
            wrt_lst.insert(0, str_addr)

        for x in range(len(wrt_lst)):
            if type(wrt_lst[x]) is str:
                wrt_lst[x] = int(wrt_lst[x], 16)
            elif type(wrt_lst[x]) is hex:
                wrt_lst[x] = int(wrt_lst[x])
        aa_i2c_write(self.handle, self.i2c_add, AA_I2C_NO_FLAGS, array('B', wrt_lst))
        aa_sleep_ms(10)

    def aa_read_i2c(self, str_addr):
        # Write the address
        aa_i2c_write(self.handle, self.i2c_add, AA_I2C_NO_STOP, array('B', [str_addr & 0xff]))
        (count, data_in) = aa_i2c_read(self.handle, self.i2c_add, AA_I2C_NO_FLAGS, self.length)
        if count < 0:
            print "error: %s" % aa_status_string(count)
            raise ValueError
        elif count == 0:
            print "error: no bytes read"
            print " please check device I2C address settings"
            raise ValueError
        elif count != self.length:
            print "error: read %d bytes (expected %d)" % (count, self.length)
            raise ValueError
        # sys.stdout.write("\nData read from device:")
        # for i in range(count):
        #     if (i & 0x0f) == 0:
        #         sys.stdout.write("\nByte 0x%02x to 0x%02x:  " % ((str_addr + i), (str_addr + i + 15)))
        #     sys.stdout.write("%02x " % (data_in[i] & 0xff))
        #     if ((i + 1) & 0x07) == 0:
        #         sys.stdout.write(" ")
        # Dump the data to the screen
        return data_in

    def close(self):
        aa_close(self.handle)
