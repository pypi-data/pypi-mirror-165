#!/usr/bin/env python3
"""
This helper file contains standard Nornir NETCONF RPC tasks like lock, validate, commit, discard and unlock.
Custom NETCONF RPC tasks like edit-config are not part of this helper file. Please take a look to
nr_netconf_tasks.

The functions are ordered as followed:
- NETCONF helper functions
- Single Nornir NETCONF tasks
- Nornir NETCONF tasks in regular function
"""

import time
from nornir_scrapli.tasks import (
    netconf_lock,
    netconf_validate,
    netconf_commit,
    netconf_unlock,
    netconf_discard,
)
from nornir.core.task import Result
from ..utils import print_task_name, task_host, task_info, task_error


__author__ = "Willi Kubny"
__maintainer__ = "Willi Kubny"
__version__ = "1.0"
__license__ = "MIT"
__email__ = "willi.kubny@kyndryl.com"
__status__ = "Production"


#### Nornir Helper Functions #################################################################################


def print_nc_ops_rpc_result(task_text, task_result, verbose=False):
    """
    This is a helper function to print the result of the custom Nornir task netconf_ops_wrapper which is a
    wrapper task to run the Scrapli NETCONF operation tasks netconf_lock, netconf_validate, netconf_commit,
    netconf_unlock or netconf_discard. The argument task_result is the Nornir result object returned from
    netconf_ops_wrapper.
    """
    # Print custom results for each host
    for host in task_result:
        msg_changed = str(task_result[host].changed)
        print(task_host(host=host, changed=msg_changed))

        # If the result is not a string, delete the task result to have only the subtask results
        if not isinstance(task_result[host].result, str):
            del task_result[host][0]

        # If the result is an exception, it has not attribute scrapli_response
        if task_result[host].result.startswith("Traceback"):
            print(
                f"{task_error(text=task_text, changed=msg_changed)}\n"
                + f"{task_result[host].result.rstrip()}"
            )
            # Set the config_sttus to False
            config_status = False

        # If the result XML payload contains <ok/>, the NETCONF result is successful
        elif "<ok/>" in str(task_result[host].result):
            print(
                f"{task_info(text=task_text, changed=msg_changed)}\n"
                + f"'{task_text}' -> {str(task_result[host].scrapli_response)} "
                + f"in {str(task_result[host].scrapli_response.elapsed_time)}s"
            )
            if verbose:
                print(f"\n{task_result[host].result.rstrip()}")
            # Set the config_sttus to False
            config_status = True

        # Else the NETCONF result is not successful
        else:
            print(
                f"{task_error(text=task_text, changed=msg_changed)}\n"
                + f"'{task_text}' -> {str(task_result[host].scrapli_response)} "
                + f"in {str(task_result[host].scrapli_response.elapsed_time)}s"
                + f"\n{task_result[host].result.rstrip()}"
            )
            # Set the config_sttus to False
            config_status = False

    return config_status


#### Single Nornir NETCONF Tasks #############################################################################


def nc_ops_rpc_task(task, nc_ops_rpc, source=False, target=False):
    """
    This custom Nornir task is a wrapper for the Scrapli NETCONF operation tasks netconf_lock,
    netconf_validate, netconf_commit, netconf_unlock or netconf_discard. The argument nc_rpc needs to be the
    Scrapli NETCONF task function which has to be imported at the beginning of the script. The result of this
    task can be printed with print_nc_ops_rpc_result
    """
    # Backoff sleep and attempt values
    config_attempts = 5
    sleep = 1
    sleep_multiplier = 1.5

    for _ in range(config_attempts):
        try:
            # If the Scrapli Nornir task is netconf_validate
            if source:
                nc_result = task.run(task=nc_ops_rpc, source=source)

            # If the Scrapli Nornir task is netconf_lock or netconf_unlock
            elif target:
                nc_result = task.run(task=nc_ops_rpc, target=target)

            # If the Scrapli Nornir task is netconf_commit or netconf_discard
            else:
                nc_result = task.run(task=nc_ops_rpc)

        except:  # pylint: disable=bare-except # nosec
            # Continue with next range() loop attempt
            time.sleep(sleep)
            sleep = sleep * sleep_multiplier
            continue

        # No exception -> Continue to return the result
        else:
            return Result(host=task.host, result=nc_result)

    return Result(host=task.host)


#### Nornir NETCONF Tasks in regular Function ################################################################


