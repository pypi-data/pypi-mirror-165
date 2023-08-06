DSC Labs common libraries.
----
A python3 library for commonly used utilities

## Installation and Usage:

#### Install with pip

```commandline
pip3 install dsc_labs --trusted-host 192.168.195.200 --no-cache-dir --extra-index-url http://192.168.195.200:8151/simple/
```

#### Usage:
1. Import libraries
```python
# example: using logger from dsc_labs
from dsc_labs.libs.logger import DSCLabsLoggerMixin
from dsc_labs.common import current_utc_timestamp

class Timer(DSCLabsLoggerMixin):
    def __init__(self):
        super().__init__()
        
    def get_current_time(self):
        utc_time = current_utc_timestamp()
        # self.log is a method that inherits from `DSCLabsLoggerMixin` class
        self.log.info('event=get-current-time message="Current time: %s"', str(utc_time))
```

2. Command line:
```commandline
dsc_labs-config -h

dsc_labs-* ...
```


## Package development

#### Install required libraries
```commandline
pip install -r requirements.txt
```

#### Build
```commandline
python setup.py sdist
```

#### Release
```commandline
python -m twine upload --repository-url http://192.168.195.200:8151 -u USERNAME -p PASSWORD -f FILEPACKAGE
```
