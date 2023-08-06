print(f'loading {__file__} (you can change it!)')

print('setting pandas defaults')

import pandas as pd
import numpy as np

pd.options.display.expand_frame_repr = False
pd.options.display.max_colwidth = 40
pd.options.display.max_columns = 0
pd.options.display.max_rows = 100
pd.options.display.min_rows = 20
pd.options.display.float_format = '{:,.1f}'.format  # display 1234.567 as 1,234.5
pd.options.plotting.backend = "plotly"

print('done')
