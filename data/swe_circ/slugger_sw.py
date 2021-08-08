""" plotting tools for slugCode, shallow water version"""
from copy import deepcopy
from mpl_toolkits import axes_grid1  # for colorbar
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits import mplot3d


def get_data(data, var):
    """Return the data of given variable name: [hght, velx, vely]"""
    try:
        var_data = getattr(data, var)
    except AttributeError:
        print("Error: " + var + " not found")
        raise

    return var_data


def add_colorbar(im, aspect=20, pad_fraction=0.5, **kwargs):
    """draw color bar in proper position and size"""
    divider = axes_grid1.make_axes_locatable(im.axes)
    width = axes_grid1.axes_size.AxesY(im.axes, aspect=1 / aspect)
    pad = axes_grid1.axes_size.Fraction(pad_fraction, width)
    current_ax = plt.gca()
    cax = divider.append_axes("right", size=width, pad=pad)
    plt.sca(current_ax)

    return im.axes.figure.colorbar(im, cax=cax, **kwargs)


class data1d:

    class ascii:

        def __init__(self, file_name):
            self.filename = file_name
            self.raw = np.loadtxt(file_name)
            self.x = self.raw[:, 0]
            self.hght = self.raw[:, 1]
            self.velx = self.raw[:, 2]

        def plot(self, var, ax, *args, **kwargs):

            var_data = get_data(self, var)

            ax.plot(self.x, var_data, label=self.filename, *args, **kwargs)


