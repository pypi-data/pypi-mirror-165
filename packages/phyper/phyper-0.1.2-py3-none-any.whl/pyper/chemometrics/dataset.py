import os
from tracemalloc import start
import numpy as np
import h5py
from matplotlib import pyplot
from pytz import NonExistentTimeError
from skimage.color import label2rgb
from skimage import transform
from typing import Optional, Union

from .preprocessing import _Preprocess
from ._gui import Gui, MaskCreator
from .. import WL_UNIT, WL_UNIT_LONG
from copy import deepcopy
from spectral import open_image
from scipy.signal import medfilt

def _docstring_parameter(*sub):
    def dec(obj):
        obj.__doc__ = obj.__doc__.format(*sub)
        return obj
    return dec

class Dataset(object):
    """
    Class for creating a simple dataset with N samples and M variables
    """

    def __init__(self, data, labels=None, label_table = []):
        """ Create a Dataset from the N-by-M numpy array with N samples and M variables.

        Parameters
        ----------
        data : ndarray
            A 2-D array of shape (N, M) with N the number of samples and M the number of variables.
        labels : ndarray, optional
            A 1-D array of shape (N,) with label ID's for every sample. Label ID's should be integers that can be found in `label_table`.
            If the integer can not be found in the label_table, or no label table is provided, a default label tabel will be generated.
        label_table : list of tuples, optional
            A list of tuples, where every tuple has the format (label_id, label_name). E.g. label_table = [(1, "good"),(2, "bad")].
        """

        # initialise empty preprocessing list
        self.preprocess_list = []
        self.catched_preprocess_list = []

        # initialise data and data_pre
        # data_pre is a cache for the data that has been preprocessed based on the preprocessing list.
        self.data = None
        self.catched_data_preproc = None
        # initialize data by setting the data to the given data
        self._set_data(data)

        #assign labels
        self.labels = labels
        self.label_table = label_table
        self._fill_label_table()

    def __array__(self, dtype=None):
        return self.get_data().copy()

    def __len__(self):
        return self.get_nb_samples()

    def __repr__(self):
        return ('A Dataset with size {0}x{1} and preprocessing {2}. {3} samples are included.'.format(self.get_nb_samples(),
                                                                                                      self.get_nb_variables(),
                                                                                                      self.preprocess_list,
                                                                                                      self.get_nb_samples(original=True)))

    @property
    def shape(self):
        """ Return the shape (N,M) of the dataset.

        N is the number of samples and M is the number of variables.
        """

        return (self.get_nb_samples(), self.get_nb_variables)

    def get_nb_samples(self, original=False) -> int:
        if original:
            return self.get_original_data().shape[0]
        else:
            return self.get_data().shape[0]

    def get_nb_variables(self) -> int:
        return self.get_data().shape[1]

    def include_only_variables(self, variables_idx):
        """ Make a selected of which variables to retrain in the dataset."""
        self.data = self.data[:, variables_idx]
        self.catched_data_preproc = None

    def include_variables_from(self, start_idx, end_idx):
        self.data = self.data[:, start_idx:end_idx]
        self.catched_data_preproc = None
    ############################# Data Handling #############################

    def _set_data(self, data, included_samples=None, labels=None):
        """ Set new data. RESTRICTED USE

        This function allows to change data for this dataset.
        As a result al labels and included samples will be reset or set to the given values.
        """
        assert(self._is_valid_data(data))
        if included_samples is None:
            self.included_samples = np.ones(data.shape[0], dtype=bool)
        self.labels = labels
        self.data = data

        self.catched_data_preproc = None

    @staticmethod
    def _is_valid_data(data) -> bool:
        """ Check if the given `data` has the correct format.

        Data should be an numpy ndarray with a shape of the format (N,M).
        """
        if isinstance(data, np.ndarray):
            return len(data.shape) == 2
        else:
            return False

    def get_original_data(self):
        """ Return the original data.

        Original data means the data as intialy provided, without preprocessing and with all samples included.
        """

        return self.data

    def get_data(self, preproc=True, fill_nans=False) -> np.ndarray:
        """ Return the data as a numpy array.

        Parameters
        ----------
        preproc : bool, default=True
            If preprocessing is selected (default), the preprocessed data will be returned. Otherwise the raw data will be returned.
        fill_nans : bool, default=False
            By default only the included samples are given. If `fill_nans` is set to True however, the returned dataset will have the same shape as the original dataset, with excluded samples having NaN as value for all variables.

        Returns
        -------
        data: ndarray
            2D dimensional array of shape (K,M) where K is the number of included samples. If `fill_nans`, K is the total number of samples.

        See Also
        --------
        get_original_data : Return the original data, without preprocessing and with the actual values for the excluded samples.
        """
        #check if preprocessed data is asked, and if so, check if catched preprocessing is still valid
        if preproc and not self._is_valid_catch():
            self.apply_preprocess()
        
        #check if asked to return filled, original or preprocessed data
        if self.has_excluded_samples() and fill_nans:
            data = np.full(self.data.shape, np.nan, dtype=self.data.dtype)
            data[self.included_samples, :] = self.get_data(preproc=preproc, fill_nans=False)
            return np.squeeze(data)
        elif (self.catched_data_preproc is not None) and preproc:
            data = self.catched_data_preproc
        else:
            data = self.get_original_data()

        # indexing takes a lot more time so check if this is needed.
        if self.has_excluded_samples():
            return np.squeeze(data[self.included_samples, :])
        else:
            return data

    ############################# Sample inclusion/exclusion #############################

    def include(self, bool_inclusion):
        """ Include only part of the samples based on a boolean array of shape (N,).

        Parameters
        ----------
        bool_inclusion : ndarray
            1-D boolean array of shape (N,) where N is the total number of samples.
            Only samples that were already in the included samples can be included.

        See Also
        --------
        include_all
        """

        self.included_samples = np.logical_and(self.included_samples, bool_inclusion)

    def include_all(self):
        """ Include all samples that were in the original dataset. Remove any exclusions.

        See Also
        --------
        include
        exclude_label
        """

        self.included_samples = np.ones(self.data.shape[0], dtype=bool)
        #TODO: also check all labels are in label table

    def has_excluded_samples(self) -> bool:
        """ Check if any of the original datasamples has been excluded.
        """

        return np.any(np.logical_not(self.included_samples))

    def exclude_label(self, label_id: int):
        """ Exclude all samples with a given `label_id`.

        Parameters
        ----------
        label_id : int
            `label_id` should correspond to one of the labels_id - label_name pairs in the label_table.

        See Also
        --------
        _has_label_id : Check if certain `label_id` is in the label_table.
        """

        if self.labels is not None:
            if np.any(self.get_labels() == label_id):
                self.include(self.labels != label_id)
                if self._has_label_id(label_id=label_id):
                    self.label_table.remove((label_id, self.get_label_name(label_id)))
            else:
                print('WARNING: Not able to exclude label {0} because it was not found in labels'.format(label_id))
        else:
            print('WARNING: Not able to exclude label {0} because not labels were found'.format(label_id))

    ############################# Preprocessing #############################

    def apply(func):
        """ Decorator. Apply preprocessing after method that changes preprocessing list. """
        def wrapper(self, *args):
            func(self, *args)
            self.apply_preprocess()

        return wrapper

    @apply
    def add_preprocess(self, preprocess: _Preprocess, position=None, allow_double=False) -> None:
        """ Add a preprocessing step to the preprocessing list.

        This method allows to add a new preprocessing step to the preprocessing list.
        This list of preprocessing steps will be applied to the data from index 0 to -1.

        Parameters
        ----------
        preprocess : _Preprocess
            Preprocessing object to be added to the preprocessing list.
        position : int, optional
            Position at which to add the new `preprocess` within the preprocessing list. If no position is given, the `preprocess` is added at the end of the list (default).
        allow_double : bool, default=False
            Normally the same type of preprocessing can not be added twice, unless `allow_double` is set to True.
        """

        assert(isinstance(preprocess, _Preprocess))
        if preprocess in self.preprocess_list and not allow_double:
            print("WARNING: \n New preprocess ({0}) was already in preprocessing list ({1}). \n If this is what you want, use allow_double=True".format(preprocess, self.preprocess_list))
        else:
            if position is None:
                self.preprocess_list.append(preprocess)
            else:
                self.preprocess_list.insert(position, preprocess)

    @apply
    def remove_preprocess(self, position:int) -> None:
        """ Remove a preprocessing step at a certain `position` from the prepocessing list.

        Parameters
        ----------
        position: int
            Index in preprocessing list.

        See Also 
        --------
        print_preprocessing_list()
        """

        self.preprocess_list.pop(position)

    def has_preprocessing(self) -> bool:
        """ Check if there are preprocessing steps in the preprocessing list."""
        return bool(self.preprocess_list)

    @apply
    def clear_preprocess(self):
        """ Clear the preprocessing list. No preprocessing will be performed anymore.

        See Also
        --------
        get_original_data : directly get the original data on which the preprocessing is being applied.
        """
        self.preprocess_list = []

    @apply
    def copy_preprocess(self, other: 'Dataset'):
        """ Copy the preprocessing steps from an other Dataset (`other`).

        This method allows to copy the preprocessing that has been performed on an other Dataset `other`, to your dataset.
        This copying also includes any calibration data from the preprocessing that has been performed on `other` (e.g. mean centering).

        Parameters
        ---------
        other: Dataset
            Dataset from which to copy the list of preprocessing

        Note
        ----
        When invocking this method, the new preprocessing list will directly be applied to the dataset. 
        The original data are stored in parallel and can be accesed using get_original_data() or by using clear_preprocess().
        """

        assert isinstance(other, Dataset)
        self.preprocess_list = deepcopy(other.preprocess_list)

    def print_preprocessing_list(self):
        """Print entire preprocessing list.
        """

        for idx, preproc in enumerate(self.preprocess_list):
            print(f'[{idx}] {preproc}')

    def _is_valid_catch(self):
        """ Check if the catched preprocessing data is still valid (preprocessing not changed since last time applying preprocessing)
        """

        return self.preprocess_list == self.catched_preprocess_list

    def apply_preprocess(self):
        """ Apply all preprocessing steps in the preprocessing list, starting from `preprocess_list[0]`.

        Normally these function does not have to be called explicitly, as it is called automaticly after every method that makes changes to the preprocessing list.

        Note
        ----
        If the preprocessing list has not changed since the last time this method was invoced, the cached prepropressing data will be used.
        """
        if self._is_valid_catch():
            return self.catched_data_preproc
        elif self.preprocess_list:
            self.catched_data_preproc = self.get_original_data().copy()
            for preproc in self.preprocess_list:
                self.catched_data_preproc = preproc.apply(self.catched_data_preproc)
        else:
            self.catched_data_preproc = None
        self.catched_preprocess_list = self.preprocess_list

    ############################# Labels #############################

    def get_label_data(self, label_id):
        """ Get the data belonging to samples with a certain `label_id`.

        If no label data is available for this Dataset, all included samples are included in the returned array.

        Parameters
        ----------
        label_id : int
            The `label_id` should be one from the label_ids listed in the label table.

        Return
        ------
        Numpy ndarray of shape (L,M) with L the number of samples for with as label id the given `label_id`.
        If the `label_id` can not be found in the label table, None will be returned.

        See Also
        --------
        get_label_table

        """

        if not self._has_labels():
            print('No lables were found, returning all data')
            return self.get_data()
        else:
            if self._has_label_id(label_id):
                class_idx = self.get_labels() == label_id
                return self.get_data()[class_idx, :]
            else:
                print('Label id ({0}) was not found in label table {1}'.format(label_id, str(self.label_table)))
                return None

    def assign_labels(self, labels, label_table=None):
        """ Assign labels to the samples in the dataset.

        Parameters
        ----------
        labels : ndarray
            1-D array of shape (N,) with N the number of included samples
        label_table : list[], optional
            List of tuples where each tuple corresponds to a lable_id, label_name pair. E.g. label_table = [(0, "good"),(1,"bad")].
            If no `label_table` is provided, a default label table will be created.
        """
        assert(labels.shape == (self.get_nb_samples(),))
        self.labels = np.full(self.data.shape[0], 0, dtype=np.int)
        self.labels[self.included_samples] = np.asarray(labels, dtype=int)
        if label_table is not None:
            for label in label_table:
                label_id, label_name = label
                self.add_label_id(label_id, label_name)
        self._fill_label_table()

    def _fill_label_table(self):
        """ Check if there are any label_ids in the labels that are not in the label_table, and add these label_ids to the label_table with a defautl label_name ('ClassX')
        """
        if self._has_labels():
            for x in np.unique(self.labels):
                if not self._has_label_id(x):
                    self.add_label_id(x, "Class_{}".format(x))

    def get_labels(self, fill=False):
        """ Get the labels belong to the samples of this dataset.


        Parameters
        ----------
        fill : bool, default=False
            By default only the labels for the included samples are given.
            If `fill` is set to True, the excluded samples get -1 as label.

        Returns
        -------
        labels: ndarrray or None
            1-D array with shape (N,) where N is the number of included samples.
            If `fill_nans` is set to True, N will be the total number of samples.
            If the `label_id` was not found in the dataset, None will be returned.
        """

        if self.labels is not None:
            if fill:
                labels = np.full(self.labels.shape, -1, dtype=int)
                labels[self.included_samples] = self.get_labels(fill=False)
                return np.squeeze(labels).astype(int)
            else:
                return np.squeeze(self.labels[self.included_samples]).astype(int)
        else:
            return None

    def _has_labels(self):
        """ Check if labels are available for the samples."""
        return self.get_labels() is not None

    def _has_label_id(self, label_id):
        for label_tuple in self.label_table:
            if label_tuple[0] == label_id:
                return True
        return False

    def add_label_id(self, label_id, label_name):
        """ Add a label with a certain `label_id` and `label_name` to the label_table.
        
        Parameters
        ----------
        label_id : int
            Unique id for the label. `label_id` should be different from the other label id's already present in the label_table.
        label_name : str
            Name for the label.
        
        See Also
        --------
        get_label_table
        get_labels
        """

        if not self._has_label_id(label_id):
            self.label_table.append((label_id, label_name))
        else:
            print('Label {0} was already in labeltabel with name {1} (instead of given name {2})'.format(label_id, self.get_label_name(label_id), label_name))

    def get_label_name(self, label_id) -> Optional[str]:
        """ Get the label name beloging to the `label_id`.
        
        Parameters
        ---------
        label_id : int
            Label_id as can be found in the labels from this dataset.
        
        Returns
        -------
        name : str
            Name for the given `label_id`. If the `label_id` was not found in the label_table, the method will return None.
        
        See Also
        --------
        get_labels
        get_label_table
        """

        for label in self.label_table:
            id, name = label
            if label_id == id:
                return name
        return None

    def get_nb_classes(self):
        """ 
        .. deprecated:: 0.0
          `get_nb_classes` will be removed. Use get_nb_labels instead.
        """

        return self.get_nb_labels()

    def get_nb_labels(self):
        """ Get the total number of unique labels for all"""
        if self.get_labels() is None:
            return 0
        else:
            return np.unique(self.get_labels()).size

    def get_label_table(self, include_quantity = False):
        """ Get overview of labels as list of tuples with label tuples as (label_id,label_name) or (label_id,label_name,nb_of_labels) if include_quantity
        """

        if not include_quantity:
            return deepcopy(self.label_table)
        else:
            label_table = list()
            for label in self.label_table:
                label_id, label_name = label
                label_quantity = sum(self.get_labels()==label_id)
                label_table.append((label_id, label_name,label_quantity))
            return label_table

    ############################# Utils #############################
    def _get_mean_data(self, by_label=True) -> Union[tuple, np.ndarray]:
        """ Get data mean. If labels are given, the mean for each label will be returned.
        
        Parameters
        ----------
        by_label : bool, optional
            Indicate if needed to calculate the mean for each label seperatly. If not, the total mean of the data will be returned.
        
        Returns
        -------
        mean_data
            If no labels are given or `by_label` is set to False, a 1-D array will be returned. 
            Otherwise, a 2-D array will be returned with diffent rows corresponding to the mean of different lables.
        labels_ids
            If the mean is calcuted for the different labels, the `labels_ids` corresponding to the different rows are given.
        """
        if (self.get_nb_classes() == 0) or not by_label:
            return np.mean(self.get_data(), axis=0)
        else:
            mean_data = np.full([self.get_nb_classes(), self.get_nb_variables()], fill_value=0, dtype=self.get_data().dtype)
            label_ids = np.full([self.get_nb_classes(),], fill_value=0, dtype=self.get_labels().dtype)
            i = 0
            for label_id, labelname in self.get_label_table():
                mean_data[i, :] = np.mean(self.get_label_data(label_id), axis=0)
                label_ids[i] = label_id
                i += 1
            return mean_data, label_ids

    def add(self, ds) -> None:
        """ 
        .. deprecated:: 0.0
          `add` will be removed. Use merge instead.
        """
        print('WARNING: DEPRECATED : Please use merge instead')
        new_data = np.concatenate((self.get_data(), ds.get_data()), axis=0)
        if self._has_labels() and ds._has_labels():
            new_labels = np.concatenate((self.get_labels(), ds.get_labels()), axis=0)
        else:
            new_labels = None
        self._set_data(data=new_data, labels=new_labels)

        #fix missing lables
        for label_id, label_name in ds.label_table:
            self.add_label_id(label_id, label_name)

    def merge(self, ds : 'Dataset or SpectralDataset') -> 'Dataset or SpectralDataset':
        """ Create a new Dataset by merging the current dataset with a new dataset `ds`.
        
        Parameters
        ----------
        ds : Dataset
            New dataset to merge with the current dataset.
        
        Returns
        -------
        ds : Dataset
            Merged dataset from the current dataset and `ds`.
        """
    
        new_data = np.concatenate((self.get_data(), ds.get_data()), axis=0)
        if self._has_labels() and ds._has_labels():
            new_labels = np.concatenate((self.get_labels(), ds.get_labels()), axis=0)
        else:
            new_labels = None
        if isinstance(ds, SpectralDataset):
            ds = SpectralDataset(data=new_data, wavelength=ds.get_wl(), labels=new_labels, label_table=self.get_label_table())
        else:
            ds = Dataset(data=new_data, labels=new_labels, label_table=self.get_label_table())

        #fix missing lables
        for label_id, label_name in ds.label_table:
            ds.add_label_id(label_id, label_name)
        return ds

    def plot(self, nb_samples=100, labels=True, label_ids = [], ax=None, show=True):
        """ Visualise the dataset by plotting some samples.
        
        Parameters
        ----------
        nb_samples : int, default=100
            Maximal number of samples to visualize on the plot. 
            If the number of samples in the dataset is higher than `nb_samples`, random samples will be selected.
        labels : bool, default=True
            If True, plot the mean value and standard deviation for all samples with the same label_id.
        label_ids : list[int], optional
            If `labels`, `labels_ids` allows to define for which labels the mean and standard deviation should be plotted.
            By default all labels are included in the list.
        ax : matplotlib.axes.Axes, optional
            Axis on which to plot the samples. By default a new figure with a new axis is generated.
        show : bool, default = True
            Automatically call pyplot.show() at the end of the method
        
        Returns
        -------
        ax : matplotlib.axes.Axes
            Axis on which the samples were plotted.
        """

        #TODO: you can not use 'get_wl() for dataset, but you need an x variable to plot against, you can not simply change the axis labels afterwards.'
        if ax is None:
            ax = pyplot.subplot(111)
        if isinstance(self,SpectralDataset):
            wl = self.get_wl()
        else:
            wl = np.arange(self.get_nb_variables())
        if labels and self._has_labels():
            for label_id, label_name in self.label_table:
                if not label_ids or label_id in label_ids:
                    data = self.get_label_data(label_id)
                    if data is not None and data.size > 0:
                        data_mean = np.mean(data, axis=0)
                        data_std = np.std(data, axis=0)
                        ax.plot(wl, data_mean, '-', label=label_name)
                        ax.fill_between(wl, data_mean - data_std, data_mean + data_std, alpha=0.2)
                        ax.legend()
        else:
            if self.get_nb_samples() > nb_samples:
                rng = np.random.default_rng(2021)
                sample_indices = rng.choice(self.get_nb_samples(), nb_samples, replace=False)
                ax.plot(wl, np.transpose(self.get_data()[sample_indices, :]))
            else:
                ax.plot(wl, np.transpose(self.get_data()))
        if show:
            pyplot.show()
        return ax
        
