"""GEO Point Class

This module defines the geo point class and some utility functions.

For representing a point in geospace as both polar and transformed cartesian.

"""

from math import pi, sin, cos, tan, sqrt

# minimum distance for equality in parametric form ~ 1m over 100km
F_EPSILON = 0.00001
_deg2rad = pi / 180.0
_rad2deg = 180.0 / pi


def ll2cart(lat, lon, clon, cnorth=0.0):
    """helper func: convert lat,lon to route specific cartesian coordinates"""
    # source: http://www.gpsy.com/gpsinfo/geotoutm/
    a = 6378137  # WGS-84 ellipsoid 'EquatorialRadius'
    eccSquared = 0.00669438  # WGS-84 ellipsoid 'EccentricitySquared'
    k0 = 0.9996
    lonTemp = (lon + 180) - int(
        (lon + 180) / 360) * 360 - 180  # -180.00 .. 179.9
    latRad = lat * _deg2rad
    lonRad = lonTemp * _deg2rad
    lonOrigin = clon
    lonOriginRad = lonOrigin * _deg2rad
    eccPrimeSquared = (eccSquared) / (1 - eccSquared)
    N = a / sqrt(1 - eccSquared * sin(latRad) * sin(latRad))
    T = tan(latRad) * tan(latRad)
    C = eccPrimeSquared * cos(latRad) * cos(latRad)
    A = cos(latRad) * (lonRad - lonOriginRad)
    M = a * (
        (1 - eccSquared / 4 - 3 * eccSquared * eccSquared / 64 -
         5 * eccSquared * eccSquared * eccSquared / 256) * latRad -
        (3 * eccSquared / 8 + 3 * eccSquared * eccSquared / 32 +
         45 * eccSquared * eccSquared * eccSquared / 1024) * sin(2 * latRad) +
        (15 * eccSquared * eccSquared / 256 +
         45 * eccSquared * eccSquared * eccSquared / 1024) * sin(4 * latRad) -
        (35 * eccSquared * eccSquared * eccSquared / 3072) * sin(6 * latRad))

    e = (k0 * N * (A + (1 - T + C) * A * A * A / 6 +
                   (5 - 18 * T + T * T + 72 * C - 58 * eccPrimeSquared) * A *
                   A * A * A * A / 120))
    n = (k0 * (M + N * tan(latRad) *
               (A * A / 2 + (5 - T + 9 * C + 4 * C * C) * A * A * A * A / 24 +
                (61 - 58 * T + T * T + 600 * C - 330 * eccPrimeSquared) * A *
                A * A * A * A * A / 720)))
    return (e, n - cnorth)


class geopt(object):
    """A class for representing geospatial point."""

    def __init__(self,
                 lat=None,
                 lng=None,
                 t=None,
                 x=None,
                 y=None,
                 z=None,
                 txt=None,
                 time=None,
                 ico=None):
        """Construct object."""
        if lat is not None:
            self.lat = float(lat)
        else:
            self.lat = None
        if lng is not None:
            self.lng = float(lng)
        else:
            self.lng = None
        if t is not None:
            self.t = float(t)
        else:
            self.t = None
        if x is not None:
            self.x = float(x)
        else:
            self.x = None
        if y is not None:
            self.y = float(y)
        else:
            self.y = None
        if z is not None:
            self.z = float(z)
        else:
            self.z = None
        self.time = time
        self.txt = txt
        self.ico = ico

    def __str__(self):
        """Return a normalised tod string."""
        return self.refstr()

    def __unicode__(self):
        """Return a normalised tod string."""
        return self.refstr()

    def __repr__(self):
        """Return object representation string."""
        return "geopt(lat={0}, lng={1}, t={2}, x={3}, y={4}, z={5}, txt={6}, time={7}, ico={8})".format(
            repr(self.lat), repr(self.lng), repr(self.t), repr(self.x),
            repr(self.y), repr(self.z), repr(self.txt), repr(self.time),
            repr(self.ico))

    def serialise(self):
        """Return a json'bl object."""
        return {
            u'lat': self.lat,
            u'lng': self.lng,
            u't': self.t,
            u'x': self.x,
            u'y': self.y,
            u'z': self.z,
            u'txt': self.txt,
            u'time': self.time,
            u'ico': self.ico
        }

    def refstr(self):
        """Return basic string form.

        'lat, lng, t, x, y, z, txt, ico'

        """
        return u'{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}'.format(
            self.lat, self.lng, self.t, self.x, self.y, self.z, self.txt,
            self.time, self.ico)

    def copy(self):
        """Return a copy of the supplied geopt."""
        return geopt(self.lat, self.lng, self.t, self.x, self.y, self.z,
                     self.txt, self.time, self.ico)

    def lerp(self, other, t):
        """Return a new geopt, linearly interpolated between self and other."""
        ret = self.copy()
        frac = (t - self.t) / (other.t - self.t)
        ret.lat = self.lat + (other.lat - self.lat) * frac
        ret.lng = self.lng + (other.lng - self.lng) * frac
        ret.x = self.x + (other.x - self.x) * frac
        ret.y = self.y + (other.y - self.y) * frac
        ret.z = self.z + (other.z - self.z) * frac
        ret.t = t
        return ret

    def __sub__(self, other):
        """Return cartesian segment length."""
        if type(other) is geopt:
            return sqrt((self.x - other.x) * (self.x - other.x) +
                        (self.y - other.y) * (self.y - other.y) +
                        (self.z - other.z) * (self.z - other.z))
        else:
            raise TypeError(u'Cannot subtract {0} from geopt.'.format(
                str(type(other).__name__)))

    def __lt__(self, other):
        if type(other) is geopt:
            return self.t < other.t
        else:
            return self.t < other

    def __le__(self, other):
        if type(other) is geopt:
            if abs(self.t - other.t) < F_EPSILON:
                return True  # same
            else:
                return self.t < other.t
        else:
            return self.t <= other

    def __eq__(self, other):
        if type(other) is geopt:
            return (abs(self.t - other.t) < F_EPSILON)
        else:
            return self.t == other

    def __ne__(self, other):
        if type(other) is geopt:
            return (abs(self.t - other.t) >= F_EPSILON)
        else:
            return self.t != other

    def __gt__(self, other):
        if type(other) is geopt:
            return self.t > other.t
        else:
            return self.t > other

    def __ge__(self, other):
        if type(other) is geopt:
            if abs(self.t - other.t) < F_EPSILON:
                return True  # same
            else:
                return self.t > other.t


def fromjsob(obj):
    ret = None
    try:
        ret = geopt(lat=obj[u'lat'],
                    lng=obj[u'lng'],
                    t=obj[u't'],
                    x=obj[u'x'],
                    y=obj[u'y'],
                    z=obj[u'z'],
                    txt=obj[u'txt'],
                    time=obj[u'time'],
                    ico=obj[u'ico'])
    except:
        pass
    return ret


# TODO: add strictly ordered list of geopts, with t lookup
