import glob
import enum
from tkinter import Tk, filedialog
import os
import numpy as np
import re
from matplotlib import pyplot
from copy import deepcopy
from datetime import datetime
from tqdm import tqdm
from xml.etree import ElementTree as ET

from ._misc import natural_keys
from . import _misc
from ..chemometrics.dataset import Dataset, SpectralDataset, HyperSpectralDataset

IMAGE_EXT = ['.tiff','.tif','.png']

def build_HC_from_folder(folder_dir=None, Y_start=0, Y_end=-1, Y_bin = 1, X_bin = 1, L_bin = 1, silent=False, dtype=np.float32) -> np.ndarray :
    """
    Build HyperSpectralDataset from folder containing png images
    """
    if folder_dir is None:
        Tk().withdraw()
        folder_dir = filedialog.askdirectory(title="Please select folder containing the linescan images")
    
    all_file_names = os.listdir(folder_dir)
    file_names = list()
    parameter_dict = dict()
    for file_name in all_file_names:
        [name,ext] = os.path.splitext(file_name)
        if ext in IMAGE_EXT:
            file_names.append(file_name)
        elif ext == '.xml':
            parameter_dict.update(read_xml_to_dict(os.path.join(folder_dir,file_name)))
        else:
            Warning("file: {0} was not included in HyperSpectralDataset because of invalid extention {1}".format(file_name,ext))
    
    file_names.sort(key=_misc.natural_keys)

    dimY = len(file_names)
    [dimL, dimX] = _misc.imread(os.path.join(folder_dir, file_names[0]))[::L_bin, ::X_bin].shape

    if Y_end == -1:
                Y_end = dimY

    HC = np.empty([len(range(Y_start, Y_end, Y_bin)), dimX, dimL], dtype=dtype)
    j = 0
    parameter_dict['Time'] = datetime.fromtimestamp(os.path.getmtime(os.path.join(folder_dir, file_names[Y_start])))
    for i in tqdm(range(Y_start, Y_end, Y_bin),desc="Building HyperSpectralDataset...",disable=silent):
        HC[j, :, :] = np.swapaxes(_misc.imread(os.path.join(folder_dir, file_names[i]))[::L_bin, ::X_bin], 0, 1)
        j = j+1
    return HC, parameter_dict

def read_xml_to_dict(path):
    file_name, ext = os.path.splitext(path)
    assert ext == ".xml"

    xml = ET.parse(path)

    root_element = xml.getroot()

    parameter_dict = dict()
    for child in root_element:
        type = child.tag
        value = child.find('Val')
        name = child.find('Name')
        if value is not None:
            if type == 'Boolean':
                parameter_dict[name.text] = value.text == '1'
            if type == 'String':
                parameter_dict[name.text] = value.text
            else:
                parameter_dict[name.text] = float(value.text)

    return parameter_dict

