# Example Usage
```
import logging
from handler import DynamoDBHandler
logging.basicConfig(level=logging.INFO, format='%(message)s')
log = logging.getLogger('logger')
dh = DynamoDBHandler(level=logging.INFO)
log.addHandler(dh)

try:
    # something
except Exception as e:
    log.error(e)
```