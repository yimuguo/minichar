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
# Initiate Aardvark and Setup I2C Comm Speed
rw_vc5 = AAReadWrite(0, device)
# First Configure First I2C Add Register
if vc5.i2c_address == 'D0':
    aa_i2c_write(rw_vc5.handle, 0x6a, AA_I2C_NO_FLAGS, array('B', array('B', [0, 96])))
vc5_write_reg = [x for x in vc5.conf[CFG_NUM] if x != '']
# Write Configs into the Chip
rw_vc5.aa_write_i2c(0, vc5_write_reg)
# Read and Confirm the Strings Match Summary
vc5_read = rw_vc5.aa_read_i2c(0)
for i in range(0, len(vc5_read)):
    if vc5_read[i] != int(vc5.conf[CFG_NUM][i], 16):
        print("Read Back Does not Match File!")
        sys.exit()

# Close the device
rw_vc5.close()