class Measurement(HyperSpectralDataset):
    """ Class to manage measurement taken with certain hyperspectral imaging setup."""
    
    def __init__(self, basepath=None, folder=None, measurement=None, camera_name=None, spectral_calib = True, reference_correction=True, **kwargs):
        """ Create measurement from folder with images

        Parameters
        ----------
        basepath: str
            Basepath where all folders are located (e.g. 'C:\myData' )
        folder: str
            A larger folder within the basepath that contains multiple measurements (e.g. 'DAY_1')
        measurement: str
            Folder containing the actual images ('e.g. 'Sample_1'),
        camera_name:
            Camera that was used for the measurements. For the Measurement class this can be either 'FX10' or 'FX17' (or 'FX35').
        kwargs:
            see pyper.chemometric.HyperSpectralDataset"""
            
        if measurement is None:
            Tk().withdraw()
            if basepath is not None and os.path.isdir(basepath):
                initialdir = basepath
            else:
                initialdir = None
            path = filedialog.askdirectory(initialdir=initialdir, title="Please select the folder that contains the RAW images")
            self.bp, self.folder, self.measurement, self.camera_name = self.split_path(path)
        else:
            if camera_name is None:
                raise ValueError('Please provide camera_name!')
            self.bp = basepath
            self.folder = folder
            self.measurement = measurement
            self.camera_name = camera_name

        # get camera from camera name
        self.camera: Camera = self.get_camera_from_name(self.camera_name)

        # get wavelengths from camera
        wavelength = self.camera.get_wl_full()
        if 'L_bin' in kwargs:
            L_bin = kwargs['L_bin']
            wavelength = wavelength[::L_bin]

        # RAW
        rawHC, parameter_dict = build_HC_from_folder(self._get_data_path(), **kwargs)
        super().__init__(hypercube=rawHC, wavelength=wavelength)
        
        self.parameter_dict = parameter_dict
        
        ## correct for white and dark reference ##

        #remove Y parameters from argument list for reference measurements.
        reference_kwargs = deepcopy(kwargs)
        reference_kwargs.pop('Y_bin', None)
        reference_kwargs.pop('Y_start', None)
        reference_kwargs.pop('Y_end', None)

        #initialze withouth reference correction
        self.isWhiteCorrected = False
        self.isDarkCorrected = False

        # WhiteRef
        if reference_correction and self._get_path_WhiteRef() is not None:
            HC, _ = build_HC_from_folder(self._get_path_WhiteRef(), **reference_kwargs)
            self.whiteHC = HyperSpectralDataset(hypercube=HC, wavelength=wavelength)
        else:
            self.whiteHC = None

        # DarkRef
        if reference_correction and self._get_path_DarkRef() is not None:
            HC, _ = build_HC_from_folder(self._get_path_DarkRef(), **reference_kwargs)
            self.darkHC = HyperSpectralDataset(hypercube=HC, wavelength=wavelength)
        else:
            self.darkHC = None        

        # perform reference correction either with true hypercubes or with None
        self.referenceCorrection(self.whiteHC, self.darkHC)

        if spectral_calib:
            #check Signal to Noise (SNR)
            if self.isWhiteCorrected and self.isDarkCorrected:
                try:
                    s2n, (start_idx, end_idx) = self.get_s2n()
                    #TODO: make shorter, wrap in warning printer or make more general, not 2x the same
                    if ( self.get_wl()[start_idx] > self.camera.get_start_wl_s2n() ) or ( self.get_wl()[end_idx] < self.camera.get_end_wl_s2n() ):
                        print(
                            'WARNING: The normal wavelength range for {0} was [{1:.1f}nm - {2:.1f}nm], while the SNR suggests a wavelenght range [{3:.1f}nm - {4:.1f}nm].'.format(
                                self.camera,
                                self.camera.get_start_wl_s2n(),
                                self.camera.get_end_wl_s2n(),
                                self.get_wl()[start_idx],
                                self.get_wl()[end_idx])
                                )
                except ValueError as e:
                    print(str(e))
            else:
                print('WARNING: Data was not white and dark corrected')

            #include only high SNR range from spectrum
            self.include_wavelengths(self.camera.get_start_wl_s2n(), self.camera.get_end_wl_s2n())

    def referenceCorrection(self, whiteRefHSD = None, darkRefHSD = None):

        # construct references based on given whiteRefHSD and darkRefHSD
        if darkRefHSD is not None:
            assert self._is_valid_reference(darkRefHSD)
            self.isDarkCorrected = True
            dark_ref = np.mean(darkRefHSD.get_HC(), axis=0)
        else:
            dark_ref = 0

        if whiteRefHSD is not None:
            assert self._is_valid_reference(whiteRefHSD)
            self.isWhiteCorrected = True
            white_ref = np.mean(whiteRefHSD.get_HC(), axis=0)

        else:
            white_ref = 1
    
        #perform reference correction
        HC = self.get_HC()

        HC = np.subtract(HC, dark_ref, out=HC)
        if self.isWhiteCorrected:
            white_ref = np.subtract(white_ref, dark_ref, out=white_ref)
            HC = np.divide(HC, white_ref, out=HC)
            
        self.set_HC(HC)
    
    @staticmethod
    def get_camera_from_name(name):
        if name == 'VISNIR':
            return Camera.BAUMER
        elif name == 'SWIR':
            return Camera.HEADWALL
        else:
            ValueError('Unknow Camera name: {0}'.format(name))
            return None

    def _get_data_path(self):
        return os.path.join(self.bp, self.folder, self.measurement, self.camera_name)

    def _get_path_WhiteRef(self):
        return self._get_path('WhRef')

    def _get_path_DarkRef(self):
        return self._get_path('DarkRef')

    def _construct_searchpath(self, RefType):
        return os.path.join(self.bp,self.folder,'{0}_{1}*'.format(RefType,self.camera_name))

    def _get_path(self, RefType):
        """ Get path from a certrain reference type ('DarkRef' or 'WhRef') """
        search_path = self._construct_searchpath(RefType)
        folder_list = glob.glob(search_path)
        
        #TODO: check with old measurments that have multiple white references, they should take the last one but not compatible with looking at time
        def sort_key_references(folder_path):
            if self.parameter_dict and 'Time' in self.parameter_dict:
                
                measurement_time = self.parameter_dict['Time']
                
                reference_image_path = os.path.join(folder_path, os.listdir(folder_path)[0])
                reference_time = datetime.fromtimestamp(os.path.getmtime(reference_image_path))
                return -abs(measurement_time - reference_time)
            else:
                return natural_keys(folder_path)
            
        folder_list.sort(key= sort_key_references)
        
        if len(folder_list) == 0:
            print('WARNING: No {0} \'s was found, continuing without'.format(RefType))
            return None
        elif len(folder_list) > 1:
            path = folder_list[-1]
            print('WARNING: Multiple {0} \'s were found, using the last one: {1}'.format(RefType, os.path.split(path)[1]))
            return path
        else:
            return folder_list[0]

    def get_s2n(self, plot=False, s2n_threshold=3):
        """ Return signal to noise ratio for measurement based on white reference and dark reference.

        plot=True gives an illustrative figure with mean white and dark reference spectra.

        Returns:
            s2n vector (1-by-nb_wavelengths)
            tuple of start index and end idx where s2n is greater then s2n_threshold. """

        mean_white_spectrum = self.whiteHC._get_mean_data()
        mean_dark_spectrum = self.darkHC._get_mean_data()
        s2n = mean_white_spectrum / mean_dark_spectrum

        if not any(s2n>s2n_threshold):
            raise ValueError('Not a single wavelength had a signal to noise ration higher then the s2n threshold ({0}). Highest SNR value was {1}.'.format(s2n_threshold, np.amax(s2n)))
        else:
            start_idx = np.nonzero(s2n>s2n_threshold)[0][0]
            end_idx = np.nonzero(s2n>s2n_threshold)[0][-1]

        if plot:
            fig, (ax1, ax2) = pyplot.subplots(1, 2, figsize=(10, 5))

            wavelength = self.whiteHC.get_wl()
            ax1.plot(wavelength, mean_white_spectrum, '-m', label= 'Mean Spectrum White Ref')
            ax1.plot(wavelength, mean_dark_spectrum, '-g', label='Mean Spectrum Dark Ref')
            ax1.axvline(x=wavelength[start_idx], color='b')
            ax1.axvline(x=wavelength[end_idx], color='b')
            ax1.legend()


            ax2.plot(s2n, color='k')
            ax2.axhline(y=s2n_threshold, color='r')
            ax2.axvline(x=start_idx, color='b')
            ax2.axvline(x=end_idx, color='b')
            ax2.set_title('Signal to Noise Ratio')

            pyplot.show()
        return s2n, (start_idx, end_idx)

    @staticmethod
    def split_path(path):
        """ Split the given path that contains the RAW images into a basepath, folder, measurement and camera."""
        path, camera = os.path.split(path)
        path, measurement = os.path.split(path)
        basepath, folder = os.path.split(path)
        return basepath, folder, measurement, camera

    
    def isVISNIR(self):
        return (max(self.get_wl()) < 1100) and (min(self.get_wl()) < 500)

    def isSWIR(self):
        return (max(self.get_wl()) > 1500) and (min(self.get_wl()) > 900)
        
