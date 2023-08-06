from abc import ABC, abstractmethod
import numpy as np
import scipy.signal as sp_signal

class _Preprocess(ABC):
    def __init__(self):
        self.calibration_data = None
    
    def is_calibrated(self):
        return self.calibration_data is None

    @abstractmethod
    def apply(self, data):
        return data

    @abstractmethod
    def __str__(self):
        return 'Default preprocessing'

    def calibrate(self, data):
        pass

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        #combare preprocessings based on their discription string
        return str(self) == str(other)

class MeanCenter(_Preprocess):

    def __init__(self):
        super().__init__()
        self.mean = None
        

    def apply(self, data):
        if self.mean is None:
            self.calibrate(data)
        return data - self.mean

    def calibrate(self, data):
        self.calibration_data = data
        self.mean = np.mean(data, axis=0)
    
    def __str__(self):
        return f'Mean Center with mean {self.mean}'
    
class Normalize(_Preprocess):
    
    def apply(self, data):
        return np.divide(data.transpose(), np.sum(data, axis=1)).transpose()

    def __str__(self):
        return 'Normalize (Area 1)'
    
class SavGol(_Preprocess):

    def __init__(self, window_width = 15, polynomial_order = 2, derivative = 1 ):
        super().__init__()
        self.window_length = window_width
        self.polynomial_order = polynomial_order
        self.derivative = derivative

    def apply(self, data):
        return  sp_signal.savgol_filter(data, window_length = self.window_length, polyorder = self.polynomial_order, deriv = self.derivative)

    def __str__(self):

        if self.derivative == 0:
            derivative_str = 'SavGol smoothing'
        elif self.derivative == 1: 
            derivative_str = 'SavGol first derivate'
        elif self.derivative == 2:
            derivative_str = 'SavGol second derivative'
        else:
            derivative_str = 'SavGol {0}\'th'.format(self.derivative)

        return derivative_str + ' with window width {0} and polynomial order {1}'.format(self.window_length,self.polynomial_order)

class SNV(_Preprocess):

    def apply(self, data): 
        x_t = data.T
        return ((x_t - x_t.mean(axis=0))/x_t.std(axis=0)).T
    
    def __str__(self):
        return 'Standard Normal Variate (SNV)'

class Binning(_Preprocess):
    """ Simple binning class""" 
    def __init__(self,binning=2):
        super().__init__()
        self.binning=binning

    def apply(self,data):
        return data[:,::self.binning] 

    def __str__(self):
        return f'Binning with bin {self.binning}'