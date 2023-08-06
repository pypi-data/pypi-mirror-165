import numpy as np
import geopandas
from scipy.interpolate import CloughTocher2DInterpolator, griddata
import matplotlib.pyplot as plt


def interpolate_xyv(gdf, col, ax=None, method='linear', extent=None, vlim=None, dx=None, dy=None,
                    xy=None, plot=True, **kwargs):
    """Interpolate values stored in a column of a geodataframe of Points on a structured or unstructured grid

    Parameters
    ----------
    gdf: geopandas.GeoDataFrame
        A geodataframe containing points and at least a column of values to interpolate
    col: str
        Name of the column containing the values to interpolate
    ax: matplotlib.pyplot.axes, default: None
        A matplotlib axes to plot the interpolated map. If None, a new figure and a new axes are created
    method: str, default: 'linear'
        An interpolation method to use for interpolation on a structured grid (nearest, linear or cubic)
    extent: iterable, default: None
        Extent of the interpolation. If None, extent is determined from the extent of gdf
    vlim: iterable, default: None
        Minimum and maximum values for the representation of the interpolated values. If None, vlim is determined from
        the range of the interpolated values
    dx: float, default: None
        Step of the grid long the x axis. If None, dx is computed from the extent
    dy: float, default: None
        Step of the grid long the y axis. If None, dx is computed from the extent
    xy: numpy.ndarray, default: None
        Coordinates of the points defining an unstructured grid for a Clough-Tocher interpolation. The method argument
        is ignored if xy is not None
    plot: bool, default: True
        Plots the interpolated map in ax
    kwargs: dict
        Keywords and arguments to pass to matplotlib.pyplot.imshow or matplotlib.pyplot.triplot

    Returns
    -------
    numpy.ndarray
        Interpolated values
    matplotlib.pyplot.AxesImages
        plotted image
    """

    xyv = gdf[['geometry', col]].copy()
    xyv.rename({col: 'v'}, axis=1, inplace=True)
    if extent is None:
        extent = xyv.total_bounds
        extent = [extent[0], extent[2], extent[1], extent[3]]
    if dx is None:
        if dy is None:
            dx = (extent[1] - extent[0]) / 800.
            dy = (extent[3] - extent[2]) / 600.
            dx = min(dx, dy)
            dy = dx
        else:
            dx = dy
    elif dy is None:
        dy = dx
    xyi = list(zip(xyv.geometry.x.values, xyv.geometry.y.values))
    vi = xyv.v.values
    x, y = np.mgrid[extent[0]:extent[1]:dx, extent[2]:extent[3]:dy]
    if plot:
        if ax is None:
            _, ax = plt.subplots()
    if xy is not None:  # unstructured grid
        interpolation_model = CloughTocher2DInterpolator(xyi, vi)
        v = interpolation_model(xy)
        if plot:
            if vlim is None:
                vlim = [np.nanmin(v), np.nanmax(v)]
            im = ax.tricontourf(xy[~np.isnan(v), 0], xy[~np.isnan(v), 1], v[~np.isnan(v)], extent=extent, vmin=vlim[0],
                                vmax=vlim[1], **kwargs)
            ax.axis('equal')
            return v, im
        else:
            return v
    else:  # structured grid
        v = np.flipud(griddata(xyi, vi, (x, y), method=method).T)
        if plot:
            if vlim is None:
                vlim = [np.nanmin(v), np.nanmax(v)]

            im = ax.imshow(v, extent=extent, vmin=vlim[0], vmax=vlim[1], **kwargs)
            ax.axis('equal')
            return v, im
        else:
            return v
