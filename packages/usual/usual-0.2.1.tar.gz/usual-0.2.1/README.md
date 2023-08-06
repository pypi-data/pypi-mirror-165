Put all your repeated imports at one place and load them with one import.

Installation:
```bash
pip install usual
```

Usage:
```python
from usual.ds import *

# now you can use pandas as it's loaded from the 'usual' package
pd.DataFrame()
```
```
loading C:\Users\israelil\Downloads\my_things\pypi\usual\src\usual\ds.py (you can change it!)
setting pandas defaults
done
```

There is also usual.basic and you can add more as you wish

Note that this is not a good practice for projects, just for small local scripts...