def nc_lock(nr_obj, datastore, verbose=False):
    """
    This function runs the custom Nornir task nc_ops_rpc_task with the Scrapli NETCONF netconf_lock function
    as nc_ops_rpc task argument. The argument nc_ops_rpc needs to be the Scrapli NETCONF task function which
    has to be imported at the beginning of the script. The result of this task is printed with
    print_nc_ops_rpc_result to avoid cluttering the std-out with the output of print_result(). A boolian will
    be returned at the end to indicate if the NETCONF RPC was successful or not.
    """
    # Set the task name, info and error text
    task_text = "NETCONF lock datastore"

    # Print the task name
    print_task_name(text=task_text)

    # Lock the NETCONF datastore with Scrapli netconf_lock
    task_result = nr_obj.run(task=nc_ops_rpc_task, nc_ops_rpc=netconf_lock, target=datastore, on_failed=True)

    # Print the NETCONF operations task result
    config_status = print_nc_ops_rpc_result(task_text=task_text, task_result=task_result, verbose=verbose)

    return config_status


def nc_validate(nr_obj, datastore, verbose=False):
    """
    This function runs the custom Nornir task nc_ops_rpc_task with the Scrapli NETCONF netconf_validate
    function as nc_ops_rpc task argument. The argument nc_ops_rpc needs to be the Scrapli NETCONF task
    function which has to be imported at the beginning of the script. The result of this task is printed with
    print_nc_ops_rpc_result to avoid cluttering the std-out with the output of print_result(). A boolian will
    be returned at the end to indicate if the NETCONF RPC was successful or not.
    """
    # Set the task name, info and error text
    task_text = "NETCONF validate datastore"

    # Print the task name
    print_task_name(text=task_text)

    # Validate the NETCONF datastore with Scrapli netconf_validate
    task_result = nr_obj.run(
        task=nc_ops_rpc_task, nc_ops_rpc=netconf_validate, source=datastore, on_failed=True
    )

    # Print the NETCONF operations task result
    config_status = print_nc_ops_rpc_result(task_text=task_text, task_result=task_result, verbose=verbose)

    return config_status


def nc_commit(nr_obj, verbose=False):
    """
    This function runs the custom Nornir task nc_ops_rpc_task with the Scrapli NETCONF netconf_commit function
    as nc_ops_rpc task argument. The argument nc_ops_rpc needs to be the Scrapli NETCONF task function which
    has to be imported at the beginning of the script. The result of this task is printed with
    print_nc_ops_rpc_result to avoid cluttering the std-out with the output of print_result(). A boolian will
    be returned at the end to indicate if the NETCONF RPC was successful or not.
    """
    # Set the task name, info and error text
    task_text = "NETCONF commit datastore"

    # Print the task name
    print_task_name(text=task_text)

    # Commit all changes in the NETCONF datastore with Scrapli netconf_commit
    task_result = nr_obj.run(task=nc_ops_rpc_task, nc_ops_rpc=netconf_commit, on_failed=True)

    # Print the NETCONF operations task result
    config_status = print_nc_ops_rpc_result(task_text=task_text, task_result=task_result, verbose=verbose)

    return config_status


def nc_unlock(nr_obj, datastore, verbose=False):
    """
    This function runs the custom Nornir task nc_ops_rpc_task with the Scrapli NETCONF netconf_unlock function
    as nc_ops_rpc task argument. The argument nc_ops_rpc needs to be the Scrapli NETCONF task function which
    has to be imported at the beginning of the script. The result of this task is printed with
    print_nc_ops_rpc_result to avoid cluttering the std-out with the output of print_result(). A boolian will
    be returned at the end to indicate if the NETCONF RPC was successful or not.
    """
    # Set the task name, info and error text
    task_text = "NETCONF unlock datastore"

    # Print the task name
    print_task_name(text=task_text)

    # Unlock the NETCONF datastore with Scrapli netconf_unlock
    task_result = nr_obj.run(
        task=nc_ops_rpc_task, nc_ops_rpc=netconf_unlock, target=datastore, on_failed=True
    )

    # Print the NETCONF operations task result
    config_status = print_nc_ops_rpc_result(task_text=task_text, task_result=task_result, verbose=verbose)

    return config_status


def nc_discard(nr_obj, verbose=False):
    """
    This function runs the custom Nornir task nc_ops_rpc_task with the Scrapli NETCONF netconf_discard
    function as nc_ops_rpc task argument. The argument nc_ops_rpc needs to be the Scrapli NETCONF task
    function which has to be imported at the beginning of the script. The result of this task is printed with
    print_nc_ops_rpc_result to avoid cluttering the std-out with the output of print_result(). A boolian will
    be returned at the end to indicate if the NETCONF RPC was successful or not.
    """
    # Set the task name, info and error text
    task_text = "NETCONF discard datastore"

    # Print the task name
    print_task_name(text=task_text)

    # Validate the NETCONF datastore with Scrapli netconf_discard
    task_result = nr_obj.run(task=nc_ops_rpc_task, nc_ops_rpc=netconf_discard, on_failed=True)

    # Print the NETCONF operations task result
    config_status = print_nc_ops_rpc_result(task_text=task_text, task_result=task_result, verbose=verbose)

    return config_status
