class carrier:

    def __init__(self, number,frequency,bandwidth,power={'signal': 0.0, 'ase': 0.0, 'nli': 0.0},latency=0.0):
    #Attributes
        self.number = number
        self.frequency =frequency
        self.bandwidth =bandwidth
        self.power = power
        self.latency = latency
    #Method

    def snr(self):
        return self.power['signal'] / (self.power['nli'] + self.power['ase'])

    def osnr(self):
        return self.power['signal'] / self.power['ase']

    def snr_nl(self):
        return self.power['signal'] / self.power['nli']