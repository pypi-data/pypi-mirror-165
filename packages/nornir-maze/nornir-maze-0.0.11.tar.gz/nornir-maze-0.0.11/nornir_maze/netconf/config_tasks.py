#!/usr/bin/env python3
"""
This helper file contains NETCONF functions and tasks related to Nornir. Standard NETCONF RPCs like lock,
validate, commit, discard and unlock are not part of this helper file. Please take a look to nr_netconf_ops.

The functions are ordered as followed:
- NETCONF helper functions
- Single Nornir NETCONF tasks
- Nornir NETCONF tasks in regular function
"""

import os
import sys
import time
from nornir_scrapli.tasks import netconf_edit_config
from nornir.core.task import Result
from nornir_jinja2.plugins.tasks import template_file
from jinja2 import Template, StrictUndefined, UndefinedError
from ..utils import (
    print_task_name,
    task_host,
    task_info,
    task_error,
    extract_interface_name,
    extract_interface_number,
    create_single_interface_list,
    create_tpl_int_list,
)


__author__ = "Willi Kubny"
__maintainer__ = "Willi Kubny"
__version__ = "1.0"
__license__ = "MIT"
__email__ = "willi.kubny@kyndryl.com"
__status__ = "Production"


#### Nornir Helper Functions #################################################################################


def create_nc_tpl_list(nr_obj, host=None):
    """
    This function loops over all host inventory keys and append each key for the NETCONF Jinja2 template path
    and its files to a dictionary and returns a Nornir AggregatedResult Object. There can be several different
    Jinja2 template paths with its files as it
    """
    nc_tpl = {}

    try:
        # For a Task object: Add all NETCONF template paths to the list nc_tpl_list
        for path in nr_obj.host.keys():
            # Match all NETCONF templates paths except for the interface templates
            if path.startswith("nc_path_tpl_int"):
                continue
            if path.startswith("nc_path_tpl"):
                # Remove the prefix to get only the path name
                foldername = path.replace("nc_path_tpl_", "")
                # Create a dict key with the NETCONF template path
                nc_tpl[path] = []

                # Add all NETCONF templates to the corresponding NETCONF path
                for template in nr_obj.host.keys():
                    # Match all NETCONF templates except for the interface templates
                    if template.startswith(f"nc_payload_tpl_{foldername}"):
                        nc_tpl[path].append(template)

    except:  # pylint: disable=bare-except
        # For a Nornir object: Add all NETCONF template paths to the list nc_tpl_list
        for path in nr_obj.inventory.hosts[host].keys():
            # Match all NETCONF templates paths except for the interface templates
            if path.startswith("nc_path_tpl_int"):
                continue
            if path.startswith("nc_path_tpl"):
                # Remove the prefix to get only the path name
                foldername = path.replace("nc_path_tpl_", "")
                # Create a dict key with the NETCONF template path
                nc_tpl[path] = []

                # Add all NETCONF templates to the corresponding NETCONF path
                for template in nr_obj.inventory.hosts[host].keys():
                    # Match all NETCONF templates except for the interface templates
                    if template.startswith(f"nc_payload_tpl_{foldername}"):
                        nc_tpl[path].append(template)

    return nc_tpl


#### Single Nornir NETCONF Tasks #############################################################################


def nc_cfg_jinja2_template_task(task):
    """
    This custom Nornir task generates a configuration from a Jinja2 template based on a path and a template
    filename. The path and the template filename needs to be Nornir inventory keys which holds the needed
    information as value.
    """
    # Gather the NETCONF templates to apply for each host
    nc_tpl_list = create_nc_tpl_list(nr_obj=task)

    for inv_key_path, inv_key_template in nc_tpl_list.items():
        for inv_template in inv_key_template:
            # Get the inventory values from the inventory keys
            path = task.host[inv_key_path]
            template = task.host[inv_template]

            # Run the Nornir Task template_file
            j2_tpl_result = task.run(task=template_file, template=template, path=path, on_failed=True)

    return Result(host=task.host, result=j2_tpl_result)


