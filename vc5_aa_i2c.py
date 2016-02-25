from lib.vc5_summary import VC5Get
from lib.aa_i2c import AAReadWrite
import sys
# ===================Read Specific Summary File From Input==================
CFG_NUM = int(sys.argv[2])
FILE_INPUT = sys.argv[1]


# ===================Create VC5 Object from Summary=========================
class VC5ReadWriteAA(AAReadWrite):

    def __init__(self, summaryfilepath, cfgnum):
        self.file = summaryfilepath
        self.cfgnum = cfgnum
        self.vc5 = VC5Get(self.file, 1, True)
        self.device = int(self.vc5.i2c_address, 16)/2
        # Initiate Aardvark and Setup I2C Comm Speed
        super(VC5ReadWriteAA, self).__init__(0, self.device)
        self.write_addr()
        self.wr_vc5_cfg(self.cfgnum)
        self.vc5_read = self.rd_vc5_cfg()
        self.rw_compare(self.cfgnum)
        self.close()

    def write_addr(self):
        if self.vc5.i2c_address == 'D0':
            self.i2c_add = 0x6a
            self.aa_write_i2c(0, [0x60])
            self.i2c_add = self.device

    def rd_vc5_cfg(self):
        return self.aa_read_i2c(0)

    def wr_vc5_cfg(self, cfgnum):
        # First Configure First I2C Add Register
        vc5_write_reg = [x for x in self.vc5.conf[cfgnum] if x != '']
        # Write Configs into the Chip
        self.aa_write_i2c(0, vc5_write_reg)
        # Read and Confirm the Strings Match Summary

    # Close the device
    def rw_compare(self, cfgnum):
        for i in range(0, len(self.vc5_read)):
            if self.vc5_read[i] != int(self.vc5.conf[cfgnum][i], 16):
                print("Read Back Does not Match File!")
                sys.exit()


def main():
    VC5ReadWriteAA(FILE_INPUT, CFG_NUM)

main()
