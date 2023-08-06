# KSTLogger

takes specific inputs and generates a JSON formatted log and prints the entry to the console/cloudwatch.

to use, import the package and initiate a logger (see below Code Usage Example):
```Python
logger=KSTLogger(source_process_name)
```

then call the logger.log to make a log message:
```Python
logger.log(log_severity,log_details,source_system,source_system_trade_number,source_system_id,**kwargs)
```

NOTE: **kwargs are optional fields in a key: "value" format. There can be as many or as few **kwargs as you'd like

```Python
logger.log(log_severity,log_details,source_system,source_system_trade_number,source_system_id,error_details="extra error message",error_type="business_error")
```

NOTE: if log_severity == "DEBUG", the package will look for os.environ["DEBUG"] and will only print if it equals "true". If it does not find one or sees it's set to "false", it will not print.

## Installation
This package is installed using pip.  The following command line will install the latest version of this component:
```
pip install git+https://ksandt.visualstudio.com/DevOps/_git/pip-kstlogger
```

To install a specific version, use the @{version_number}:
```
pip install git+https://ksandt.visualstudio.com/DevOps/_git/pip-kstlogger@0.2.0
```


## Code Usage Example:
```Python
from KSTLogger import KSTLogger
import os

logger=KSTLogger("testingApplication")

logger.log("INFO","insert log message","TPT","13097","TPT.13097")
```
Output of the above would be:
{"log_severity": "INFO", "source_process_name": "testingApplication", "log_timestamp_utc": "2019-09-04 21:53:57", "log_detail": "insert log message", "source_system": "TPT", "source_system_trade_number": "13097", "source_system_id": "TPT.13097"}

```Python
from KSTLogger import KSTLogger
import os

logger=KSTLogger("testingApplication")

logger.log("INFO","insert log message","TPT.13097","TPT","13097",any_key="any_value",any_key_nth="any_value_nth")
```
{"log_severity": "INFO", "source_process_name": "testingApplication", "log_timestamp_utc": "2019-09-04 21:53:57", "log_detail": "insert log message", "source_system": "TPT", "source_system_trade_number": "13097", "source_system_id": "TPT.13097", "any_key": "any_value", "any_key_nth": "any_value_nth}




