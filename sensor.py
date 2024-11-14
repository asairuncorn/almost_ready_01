from time import sleep
import Adafruit_ADS1x15

class PresureSensor:
    def __init__(self):



        #Gain = 2/3 for reading voltages from 0 to 6.144V.
        #See table 3 in ADS1115 datasheet
        self.volts = None
        self.adc = None
        self.psi = 0
        self.GAIN = 2 / 3
        self.value = [0]


    def read_data(self):

        self.adc = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1)

# Read ADC channel 0
        self.value[0] = self.adc.read_adc(0, gain=self.GAIN)
# Ratio of 15 bit value to max volts determines volts
        self.volts = self.value[0] / 32767.0 * 6.144
# Tests shows linear relationship between psi & voltage:
        self.psi = 50.0 * self.volts - 25.0
# Bar conversion
      #  bar = psi * 0.0689475729

        print("Voltage: {0:0.3f}V, PSI: {1:0.0f}".format(self.volts, self.psi))

        return self.psi

