import package.import_json as js
import numpy as np
import matplotlib.pyplot as plt
from mylibrary.Spectral_information_1 import Spectralinformation


def main():

    json_filename = './json_line_system_exercise_2__transparency.json'
    #json_filename = './json_line_system_exercise_2__custom_output_power.json'

    network_elements_list = js.import_netelems_from_json(json_filename)
    n_ch = 91                   # number of channels
    bw_3dB = 32e9               # -3dB bandwidth
    first_central_f = 191.6e12  # first central frequency
    off_f = 50e9                # frequency offset
    p_ch = 0.02e-3              # power per channel
    p_ase = 0                   # ASE noise
    p_nli = 0                   # NLI noise

    ###################################################################################################################

    n_samples=12
    sweeped_signal_power = np.empty(shape=n_samples, dtype=float)
    sweeped_ase_power = np.empty(shape=n_samples, dtype=float)
    sweeped_nli_power = np.empty(shape=n_samples, dtype=float)
    snr = np.empty(n_samples, dtype=float)
    osnr = np.empty(n_samples, dtype=float)

    for i in range(-4, 7):

        sweep = (10 ** ((i - 4) / 10))
        power_dict = {'signal': p_ch * sweep, 'ase': p_ase, 'nli': p_nli}  # dictionary
        sp = Spectralinformation(n_channels=n_ch, start_frequency=first_central_f,
                                 frequency_offset=off_f, power_inf=power_dict, bandwidth=bw_3dB)

        LS = network_elements_list[0]
        LS.control_plane()
        LS.propagate(sp)
        sweeped_signal_power[i + 4] = (LS.power_signal_sweep[i+4])
        sweeped_ase_power[i + 4] = (LS.power_ase_sweep[i+4])
        sweeped_nli_power[i + 4] = (LS.nli_power_sweep[i+4])
        del LS
        del sp

    for i in range(0, n_samples):
        snr[i] = 10 * np.log10(sweeped_signal_power[i] / (sweeped_ase_power[i] + sweeped_nli_power[i]))
        osnr[i] = 10 * np.log10(sweeped_signal_power[i] / sweeped_ase_power[i])
    # nli[i] = 10 * np.log10(sweeped_nli_power[i])

    x = range(-4, 8)

    plt.figure(1)
    plt.plot( x,snr, 'r--')
    plt.plot( x,osnr, 'b--')

    plt.title('SNR')
    plt.xlabel('Node')
    plt.ylabel('Power [dBm]')
    plt.grid(True)
    plt.show()

    print('End')


if __name__ == "__main__":
    main()