class data2d:

    class ascii:

        def __init__(self, file_name):
            self.raw = np.loadtxt(file_name)
            # self.bins = int(np.sqrt(np.size(self.raw[:, 0])))
            self.xbins = int(np.shape(np.unique(self.raw[:, 0]))[0])
            self.ybins = int(np.shape(np.unique(self.raw[:, 1]))[0])
            self.x = np.reshape(self.raw[:, 0], (self.xbins, self.ybins)).T
            self.y = np.reshape(self.raw[:, 1], (self.xbins, self.ybins)).T
            self.hght = np.reshape(self.raw[:, 2], (self.xbins, self.ybins)).T
            self.velx = np.reshape(self.raw[:, 3], (self.xbins, self.ybins)).T
            self.vely = np.reshape(self.raw[:, 4], (self.xbins, self.ybins)).T

        def __add__(self, other):
            total = deepcopy(self)
            total.raw = 0.
            # total.bins = self.bins
            total.xbins = self.xbins
            total.ybins = self.ybins
            total.x = self.x
            total.y = self.y

            total.hght = self.hght + other.hght
            total.velx = self.velx + other.velx
            total.vely = self.vely + other.vely

            return(total)

        def __sub__(self, other):
            total = deepcopy(self)
            total.raw = 0.
            # total.bins = self.bins
            total.xbins = self.xbins
            total.ybins = self.ybins
            total.x = self.x
            total.y = self.y

            total.hght = self.hght - other.hght
            total.velx = self.velx - other.velx
            total.vely = self.vely - other.vely

            return(total)

        def edge_grid(self):

            dx = self.x[0, 1] - self.x[0, 0]
            dy = self.y[1, 0] - self.y[0, 0]

            # shift center points by delta/2
            # this is one dimensional array
            xx = self.x[0, :] - dx/2.
            yy = self.y[:, 0] - dy/2.

            # append last point
            xi = np.append(xx, xx[-1]+dx)
            yi = np.append(yy, yy[-1]+dy)

            return xi, yi

        def check_symmetric(self, var, tol=1e-8):

            var_data = get_data(self, var)

            sym_diag = np.allclose(var_data, var_data.T, atol=tol)
            sym_lr = np.allclose(var_data, np.fliplr(var_data), atol=tol)
            sym_ud = np.allclose(var_data, np.flipud(var_data), atol=tol)
            symmetric = sym_lr and sym_ud and sym_diag
            print(sym_lr, sym_ud, sym_diag, symmetric)

            if(not symmetric):
                print("[[[ WARN: DATA IS ASYMMETRIC ]]]")

            return(symmetric)

        def plot_cmap(self, var, ax, *args, **kwargs):

            var_data = get_data(self, var)

            xi, yi = self.edge_grid()

            im = ax.pcolormesh(xi, yi, var_data, *args, **kwargs)
            ax.set_title(var)
            add_colorbar(im)

        def plot_contour(self, var, ax, nlevel=20, *args, **kwargs):

            var_data = get_data(self, var)

            extent = (np.amin(self.x), np.amax(self.x),
                      np.amin(self.y), np.amax(self.y))

            levels = np.linspace(var_data.min(), var_data.max(), nlevel)
            # levels = np.log(levels)
            # levels = np.logspace(var_data.min(), var_data.max(), nlevel)

            ax.contour(var_data, extent=extent, levels=levels, *args, **kwargs)
            ax.set_title(var)

        def plot_slicex(self, var, ax, *args, **kwargs):

            var_data = get_data(self, var)

            if self.xbins % 2 == 0:
                pos1 = int(self.xbins/2)
                pos2 = int(self.xbins/2) + 1
                slice_data = 0.5*(var_data[:, pos1] + var_data[:, pos2])
            else:
                pos = int(self.xbins/2) + 1
                slice_data = var_data[:, pos]

            ax.plot(self.x[0, :], slice_data, *args, **kwargs)
            ax.set_title(var + ":slice in x")

        def plot_slicey(self, var, ax, *args, **kwargs):

            var_data = get_data(self, var)

            if self.ybins % 2 == 0:
                pos1 = int(self.ybins/2)
                pos2 = int(self.ybins/2) + 1
                slice_data = 0.5*(var_data[pos1, :] + var_data[pos2, :])
            else:
                pos = int(self.ybins/2) + 1
                slice_data = var_data[pos, :]

            ax.plot(self.y[:, 0], slice_data, *args, **kwargs)
            ax.set_title(var + ":slice in y")

        def plot_slice45(self, var, ax, *args, **kwargs):

            var_data = get_data(self, var)

            slice45 = np.zeros(self.xbins)
            for i in range(self.xbins):
                slice45[i] = var_data[i, i]

            ax.plot(np.sqrt(2)*self.x[0, :], slice45, *args, **kwargs)
            ax.set_title(var + ":slice in 45 degree")

        def plot_symlr(self, var, ax, *args, **kwargs):

            var_data = get_data(self, var)
            data_lr = np.fliplr(var_data)

            diff = np.abs(var_data - data_lr)
            xi, yi = self.edge_grid()

            im = ax.pcolormesh(xi, yi, diff, *args, **kwargs)
            ax.set_title('diff_LR : ' + var + '\nsum : ' +
                         format(np.sum(diff), 'e'))
            add_colorbar(im)

        def plot_symud(self, var, ax, *args, **kwargs):

            var_data = get_data(self, var)
            data_ud = np.flipud(var_data)

            diff = np.abs(var_data - data_ud)
            xi, yi = self.edge_grid()

            im = ax.pcolormesh(xi, yi, diff, *args, **kwargs)
            ax.set_title('diff_UD : ' + var + '\nsum : ' +
                         format(np.sum(diff), 'e'))
            add_colorbar(im)

        def plot_sym45(self, var, ax, *args, **kwargs):

            var_data = get_data(self, var)
            data_45 = var_data.T

            diff = np.abs(var_data - data_45)
            xi, yi = self.edge_grid()

            im = ax.pcolormesh(xi, yi, diff, *args, **kwargs)
            ax.set_title('diff_45 : ' + var + '\nsum : ' +
                         format(np.sum(diff), 'e'))
            add_colorbar(im)

        def plot_surf(self, var, ax, *args, **kwargs):

            var_data = get_data(self, var)

            im = ax.plot_surface(self.x, self.y, var_data, cmap=cm.Blues, *args, **kwargs)
            ax.set_title(var)
            add_colorbar(im)
