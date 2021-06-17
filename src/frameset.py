import numpy as np
import pandas as pd

'''For Chest'''
# x = {'min': -1.0, 'max': 1.0, 'sigma': 0.01}
# y = {'min': 0.0, 'max': 0.0, 'sigma': 0.01}
# z = {'min': -4.0, 'max': -4.0, 'sigma': 0}
# rx = {'min': 0.0, 'max': 0.0, 'sigma': 0.5}
# ry = {'min': -60.0, 'max': -60.0, 'sigma': 0.5}
# rz = {'min': 0.0, 'max': 0.0, 'sigma': 0.5}
'''For Small Tropical Island'''
# x = {'min': 0.0, 'max': 0.0, 'sigma': 1}
# y = {'min': 0.0, 'max': 0.0, 'sigma': 1}
# z = {'min': -400.0, 'max': -400.0, 'sigma': 0}
# rx = {'min': 10.0, 'max': 46.0, 'sigma': 0.1}
# ry = {'min': 0.0, 'max': 360.0, 'sigma': 0.1}
# rz = {'min': 0.0, 'max': 0.0, 'sigma': 0.1}
# split = 360
store = 'frameset.csv'

if __name__ == '__main__':
    np.random.seed(0)
    d = {
        'x': np.linspace(x['min'], x['max'], num=split+1),
        'dx': np.random.normal(0, x['sigma'], size=(split+1,)),
        'y': np.linspace(y['min'], y['max'], num=split+1),
        'dy': np.random.normal(0, y['sigma'], size=(split+1,)),
        'z': np.linspace(z['min'], z['max'], num=split+1),
        'dz': np.random.normal(0, z['sigma'], size=(split+1,)),
        'rx': np.linspace(rx['min'], rx['max'], num=split+1),
        'drx': np.random.normal(0, rx['sigma'], size=(split+1,)),
        'ry': np.linspace(ry['min'], ry['max'], num=split+1),
        'dry': np.random.normal(0, ry['sigma'], size=(split+1,)),
        'rz': np.linspace(rz['min'], rz['max'], num=split+1),
        'drz': np.random.normal(0, rz['sigma'], size=(split+1,))
    }

    df = pd.DataFrame(d)
    print(df)
    df.to_csv(store, index=False)
