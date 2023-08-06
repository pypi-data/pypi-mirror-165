from abc import ABC, abstractmethod
import numpy as np
from copy import deepcopy

from .dataset import Dataset, SpectralDataset, HyperSpectralDataset
from .preprocessing import MeanCenter

from sklearn import cross_decomposition, svm, decomposition, cluster
from skimage import segmentation
from scipy import interpolate

class Analysis(ABC):

    def __init__(self):
        super().__init__()
        self.X_cal = None
        self.Y_cal = None
        self.preprocessing_list = None
        self.model = None

    def set_calibration_data(self, X_cal=None, Y_cal=None, copy=True):
        if isinstance(X_cal, Dataset):
            self.preprocessing_list = deepcopy(X_cal.preprocess_list)
            is_mean_centered = False
            for preprocess in self.preprocessing_list:
             if isinstance(preprocess, MeanCenter):
                is_mean_centered = True
            if not is_mean_centered:
                print('WARNING: Preprocessing does not contain mean-centering. Mean centering is often required for optimal algorithm performance!')
        if copy:
            self.X_cal = deepcopy(X_cal)
            self.Y_cal = deepcopy(Y_cal)
        else:
            self.X_cal = X_cal
            self.Y_cal = Y_cal

    def has_preprocessing(self):
        return bool(self.preprocessing_list)

    def get_calibration_data(self):
        """ Get shallow copy of X_cal and Y_cal"""
        return self.X_cal, self.Y_cal
    
    def get_X_cal(self):
        return self.get_calibration_data()[0]

    def get_Y_cal(self):
        if self.get_calibration_data()[1] is None:
            if isinstance(self.get_X_cal(), Dataset) and self.get_X_cal().get_labels() is not None:
                return self.get_X_cal().get_labels()
            else:
                return None
        else:
            return self.get_calibration_data()[1]

    def return_as(self, result, input_data):
        if isinstance(input_data, HyperSpectralDataset):
            return np.reshape(result, input_data.get_image_size())
        else:
            return result

# ----------------- Classification -----------------

class Classification(Analysis):
    """ Wrapper class for all classification classes (e.g. PLSDA/LDA/QDA/SVM...) """

    def __init__(self):
        super(Classification, self).__init__()

    def calibrate(self, X_cal=None, Y_cal=None):
        self.set_calibration_data(X_cal, Y_cal)

        if self.get_X_cal() is None or self.get_Y_cal() is None:
            raise ValueError('Can not calibrate with X_cal or Y_cal missing.')

        self.model.fit(np.asarray(self.get_X_cal()), np.asarray(self.get_Y_cal()))

    def predict(self, X_test):
        X_test = deepcopy(X_test)
        if isinstance(X_test, Dataset) and isinstance(self.get_X_cal(), Dataset):
            X_test.copy_preprocess(self.get_X_cal())
        class_labels = self.model.predict(X_test)
        if isinstance(X_test, HyperSpectralDataset):
            X_test.assign_labels(class_labels)
            return X_test.get_label_image()
        elif isinstance(X_test, Dataset):
            X_test.assign_labels(class_labels)
            return X_test.get_labels()
        else:
            return class_labels

    def accuracy(self):
        return sum(np.equal(self.predict(self.get_X_cal()), self.get_Y_cal())) / self.get_Y_cal().size

