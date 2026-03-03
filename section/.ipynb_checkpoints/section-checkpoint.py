import pandas as pd

class Section:
    def __init__(self):
        self._xz = [(0., 0.), (1., 0.)]

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

    def to_df(self, x_field="distance", z_field="altitude"):
        
        return pd.DataFrame(
            {
                "distance" : self.x,
                "altitude" : self.z
            }
        )

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