class FxMeasurement(Measurement):

    def __init__(self, basepath=None, folder=None, measurement=None, camera_name=None, **kwargs):
        super().__init__(basepath=basepath,
                         folder=folder,
                         measurement=measurement,
                         camera_name=camera_name,
                         **kwargs)

    @staticmethod
    def get_camera_from_name(name):
        if name == 'FX10':
            return Camera.SPECIM_FX10
        elif name in ['FX17','FX35', 'FX35']:
            return Camera.SPECIM_FX17
        else:
            ValueError('Unknow Camera name: {0}'.format(name))
            return None

    @staticmethod
    def split_path(path):
        path, measurement = os.path.spit(path)
        path, camera_name = os.path.split(path)
        basepath, folder = os.path.split(path)
        return (basepath, folder, measurement, camera_name)

    def _get_data_path(self):
        return os.path.join(self.bp,self.folder,self.camera_name,self.measurement)

    def _get_path_WhiteRef(self):
        return self._get_path('WhiteRef')
    
    def _construct_searchpath(self, RefType):
        return os.path.join(self.bp,self.folder,self.camera_name,'{0}*'.format(RefType))


class Camera(enum.Enum):
    BAUMER = ('VISNIR',
        (3.167478045363729e+02, 1.015349419043834e+03),
        520,
        (64, 519))

    HEADWALL = ('SWIR', 
        (859, 2748),
        256,
        (22, 213))

    SPECIM_FX10 = ('VISNIR',
        (397.66, 1003.81),
        224,
        (12, 223))

    SPECIM_FX17 = ('SWIR',
        (935.61, 1720.23),
        224,
        (4, 212))
    
    def __init__(self, spectral_name, spectral_range_nm, nb_wl_channels, signal_2_noise_indices):
        self.spectral_name = spectral_name
        self.spectral_range_nm = spectral_range_nm
        self.nb_wl_channels = nb_wl_channels
        self.signal_2_noise_indices = signal_2_noise_indices
    
    def get_wl_full(self):
        return np.linspace(self.spectral_range_nm[0],self.spectral_range_nm[1],self.nb_wl_channels)

    def get_wl(self):
        return self.get_wl_full()[self.signal_2_noise_indices[0] : self.signal_2_noise_indices[1]]

    def get_start_idx_s2n(self):
        return self.signal_2_noise_indices[0]

    def get_start_wl_s2n(self):
        return self.get_wl_full()[self.get_start_idx_s2n()]
    
    def get_end_idx_s2n(self):
        return self.signal_2_noise_indices[1]
    
    def get_end_wl_s2n(self):
        return self.get_wl_full()[self.get_end_idx_s2n()]

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

    