import numpy as np
import matplotlib.pyplot as plt
from mylibrary.Spectral_information_1 import Spectralinformation


def main():
    n_ch = 91                   # number of channels
    BW_3dB = 32e9               # -3dB bandwidth
    first_central_f = 191.6e12  # first central frequency
    off_f = 50e9                # frequency offset
    p_ch = 0.5e-3               # power per channel
    p_ase = 4e-6                # ASE noise
    p_nli = 2e-6                # NLI

    power_dict = {'signal': p_ch, 'ase': p_ase, 'nli': p_nli}  # dictionary

    # first achievement

    sp = Spectralinformation(n_channels=n_ch, start_frequency=first_central_f,
                             frequency_offset=off_f, power_inf=power_dict,bandwidth=BW_3dB)

    # second and third achievements

    x = np.empty(n_ch, dtype=float)
    y_signal = np.empty(n_ch, dtype=float)
    y_ase = np.empty(n_ch, dtype=float)
    y_nli = np.empty(n_ch, dtype=float)

    for i in range(0, n_ch):
        x[i] = sp.carriers_list[i].frequency / 10 ** 12
        y_signal[i] = 10 * np.log10(sp.carriers_list[i].power['signal'] * 10 ** 3)
        y_ase[i] = 10 * np.log10(sp.carriers_list[i].power['ase'] * 10 ** 3)
        y_nli[i] = 10 * np.log10(sp.carriers_list[i].power['nli'] * 10 ** 3)

    y_snr = 10 * np.log10(sp.snr())
    y_osnr = 10 * np.log10(sp.osnr())
    y_snr_nl = 10 * np.log10(sp.snr_nl())

    # plot 1
    plt.figure(1)
    plt.plot(x, y_signal, 'ro')
    plt.plot(x, y_ase, 'go')
    plt.plot(x, y_nli, 'bo')
    plt.title('Channel power (r), ASE power (g), NLI power (b)')
    plt.xlabel('freq [THz]')
    plt.ylabel('Power [dBm]')
    plt.grid(True)

    # plot 2

    plt.figure(2)
    plt.plot(x, y_snr, 'ro')
    plt.plot(x, y_osnr, 'go')
    plt.plot(x, y_snr_nl, 'bo')
    plt.title('SNR (r), OSNR (g), SNR NL (b)')
    plt.xlabel('freq [THz]')
    plt.ylabel('Power [dB]')
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()
