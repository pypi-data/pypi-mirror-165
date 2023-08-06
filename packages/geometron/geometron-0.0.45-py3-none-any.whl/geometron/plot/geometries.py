import matplotlib.pyplot as plt
from matplotlib import transforms
from matplotlib.patheffects import SimpleLineShadow, Stroke, Normal
import numpy as np
import shapely.wkb
from shapely.geometry import Point, LineString, LinearRing, Polygon, MultiPoint, MultiLineString
from descartes import PolygonPatch
from .symbols import symbols, symbols_extra_properties
import geopandas as gpd


def effects(highlight):
    """
    Parameters
    ----------
    highlight : bool, default: True
        Adds a white glow around symbol and label if True

    Returns
    -------
    set
        path_effects, stroke_effects
    """

    if highlight:
        path_effects = [SimpleLineShadow(offset=(0., 0.), shadow_color='w', alpha=.5, linewidth=5, capstyle='round')]
        stroke_effects = [Stroke(linewidth=5, foreground='white', alpha=0.75)]
    else:
        path_effects = []
        stroke_effects = []
    path_effects.append(Normal())
    stroke_effects.append(Normal())
    return path_effects, stroke_effects


def plot_shapely_obj(obj=None, ax=None, **kwargs):
    """ Plots a shapely object in matplotlib axes

    Parameters
    ----------
    obj : shapely.geometry
        A shapely object to plot
    ax : matplotlib.axes
        Axes in which the shapely object should be plotted
    kwargs : dict
        Keywords and arguments to pass to matplotlib plot for Point, MultiPoint, LineString, MultiLineString or
        LinearStrings and to patches for polygons

    Returns
    -------
    matplotlib.axes
        the matplotlib axes object used to plot the shapely object
    """

    if ax is None:
        fig, ax = plt.subplots()
        ax.axis('equal')
    if isinstance(obj, Point) or isinstance(obj, LineString) or isinstance(obj, LinearRing):
        x, y = obj.xy
        ax.plot(x, y, **kwargs)
    elif isinstance(obj, MultiLineString) or isinstance(obj, MultiPoint):
        for i in obj:
            plot_shapely_obj(ax=ax, obj=i, **kwargs)
    elif isinstance(obj, Polygon):
        patch = PolygonPatch(obj, **kwargs)
        ax.add_patch(patch)
    else:
        print(f'Warning:Invalid object type - {obj} : {type(obj)}...')
    ax.axis('equal')
    return ax


def plot_profile(obj, ax=None, name='', **kwargs):
    """ Plots a shapely LineString as a profile

    Parameters
    ----------
    obj : shapely.geometry
        A shapely object to plot
    ax : matplotlib.axes
        Axes in which the shapely object should be plotted
    name : str
        Name of the profile

    Returns
    -------
        the matplotlib axes object used to plot
    """

    kwargs.pop('kind')
    kind = 'profile'
    plot_line(obj, ax, name, kind, **kwargs)


def plot_line(obj, ax=None, name='', kind='', highlight=True):
    """ Plots a shapely LineString as a line using a symbology stored in symbols depending on the kind

    Parameters
    ----------
    obj : shapely.geometry
        A shapely object to plot
    ax : matplotlib.axes
        Axes in which the shapely object should be plotted
    name : str
        Name of the line
    kind : str
        Kind of line (i.e. profile, baseline...)
    highlight : bool, default: True
        Adds a white glow around line and label if True

    Returns
    -------
    matplotlib.axes
        the matplotlib axes object used to plot
    """

    if isinstance(obj, LineString):
        path_effects, stroke_effects = effects(highlight)
        if kind in symbols.keys():
            line_symbol = symbols[kind]
        else:
            line_symbol = symbols['default_line']
        ax = plot_shapely_obj(ax=ax, obj=obj, **line_symbol, path_effects=path_effects)
        fig = plt.gcf()
        for i in range(1, len(obj.coords)-1):
            plot_shapely_obj(ax=ax, obj=Point(obj.coords[i]), **symbols['stake'], path_effects=path_effects)
        if kind == 'profile':
            plot_shapely_obj(ax=ax, obj=Point(obj.coords[0]), **symbols['start'])  # start
            plot_shapely_obj(ax=ax, obj=Point(obj.coords[-1]), **symbols['end'])  # end
        theta = np.arctan2(obj.coords[-1][1] - obj.coords[0][1], obj.coords[-1][0] - obj.coords[0][0])
        label_shift = ax.transData + transforms.ScaledTranslation(.075 * np.cos(theta + np.pi/2),
                                                                  .075 * np.sin(theta + np.pi/2), fig.dpi_scale_trans)
        label_pos = obj.interpolate(0.45, normalized=True)
        ax.text(label_pos.x, label_pos.y, name, rotation=np.rad2deg(theta), transform=label_shift,
                path_effects=stroke_effects,
                horizontalalignment='center', verticalalignment='center', multialignment='center')
    return ax


