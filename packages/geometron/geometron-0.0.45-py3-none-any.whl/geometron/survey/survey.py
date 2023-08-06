import shapely.wkt
from geometron.plot import plot_point, plot_line, symbols
from shapely.geometry import Point, LineString, shape, mapping


class TopoObject:
    def __init__(self, wkt, name='', kind='', show_label=True):
        self._name = ''
        self.name = name
        self._kind = ''
        self.kind = kind.lower()
        self._show_label = True
        self.show_label=show_label
        self._geometry = None
        self.__geo_interface__ = {}
        self.geometry = shapely.wkt.loads(wkt)

    @property
    def show_label(self):
        return self._show_label

    @show_label.setter
    def show_label(self, val):
        assert isinstance(val, bool)
        self._show_label = val

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        assert isinstance(val, str)
        self._name = val

    @property
    def kind(self):
        return self._kind

    @kind.setter
    def kind(self, val):
        assert isinstance(val, str)
        self._kind = val

    @property
    def geometry(self):
        return self._geometry

    @geometry.setter
    def geometry(self, val):
        # assert isinstance(val, shapely.geometry.?)  # TODO: check that geometry is a valid shapely geometry
        self._geometry = val
        self.to_geo()

    def to_geo(self):
        self.__geo_interface__ = {'type': 'Feature',
                                  'properties': {'id': self.name, 'label': self.name if self.show_label else '',
                                                 'kind': self.kind, 'class': str(self.__class__).split('.')[-1][:-2]},
                                  'geometry': mapping(self.geometry)}


class TopoPoint(TopoObject):
    def __init__(self, wkt='POINT (0. 0.)', **kwargs):
        if isinstance(wkt, Point):
            wkt = wkt.wkt
        super().__init__(wkt, **kwargs)
        assert isinstance(self.geometry, Point)
        if self.kind in symbols.keys():
            self.symbol = symbols[self.kind]
        else:
            self.symbol = '.'

    def plot(self, ax=None):
        plot_point(self.geometry, ax=ax, name=self.name, kind=self.kind)


class TopoLine(TopoObject):
    def __init__(self, wkt, **kwargs):
        if isinstance(wkt, LineString):
            wkt = wkt.wkt
        super().__init__(wkt, **kwargs)
        assert isinstance(self.geometry, LineString)

    def plot(self, ax=None):
        plot_line(ax=ax, obj=shape(self.geometry), name=self.name, kind=self.kind)

