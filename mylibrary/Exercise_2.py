import package.import_json as js
import numpy as np
import matplotlib.pyplot as plt
from mylibrary.Spectral_information_1 import Spectralinformation
#from package.definitions import LineSystem


def main():
    # path to the json file
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

    power_dict = {'signal': p_ch, 'ase': p_ase, 'nli': p_nli}  # dictionary

    sp = Spectralinformation(n_channels=n_ch, start_frequency=first_central_f,
                             frequency_offset=off_f, power_inf=power_dict, bandwidth=bw_3dB)
    LS = network_elements_list[0]
    LS.control_plane()
    LS.propagate(sp)
    ###################################################################################################################

    x = range(0, len(LS.power_list_signal))
    y_signal = 10 * np.log10(np.array(LS.power_list_signal) * 10 ** 3)
    y_ase = 10 * np.log10(np.array(LS.power_list_ase) * 10 ** 3)
    y_signal_ase= 10 * np.log10((np.array(LS.power_list_signal)+np.array(LS.power_list_ase))* 10 ** 3)
    y_signal_osnr = np.array(y_signal) - np.array(y_ase)

    plt.figure(1)
    plt.plot(x, y_signal, 'r-')
    plt.plot(x, y_ase, 'b--')
    plt.plot(x, y_signal_ase, 'k--')

    plt.title('Signal power (r), ASE power (blue), Total Power (black)')
    plt.xlabel('Node')
    plt.ylabel('Power [dBm]')
    plt.grid(True)

    plt.figure(2)
    plt.title('OSNR ')

    plt.plot(x, y_signal_osnr, 'y--')
    plt.show()


    print('End')



if __name__ == "__main__":
    main()