def plot_point(obj, ax=None, name='', kind='', highlight=True):
    """ Plots a shapely Point as a marker using a symbology stored in symbols depending on the kind

    Parameters
    ----------
    obj : shapely.geometry
        A shapely object to plot
    ax : matplotlib.axes
        Axes in which the shapely object should be plotted
    name : str
        Name of the line
    kind : str
        Kind of point (i.e. landmark, station...)
    highlight : bool, default: True
        Adds a white glow around symbol and label if True

    Returns
    -------
    matplotlib.axes
        the matplotlib axes object used to plot
    """

    if isinstance(obj, Point):
        if ax is None:
            _, ax = plt.subplots()
        if kind in symbols.keys():
            symbol = symbols[kind]
        else:
            symbol = symbols['default_point']
        fig = plt.gcf()
        va = 'top'
        v_shift = .25
        if kind in symbols_extra_properties.keys():
            extra_properties = symbols_extra_properties[kind]
            if 'labelpos' in extra_properties.keys():
                if extra_properties['labelpos'].lower() == 'below':
                    v_shift = -.25
                    va = 'bottom'
        label_shift = ax.transData + transforms.ScaledTranslation(0., v_shift, fig.dpi_scale_trans)
        path_effects, stroke_effects = effects(highlight)
        ax.plot(obj.x, obj.y, **symbol, path_effects=path_effects)
        ax.text(obj.x, obj.y, name, transform=label_shift, va=va, ha='center', path_effects=stroke_effects)
    return ax


def plot_gdf_survey(gdf, ax=None, extent=None, grid='off', highlight=True):
    """ Plots elements of a geodataframe describing a survey using a symbology stored in symbols depending on the kind

    Parameters
    ----------
    gdf : pandas.GeoDataFrame
        A geodataframe to plot
    ax : matplotlib.axes
        Axes in which the shapely object should be plotted
    extent : list
        [xmin, xmax, ymin, ymax]
    grid : str, default: 'off'
        'on' to show the grid, 'off' to hide the grid
    highlight : bool, default: True
        Adds a white glow around symbols, lines and labels if True

    Returns
    -------
    matplotlib.axes
        the matplotlib axes object used to plot
    """

    assert isinstance(gdf, gpd.GeoDataFrame)
    assert 'kind' in gdf.columns
    if ax is None:
        _, ax = plt.subplots()
    aspect_ratio = ax.get_aspect()
    for idx, row in gdf.iterrows():
        if row['class'] == 'TopoLine':
            plot_line(row['geometry'], ax=ax, name=row['label'], kind=row['kind'], highlight=highlight)
        if row['class'] == 'TopoPoint':
            plot_point(row['geometry'], ax=ax, name=row['label'], kind=row['kind'], highlight=highlight)
    if extent is not None:
        ax.set_xlim([extent[0], extent[1]])
        ax.set_ylim([extent[2], extent[3]])
    ax.grid(grid)
    if aspect_ratio != 'auto':
        ax.set_aspect(aspect_ratio)
        ax.axis('tight')
    else:
        ax.axis('equal')
    return ax
