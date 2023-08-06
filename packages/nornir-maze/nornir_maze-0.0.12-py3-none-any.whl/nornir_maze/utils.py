#!/usr/bin/env python3
"""
This helper file contains general functions and tasks related to Nornir.

The functions are ordered as followed:
- Helper Functions
- Nornir print functions
- Nornir Helper Tasks
"""

import os
import sys
import re
import argparse
from nornir_jinja2.plugins.tasks import template_file
from nornir.core.task import Result
from nornir.core.filter import F
from nornir_salt.plugins.functions import FFun


__author__ = "Willi Kubny"
__maintainer__ = "Willi Kubny"
__version__ = "1.0"
__license__ = "MIT"
__email__ = "willi.kubny@kyndryl.com"
__status__ = "Production"


#### Helper Functions ########################################################################################


def index_of_first_number(string):
    """
    Return the index of the first number in a string
    """
    # pylint: disable=invalid-name
    for i, c in enumerate(string):
        if c.isdigit():
            index = i
            break

    return index


def extract_interface_number(string):
    """
    Removes the interface name and returns only the interface number
    """
    try:
        index = index_of_first_number(string)
        interface_number = string[index:]

    except UnboundLocalError:
        interface_number = string

    return interface_number


def extract_interface_name(string):
    """
    Removes the interface number and returns only the interface name
    """
    try:
        index = index_of_first_number(string)
        interface_name = string[:index]

    except UnboundLocalError:
        interface_name = string

    return interface_name


def complete_interface_name(interface_string):
    """
    This function takes a string with an interface name only or a full interface with its number and returns
    the full interface name but without the number:
    Gi -> GigabitEthernet
    Tw -> TwentyFiveGigE
    etc.
    """
    # pylint: disable=no-else-return, unidiomatic-typecheck

    error_msg = "Variable interface_string"

    if type(interface_string) is str:
        # Extract the interface name / delete the interface number
        interface_name = extract_interface_name(interface_string)
        # Define the name of the interface
        if interface_name.startswith("Eth"):
            interface_name = "Ethernet"
        elif interface_name.startswith("Fa"):
            interface_name = "FastEthernet"
        elif interface_name.startswith("Gi"):
            interface_name = "GigabitEthernet"
        elif interface_name.startswith("Te"):
            interface_name = "TenGigabitEthernet"
        elif interface_name.startswith("Tw"):
            interface_name = "TwentyFiveGigE"
        elif interface_name.startswith("Hu"):
            interface_name = "HundredGigE"
        else:
            raise ValueError(f"{error_msg} value is not a known interface name")

        return interface_name

    else:
        raise TypeError(f"{error_msg} is not a type string")


def load_credentials_from_env(username: str, password: str) -> tuple:
    """
    This function loads the login credentials from environment variables and stores them in the defaults
    """
    # Verify that login credentials are set as environment variables. Raise a KeyError when is None
    try:
        print_task_name(text="NORNIR load credentials from environment variable")

        credentials = os.environ[username], os.environ[password]

        print(task_info(text="NORNIR load credentials from environment variable", changed="False"))
        print(f"'Load env {username}' -> OS.EnvironResponse <Success: True>")
        print(f"'Load env {password}' -> OS.EnvironResponse <Success: True>")

    except KeyError as error:
        print(task_error(text="NORNIR load credentials from environment variable", changed="False"))
        print(f"'Load env {error}' -> OS.EnvironResponse <Success: False>")
        print(f"\nEnvironment variable {error} not found\n")
        sys.exit()

    return credentials


class NornirArgParse(argparse.ArgumentParser):
    """
    This class takes the argparse.ArgumentParser function as a superclass and overwrites the argparse error
    function. Every time that argparse calls the error function the following error function will be executed.
    """

    def error(self, message):
        """
        This function overwrites the standard argparse error function
        """
        print(task_error(text="Filter Nornir inventory", changed="False"))
        print(f"error: {message}\n")
        self.print_help()
        print("\n")
        sys.exit()


