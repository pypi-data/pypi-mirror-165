# UTILITY PACKAGE
### OVER VIEW
* **timer** - counter a runtime 
* **configure** - reading configure file in yaml format
* **data** - load & save plain text & object 
* **log** - log manager

### DEMO LOG 
``` python
import muuusiiik.util as msk

# define logger
logger = msk.log.GetLogger(level=msk.log.DEBUG, formatter='minimal')
hand   = msk.log.GetHandler(filename='logs/usage.log', when='daily', level=msk.log.WARNING, formatter='full')
logger.addHandler(hand)

# use logger
logger.info(' > info')
logger.debug(' > debug')
logger.warning(' > warning')
logger.error(' > error')
logger.critical(' > critical')
```

### HOW TO BUILD A PACKAGE TO PYPI
prerequisite
``` shell
pip install setuptools wheel tqdm twine
```

build and upload package
```
# preparing tar.gz package 
python setup.py sdist
# uploading package to pypi server
python -m twine upload dist/* --verbose
```

install package
``` shell
# install latest version
pip install muuusiiik --upgrade
# specific version with no cache
pip install muuusiiik==0.0.11  --no-cache-dir
```