def nc_edit_config(task, nc_config_list, config_attempts, verbose=False):
    """
    This functions is a Nornir Task which takes Nornir AggregatedResult object, which is a list of NETCONF
    config payloads and configures each of these payloads.All results are processed with try/except statements
    and will return its results with the Nornir Result() function for further processing.
    """
    # pylint: disable=too-many-locals

    # Backoff sleep and multiplier values
    sleep = 1
    sleep_multiplier = 1.5

    # Read the host NETCONF config list from the Nornir Jinja2 result object
    nc_config_list = nc_config_list[str(task.host)]

    # Set the Nornir std-out text
    task_text = "NETCONF edit config"

    # The result list will be filled with the result of each NETCONF payload
    result = []

    # Gather the NETCONF templates to apply for the host
    nc_tpl_result = create_nc_tpl_list(nr_obj=task)

    # Create a list which have only the template filenames
    nc_tpl = []
    for nc_tpl_list in nc_tpl_result.values():
        for nc_tpl_name in nc_tpl_list:
            nc_tpl.append(task.host[nc_tpl_name])

    # The index is used during the loop to identify the filename
    index = 0

    for nc_config in nc_config_list:
        # Set the variable for the Jinja2 template filename
        filename = nc_tpl[index]

        for _ in range(config_attempts):
            try:
                # Apply config to the NETCONF candidate datastore
                nc_response = task.run(task=netconf_edit_config, config=nc_config.result, target="candidate")

            except:  # pylint: disable=bare-except # nosec
                # Continue with next range() loop attempt to apply the config
                time.sleep(sleep)
                sleep = sleep * sleep_multiplier
                continue

            # No exception -> Create the result for this config
            else:
                # If the task netconf_edit_config failed {interface}
                if nc_response[0].failed:
                    result.append(
                        f"{task_error(text=task_text, changed='False')}\n"
                        + f"'{filename}' -> {str(nc_response[0].scrapli_response)} "
                        + f"in {str(nc_response[0].scrapli_response.elapsed_time)}s"
                        + f"\n\n{nc_response[0].scrapli_response.result}"
                    )
                # If the task netconf_edit_config was successful
                else:
                    if verbose:
                        result.append(
                            f"{task_info(text=task_text, changed='True')}\n"
                            + f"'{filename}' -> {str(nc_response[0].scrapli_response)} "
                            + f"in {str(nc_response[0].scrapli_response.elapsed_time)}s"
                            + f"\n\n{nc_response[0].scrapli_response.result}"
                        )
                    else:
                        result.append(
                            f"{task_info(text=task_text, changed='True')}\n"
                            + f"'{filename}' -> {str(nc_response[0].scrapli_response)} "
                            + f"in {str(nc_response[0].scrapli_response.elapsed_time)}s"
                        )
                # Break out of the range() loop to the next interface
                index += 1
                break

        # If all attempts failed this else clause will be executed
        else:
            result.append(
                f"{task_error(text=task_text, changed='False')}\n"
                + f"'{filename}' -> All {config_attempts} config attempts failed"
            )
            index += 1

    # Return the Nornir NETCONF result as the whole Nornir task was successful
    return Result(host=task.host, result=result)