def get_nr_filter_obj_and_args(nr_obj, argparse_prog_name: str) -> tuple:
    """
    This function filters the Nornir inventory with a tag or a host argument provided by argparse. Input
    validation will ensure that only one argument is present and that the tag or host argument creates a
    correct inventory filtering. The new filtered Nornir object will be returned or the script terminates.
    """
    task_text = "NORNIR filter inventory"
    print_task_name(text=task_text)

    # Define the arguments which needs to be given to the script execution
    argparser = NornirArgParse(
        prog=argparse_prog_name,
        description="Filter the Nornir inventory based on a tag or a host",
        epilog="Only one of the mandatory arguments can be specified.",
    )

    # Create a mutually exclusive group. Argparse will make sure that only one of the arguments in the group
    # was present on the command line
    arg_group = argparser.add_mutually_exclusive_group(required=True)

    # Add arg_group parser arguments
    arg_group.add_argument(
        "--tag", type=str, metavar="<TAG>", help="inventory filter for a single Nornir tag"
    )
    arg_group.add_argument(
        "--hosts", type=str, metavar="<HOST-NAMES>", help="inventory filter for comma seperated Nornir hosts"
    )

    # Add the optional verbose argument
    argparser.add_argument(
        "-v", "--verbose", action="store_true", default=False, help="show extensive result details"
    )

    # Add the optional rebuild argument
    argparser.add_argument(
        "-r",
        "--rebuild",
        action="store_true",
        default=False,
        help="rebuild the config from day0 (default: golden-config)",
    )

    # Verify the provided arguments and print the custom argparse error message in case any error or wrong
    # arguments are present and exit the script
    args = argparser.parse_args()

    # If the --hosts argument is set, verify that the host exist
    if args.hosts:
        # Create a list from the comma separated hosts argument
        args_hosts_list = args.hosts.split(",")

        # Use Nornir-Salt FFun Filter-List option to filter on a list of hosts
        nr_f_obj = FFun(nr_obj, FL=args_hosts_list)

        # Create a list with all filteres Nornir hosts for verification
        nr_hosts_list = list(nr_f_obj.inventory.hosts.keys())

        # Verify that each host in from the --host argument is part of the filtered Nornir inventory, else
        # the diff host will be in the list
        host_diff_list = [x for x in args_hosts_list if x not in nr_hosts_list]
        if host_diff_list:
            print(task_error(text=task_text, changed="False"))
            print(f"'{task_text} for hosts' -> NornirResponse <Success: False>")
            print("\nHosts not part of the hosts.yaml inventory file")
            for host in host_diff_list:
                print(f"-> {host}")
            print(
                "\n\033[1m\u001b[31m"
                "-> Analyse the Nornir inventory and filter for an existing host\n\n"
                "\033[0m"
            )
            sys.exit()
        else:
            print(task_info(text=task_text, changed="False"))
            print(f"'{task_text} for hosts' -> NornirResponse <Success: True>\n")
            for host in nr_hosts_list:
                print(f"-> {host}")

    # If the --tag argument is set, verify that the tag has hosts assigned to
    if args.tag:
        # Filter the inventory based on the argument tag
        nr_f_obj = nr_obj.filter(F(tags__contains=args.tag))

        # If the filteres object have no hosts, exit with a error message
        if nr_f_obj.inventory.hosts.keys():
            print(task_info(text=task_text, changed="False"))
            print(f"'{task_text} for tag {args.tag}' -> NornirResult <Success: True>")

        else:
            print(task_error(text=task_text, changed="False"))
            print(
                f"'Filter inventory for tag {args.tag}' -> NornirResult <Success: False>"
                + f"\n\nNo host with tag '{args.tag}' in hosts.yaml inventory file"
                + "\n\033[1m\u001b[31m"
                + "-> Analyse the Nornir inventory and filter for a tag assigned to hosts\n\n"
                + "\033[0m"
            )
            sys.exit()

    return (nr_f_obj, args)


def nr_filter_inventory_from_host_list(nr_obj, filter_reason, host_list):
    """
    This function takes a Nornir object, a filter reason to print in Nornir style to std-out and a list of
    hosts. It can be a list of hosts or a list of strings where the hostname is part of the string, as the
    function checks if the hostname from the Nornir object is in that host list or list of strings. Every host
    that matches will be added to the new filter target and the new filtered Nornir object will be returned.
    """
    task_text = "NORNIR re-filter inventory"
    print_task_name(task_text)

    # Re-filter the Nornir inventory only on hosts that need to be reconfigured.
    # Create an empty list to fill with all hosts that need reconfiguration.
    filter_target = []

    # Iterate over all diff files and add the host to the filter_target list if the Nornir inventory host is
    # in the diff file name
    for item in host_list:
        for host in nr_obj.inventory.hosts.keys():
            if host in item:
                filter_target.append(host)
                break

    # Remove possible duplicate hosts in the list
    filter_target = list(set(filter_target))

    # Use Nornir-Salt FFun Filter-List option to filter on a list of hosts
    nr_obj = FFun(nr_obj, FL=filter_target)

    print(task_info(text=task_text, changed="False"))
    print(f"'{task_text} for hosts' -> NornirResponse <Success: True>")
    print(f"\n{filter_reason}")
    for host in nr_obj.inventory.hosts.keys():
        print(f"-> {host}")

    return nr_obj


