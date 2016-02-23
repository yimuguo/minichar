from lib.vc5_summary import VC5Get
from lib.aa_i2c import *
# ===================Read Specific Summary File From Input==================
CFG_NUM = int(sys.argv[2])
file_input = sys.argv[1]
vc5 = VC5Get(file_input, 1, True)
# ==========================================================================
# I2C R/W MAIN PROGRAM
# ==========================================================================
device = int(vc5.i2c_address, 16)/2

    if self.i2c_add == 'D0':
        aa_i2c_write(self.handle, device, AA_I2C_NO_FLAGS, array('B', array('B', [0, 96])))

    vc5_write_reg = [x for x in vc5.conf[CFG_NUM] if x != '']
# Perform the operation
vc5_read = vc5_read_i2c(handle, device, addr, length)
for i in range(0, len(vc5_read)):
    if vc5_read[i] != write2aa[i+1]:
        print("Read Back Does not Match File!")

# Close the device
aa_close(handle)