class SpectralDataset(Dataset):
    """
    Class for managing a hyperspectral dataset with N samples and M wavelengths
    """
    def __init__(self, data, wavelength, **kwargs):
        """ Create SpectralDataset using measurment data (N-by-M) with N samples and M wavelengths.

        This method extends the constructor from Dataset.
        
        Parameters
        ----------
        data : ndarray
            A 2-D array of shape (N, M) with N the number of samples and M the number of wavelengths.
        wavelenghts : ndarray
            A 1-D array of shape (M,) with M the number of wavelenghts.
        **kwargs: 
            See Dataset.__init__
        """

        super().__init__(data, **kwargs)
        self.set_wl(wavelength)
    
    def set_wl(self, wavelength):
        """ Set the wavelengths to the given `wavelength`.
        
        Parameters
        ----------
        wavelengths : ndarray
            A 1-D array of shape (M,) with M the number of wavelengths.
        """
        
        assert (self._are_valid_wavelengths(wavelength))
        self.wl = deepcopy(wavelength)

    def get_wl(self):
        """ Get wavelenghts as numpy array.
        
        Returns
        -------
        wavelengths: ndarray
            A 1-D array of shape (M,) with M the number of wavelengths.
        """
        return np.asarray(self.wl)

    @_docstring_parameter(WL_UNIT)
    def include_wavelengths(self, start_wl, end_wl):
        """ Include only the spectral region between `start_wl` and `end_wl`.

        Parameters
        ----------
        start_wl: float
            Start wavelength [{0}]
        end_wl: float
            End wavelength [{0}] 
        """
        start_idx = self.get_wl_idx(start_wl)
        end_idx = self.get_wl_idx(end_wl)
        self._set_data(self.data[:,start_idx:end_idx])
        self.set_wl(self.get_wl()[start_idx:end_idx])

    @_docstring_parameter(WL_UNIT)
    def _is_valid_wavelength(self, wavelength):
        """ Check if a certain `wavelength` is valid for this SpectralDataset with given wavelengths.
        
        Parameters
        ----------
        wavelength: float
            Wavelength [{0}] to check
        
        See Also
        --------
        get_wl: get entire array of wavelengths
        """

        if self.get_wl() is None:
            print('No wavelength variables were given to the SpectralDataset. So could not check wavelength of {0}{1}'.format(wavelength, WL_UNIT))
            return False
        elif wavelength < min(self.get_wl()):
            print('Given wavelength ({0}{2}) should be greater then {1}{2}'.format(wavelength, min(self.get_wl()), WL_UNIT))
            return False
        elif wavelength > max(self.get_wl()):
            print('Given wavelength ({0}{2}) should be smaller then {1}{2}'.format(wavelength, max(self.get_wl()), WL_UNIT))
            return False
        else:
            return True

    @_docstring_parameter(WL_UNIT_LONG)
    def _are_valid_wavelengths(self, wavelengths):
        """ Check if the given array of wavelenghts `wavelengths` matches the data structure already present. 
        First assign data before assigning wavelengths.

        Parameters
        ----------
        wavelengths: ndarray
            A 1-D array of shape (M,) with M the number of wavelengths. Wavelengths should be given in {0}.
        """
        assert(isinstance(wavelengths, np.ndarray))

        if wavelengths.shape == (self.get_nb_variables(),):
            return True
        else:
            print('Wavelength was shape {0}, while number of variables was {1}'.format(wavelengths.shape, self.get_nb_variables()))
            return False
    
    @_docstring_parameter(WL_UNIT)
    def get_wl_idx(self, wavelength):
        """ Get index closes to a certain `wavelength` [{0}].

        Parameters
        ----------
        wavelength: float
            Wavelength [{0}]. Wavelength should be in valid range of given wavelengths.

        Returns
        -------
        idx: int
            Index along the spectral dimensions for which get_wl()[idx] is the closest to `wavelength`.
        
        Raises
        ------
        ValueError
            If the given wavelength is outside the wavelength range for this SpectralDataset.
        """

        if not self._is_valid_wavelength(wavelength):
            raise ValueError('Invalid wavelength {0}{1}.'.format(wavelength, WL_UNIT))

        diff = (np.abs(self.get_wl() - wavelength))

        idx = diff.argmin()
        return idx

    def plot(self, nb_spectra=100, labels=True, ax=None, class_ids = [], show=True):
        """ See Dataset.plot """
        if ax is None:
            ax = pyplot.subplot(111)
        ax.set_xlabel('Wavelength [{0}]'.format(WL_UNIT))
        ax.set_ylabel('Reflectance [-]')
        super(SpectralDataset, self).plot(nb_samples=nb_spectra, labels=labels, ax=ax, label_ids=class_ids, show=show)

