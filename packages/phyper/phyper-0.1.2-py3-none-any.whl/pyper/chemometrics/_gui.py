from matplotlib import pyplot
from matplotlib.path import Path
from matplotlib.widgets import PolygonSelector, LassoSelector
import numpy as np

from .. import WL_UNIT, WL_UNIT_LONG

class Gui(object):
    """ Helper class for managing a gui for exploring an HyperSpectralDataset object """

    def __init__(self, HSD):
        self.HSD = HSD

        self.wl_idx = 0
        included_image = self.HSD.get_included_image()
        row_idx, col_idx = np.nonzero(included_image)
        # list of type SpectrumPoint. Initialise with some point inside included data
        self.spectra = [self.SpectrumPoint(col_idx[0], row_idx[0], 0)]

        self.selected_point = None
        self.selected_line = None

        self.vline_artist = None

        self.fig, [self.image_ax, self.spectral_ax] = pyplot.subplots(1, 2)

        self.fig.canvas.mpl_connect('pick_event', self.on_pick)
        self.fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.fig.canvas.mpl_connect('key_press_event', self.on_key)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event):
        if self.selected_point is not None or self.selected_line is not None:
            return
        if not event.dblclick:
            # TODO: make sure only add spectrum when press event is in image axis.
            # Watch out with notebook!! -> event.isaxis == self.image_ax doesn't work.
            return
        # add new SpectrumPoint to list of spectra
        self.spectra.append(self.SpectrumPoint(round(event.xdata), round(event.ydata), len(self.spectra) + 1))

        self.update_axes()

    def on_key(self, event):
        if event.key == 'left':
            self.wl_idx = max([0, self.wl_idx - 1])
            self.update_axes()
        elif event.key == 'right':
            self.wl_idx = min([self.HSD.get_dimL(), self.wl_idx + 1])
            self.update_axes()

    def on_pick(self, event):
        if event.mouseevent.button == 3:
            # remove point if right-clicked
            self.spectra.remove(event.artist.obj)
            self.update_axes()
        elif event.mouseevent.button == 1:
            if hasattr(event.artist, 'obj'):
                self.selected_point = event.artist
            elif self.vline_artist == event.artist:
                self.selected_line = event.artist

    def on_motion(self, event):
        if self.selected_line is None and self.selected_point is None:
            return
        elif self.selected_point is not None and event.xdata is not None:
            self.selected_point.obj.x = round(event.xdata)
            self.selected_point.obj.y = round(event.ydata)
            self.update_axes()
        elif self.selected_line is not None and event.xdata is not None:
            request_wl = np.clip(round(event.xdata), min(self.HSD.get_wl()), max(self.HSD.get_wl()))
            self.wl_idx = self.HSD.get_wl_idx(request_wl)
            self.update_axes()

    def on_release(self, event):
        self.selected_line = None
        self.selected_point = None

    def update_axes(self):

        # save x/y limits of axes to retain zoom ratio when updating window
        old_xlim_image = self.image_ax.get_xlim()
        old_ylim_image = self.image_ax.get_ylim()

        old_xlim_spectral = self.spectral_ax.get_xlim()

        # clear axes
        self.image_ax.clear()
        self.spectral_ax.clear()

        # show band image in image axis
        self.image_ax.imshow(self.HSD.get_band_image(self.wl_idx))

        # indicate wavelength
        self.vline_artist = self.spectral_ax.axvline(x=self.HSD.get_wl()[self.wl_idx], color='k', picker=True,
                                                     pickradius=20)

        # plot points and spectra for each spectrum in list with SpectrumPoints
        for spectrum in self.spectra:
            # draw point in image axis
            spectrum.draw_point(self.image_ax)

            # draw spectrum in spectral axis
            spectrum.draw_spectrum(self.spectral_ax, self.HSD.get_wl(),
                                   self.HSD.get_spectrum_at(spectrum.y, spectrum.x))

        # format axes titles and labels
        self.image_ax.set_title('Wavelenght = {0:.1f} [{1}]'.format(self.HSD.get_wl()[self.wl_idx], WL_UNIT))
        if old_xlim_image != (0, 1):
            self.image_ax.set_xlim(old_xlim_image)
            self.image_ax.set_ylim(old_ylim_image)

        self.spectral_ax.set_xlabel(f'Wavelength [{WL_UNIT}]')
        self.spectral_ax.set_ylabel('Reflectance [-]')
        if old_xlim_spectral != (0, 1):
            self.spectral_ax.set_xlim(old_xlim_spectral)

        # draw new canvas
        self.fig.canvas.draw()

    class SpectrumPoint:
        """ Helper class to manage points for which the spectrum is requested """
        colors = ['#006BA4', '#FF800E', '#ABABAB', '#595959', '#5F9ED1', '#C85200', '#898989', '#A2C8EC', '#FFBC79',
                  '#CFCFCF']
        picker_tolerance = 5
        marker = 'o'
        marker_size = 10

        def __init__(self, Xpos, Ypos, unique_id):
            self.x = Xpos
            self.y = Ypos
            self.id = unique_id
            self.color = self.colors[self.id % len(self.colors)]
            self.point_artist = None  # initialize artist in image axis to None untill first draw
            self.line_artist = None  # initialize artist in spectral axis to None untill first draw

        def draw_point(self, axis):
            self.point_artist = axis.plot(self.x, self.y, color=self.color, marker=self.marker, picker=True,
                                          pickradius=self.picker_tolerance)[0]
            self.point_artist.obj = self

        def draw_spectrum(self, axis, wl, spectrum):
            axis.plot(wl, spectrum, color=self.color)

class MaskCreator(object):
    """Draw mask using selector
    """
    def __init__(self, ax, selector = 'polygon'):
        ''' Selector can be 'lasso' or 'polygon'
        '''
        if selector == 'lasso':
            self.selector = LassoSelector(ax,
                                          self.onselect,
                                          lineprops={'color':'r','linewidth':5})
        else:
            self.selector = PolygonSelector(ax,
                                            self.onselect,
                                            useblit=True,
                                            lineprops={'color':'r'},
                                            markerprops={'color':'r'})
        self.path = None

    def get_mask(self, shape):
        """Return image mask given by mask creator"""
        if self.path is None:
            return np.zeros(shape,dtype=bool)
        h, w = shape
        y, x = np.mgrid[:h, :w]
        points = np.transpose((x.ravel(), y.ravel()))
        grid = self.path.contains_points(points)  # now you have a mask with points inside a polygon
        return grid.reshape(h, w)

    def onselect(self, verts):
        self.path = Path(verts)


def mask_creator_demo():
    img = np.random.uniform(0, 255, size=(100, 100))
    ax = pyplot.subplot(111)
    ax.imshow(img)

    mc = MaskCreator(ax, 'lasso')
    pyplot.show()

    mask = mc.get_mask(img.shape)
    img[~mask] = np.uint8(np.clip(img[~mask] - 100., 0, 255))
    pyplot.imshow(img)
    pyplot.title('Region outside of mask is darkened')
    pyplot.show()


if __name__ == '__main__':
    mask_creator_demo()