from math import sqrt

import numpy as np
import pandas as pd
from shapely.geometry import LineString, Point

class Section:
    def __init__(self):
        self._xz = [(0., 0.), (1., 0.)]

    def add_point(self, point):
        """
        add a point
        
        arguments:
        - point: (x, z) - tuple
            - x: distance (m) - int | float
            - z: altitude (m) - int | float

        returns:
        - True if success
        - False else

        examples:
        >>> section.add_point((5., 1210.))

        """
        if not isinstance(point, tuple):
            return False
        elif not len(point) > 1:
            return False
        else:
            x, z = point[0], point[1]
            if not (isinstance(x, (int, float)) and isinstance(z, (int, float))):
                return False
            elif x in self.x:
                return False
            else:
                self._xz.append((float(x), float(z)))
                self._xz.sort()
                return True

    def area(self, kind="below"):
        """
        calculate the area below or above the section

        arguments:
        - kind: "below" | "above" - str

        returns:
        - area: area (m2) - float
        or
        - None - NoneType

        examples:
        >>> area = section.area()
        
        """
        if kind not in ["above", "below"]:
            return None
        else:
            x = self.x
            z = [z - min(self.z) for z in self.z]

            if kind == "below":
                return float(np.trapezoid(z, x))
            else:
                return (self.length() * (max(z) - min(z))) - float(np.trapezoid(z, x))

    def critical(self, altitude, g=9.81):
        if not (isinstance(altitude, float) or isinstance(altitude, int)):
            return None
        elif not min(self.z) <= altitude <= max(self.z):
            return None

        if not(isinstance(g, float) or isinstance(g, int)):
            return None
        elif not g > 0:
            return None

        geom_props = self.geometric_properties(altitude)

        if not geom_props:
            return None

        B, P, A, R, D = geom_props

        u = sqrt(g * D)
        
        Q = u * A

        return float(Q)

    def duplicate(self):
        """
        duplicate the section

        returns:
        - new_section: duplicated section - Section

        examples:
        >>> new_section = section.duplicate()

        """
        new_section = Section()
        
        new_section.xz = list(self._xz)
        
        return new_section

    def ferguson(self, altitude, slope, d84, g=9.81):
        if not (isinstance(altitude, float) or isinstance(altitude, int)):
            return None
        elif not min(self.z) <= altitude <= max(self.z):
            return None

        if not (isinstance(slope, float) or isinstance(slope, int)):
            return None
        elif not slope >= 0:
            return None

        if not (isinstance(d84, float) or isinstance(d84, int)):
            return None
        elif not d84 > 0:
            return None

        if not(isinstance(g, float) or isinstance(g, int)):
            return None
        elif not g > 0:
            return None

        geom_props = self.geometric_properties(altitude)

        if not geom_props:
            return None

        B, P, A, R, D = geom_props

        u = 2.5 * (R / d84)
        u *= sqrt(g * slope * R)
        u /= sqrt(1 + 0.15 * (R / d84)**(5./3.))

        Q = u * A

        return float(Q)

    def from_df(self, df, x_field="X", z_field="Z"):
        if not isinstance(df, pd.DataFrame):
            return False

        if not (isinstance(x_field, str) and isinstance(z_field, str)):
            return False

        df = df.dropna()

        if df.shape[0] < 2 or df.shape[1] < 2:
            return False

        if not (x_field in list(df.columns) and z_field in list(df.columns)):
            return False

        if not (df.loc[:, x_field].dtype in ['float64', 'int64'] and \
                df.loc[:, z_field].dtype in ['float64', 'int64']):
            return False

        i = list(df.columns).index(x_field)
        x = list(df.values[:, i])
        
        i = list(df.columns).index(z_field)
        z = list(df.values[:, i])
        
        xz = [(float(x), float(z)) for x, z in zip(x, z)]
        
        xz.sort()

        self.xz = xz
        return True

    def geometric_properties(self, altitude):
        if not (isinstance(altitude, float) or isinstance(altitude, int)):
            return None
        elif not min(self.z) <= altitude <= max(self.z):
            return None

        lines = self.water_lines(altitude)

        # top width
        B = 0.

        # wetted perimter
        P = 0.

        # wetted area
        A = 0.

        if len(lines) == 0:
            return None

        for line in lines:
            b = line[-1][0] - line[0][0]
            B += b

            sub_section = self.truncate(distances=(line[0][0], line[-1][0]))

            p = sub_section.length(dim="3D")
            P += p

            a = sub_section.area(kind="above")
            A += a

        R = A/P
        D = A/B

        return B, P, A, R, D

    def interpolate(self, x):
        """
        interpolate the section

        arguments:
        - x: distance (m) - int | float

        returns:
        - z: interpolated altitude (m) - float
        or
        - None - NoneType

        examples:
        >>> z = section.interpolate(x=10.)

        """
        if not isinstance(x, (int, float)):
            return None
        elif not min(self.x) <= x <= max(self.x):
            return None
        else:
            x = float(x)
            Xs = self.x
            Xs.append(x)
            Xs.sort()

            if x == Xs[0]:
                return float(self.z[0])
            elif x == Xs[-1]:
                return float(self.z[-1])
            else:
                return float(np.interp(x, self.x, self.z))

    def intersect(self, curve):
        line1 = LineString(self.xz)
        line2 = LineString(curve)

        intersections = line1.intersection(line2)

        points = []

        if intersections.is_empty:
            return points
        elif intersections.geom_type == "Point":
            points += list(intersections.coords)
        elif intersections.geom_type == "MultiPoint":
            for geom in intersections.geoms:
                points += list(geom.coords)
        elif intersections.geom_type == "LineString":
            points += list(intersections.coords)
        elif intersections.geom_type == "MultiLineString":
            for geom in intersections.geoms:
                points += list(geom.coords)
        elif intersections.geom_type == "GeometryCollection":
            for geom in intersections.geoms:
                points += list(geom.coords)

        return sorted(points)

    def length(self, dim="2D"):
        """
        calculate the section length

        arguments:
        - dim: "2D" for plan length or "3D" for actual length - str
        
        returns:
        - plan length (m) - float
        or
        - actual length (m) - float
        or
        - None - NoneType

        examples:
        >>> length = section.length()
        
        """
        if not isinstance(dim, str):
            return None
        elif dim.upper() not in ["2D", "3D"]:
            return None
        elif dim.upper() == "2D":
            return float(self._xz[-1][0] - self._xz[0][0])
        else:
            dist = 0
            for i in range(1, len(self._xz)):
                dist += ((self.x[i] - self.x[i-1])**2 + (self.z[i] - self.z[i-1])**2)**0.5
            return float(dist)

    def strickler(self, altitude, slope, coefficient):
        if not (isinstance(altitude, float) or isinstance(altitude, int)):
            return None
        elif not min(self.z) <= altitude <= max(self.z):
            return None

        if not (isinstance(slope, float) or isinstance(slope, int)):
            return None
        elif not slope >= 0:
            return None

        if not (isinstance(coefficient, float) or isinstance(coefficient, int)):
            return None
        elif not coefficient > 0:
            return None

        geom_props = self.geometric_properties(altitude)

        if not geom_props:
            return None

        B, P, A, R, D = geom_props

        u = coefficient * R**(2./3.) * slope**(1./2.)
        
        Q = u * A

        return float(Q)

    def to_df(self, x_field="distance", z_field="altitude"):
        
        return pd.DataFrame(
            {
                "distance" : self.x,
                "altitude" : self.z
            }
        )

    def truncate(self, **kwargs):
        """
        truncate the section

        arguments:
        - indexes = (i_start, i_end) - tuple
            - i_start: start index - int
            - i_end: end index - int
        or
        - distances = (x_start, x_end) - tuple
            - x_start: start distance - int | float
            - x_end: end distance - int | float

        returns:
        - new_section: truncated section - Section
        or
        - None - NoneType

        examples:
        >>> new_section = section.truncate(indexes=(10, 20))

        """
        new_section = self.duplicate()

        if 'indexes' in kwargs.keys():
            if not isinstance(kwargs['indexes'], tuple):
                return None
            elif not 1 < len(kwargs['indexes']):
                return None
            else:
                indexes = kwargs['indexes']
            
            if not (isinstance(indexes[0], int) and isinstance(indexes[1], int)):
                return None
            else:
                i_start = indexes[0]
                i_end = indexes[1]
            
            if not 0 <= i_start < i_end < len(self._xz):
                return None
            else:
                new_section.xz = self._xz[i_start:i_end+1]
                
                return new_section

        elif 'distances' in kwargs.keys():            
            if not isinstance(kwargs['distances'], tuple):
                return None
            elif not 1 < len(kwargs['distances']):
                return None
            else:
                distances = kwargs['distances']

            if not (isinstance(distances[0], (int, float)) and isinstance(distances[1], (int, float))):
                return
            else:
                x_start = float(distances[0])
                x_end = float(distances[1])

                if not self.x[0] <= x_start < x_end <= self.x[-1]:
                    return None
                else:
                    new_section.add_point((x_start, new_section.interpolate(x_start)))
                    new_section.add_point((x_end, new_section.interpolate(x_end)))

                    i_start = new_section.x.index(x_start)
                    i_end = new_section.x.index(x_end)

                    new_section.xz = new_section.xz[i_start:i_end+1]

                    return new_section
        
        else:
            return None

    def water_lines(self, altitude):
        if not (isinstance(altitude, float) or isinstance(altitude, int)):
            return None
        elif not min(self.z) <= altitude <= max(self.z):
            return None

        lines = []
        
        points = self.intersect([(self.x[0], altitude),
                                 (self.x[-1], altitude)])

        if len(points) < 2:
            return lines

        for i in range(0, len(points)-1):
            x_start, x_end = points[i][0], points[i+1][0]
            sub_section = self.truncate(distances=(x_start, x_end))

            if len(sub_section.xz) == 2:
                continue

            if all([z >= 0 for z in np.array(altitude) - np.array(sub_section.z)][1:-1]):
                lines.append([(x_start, self.interpolate(x_start)), (x_end, self.interpolate(x_end))])

        return lines

    @property
    def xz(self):
        return list(self._xz)

    @xz.setter
    def xz(self, xz):
        if not isinstance(xz, list):
            return
        elif not len(xz) > 1:
            return
        
        xz_new = []
        for item in xz:
            if not isinstance(item, (tuple, list)):
                return
            elif not len(item) > 1:
                return
            else:
                x, z = item[0], item[1]
            
            if not (isinstance(x, (int, float)) and isinstance(z, (int, float))):
                return
            elif x not in [x for x, z in xz_new]:
                xz_new.append((float(item[0]), float(item[1])))
            
        xz_new.sort()
        if not len(xz_new) > 1:
            return
        else:
            self._xz = xz_new

    @property
    def x(self):
        return [x for x, z in self._xz]

    @property
    def z(self):
        return [z for x, z in self._xz]
