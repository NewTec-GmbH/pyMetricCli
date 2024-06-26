"""The main module with the program entry point."""

# BSD 3-Clause License
#
# Copyright (c) 2024, NewTec GmbH
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICU5LAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

################################################################################
# Imports
################################################################################

import sys
import logging
import argparse
import os.path
import importlib.util
import json

from pyMetricCli.version import __version__, __author__, __email__, __repository__, __license__
from pyMetricCli.ret import Ret

################################################################################
# Variables
################################################################################

LOG: logging.Logger = logging.getLogger(__name__)

PROG_NAME = "pyMetricCli"
PROG_DESC = "Collection of scripts and API implementations for generating and playing with metrics."
PROG_COPYRIGHT = f"Copyright (c) 2024 NewTec GmbH - {__license__}"
PROG_GITHUB = f"Find the project on GitHub: {__repository__}"
PROG_EPILOG = f"{PROG_COPYRIGHT} - {PROG_GITHUB}"

################################################################################
# Classes
################################################################################

################################################################################
# Functions
################################################################################


def add_parser() -> argparse.ArgumentParser:
    """ Add parser for command line arguments and
        set the execute function of each 
        cmd module as callback for the subparser command.
        Return the parser after all the modules have been registered
        and added their subparsers.


    Returns:
        argparse.ArgumentParser:  The parser object for commandline arguments.
    """
    parser = argparse.ArgumentParser(prog=PROG_NAME,
                                     description=PROG_DESC,
                                     epilog=PROG_EPILOG)

    required_arguments = parser.add_argument_group('required arguments')

    required_arguments.add_argument('-c',
                                    '--config_file',
                                    type=str,
                                    metavar='<config_file>',
                                    required=True,
                                    help="Configuration file to be used.")

    parser.add_argument("--version",
                        action="version",
                        version="%(prog)s " + __version__)

    parser.add_argument("-v",
                        "--verbose",
                        action="store_true",
                        help="Print full command details before executing the command.\
                            Enables logs of type INFO and WARNING.")

    return parser


def import_handler(adapter_path: str) -> type:
    """
    Import the adapter module from the given path.

    Args:
        adapter_path (str): The path to the adapter module.

    Returns:
        type: The Adapter Class.
    """
    adapter_name = "adapter"

    if not os.path.isfile(adapter_path):
        raise ValueError(f"File not found: {adapter_path}")

    module_spec = importlib.util.spec_from_file_location(adapter_name,
                                                         adapter_path)
    adapter = importlib.util.module_from_spec(module_spec)
    sys.modules[adapter_name] = adapter
    module_spec.loader.exec_module(adapter)

    return adapter.Adapter()


def set_key_value_pair(key: str, value: str) -> bool:
    """
    Set the value of a key in a dictionary.

    Args:
        key (str): The key.
        value (str): The value.

    Returns:
        bool: True if the key-value pair was set successfully, False otherwise.
    """
    print(f"Setting key '{key}' to value '{value}'")
    return True


def main() -> Ret:
    """ The program entry point function.

    Returns:
        int: System exit status.
    """
    ret_status = Ret.OK

    # Create the main parser and add the subparsers.
    parser = add_parser()

    # Parse the command line arguments.
    args = parser.parse_args()

    # Check if the command line arguments are valid.
    if args is None:
        ret_status = Ret.ERROR_ARGPARSE
        parser.print_help()
    else:
        # If the verbose flag is set, change the default logging level.
        if args.verbose:
            logging.basicConfig(level=logging.INFO)
            LOG.info("Program arguments: ")
            for arg in vars(args):
                LOG.info("* %s = %s", arg, vars(args)[arg])

        try:
            # Check if the config file is a JSON file.
            if args.config_file.endswith(".json") is False:
                raise ValueError(
                    "Invalid config_file format. Please provide a JSON file.")

            # Load the config file.
            with open(args.config_file, "r", encoding="UTF-8") as file:
                config_data = json.load(file)

            # Check if the adapter_path is present in the config file.
            if "adapter_path" not in config_data:
                raise ValueError("adapter_path not found in config file.")

            # Import the adapter module.
            adapter = import_handler(config_data["adapter_path"])

            # Get data from JIRA and Polarion.
            LOG.info("Getting data from JIRA and Polarion...")

            # Call the handler functions to extract the data.
            adapter.handle_jira({}, set_key_value_pair)
            adapter.handle_polarion({}, set_key_value_pair)

            # Save the output dictionary to a temporary file.
            LOG.info("Saving output to a temporary file...")

            # Send the temporary file to the metric server using Superset.
            LOG.info("Sending the temporary file to the metric server...")

            # Remove the temporary file.
            LOG.info("Removing the temporary file...")

        except Exception as e:  # pylint: disable=broad-except
            LOG.error("An error occurred: %s", e)
            ret_status = Ret.ERROR

    return ret_status

################################################################################
# Main
################################################################################


if __name__ == "__main__":
    sys.exit(main())