class PLSDA(Classification):

    def __init__(self, nb_latent_variables=2):
        super(PLSDA, self).__init__()
        self.nb_latent_variables = nb_latent_variables
        self.model = cross_decomposition.PLSRegression(n_components=self.nb_latent_variables, scale=False)

    def calibrate(self, X_cal=None, Y_cal=None):
        self.set_calibration_data(X_cal, Y_cal)

        if self.get_X_cal() is None:
            raise ValueError('Can not calibrate PLSDA with X_cal missing.')
        if self.get_Y_cal() is None:
            raise ValueError('Can not calibrate PLSDA with Y_cal missing.')

        Y_regression = self.class_to_regression(self.get_Y_cal())
        print(np.asarray(X_cal).shape, np.asarray(Y_regression).shape)
        self.model.fit(np.asarray(X_cal), np.asarray(Y_regression))

    def predict(self, X_test, decision_rule=0.5):
        X_test = deepcopy(X_test)
        if isinstance(X_test, Dataset) and isinstance(self.get_X_cal(), Dataset):
            if self.has_preprocessing():
                X_test.preprocess_list = self.preprocessing_list
                X_test.apply_preprocess()
        Y_regression = self.model.predict(np.asarray(X_test))
        class_labels = self.regression_to_class(Y_regression, decision_rule=decision_rule)
        if isinstance(X_test, HyperSpectralDataset):
            X_test.assign_labels(class_labels)
            return X_test.get_label_image()
        elif isinstance(X_test, Dataset):
            X_test.assign_labels(class_labels)
            return X_test.get_labels()
        else:
            return class_labels

    def get_class_ids(self):
        if self.get_Y_cal() is not None:
            return np.unique(self.get_Y_cal())
        else:
            raise AttributeError('Please provide Y calibration data before requesting class ids')

    def get_nb_classes(self):
        """ TODO: make independed of changes in calibration data (because atm shallow copy)."""
        return self.get_class_ids().size

    def class_to_regression(self, Y_class):
        nb_samples = Y_class.shape[0]
        nb_classes = self.get_nb_classes()
        class_ids = self.get_class_ids()

        Y_reg = np.zeros((nb_samples, nb_classes), dtype=int)
        for i in range(nb_classes):
            Y_reg[:, i] = Y_class == class_ids[i]

        return Y_reg

    def regression_to_class(self, Y_regression, decision_rule=0.5):
        """ decision rule options: 'most_probable' or float percentage (e.g. 0.5).
        Uncertain values are returned as -1
        """
        assert self.get_nb_classes() == Y_regression.shape[1]

        nb_samples, nb_classes = Y_regression.shape
        class_ids = self.get_class_ids()

        if isinstance(decision_rule, float):
            binary_matrix = Y_regression > decision_rule

        elif decision_rule == 'most_probable':
            max_prop = np.amax(Y_regression, axis=1)
            binary_matrix = np.equal(Y_regression.transpose(), max_prop).transpose()
        else:
            raise ValueError('Unknown decision rule {0}'.format(decision_rule))

        Y_class = np.full([nb_samples, ], -1, dtype=int)

        for i in range(nb_classes):
            Y_class[binary_matrix[:, i]] = class_ids[i]
        return Y_class

    def get_coeffs(self):
        return self.model.coef_

    def get_vips(self):
        if self.model is not None:
            t = self.model.x_scores_
            w = self.model.x_weights_
            q = self.model.y_loadings_
            p, h = w.shape
            vips = np.zeros((p,))
            s = np.diag(t.T @ t @ q.T @ q).reshape(h, -1)
            total_s = np.sum(s)
            for i in range(p):
                weight = np.array([(w[i, j] / np.linalg.norm(w[:, j])) ** 2 for j in range(h)])
                vips[i] = np.sqrt(p * (s.T @ weight) / total_s)
            return vips

class SVM(Classification):

    def __init__(self):
        super(SVM, self).__init__()
        self.model = svm.LinearSVC()
# ----------------- Decomposition -----------------

class Decomposition(Analysis):

    def __init__(self):
        super().__init__()

    def calibrate(self, X_cal=None):
        if X_cal is not None:
            self.set_calibration_data(X_cal)

        if self.get_X_cal() is None:
            raise ValueError('Can not calibrate because no calibration data (X_cal) was provided')
        else:
            self.model.fit(self.get_X_cal())


class PCA(Decomposition):

    def __init__(self, number_of_components='mle'):
        """ Create PCA model.
            number_of_components: (int, float, 'mle', None)
                - int: fixed number of components
                - float: number between 0 and 1: find number of components that explains this percentage of variance
                - 'mle' {default}: automaticaly find number of components based on max likelihood estimation
                - None: take maximal number of components (based on nb_variables and nb_samples)"""

        super().__init__()
        self.model = decomposition.PCA(n_components=number_of_components)

    def scores_plot(self, score_1, score_2):
        scores_matrix = self.get_scores()
        plt.scatter(scores_matrix[:, score_1], scores_matrix[:, score_2])
        plt.show()

    def plot_loadings(self):
        plt.plot(self.get_loadings())
        plt.show()

    def get_scores(self):
        return self.apply(self.get_X_cal())

    def apply(self, X):
        if self.model is None:
            raise Exception('Please calibrate model before applying to test data')
        else:
            scores = self.model.transform(X)
            if isinstance(X, HyperSpectralDataset):
                return HyperSpectralDataset(
                    hypercube=np.reshape(scores, [X.get_dimY(), X.get_dimX(), self.get_nb_components()]))
            elif isinstance(X, Dataset):
                return Dataset(scores)
            else:
                return scores

    def get_loadings(self):
        if self.model is None:
            raise Exception('Please calibrate model before getting score')
        else:
            return self.model.components_

    def get_nb_components(self):
        if self.model is None:
            raise Exception('Please calibrate model before getting score')
        else:
            return self.model.n_components_