def nc_edit_tpl_int_config(task, tpl_int_name, config_attempts, verbose=False):
    """
    This functions is a Nornir Task which takes a list of interfaces (tpl_int_name) and creates fully
    specified interfaces in case there is a Cisco like range list item. Then all these interfaces will be
    configured with a Jinja2 rendered NETCONF template config. All results are processed with try/except
    statements and will return its results with the Nornir Result() function for further processing.
    """
    # pylint: disable=too-many-locals

    # Backoff sleep and multiplier values
    sleep = 1
    sleep_multiplier = 1.5

    # Set the task info and error text
    task_text = "NETCONF interface config"

    #### Create full specified interface list from tpl_int_name ##############################################

    try:
        # Create a list of full specified interfaces from a Cisco range like list.
        # Gi1/0/1 - 10 -> GigabitEthernet1/0/1, GigabitEthernet1/0/2, etc.
        interfaces = create_single_interface_list(task.host[tpl_int_name])

    except TypeError:
        # TypeError Exception handles empty host inventory interface lists
        # Print the exception result to avoid that Nornir interrupts the script
        result = [
            (
                f"{task_info(text=task_text, changed='False')}\n"
                + f"No interface in template group {tpl_int_name}"
            ),
        ]
        # No interfaces in tpl_int_name (emtpy list).
        # Return the Nornir result as True as no interface should be configured
        return Result(host=task.host, result=result)

    except KeyError:
        # KeyError exception handles not existing host inventory data keys. Return None -> Less content in
        # hosts.yaml as the template groups are only on hosts with interfaces in this group needed
        return Result(host=task.host, result=None)

    #### Create the Jinja2 Template ##########################################################################

    try:
        # Find the host keys to construct the NETCONF payload file path
        nc_path = task.host["nc_path_tpl_int"]
        nc_payload = task.host[f"nc_payload_{tpl_int_name}"]

        # Define the Jinja2 template -> config of all interfaces from the list StrictUndefined raises a
        # exception when the template gets rendered and the Jinja2 template variable is undefined
        with open(os.path.join(nc_path, nc_payload), "r", encoding="utf-8") as stream:
            j2_tpl_int = Template(stream.read(), undefined=StrictUndefined)

    except FileNotFoundError as error:
        # Jinja2 interface template not found for interface to configure
        result = [f"{task_error(text=task_text, changed='False')}\n{error}"]

        # Return the Nornir result as error -> interface can not be configured
        return Result(host=task.host, result=result, failed=True)

    except KeyError as error:
        # Jinja2 Nornir inventory key not found. Key which specify the path and the file don't exist
        result = [
            (
                f"{task_error(text=task_text, changed='False')}\n"
                + f"Nornir inventory key task.host[{error}] not found"
            ),
        ]

        # Return the Nornir result as error -> interface can not be configured
        return Result(host=task.host, result=result, failed=True)

    #### Configure each interface with the Jinja2 rendered template ##########################################

    # The result list will be filled with the result of each interface
    result = []

    for interface in interfaces:
        for _ in range(config_attempts):
            try:
                # Extract the interface name and the interface number into a variable
                interface_name = extract_interface_name(interface)
                interface_number = extract_interface_number(interface)

                # Render the Jinja2 template with variable passed as **kwargs
                j2_tpl_var_kwargs = {
                    "interface_name": interface_name,
                    "interface_number": interface_number,
                }
                nc_config = j2_tpl_int.render(**j2_tpl_var_kwargs)

                # Apply interface config to the NETCONF candidate datastore
                nc_response = task.run(
                    task=netconf_edit_config,
                    config=nc_config,
                    target="candidate",
                )

            except UndefinedError as error:
                # Variable in Jinja2 template is undefined -> can not be rendered.
                # Prepare needed Jinja2 template variables in string for Nornir result.
                j2_tpl_vars = "Jinja2 template needs variable:\n"
                for key in j2_tpl_var_kwargs:
                    j2_tpl_vars += f"{key}\n"

                result.append(
                    f"{task_error(text=task_text, changed='False')}\n"
                    + f"Jinja2 variable {error} for template {nc_payload}\n"
                    + j2_tpl_vars.rstrip()
                )

                # Return the Nornir result as error -> template can not be rendered
                return Result(host=task.host, result=result, failed=True)

            except:  # pylint: disable=bare-except # nosec
                # Continue with next range() loop attempt for the same interface
                time.sleep(sleep)
                sleep = sleep * sleep_multiplier
                continue

            # No exception -> Create the result for this interface
            else:
                # If the task netconf_edit_config failed
                if nc_response[0].failed:
                    result.append(
                        f"{task_error(text=task_text, changed='False')}\n"
                        + f"'{interface}' -> {str(nc_response[0].scrapli_response)} "
                        + f"in {str(nc_response[0].scrapli_response.elapsed_time)}s"
                        + f"\n\n{nc_response[0].scrapli_response.result}"
                    )
                # If the task netconf_edit_config was successful
                else:
                    if verbose:
                        result.append(
                            f"{task_info(text=task_text, changed='True')}\n"
                            + f"'{interface}' -> {str(nc_response[0].scrapli_response)} "
                            + f"in {str(nc_response[0].scrapli_response.elapsed_time)}s"
                            + f"\n\n{nc_response[0].scrapli_response.result}"
                        )
                    else:
                        result.append(
                            f"{task_info(text=task_text, changed='True')}\n"
                            + f"'{interface}' -> {str(nc_response[0].scrapli_response)} "
                            + f"in {str(nc_response[0].scrapli_response.elapsed_time)}s"
                        )
                # Break out of the range() loop to the next interface
                break

        # If all attempts failed this else clause will be executed
        else:
            result.append(
                f"{task_error(text=task_text, changed='False')}\n"
                + f"'{interface}' -> All {config_attempts} config attempts failed"
            )

    # Return the Nornir NETCONF result as the whole Nornir task was successful
    return Result(host=task.host, result=result)