def create_single_interface_list(interface_list):
    """
    This function takes a list of interfaces that are like the cisco interface range command and makes a list
    of full interface names for each interface:
    Gi1/0/1 -> GigabitEthernet1/0/1
    Gi1/0/1 - 10 -> GigabitEthernet1/0/1, GigabitEthernet1/0/2, etc.
    Gi1/0/1 - Gi1/0/10 -> GigabitEthernet1/0/1, GigabitEthernet1/0/2, etc.
    """
    # Define a list to return at the end of the function
    single_interface_list = []

    # Create the full interface name
    for interface in interface_list:
        # Create the full name of the interface, eg. Gi -> GigabitEthernet
        interface_name = complete_interface_name(interface)

        # If the list element is a interface range fullfil every single interface
        if "-" in interface:
            # Create a list with the two interfaces for the range
            interface_range = interface.replace(" ", "")
            interface_range = interface.split("-")

            # Regex pattern to match only the last number after the /
            pattern = r"(\d+)(?!.*\d)"

            # 1. Match the interface number prefix without the last number
            interface_prefix = extract_interface_number(interface_range[0])
            interface_prefix = re.sub(pattern, "", interface_prefix)

            # 2. Match the number after the last / in the interface number
            last_interface_numbers = []
            for interface in interface_range:
                # Extract only the interface number
                interface_number = extract_interface_number(interface)
                last_interface_number = re.findall(pattern, interface_number)
                last_interface_numbers.append(last_interface_number[0])

            # Define integers for the first and the last number of the range
            range_first_number = int(last_interface_numbers[0])
            range_last_number = int(last_interface_numbers[1])
            # Iterate over the range and construct each single interface
            while range_first_number <= range_last_number:
                single_interface = interface_name + interface_prefix + str(range_first_number)
                single_interface = single_interface.replace(" ", "")
                single_interface_list.append(single_interface)
                range_first_number += 1

        # If the list element is a single interface add it to the list to return
        else:
            interface_number = extract_interface_number(interface)
            single_interface = interface_name + interface_number
            single_interface_list.append(single_interface)

    return single_interface_list


#### Nornir Print Functions ##################################################################################


def print_task_title(text):
    """
    Prints a Nornir style title
    """
    asteriks_line = (74 - len(text)) * "*"
    color = "\033[1m\u001b[32m"
    color_end = "\033[0m"

    print(f"\n{color}**** {text} {asteriks_line}{color_end}")


def print_task_name(text):
    """
    Returns a Nornir style host task name
    """
    asteriks_line = (79 - len(text)) * "*"
    color = "\033[1m\u001b[36m"
    color_reset = "\033[0m"

    print(f"\n{color}{text} {asteriks_line}{color_reset}")


def task_host(host, changed):
    """
    Returns a Nornir style host task title
    """
    text = f"* {host} ** changed : {changed}"

    asteriks_line = (79 - len(text)) * "*"
    color = "\033[1m\u001b[34m"
    color_reset = "\033[0m"

    return f"{color}{text} {asteriks_line}{color_reset}"


def task_info(text, changed):
    """
    Returns a Nornir style task info message
    """
    text = f"---- {text} ** changed : {changed}"

    if "True" in changed:
        color = "\033[1m\u001b[33m"
    else:
        color = "\033[1m\u001b[32m"

    dash_line = (79 - len(text)) * "-"
    color_reset = "\033[0m"

    return f"{color}{text} {dash_line} INFO{color_reset}"


def task_error(text, changed):
    """
    Returns a Nornir style task error message
    """
    text = f"---- {text} ** changed : {changed}"

    dash_line = (79 - len(text)) * "-"
    color = "\033[1m\u001b[31m"
    color_reset = "\033[0m"

    return f"{color}{text} {dash_line} ERROR{color_reset}"


#### Nornir Helper Tasks #####################################################################################


def create_tpl_int_list(task):
    """
    This function loops over all host inventory keys and append the key which start with tpl_int to the list
    of interface groups and returns a Nornir AggregatedResult Object
    """
    tpl_int_list = []
    for key in task.host.keys():
        if key.startswith("tpl_int"):
            tpl_int_list.append(key)

    return tpl_int_list


def template_file_custom(task, task_msg, path, template):
    """
    This custom Nornir task generates a configuration from a Jinja2 template based on a path and a template
    filename. The path and the template filename needs to be Nornir inventory keys which holds the needed
    information as value.
    """
    try:
        path = task.host[path]
        template = task.host[template]

    except KeyError as error:
        # Jinja2 Nornir inventory key not found. Key which specify the path and the file don't exist
        error_msg = (
            f"{task_error(text=task_msg, changed='False')}\n"
            + f"'nornir.core.inventory.Host object' has no attribute {error}"
        )

        # Return the Nornir result as error -> interface can not be configured
        return Result(host=task.host, result=error_msg, failed=True)

    # Run the Nornir Task template_file
    j2_tpl_result = task.run(task=template_file, template=template, path=path, on_failed=True)

    return Result(host=task.host, result=j2_tpl_result)