class HyperSpectralDataset(SpectralDataset):
    """
    Class for handeling HyperSpectralDataset objects.
    """

    def __init__(self, hypercube, wavelength=None, labels=None):
        """
        Create a HyperSpectralDataset.

        Parameters
        ----------
        hypercube: ndarray
            A 3-dimensional array with shape (Y,X,L) where Y and X are the spatial dimension and L is the spectral dimension.
        wavelength: ndarray or list, optional
            A 1-dimensional list or array with shape (L,). If no wavelengths are provided, the spectral indices are used as wavelengths.
        labels: ndarray of ints, optional
            If given, a 1-dimensional array with shape (X*Y,) that contains a label for every spatial position in the X-Y plane.
        
        See Also
        --------
        SpectralDataset
        Dataset
        """
        
        dimY, dimX, dimL = hypercube.shape

        self.image_size = (dimY, dimX)

        if wavelength is None:
            wavelength = range(dimL)
        
        #convert wavelength lists to arrays
        wavelength = np.asarray(wavelength)
        
        self.gui = None

        # first try to reshape inplace to save memory footprint
        try:
            hypercube.shape = (dimY*dimX, dimL)
        except AttributeError:
            hypercube = hypercube.reshape(dimY*dimX, dimL)

        super().__init__(hypercube, wavelength, labels=labels)

    def __getitem__(self, val):
        """ Index a hyperspectral dataset as if it would be a numpy array.
        
        Returns:
        other: HyperSpectralDataset
            New hyperspectral dataset with indexed selection
        """

        #TODO: also allow transfer of labels and included pixels
        HC = self.get_HC(preprocessed=False).__getitem__(val)

        if isinstance(val, tuple) and len(val)==3:
            wl = self.get_wl().__getitem__(val[2])
        else:
            wl = self.get_wl()
        
        return HyperSpectralDataset(hypercube=HC, wavelength=wl)
    
    def __truediv__(self, other) -> None:
        """ Divide this hyperspectral dataset with an other as if they were 3-D numpy arrays."""
        self._as_numpy_function(other, np.divide)
    
    def __sub__(self, other) -> None:
        """ Substract an other hyperspectral dataset with this one as if they were 3D numpy arrays."""
        self._as_numpy_function(other, np.subtract)

    def __add__(self, other) -> None:
        """ Add an other hyperspectral dataset to this one as if they were 3D numpy arrays."""
        self._as_numpy_function(other, np.add)

    def _as_numpy_function(self, other, np_func)-> None:
        """ Helper function to apply numpy mathematical operations on the hypercube. Operations happen inplace.
        
        Parameters
        ----------
        other: HyperSpectralDataset or ndarray
            Argument required for the `np_func`supplied
        np_func: numpy method
            Mathematical method form the numpy library. e.g. np.divide
        """
        HC = self.get_HC()
        if isinstance(other, HyperSpectralDataset):
            HC = np_func(HC, other.get_HC(), out=HC)
        elif isinstance(other, np.ndarray):
            HC = np_func(HC, other, out=HC)
        else:
            raise AttributeError(f'{np_func} on HyperSpectralDataset is not possible with {other.type}')
        self.set_HC(HC)

    def median_filter(self, kernel_size=[3, 3, 3]):
        HC = self.get_HC()
        HC = medfilt(HC, kernel_size=kernel_size)
        self.set_HC(HC)

    @property
    def shape(self):
        return (self.get_dimY(), self.get_dimX(), self.get_dimL())

    def get_label_image(self):
        return self.get_labels(fill=True).reshape((self.get_dimY(), self.get_dimX()))

    def get_band_image(self, band_idx, labeloverlay=False):
        """
        Get image of certain band as Y-by-X ndarray.

        If labeloverlay is true and the HyperSpectralDataset has labels assigend, then an fake RGB image is given with labels overlayed.
        """
        im = np.squeeze(self.get_HC()[:, :, band_idx])
        if labeloverlay and self._has_labels():
            return label2rgb(self.get_label_image(), image=im)
        else:
            return im

    def get_band_ratio_image(self, band1_idx, band2_idx):
        """ Return ratio image of (Band1-Band2)/(Band1+Band2).
        """
        im1 = self.get_band_image(band1_idx)
        im2 = self.get_band_image(band2_idx)
        return (im1-im2)/(im1+im2)

    @_docstring_parameter(WL_UNIT_LONG)
    def get_wl_image(self, wavelength):
        """ Get image at certain wavelength, given in {0}.
        """
        assert self._is_valid_wavelength(wavelength)
        return self.get_band_image(self.get_wl_idx(wavelength))

    def get_wl_ratio_image(self, wavelength1, wavelength2):
        """ Get ratio image between two wavelengths.
        
        Parameters
        ----------
        wavelength1: float
            Wavelength of band 1 [{0}]
        wavelength2: flaot
            Wavelength of band 2 [{0}]
        
        Returns
        -------
        ratio_image: ndarray
            A 2-dimensional array with shape Y by X.
        """
        assert self._is_valid_wavelength(wavelength1) and self._is_valid_wavelength(wavelength2)
        return self.get_band_ratio_image(self.get_wl_idx(wavelength1), self.get_wl_idx(wavelength2))

    def get_spectrum_at(self, posY, posX):
        """ Get spectrum at a certain pixel position Y-X
        """
        spectrum_idx = np.ravel_multi_index((posY, posX), self.get_image_size())
        return np.squeeze(self.get_data(preproc=True, fill_nans=True)[spectrum_idx, :])

    def get_HC(self, preprocessed=True):
        """Get HyperSpectralDataset as ndarray with dimensions dimY-by-dimX-by-dimL.
        By default preprocessed data are given based on self.preprocess_list.
        """
        return self.get_data(preproc=preprocessed, fill_nans=True).reshape((self.get_dimY(), self.get_dimX(), self.get_dimL()))

    def set_HC(self, HC):
        dimY, dimX, dimL = HC.shape

        self.image_size = (dimY, dimX)
        self._set_data(HC.reshape(dimY * dimX, dimL))

    def crop(self, mask):
        assert mask.shape == self.get_image_size()
        rows, cols = np.where(mask)
        return self.get_roi(min_row = min(rows),
                            min_col = min(cols),
                            max_row = max(rows),
                            max_col = max(cols))

    def get_roi(self, min_row=0, min_col=0, max_row=-1, max_col=-1):
        """ Select a Region Of Interest (ROI) for the HyperSpectralDataset. 

        ROI should be defined as a rectangular area defined from a min_row to max_row, and min_col to max_col.
        TODO: can possible be removed with fancy indexing now with __getitem__
        """
        #TODO: make returning copy of self more elegent, maybe use deep copy and change only certain parameters
        if ((min_row >= 0 and min_col >= 0) and (max_row <= self.get_dimY() and max_col <= self.get_dimX())):
            roiHSD = deepcopy(self)
            roiHSD.set_HC(self.get_HC()[round(min_row):round(max_row),round(min_col):round(max_col),:])
            return roiHSD
        else:
            print('ROI does not agree with hypercube dimensions ({0},{1})'.format(self.get_dimY(),self.get_dimX()))
            return None

    def get_rgb(self, preprocessed=False, labeloverlay=True, raw=False):

        try:
            red_idx = self.get_wl_idx(570)
            green_idx = self.get_wl_idx(540)
            blue_idx = self.get_wl_idx(500)
        except:
            red_idx = self.get_wl_idx(1100)
            green_idx = self.get_wl_idx(1300)
            blue_idx = self.get_wl_idx(1600)

        reflectance_im = self.get_HC(preprocessed=preprocessed)[:, :, [red_idx, green_idx, blue_idx]]

        #scale raw images to max bit value
        if raw:
            #TODO: make valid for all kinds of bit depth images. Mabye store type
            reflectance_im = reflectance_im/(2**12-1)
        
        #convert to 8bit RGB
        reflectance_im = np.clip(reflectance_im, 0, 1)

        im = np.multiply(reflectance_im, 255).astype(np.uint8)
        if labeloverlay and self._has_labels():
            return label2rgb(self.get_label_image(), image=im, bg_label=0)
        else:
            return im

    def get_dimY(self):
        """
        Get dimension along scanning direction (Y)
        """
        return self.get_image_size()[0]

    def get_dimX(self):
        """
        Get dimension along spatial direction (X)
        """
        return self.get_image_size()[1]

    def get_dimL(self):
        """
        Get dimension along spectral direction (L)
        """
        return self.get_data().shape[1]

    def get_image_size(self):
        """ Get spatial image size as Y-by-X.
        """
        return self.image_size

    def explore(self):
        """ Interactive gui for exploring the hypercube.
        
        Note
        ----
        Explore functionality is not gauranteed to work in an interactive Python environment like Jupyter Notebook. Use `%matplolib qt5` magic to activate Qt5 backend.
        """

        self.gui = Gui(self)
        self.gui.update_axes()
        pyplot.show()

    @classmethod
    def load(cls, path, **kwargs):
        """ Load HyperSpectralDataset from file. 
        
        File can be either custom hdf5 format or standard remote sensing format like ENVI, Erdas or Aviris.

        Parameters
        ----------
        path: str
            Relative or absolute path to the datafile. For ENVI files, the path to the .hdr file should be given.
        Y_bin: int (optional)
            Binning to be applied along Y dimension before loading
        X_bin: int (optional)
            Binning to be applied along X dimension before loading
        L_bin: int (optional)
            Binning to be applied along L dimension before loading   
        
        Returns
        -------
        hyperspectraldatset: HyperSpectralDataset
            Hyperspectral dataset object from file
        
        See Also
        --------
        _read_from_remote_sensing_format
        _read_from_hdf5
        """
        root, ext = os.path.splitext(path)
        if ext in ['.hdf5','.h5']:
            HC, wavelength, labels = HyperSpectralDataset._read_from_hdf5(path, **kwargs)
        else:
            HC, wavelength = HyperSpectralDataset._read_from_remote_sensing_format(path, **kwargs)
            labels = None
        
        return cls(HC, wavelength, labels)

    def _read_from_remote_sensing_format(path, Y_bin=1, X_bin=1, L_bin=1):
        """ Use the `spectral` library to open ENVI (.hdr), Erdas (.lan) or Aviris (.rfl/.spc) files.
        
        Parameters
        ----------
        path: str
            Relative or absolute path to the datafile. For ENVI files, the path to the .hdr file should be given.
        Y_bin: int (optional)
            Binning to be applied along Y dimension before loading
        X_bin: int (optional)
            Binning to be applied along X dimension before loading
        L_bin: int (optional)
            Binning to be applied along L dimension before loading   
        Returns
        -------
        HC
        wl
        """
        spyfile = open_image(path)
        image_array = spyfile[::Y_bin, ::X_bin, ::L_bin]
        HC = np.asarray(image_array)
        if spyfile.bands.centers is not None:
            wl = spyfile.bands.centers
        else: 
            wl = np.arange(spyfile.nbands)
        wl = wl[::L_bin]
        return HC, wl

    @staticmethod
    def _read_from_hdf5(path, Y_bin=1, X_bin=1, L_bin=1):
        """ Read HyperSpectralDataset object from custom hdf5 format.
        
        See Also
        --------
        save_to_hdf5
        """

        with h5py.File(path, 'r') as hf:
            HC = hf['Hypercube'][::Y_bin,::X_bin,::L_bin]
            wavelength = hf['Wavelengths'][::L_bin]
            labels = None

            if 'Labels' in hf.keys():
                # TODO: include label tablelabel_table=hf['Labels'].attrs['Label_table']
                labels = labels=hf['Labels'][::Y_bin,::X_bin,::L_bin]

        return HC, wavelength, labels

    def save_to_hdf5(self, path, overwrite=False, preprocessed=False):
        #TODO: allow saving preprocessed
        #TODO: make more elegant and future proof using dict (cfr vars(object) -> {'HC': numpy.ndarray, ...}
        if not os.path.isfile(path) or overwrite:
            with h5py.File(path, 'w') as hf:
                #TODO also include inclusion
                self.include_all()
                hf.create_dataset('Hypercube', data=self.get_HC(preprocessed=preprocessed))
                hf.create_dataset('Wavelengths', data=self.get_wl())
                # TODO include preprocessing list. Problem is that preprocessing objects can be not saved to a HDF5 dataset.
                #  Maybe use String representation for preprocessing or never save preprocessing or save preprocessed data.

                if self.labels is not None:
                    label_dataset = hf.create_dataset('Labels', data=self.get_labels())
                    # TODO include label table
                    #label_dataset.attrs['Label_table'] = np.asarray(self.label_table)
        else:
            print('File {0} already exists. Use overwrite=True to overwrite file'.format(path))
            return

    def _is_valid_reference(self, refHSD) -> bool:
        """ Check if a dark or white reference is the correct format"""
        return refHSD.get_dimL() == self.get_dimL()

    def assign_label_image(self, label_image, label_table=None):
        self.assign_labels(label_image.reshape(self.get_dimY()*self.get_dimX(),), label_table=label_table)

    def draw_mask(self, title='Please draw mask'):
        """ Helper function for drawing mask on RGB image from hyperspectraldataset."""
        img = self.get_rgb()
        fig, ax = pyplot.subplots(1, 1)
        fig.suptitle(title, fontsize=16)
        ax.imshow(img)

        mc = MaskCreator(ax)
        pyplot.show()

        mask = mc.get_mask(self.get_image_size())

        return mask

    def draw_labels(self, label_table)->None:
        """ Interactive tool to draw labels on an image. 
        
        Allows you to draw a polygon area for every label in the label_table. Labels are saved inplace at the end.

        Parameters
        ----------
        label_table : list of tuples, optional
            A list of tuples, where every tuple has the format (label_id, label_name). E.g. label_table = [(1, "good"),(2, "bad")].
        """

        label_image = np.zeros(self.get_image_size())

        for label_id, label_name in label_table:
            mask = self.draw_mask('Please select {0}'.format(label_name))
            label_image[mask] = label_id

        self.assign_label_image(label_image, label_table=label_table)

    def get_included_image(self):
        """Get binary image for pixels that are included.
        
        Returns
        -------
        mask: ndarray of booleans
            A Y-by-X boolean array
        
        See Also
        --------
        include
        """
        return self.included_samples.reshape(self.get_dimY(), self.get_dimX())
    
    def include(self, mask):
        """ Include only the pixels from the mask.
        
        See Also
        --------
        Dataset.include
        """
        assert((mask.shape == self.get_image_size()) or (mask.shape == (np.prod(self.get_image_size()))) )
        super(HyperSpectralDataset, self).include(np.ravel(mask))

    def rotate(self, angle, center=None, resize=False):
        """ Return a rotated HyperSpectralDataset. Based on skimage.transform.rotate

        angle: float
            Rotation angle in degrees in counter-clockwise direction.
        center: iterable of length 2, optional: Default None
            The rotation center. If center = None, the hypercube is rotated around its image center, i.e. center = self.get_image_size()/2
        resize: bool, optional: default False
            Determine whether the shape of the input image will be automatically calculated, so the complete rotated image exaclty fits.
        """
        #TODO also include labels and inclusion in rotation
        return HyperSpectralDataset(hypercube=transform.rotate(self.get_HC(), angle, center=center, resize=resize),
                                    wavelength= self.get_wl())

    def __deepcopy__(self, memodict={}):
        self.gui = None
        cls = self.__class__  # Extract the class of the object
        result = cls.__new__(cls)  # Create a new instance of the object based on extracted class
        memodict[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v,memodict))  # Copy over attributes by copying directly or in case of complex objects like lists for exaample calling the `__deepcopy()__` method defined by them. Thus recursively copying the whole tree of objects.
        return result


