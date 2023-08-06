print(f'loading {__file__} (you can change it!)')

print('setting pandas defaults')

import pandas as pd
import numpy as np

print(f'you can edit this package at {__file__}')

from pandas import options

options.display.expand_frame_repr = False
options.display.max_colwidth = 40
options.display.max_columns = 0
options.display.max_rows = 100
options.display.min_rows = 20
options.display.float_format='{:,.1f}'.format  # display 1234.567 as 1,234.5
print('done')