#### Nornir NETCONF Tasks in regular Function ################################################################


def nc_cfg_jinja2(nr_obj, verbose=False):
    """
    This function runs the Nornir task nc_cfg_jinja2_template_task and renders all Jinja2 NETCONF templates
    which are specified within the Nornir inventory. If one hosts fails to render a template the function
    terminates the script with a proper error message to std-out. Only when all hosts were successful the
    function will configure the renderes Jinja2 templates to the hosts.
    """
    # pylint: disable=too-many-branches

    #### Render all NETCONF Jinja2 templates #################################################################

    print_task_name(text="Jinja2 render NETCONF payload templates")

    # Run the Nornir Task template_file
    j2_config = nr_obj.run(task=nc_cfg_jinja2_template_task, on_failed=True)

    for host in j2_config:
        # Gather the NETCONF templates to apply for the host
        nc_tpl_result = create_nc_tpl_list(nr_obj=nr_obj, host=host)

        # Create a list which have only the template filenames
        nc_tpl = []
        for nc_tpl_list in nc_tpl_result.values():
            for nc_tpl_name in nc_tpl_list:
                nc_tpl.append(nr_obj.inventory.hosts[host][nc_tpl_name])

        # The index is used during the loop to identify the filename
        index = 0
        # Delete the Task result to have only Subtask results
        del j2_config[host][0]

        # Print all Jinja2 templating results
        print(task_host(host=host, changed="False"))
        task_mgs = "Jinja2 template file"

        for j2_result in j2_config[host]:
            if j2_result.failed:
                # If the task fails print the returned result
                print(task_error(text=task_mgs, changed="False"))

                # If the Jinja2 template is not found by the template_file task
                if "TemplateNotFound" in j2_result.result:
                    print(f"Jinja2 template '{nc_tpl[index]}' not found")
                    index += 1

                # If the Jinja2 templating rendering catches an exception
                else:
                    print(f"'{nc_tpl[index]}' -> Jinja2Response <Success: False>")
                    print(f"\n{j2_result.exception}")
                    index += 1

            # If no condition matched the task was successful
            else:
                print(task_info(text=task_mgs, changed="False"))
                # Read the template filename from the Nornir inventory.
                # file = nr_obj.inventory.hosts[host][template]
                print(f"'{nc_tpl[index]}' -> Jinja2Response <Success: True>")
                index += 1

                if verbose:
                    print(f"\n{j2_result.result}")

    if j2_config.failed_hosts:
        # If one or more of the Jinja2 template tasks failed
        print("\n")
        print(task_error(text=task_mgs, changed="False"))
        print("\U0001f4a5 ALERT: JINJA2 CONFIG TEMPLATING FAILED! \U0001f4a5")
        print(
            "\n\033[1m\u001b[31m"
            "-> Analyse the Nornir output for failed Jinja2 tasks\n"
            "-> May apply Nornir inventory changes and run the script again\n\n"
            "No config changes has been made yet!\n"
            "\033[0m"
        )
        # Terminate the script with successful exit code 0
        sys.exit()

    #### Configure all NETCONF Jinja2 templates ##############################################################

    print_task_name(text="NETCONF configure Jinja2 payload templates")

    # Backoff config attempt value
    config_attempts = 5

    # Configure the NETCONF payload from the Nornir Jinja2 result object
    nc_result = nr_obj.run(
        task=nc_edit_config,
        nc_config_list=j2_config,
        verbose=verbose,
        config_attempts=config_attempts,
        on_failed=True,
    )

    # To verify the config status of each subtask and as function return
    config_status = True

    # All results from the task custom nc_edit_config have been processed and returned with Nornir Result()
    # by the task to use custom std-out printing and to avoid the Nornir default print_result().
    for host in nc_result:
        # Print extensive result which is the host Return variable from nc_edit_config()
        print(task_host(host=host, changed=str(nc_result[host].changed)))

        # If the task fails and a exceptions is the result
        if isinstance(nc_result[host].result, str):
            print(nc_result[host].result)
        else:
            # The custom returned result item 0 from nc_edit_config() is a list. Print every list
            # item == NETCONF result Standard Nornir result starts at index 1 -> index 0 is custom return
            index = 1
            for result in nc_result[host].result:
                # If the result is an Nornir ERROR type == failed
                if "ERROR" in result:
                    config_status = False
                    # Print the custom result
                    print(result.rstrip())
                    # Print the last Nornir config attempt result
                    index = index + config_attempts - 1
                    print(f"\n{nc_result[host][index].result.rstrip()}")
                    index += 1

                # If the result is not an Nornir ERROR type == success
                else:
                    # Print the custom result
                    print(result.rstrip())
                    index += 1

    # If the task failed -> task.failed is True. So the function need to return False if task.failed is True
    if nc_result.failed:
        config_status = False

    return config_status


