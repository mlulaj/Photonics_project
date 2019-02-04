import numpy as np
from mylibrary.carrier import carrier


class Spectralinformation:
    # Constructor
    def __init__(self, n_channels=0,bandwidth=None, start_frequency=None, frequency_offset=None,
                 power_inf={'signal': float, 'ase': float, 'nli': float}):
        # Attributes
        self.n_channels = n_channels               # number of channels
        self.start_frequency = start_frequency     # central freq first channel
        self.frequency_offset = frequency_offset   # between two adjacent channels
        self.carriers_list = []                    # list of Carrier
        self.bandwidth = bandwidth

        for i in range(0, n_channels):
            id_temp = i + 1
            freq_temp = start_frequency + frequency_offset * i
            carr_temp = carrier(number=id_temp, frequency=freq_temp,bandwidth=bandwidth, power=dict(power_inf))
            self.carriers_list.append(carr_temp)

    # Method
    def snr(self):
        x_snr = np.empty(self.n_channels, dtype=float)
        for i in range(0, self.n_channels):
            x_snr[i] = self.carriers_list[i].snr()
        return x_snr

    def osnr(self):
        x_osnr = np.empty(self.n_channels, dtype=float)
        for i in range(0, self.n_channels):
            x_osnr[i] = self.carriers_list[i].osnr()
        return x_osnr

    def snr_nl(self):
        x_snr_nl = np.empty(self.n_channels, dtype=float)
        for i in range(0, self.n_channels):
            x_snr_nl[i] = self.carriers_list[i].snr_nl()
        return x_snr_nl