class Spline(Analysis):
    """ good website with information on splines: https://observablehq.com/@herbps10/b-splines"""

    def __init__(self, nb_splines, spline_degree=2):
        """ Default: cubic spline (degree 2)"""
        super().__init__()
        self.nb_splines = nb_splines
        self.spline_degree = spline_degree

    def apply(self, X):
        data_array = np.asarray(X)
        nb_samples = data_array.shape[0]
        spline_coeff_array = np.zeros((nb_samples, self.nb_splines))
        predicted_data = np.zeros(data_array.shape)

        # work with wavelengths as x for Spectral data
        if isinstance(X, SpectralDataset):
            x = X.get_wl()
        else:
            x = np.linspace(0, data_array.shape[1])

        # iterate over all samples. Fit least squares spline estimation for each sample
        for i in range(nb_samples):
            nb_knots = self.nb_splines - 2 * self.spline_degree
            knots = np.linspace(x[0], x[-1], nb_knots)
            knots = knots[1:-1]
            y = data_array[i]

            t, c, k = interpolate.splrep(x=x, y=y, k=self.spline_degree, t=knots)

            spline_coeff_array[i] = c
            # predicted_data[i] = sp_interp.splev(x,(t,c,k))

        if isinstance(X, HyperSpectralDataset):
            return HyperSpectralDataset(
                hypercube=np.reshape(spline_coeff_array, [X.get_dimY(), X.get_dimX(), self.nb_splines]), wavelength=t)
        if isinstance(X, SpectralDataset):
            return SpectralDataset(spline_coeff_array, t)
        elif isinstance(X, Dataset):
            return Dataset(spline_coeff_array)
        else:
            return spline_coeff_array

# ----------------- Clustering -----------------

class Cluster(Analysis):

    def __init__(self):
        super().__init__()


class KMeans(Cluster):

    def __init__(self, n_clusters=8):
        super().__init__()
        self.model = cluster.MiniBatchKMeans(n_clusters=n_clusters)

    def apply(self, X):
        self.set_calibration_data(X_cal=X)
        return self.return_as(self.model.fit_predict(X=X), X)

class SlicKMeans(Cluster):
    """ Class for fast clustering of Hyperspectral Images.

    First a SLIC will be performed on the fake RGB image. In a second step, the mean spectrum from each superpixel will be clustered.
    """

    def __init__(self, n_clusters=8, n_pixels=1000):
        super().__init__()
        self.n_clusters = n_clusters
        self.n_pixels = n_pixels

    def apply(self, X):
        if not isinstance(X, HyperSpectralDataset):
            raise ValueError('SlicKMeans algorithm can only be applied to objects of class "HypespectralDataset"')
        else:
            self.set_calibration_data(X_cal=X)

            #determine superpixels and extract mean spectra
            slic_seg = segmentation.slic(self.get_X_cal().get_rgb(), n_segments=self.n_pixels, start_label=1)
            self.get_X_cal().assign_label_image(slic_seg)
            data, labels = self.get_X_cal()._get_mean_data()

            #cluster mean spectra
            cluster_labels = cluster.MiniBatchKMeans(n_clusters=self.n_clusters).fit_predict(data)

            #reconstruct label image with cluster output
            #TODO: make fool proof is nuber of clusters is creater than 255
            label_image = np.full(self.get_X_cal().get_image_size(), fill_value=0, dtype=np.uint8)
            for i in range(len(labels)):
                label_image[slic_seg == labels[i]] = cluster_labels[i]
            return label_image

