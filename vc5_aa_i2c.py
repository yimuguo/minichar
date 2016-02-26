from lib.vc5_summary import VC5Get
from lib.aa_i2c import AAReadWrite
import sys
# ===================Read Specific Summary File From Input==================
CFG_NUM = int(sys.argv[2])
FILE_INPUT = sys.argv[1]


# ===================Create VC5 Object from Summary=========================
class VC5ReadWriteAA(AAReadWrite):

    def __init__(self, summary_path, cfgnum):
        self.cfgnum = cfgnum
        self.vc5 = VC5Get(summary_path, 1, True)
        self.device = int(self.vc5.i2c_address, 16)/2
        super(VC5ReadWriteAA, self).__init__(0, self.device)
        self.write_addr()
        self.wrt_vc5_cfg(self.cfgnum)
        self.rw_compare(self.cfgnum)
        self.close()

    def write_addr(self):
        self.length = 1
        if self.vc5.i2c_address == 'D0':
            try:
                self.i2c_add = 0x6a
                self.aa_read_i2c(0)
                self.aa_write_i2c(0, [0x60])
            except ValueError:
                self.i2c_add = 0x68
                self.aa_read_i2c(0)
        elif self.vc5.i2c_address == 'D4':
            try:
                self.aa_read_i2c(0)
            except ValueError:
                self.i2c_add = 0x68
                self.aa_read_i2c(0)
                self.aa_write_i2c(0, [0x61])
        self.i2c_add = self.device
        self.length = 106

    def wrt_vc5_cfg(self, cfgnum):
        # First Configure First I2C Add Register
        vc5_write_reg = [x for x in self.vc5.conf[cfgnum] if x != '']
        # Write Configs into the Chip
        self.aa_write_i2c(0, vc5_write_reg)
        # Read and Confirm the Strings Match Summary

    # Close the device
    def rw_compare(self, cfgnum):
        match_flag = True
        vc5_read = self.aa_read_i2c(0)
        for i in range(0, len(vc5_read)):
            if vc5_read[i] != int(self.vc5.conf[cfgnum][i], 16):
                match_flag = False
                print("Byte %s Read Back Does not Match File!\n", str(i))
        if match_flag:
            print("\nReadback Match")
        else:
            raise Warning("Read Back does NOT MATCH")


def main():
    VC5ReadWriteAA(FILE_INPUT, CFG_NUM)

if __name__ == '__main__':
    main()
