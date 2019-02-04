import package.definitions as clt
import numpy as np


class BaseClass:
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            if isinstance(val, dict):
                setattr(self, key, BaseClass(**val))
            elif isinstance(val, list):
                paramlist = []
                for netnode in val:
                    paramlist.append(BaseClass(**netnode))
                setattr(self, key, paramlist)
            else:
                setattr(self, key, val)


class LineSystem(BaseClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._set_elements()
        self.element_counter =  0
        self.power_list_signal=[]
        self.power_list_ase = []
        self.power_list_osnr = []
        self.nli_power_list = []
        self.power_signal_sweep = []
        self.power_ase_sweep = []
        self.power_osnr_sweep = []
        self.nli_power_sweep = []
        self.p_base=6.626 * 10 ** -34 *191.6e12 *32e9
        self.attenuation_coefficient_value = 0.2         # elem.attenuation_coefficient.value
        self.fiber_length_value = 75                     # elem.length.value
        self.dispersion_value = 21.27                    # elem.dispersion.value
        self.nonlinear_coefficient_value = 1.27          # elem.nonlinear_coefficient.value

    def _set_elements(self):
        elements = []
        if hasattr(self, 'elements_list'):
            for elem in self.elements_list:
                element = getattr(clt, elem.type)(**elem.__dict__)
                elements.append(element)
        self.elements = elements

############################################# Control Plane ######################################################

    def control_plane(self):

        # Transparency mode

     if self.power_control == "transparency":
            for elem in self.elements:
                if elem.model == "BOOSTER":
                    setattr(elem, 'gain', elem.default_gain.value)          #set gain in db
                    elem.working_mode = "fixed_gain"
                elif elem.type == "Fiber":
                    temp_attenuation = elem.attenuation_coefficient.value * elem.length.value
                else:
                    setattr(elem, 'gain', temp_attenuation)
                    elem.working_mode = "fixed_gain"

        # Custom Output power mode

     elif self.power_control=='custom_output_power':
         for elem in self.elements:
             if elem.type == "Amplifier":
                  setattr(elem, 'output_power', self.set_power_ch.value)
                  setattr(elem, 'working_mode', "fixed_output_power")
                  elem.working_mode = "fixed_output_power"

        # LOGO

     elif self.power_control=='logo' :
         for elem in self.elements:
             elem.working_mode = "fixed_output_power"
             if elem.type == "Amplifier":
                if elem.model != "PRE-AMP":
                    self.noise_figure_=elem.noise_figure.value
                    self.field_attenuation = self.attenuation_coefficient_value / (20 * np.log10(np.exp(1)))
                    self.effective_length = (1 - np.exp(-2 * self.field_attenuation * self.fiber_length_value)) / (
                                2 * self.field_attenuation)
                    self.fiber_loss = 10 ** (-(self.attenuation_coefficient_value * self.fiber_length_value) / 10)

                    self.eta_1 = (16 / (27 * np.pi)) * (self.field_attenuation / self.dispersion_value)
                    self.eta_2 = ((self.nonlinear_coefficient_value * self.effective_length) / (
                            32e9 * 10 ** -12)) ** 2
                    self.eta_3 = np.log(((np.pi) ** 2) * np.abs(self.dispersion_value) * (
                                (32e9 * 10 ** -12) ** 2) * (
                                            91) ** ((2 * 32e9 ) / (
                        50e9)))
                    self.etafinal = self.eta_1 * self.eta_2 * self.eta_3
                    self.p_opt=91*np.cbrt(elem.noise_figure.value*self.fiber_loss*self.p_base)/(2*self.etafinal)
                    self.p_opt_dbm=10 * np.log10(self.p_opt* 10 ** 3)
                    setattr(elem, 'output_power', self.p_opt_dbm)
                else:
                    setattr(elem, 'output_power', -9)

    def propagate(self, spectralinformation):
        index=0
        self.nli_power_list_propagated=[]
        for element in self.elements:
            element.propagate(spectralinformation)
            self.power_list_signal.append(element.signal_power_temp)
            self.power_list_ase.append(element.ase_power_temp)
            self.nli_power_list.append(element.nli_power)
            if index==34:
                self.power_signal_sweep.append(element.signal_power_temp)
                self.power_ase_sweep.append(element.ase_power_temp)
                self.nli_power_sweep.append(element.nli_power)
            index = index + 1


class Fiber(BaseClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.signal_power_temp = 0
        self.ase_power_temp = 0
        self.nli_power_temp = 0
        self.temp_nli=0

    def propagate(self, spectralinformation):
        for elem in spectralinformation.carriers_list:
            elem.power['ase'] = elem.power['ase'] / 10**(self.attenuation_coefficient.value *
                                                         self.length.value/10)
            self.temp_nli = elem.power['nli'] / (10**(self.attenuation_coefficient.value *
                                                              self.length.value/10))
            elem.power['nli'] = self.evaluate_nli(elem,spectralinformation) + self.temp_nli

            elem.power['signal'] = elem.power['signal'] / 10 ** (self.attenuation_coefficient.value *
                                                                 self.length.value / 10)

            if elem.number == 46:
                self.signal_power_temp =elem.power['signal']
                self.ase_power_temp = elem.power['ase']
                self.nli_power = elem.power['nli']

    def evaluate_nli(self,elem,spectralinformation):

            self.field_attenuation = self.attenuation_coefficient.value  / (20*np.log10(np.exp(1)))
            self.effective_length = (1-np.exp(-2*self.field_attenuation*self.length.value)) / (2* self.field_attenuation)
            self.fiber_loss = 10**(-(self.attenuation_coefficient.value * self.length.value )/ 10)
            #to check for the minus

            self.eta_1=(16/(27*np.pi))*(self.field_attenuation/self.dispersion.value)
            self.eta_2=((self.nonlinear_coefficient.value*self.effective_length)/(spectralinformation.bandwidth*10**-12))**2
            self.eta_3=np.log(((np.pi)**2)*np.abs(self.dispersion.value)*((spectralinformation.bandwidth*10**-12)**2)* (spectralinformation.n_channels)**((2*spectralinformation.bandwidth)/(spectralinformation.frequency_offset)))
            self.etafinal=self.eta_1*self.eta_2*self.eta_3
            self.eta = (16*np.log(((np.pi**2 ) * np.abs(self.dispersion.value) * ((elem.bandwidth*10**-12) **2 )*
                              spectralinformation.n_channels**(2*elem.bandwidth/spectralinformation.frequency_offset) )/ (2*self.field_attenuation)) * self.field_attenuation* (
            self.nonlinear_coefficient.value *  self.effective_length )**2 )/ (27*np.pi * self.dispersion.value *((elem.bandwidth)**2))

            self.nli_power_temp= (self.etafinal * (elem.power['signal']) ** 3 ) * self.fiber_loss
            return self.nli_power_temp

class Amplifier(BaseClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nli_power_temp = 0
        self.signal_power_temp = 0
        self.ase_power_temp = 0
    def propagate (self, spectralinformation):

        if self.working_mode == "fixed_gain" :

            for elem in spectralinformation.carriers_list:
                elem.power['signal'] = elem.power['signal'] * 10**(self.gain/10)
                ase_power_temp = elem.power['ase'] * 10**(self.gain/10)
                ase_power_actual = elem.bandwidth * ((10**(self.gain/10))-1) * \
                                  (10**(self.noise_figure.value/10)) * \
                                  elem.frequency*6.626*10 ** (-34)
                elem.power['ase'] = ase_power_temp + ase_power_actual

                elem.power['nli'] = elem.power['nli'] * 10 ** (self.gain / 10)
                if elem.number == 46:
                    self.signal_power_temp = elem.power['signal']
                    self.ase_power_temp = elem.power['ase']
                    self.nli_power = elem.power['nli']

        elif self.working_mode =="fixed_output_power":

            for elem in spectralinformation.carriers_list:
                self.power_in = 10 * np.log10((elem.power['signal'] + elem.power['ase'] )* 10 ** 3)
                setattr(self,'gain' , self.output_power-self.power_in)
                elem.power['signal'] = elem.power['signal'] * 10 ** (self.gain / 10)
                ase_power_temp = elem.power['ase'] * 10 ** (self.gain / 10)
                ase_power_actual = elem.bandwidth * ((10 ** (self.gain / 10)) - 1) * \
                                   (10 ** (self.noise_figure.value / 10)) * \
                                   elem.frequency * 6.626 * 10 ** -34
                elem.power['ase'] = ase_power_temp + ase_power_actual
                elem.power['nli']= elem.power['nli'] * 10**(self.gain/10)

                if elem.number == 46:
                    self.signal_power_temp = elem.power['signal']
                    self.ase_power_temp = elem.power['ase']
                    self.nli_power = elem.power['nli']

