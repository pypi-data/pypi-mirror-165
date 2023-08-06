from pathlib import Path as plPath
import numpy as np
import matplotlib.path as mpath
from svgpathtools import svg2paths
import svgpath2mpl


def svg_to_marker(filename, x_reduce=np.mean, y_reduce=np.mean, x_flip=False, y_flip=True):
    """ Converts a svg symbol to a matplotlib path to use as a marker

    Parameters
    ----------
    filename: str
              name of the svg file
    x_reduce: function
              function to use for x coordinates reduction (default: np.mean)

    y_reduce: function
              function to use for y coordinates reduction (default: np.mean)

    x_flip: bool
            if true, x coordinates are reversed

    y_flip: bool
            if true, y coordinates are reversed

    Returns
    -------
    marker: matplotlib.path.Path
            a path to use as a marker in matplotlib plots
    """

    if x_flip:
        x_flip = -1
    else:
        x_flip = 1
    if y_flip:
        y_flip = -1
    else:
        y_flip = 1
    # print(f'filename: {filename}, type: {type(filename)}')
    svg = svg2paths(filename)

    # noinspection SpellCheckingInspection
    verts = np.concatenate([svgpath2mpl.parse_path(i.d()).vertices for i in svg[0]])
    codes = np.concatenate([svgpath2mpl.parse_path(i.d()).codes for i in svg[0]])
    marker = mpath.Path(verts, codes)
    marker.vertices[:, 0] -= x_reduce(marker.vertices[:, 0])
    marker.vertices[:, 1] -= y_reduce(marker.vertices[:, 1])
    marker.vertices[:, 0] = x_flip * marker.vertices[:, 0]
    marker.vertices[:, 1] = y_flip * marker.vertices[:, 1]
    return marker


SYM_DIR = (plPath(__file__).parent.absolute() / 'svg_symbols').resolve()


symbols = {'station': {'marker': svg_to_marker(str(SYM_DIR / 'station.svg')), 'alpha': 1.,
                       'markerfacecolor': 'none', 'markeredgecolor': 'black', 'markersize': 12},
           'landmark': {'marker': svg_to_marker(str(SYM_DIR / 'landmark.svg')), 'alpha': 1.,
                        'markerfacecolor': 'none', 'markeredgecolor': 'black', 'markersize': 12},
           'stake': {'marker': svg_to_marker(str(SYM_DIR / 'stake.svg')), 'alpha': 1.,
                     'markerfacecolor': 'none', 'markeredgecolor': 'black', 'markersize': 8},
           'start': {'marker': 'o', 'alpha': 0.75, 'markerfacecolor': 'lightgreen', 'markeredgecolor': 'green',
                     'markersize': 10},
           'end': {'marker': 's', 'alpha': 0.75,
                   'markerfacecolor': 'red', 'markeredgecolor': 'firebrick', 'markersize': 10},
           'shot': {'marker': svg_to_marker(str(SYM_DIR / 'shot.svg')), 'alpha': 1., 'markerfacecolor': 'red',
                    'markeredgecolor': 'black', 'markersize': 12},
           'geophone': {'marker': svg_to_marker(str(SYM_DIR / 'geophone.svg')), 'alpha': 1., 'markerfacecolor': 'none',
                        'markeredgecolor': 'black', 'markersize': 8},
           'default_point': {'marker': '.', 'alpha': 1.0, 'markerfacecolor': 'black', 'markeredgecolor': 'black',
                             'markersize': 6},
           'profile': {'linestyle': '--', 'linewidth': 0.75, 'color': 'black', 'alpha': 1.},
           'default_line': {'linestyle': '-', 'linewidth': 0.75, 'color': 'black', 'alpha': 1.}
           }

symbols_extra_properties = {'station': {'labelpos': 'above'},
                            'landmark': {'labelpos': 'below'},
                            'stake': {'labelpos': 'above'},
                            'start': {},
                            'end': {},
                            'shot': {'labelpos': 'below'},
                            'geophone': {'labelpos': 'above'},
                            'default_point': {'labelpos': 'above'},
                            'profile': {},
                            'default_line': {}
                            }
