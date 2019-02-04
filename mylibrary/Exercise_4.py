import package.import_json as js
import numpy as np
import matplotlib.pyplot as plt
from mylibrary.Spectral_information_1 import Spectralinformation


def main():

    json_filename = './json_line_system_exercise_4_1_logo_uniform.json'
    #json_filename = './json_line_system_exercise_2__custom_output_power.json'

    network_elements_list = js.import_netelems_from_json(json_filename)
    n_ch = 91                    # number of channels
    bw_3dB = 32e9                # -3dB bandwidth
    first_central_f = 191.6e12   # first central frequency
    off_f = 50e9                 # frequency offset
    p_ch = (10**-3)*10**(-18/10) # power per channel
    p_ase = 0                    # ASE noise
    p_nli = 0                    # NLI noise

    power_dict = {'signal': p_ch, 'ase': p_ase, 'nli': p_nli}  # dictionary
    sp = Spectralinformation(n_channels=n_ch, start_frequency=first_central_f,
                             frequency_offset=off_f, power_inf=power_dict, bandwidth=bw_3dB)
    LS = network_elements_list[0]
    LS.control_plane()
    LS.propagate(sp)

    ###################################################################################################################

    y_signal = 10 * np.log10(np.array(LS.power_list_signal) * 10 ** 3)
    y_ase = 10 * np.log10(np.array(LS.power_list_ase) * 10 ** 3)
    y_nli = 10 * np.log10(np.array(LS.nli_power_list) * 10 ** 3)
    y_signal_total = 10 * np.log10((np.array(LS.power_list_signal) + np.array(LS.power_list_ase)+np.array(LS.nli_power_list)) * 10 ** 3)
    y_signal_snr = 10 * np.log10((np.array(LS.power_list_signal)) / (np.array(LS.power_list_ase) + np.array(LS.nli_power_list)) )
    y_nli_snr = 10 * np.log10((np.array(LS.power_list_signal)) / ( np.array(LS.nli_power_list)) )
    y_osnr = 10 * np.log10((np.array(LS.power_list_signal)) / ( np.array(LS.power_list_ase)) )


    plt.figure(1)
    plt.plot( y_signal, 'r-')
    plt.plot( y_ase, 'b--')
    plt.plot( y_signal_total, 'k--')
    plt.plot( y_nli, 'y--')

    plt.title('Signal power (r), ASE power (blue), NLI power(yellow), Total Power (black)')
    plt.xlabel('Node')
    plt.ylabel('Power [dBm]')
    plt.grid(True)

    plt.figure(2)
    plt.title('SNR ')
    plt.plot( y_signal_snr, 'y--')

    plt.figure(3)
    plt.title('SNR NLI ')
    plt.plot( y_nli_snr, 'r--')

    plt.figure(4)
    plt.title('OSNR')
    plt.plot( y_osnr, 'b--')

   # plt.title('SNR (y), SNR NLI(r), OSNR(b)')
    plt.xlabel('Node')
   # plt.ylabel('Power [dBm]')

    plt.show()

    print('End')


if __name__ == "__main__":
    main()
