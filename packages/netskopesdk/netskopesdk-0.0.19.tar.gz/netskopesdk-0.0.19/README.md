# Netskope SDK

Neskope SDK is Python library for dealing with API's to download the Netskope events. 

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install NetskopeSDK.

```bash
pip install netskopesdk
```

## Rest sdk Usage to pull the Alert & Events 

```python
from netskope_api.iterator.netskope_iterator import NetskopeIterator
from netskope_api.iterator.const import Const
from requests.exceptions import RequestException
import time

# Construct the params dict to pass the authentication details 
params = {
        Const.NSKP_TOKEN : "<REST-API-TOKEN>",
        Const.NSKP_TENANT_HOSTNAME : "<HOSTNAME>",
        # Optional param to pass the proxy hosts.
        Const.NSKP_PROXIES : {"<PROXY-HOSTS>"},
        Const.NSKP_EVENT_TYPE : "<EVENT-TYPE>",
        Const.NSKP_ITERATOR_NAME : "<ITERATOR-NAME>"
    }

DEFAULT_WAIT_TIME = 30
RESULT = "result"
WAIT_TIME = "wait_time"

# Create an Iterator
iterator = NetskopeIterator(params)

# Use the next() iterator to download the logs. 
# Consume the message indefinitely in a loop and ingest the data to SIEM
while True:
    response = (iterator.next())
    try:
        if response:
            data = response.json()
            if RESULT in data and len(data[RESULT]) != 0:
                # processData() 
                # sleep() the thread to avoid constant polling
                if WAIT_TIME in data:
                    time.sleep(data[WAIT_TIME])
                else:
                    time.sleep(DEFAULT_WAIT_TIME)
            else:
                print("No response received from the iterator")
                time.sleep(DEFAULT_WAIT_TIME)
    except Exception as e:
        time.sleep(DEFAULT_WAIT_TIME)
        raise RequestException(e)
```