def nc_cfg_tpl_int(nr_obj, verbose=False):
    """
    This function creates a list of all Nornir inventory tpl_int interface templates and runs the task
    nc_edit_tpl_int_config against all interface template groups in the list. The task nc_edit_tpl_int_config
    returns custom Nornir results with the Result() function and these results are processed for each
    interface template group after the task is finished. If all subtasks were successful the function returns
    True, else False.
    """
    # To verify the config status of each subtask and as function return
    config_status = True

    # Gather the tpl_int templates from all hosts
    task = nr_obj.run(task=create_tpl_int_list, on_failed=True)

    # Create a union of the results from all hosts -> no duplicate items
    tpl_int_list = []
    for host in task:
        tpl_int_list = list(set().union(tpl_int_list, task[host].result))

    # Backoff config attempt value
    config_attempts = 5

    for tpl_int_name in tpl_int_list:
        print_task_name(text=f"NETCONF configure Jinja2 template {tpl_int_name}")

        # Run the custom nornir task nc_edit_tpl_int_config
        nc_result = nr_obj.run(
            task=nc_edit_tpl_int_config,
            tpl_int_name=tpl_int_name,
            verbose=verbose,
            config_attempts=config_attempts,
            on_failed=True,
        )

        # All results from the task custom nc_edit_tpl_int_config have been processed and returned with Nornir
        # Result() by the task to use custom std-out printing and to avoid the Nornir default print_result().
        for host in nc_result:
            # If the result is not None -> Skip all results which are NoneType.
            # These are KeyErrors of not existing tpl_int on a host.
            if nc_result[host].result is None:
                continue
            # Print results for each interface which is the host Return variable from nc_edit_tpl_int_config()
            print(task_host(host=host, changed=str(nc_result[host].changed)))

            # If the task fails and a exceptions is the result
            if isinstance(nc_result[host].result, str):
                print(nc_result[host].result)

            else:
                # The custom returned result item 0 from nc_edit_config() is a list. Print every list
                # item == NETCONF result Standard Nornir result starts at index 1 -> index 0 is custom return
                index = 1
                for result in nc_result[host].result:
                    # If the result is an Nornir ERROR type == failed
                    if "ERROR" in result:
                        config_status = False
                        # Print the custom result
                        print(result.rstrip())
                        # Print the last Nornir config attempt result
                        index = index + config_attempts - 1
                        print(f"\n{nc_result[host][index].result.rstrip()}")
                        index += 1

                    # If the result is not an Nornir ERROR type == success
                    else:
                        # Print the custom result
                        print(result.rstrip())
                        index += 1

    # If the task failed -> nc_result.failed is True. So return False if nc_result.failed is True
    if nc_result.failed:
        config_status = False

    return config_status
