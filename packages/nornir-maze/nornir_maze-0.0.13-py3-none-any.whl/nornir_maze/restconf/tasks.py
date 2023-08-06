#!/usr/bin/env python3
"""
This helper file contains RESTCONF functions and tasks related to Nornir.

The functions are ordered as followed:
- Single Nornir RESTCONF tasks
- Nornir RESTCONF tasks in regular function
"""

import requests
from nornir.core.task import Result


__author__ = "Willi Kubny"
__maintainer__ = "Willi Kubny"
__version__ = "1.0"
__license__ = "MIT"
__email__ = "willi.kubny@kyndryl.com"
__status__ = "Production"


#### Single Nornir RESTCONF Tasks ############################################################################


def rc_cisco_get_task(task, yang_data_query):
    """
    This custom Nornir task executes a RESTCONF GET request to a yang data query and returns a dictionary with
    the whole RESTCONF response as well as some custom formated data for further processing.
    """
    # RESTCONF HTTP URL
    restconf_path = f"/restconf/data/{yang_data_query}"
    url = f"https://{task.host.hostname}:{task.host['restconf_port']}{restconf_path}"

    # RESTCONF HTTP header
    headers = {
        "Accept": "application/yang-data+json",
        "Content-Type": "application/yang-data+json",
    }

    # RESTCONF HTTP API call
    rc_response = requests.get(  # nosec
        url=url, headers=headers, auth=(task.host.username, task.host.password), verify=False, timeout=120
    )

    # Result dict to return as task result
    result = {
        "url": url,
        "response": rc_response,
        "method": rc_response.request,
        "status_code": rc_response.status_code,
        "elapsed": rc_response.elapsed.total_seconds(),
        "json": rc_response.json(),
    }

    return Result(host=task.host, result=result)


#### Nornir RESTCONF tasks in regular Function ###############################################################

# -> Write a print_rc_get_result() function
