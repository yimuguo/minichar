import visa
from lib.aa_i2c import AAReadWrite
import time


class SweepTempVCO(object):
    def __init__(self):
        self.dut_i2c = AAReadWrite(0, 0x68, True)
        self.power = visa.ResourceManager().open_resource('GPIB0::13::INSTR')
        self.freq = visa.ResourceManager().open_resource('GPIB0::3::INSTR')
        self.dut_i2c.length = 1
        self.power.write("APPL P6V,5,0.3")
        self.power.write("APPL P25V,3.3,0.2")
        self.chamber = visa.ResourceManager().open_resource('GPIB0::1::INSTR')

    def cal_vco(self):
        self.dut_i2c.aa_write_i2c(40, [0])
        self.dut_i2c.aa_write_i2c(26, [0])
        self.dut_i2c.aa_write_i2c(26, [0x80])
        vco_band = list(self.dut_i2c.aa_read_i2c(47))
        return vco_band[0]

    def power_on(self, on=True):
        if on:
            self.power.write("OUTPUT:STATe ON")
        else:
            self.power.write("OUTPUT:STATe OFF")

    def freq_counter(self):
        self.freq.write(':SENSe:DATA?')
        curr_freq = self.freq.read()
        return float(curr_freq)

    def set_temp(self, temp):
        self.chamber.write('TEMP, S' + str(temp))
        time.sleep(0.5)

    def read_temp(self):
        self.chamber.write('TEMP?')
        time.sleep(0.1)
        read_val = self.chamber.read()
        time.sleep(0.5)
        return float(read_val.split(',')[0])


def main():
    ak692 = SweepTempVCO()
    time.sleep(0.01)
    ak692.power_on(False)
    start_temp = -50
    stop_temp = 95
    tol_temp = 3

    ak692.set_temp(start_temp)

    for temp in range(start_temp, stop_temp, 10):
        curr_temp = ak692.read_temp()
        while not((curr_temp < temp + tol_temp) and (curr_temp > temp - tol_temp)):
            curr_temp = ak692.read_temp()
        frequency = ak692.freq_counter()
        vco_band = ak692.dut_i2c.aa_read_i2c(47)[0]
        print(str(temp) + '\t' + str(frequency) + '\t' + str(vco_band))
        if temp == start_temp:
            ak692.set_temp(stop_temp)

if __name__ == '__main__':
    main()
