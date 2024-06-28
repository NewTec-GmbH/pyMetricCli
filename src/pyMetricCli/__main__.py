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
import datetime
import shutil

from pyMetricCli.version import __version__, __author__, __email__, __repository__, __license__
from pyMetricCli.ret import Ret
from pyMetricCli.jira import Jira
from pyMetricCli.polarion import Polarion
from pyMetricCli.superset import Superset
from pyMetricCli.adapter_interface import AdapterInterface

################################################################################
# Variables
################################################################################

LOG: logging.Logger = logging.getLogger(__name__)

PROG_NAME = "pyMetricCli"
PROG_DESC = "Collection of scripts and API implementations for generating and playing with metrics."
PROG_COPYRIGHT = f"Copyright (c) 2024 NewTec GmbH - {__license__}"
PROG_GITHUB = f"Find the project on GitHub: {__repository__}"
PROG_EPILOG = f"{PROG_COPYRIGHT} - {PROG_GITHUB}"

_TEMP_DIR_NAME = "temp"
_TEMP_FILE_NAME = "superset_input.json"
_TEMP_FILE_PATH = os.path.join(_TEMP_DIR_NAME, _TEMP_FILE_NAME)

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

    required_arguments.add_argument('-a',
                                    '--adapter_file',
                                    type=str,
                                    metavar='<adapter_file>',
                                    required=True,
                                    help="Adapter file to be used.")

    parser.add_argument("--version",
                        action="version",
                        version="%(prog)s " + __version__)

    parser.add_argument("-v",
                        "--verbose",
                        action="store_true",
                        help="Print full command details before executing the command.\
                            Enables logs of type INFO and WARNING.")

    return parser


def _import_adapter(adapter_path: str) -> AdapterInterface:
    """
    Import the adapter module from the given path.

    Args:
        adapter_path (str): The path to the adapter module.

    Returns:
        AdapterInterface: Instance of an adapter class inherited from AdapterInterface.
    """
    adapter_name = "adapter"
    adapter_instance = None

    if not os.path.isfile(adapter_path):
        LOG.error("The adapter file does not exist.")
    else:
        module_spec = importlib.util.spec_from_file_location(adapter_name,
                                                             adapter_path)
        adapter = importlib.util.module_from_spec(module_spec)
        sys.modules[adapter_name] = adapter
        module_spec.loader.exec_module(adapter)
        if not hasattr(adapter, "Adapter"):
            LOG.error("The adapter module must have an 'Adapter' class.")
            adapter_instance = None
        else:
            adapter_instance = adapter.Adapter()

    # Check all required attributes and methods of the adapter class.
    # Must be done as Python does not enforce interfaces.
    if not isinstance(adapter_instance, AdapterInterface):
        LOG.error("The adapter class must inherit from AdapterInterface.")
        adapter_instance = None
    elif not hasattr(adapter_instance, "output"):
        LOG.error("The adapter class must have an 'output' attribute.")
        adapter_instance = None
    elif not hasattr(adapter_instance, "jira_config"):
        LOG.error("The adapter class must have a 'jira_config' attribute.")
        adapter_instance = None
    elif not hasattr(adapter_instance, "polarion_config"):
        LOG.error("The adapter class must have a 'polarion_config' attribute.")
        adapter_instance = None
    elif not hasattr(adapter_instance, "superset_config"):
        LOG.error("The adapter class must have a 'superset_config' attribute.")
        adapter_instance = None
    elif not hasattr(adapter_instance, "handle_jira"):
        LOG.error("The adapter class must have a 'handle_jira' method.")
        adapter_instance = None
    elif not hasattr(adapter_instance, "handle_polarion"):
        LOG.error("The adapter class must have a 'handle_polarion' method.")
        adapter_instance = None
    else:
        LOG.info("Adapter class successfully imported.")

        # Check if the values of the output dictionary in the adapter class are unique.
        output_list = list(adapter_instance.output.keys())
        output_list_lowercase = [status.lower() for status in output_list]

        number_unique_values = len(set(output_list_lowercase))
        if number_unique_values != len(output_list):
            LOG.error(
                "The keys in the output dictionary in the adapter class must be unique.")
            adapter_instance = None

    return adapter_instance


def _process_jira(adapter: AdapterInterface) -> Ret:
    """
    Process the Jira query and search results.

    Returns:
        Ret: The return status.
    """
    ret_status = Ret.OK

    if adapter.jira_config.get("filter", "") != "":
        # Overwrite the output directory with the temp directory.
        adapter.jira_config["file"] = os.path.join(
            _TEMP_DIR_NAME, "jira_search_results.json")

        LOG.info("Searching in Jira: %s",
                 adapter.jira_config["filter"])

        jira_instance = Jira(adapter.jira_config)
        if jira_instance.is_installed is False:
            LOG.error("pyJiraCli is not installed!")
            ret_status = Ret.ERROR_NOT_INSTALLED_JIRA
        else:
            jira_results = jira_instance.search()
            if adapter.handle_jira(jira_results) is False:
                ret_status = Ret.ERROR_ADAPTER_HANDLER_JIRA

    return ret_status


def _process_polarion(adapter: AdapterInterface) -> Ret:
    """
    Process the Polarion query and search results.

    Returns:
        Ret: The return status.
    """
    ret_status = Ret.OK

    if adapter.polarion_config.get("query", "") != "":
        # Overwrite the output directory with the temp directory.
        adapter.polarion_config["output"] = _TEMP_DIR_NAME

        LOG.info("Searching in Polarion: %s",
                 adapter.polarion_config["query"])

        polarion_instance = Polarion(adapter.polarion_config)
        if polarion_instance.is_installed is False:
            LOG.error("pyPolarionCli is not installed!")
            ret_status = Ret.ERROR_NOT_INSTALLED_POLARION
        else:
            polarion_results = polarion_instance.search()
            if adapter.handle_polarion(polarion_results) is False:
                ret_status = Ret.ERROR_ADAPTER_HANDLER_POLARION

    return ret_status


def _save_temp_file(output: dict) -> Ret:
    """
    Save the output dictionary to a temporary file.

    Args:
        output (dict): The output dictionary.

    Returns:
        Ret: The return status.
    """
    ret_status = Ret.OK

    try:
        # Write to the file.
        with open(_TEMP_FILE_PATH, "w", encoding="UTF-8") as file:
            json.dump(output, file, indent=2)
    except Exception as e:  # pylint: disable=broad-except
        LOG.error("An error occurred writing the temporary file: %s", e)
        ret_status = Ret.ERROR

    return ret_status


def _process_superset(adapter: AdapterInterface) -> Ret:
    """
    Process the Superset file upload.

    Returns:
        Ret: The return status.
    """
    ret_status = Ret.OK

    # Send the temporary file to the metric server using Superset.
    superset_instance = Superset(adapter.superset_config)
    if superset_instance.is_installed is False:
        LOG.error("pySupersetCli is not installed!")
        ret_status = Ret.ERROR_NOT_INSTALLED_SUPERSET
    else:
        ret = superset_instance.upload(_TEMP_FILE_PATH)

        if 0 != ret:
            ret_status = Ret.ERROR_SUPERSET_UPLOAD
            LOG.error("Error while uploading to Superset!")
        else:
            LOG.info("Successfully uploaded to Superset!")

    return ret_status


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
        adapter: AdapterInterface = None

        # If the verbose flag is set, change the default logging level.
        if args.verbose:
            logging.basicConfig(level=logging.INFO)
            LOG.info("Program arguments: ")
            for arg in vars(args):
                LOG.info("* %s = %s", arg, vars(args)[arg])

        # Check if temp directory exists, if not create it.
        os.makedirs(_TEMP_DIR_NAME, exist_ok=True)

        # Check if the adapter is a Python file.
        if args.adapter_file.endswith(".py") is False:
            ret_status = Ret.ERROR_INVALID_ARGUMENT
            LOG.error("The adapter must be a Python file.")
        else:
            adapter = _import_adapter(args.adapter_file)

            if adapter is None:
                LOG.error("The adapter module could not be imported.")
                ret_status = Ret.ERROR
            else:
                if Ret.OK != _process_jira(adapter=adapter):
                    LOG.error("Error while processing Jira.")
                    ret_status = Ret.ERROR_ADAPTER_HANDLER_JIRA

                elif Ret.OK != _process_polarion(adapter=adapter):
                    LOG.error("Error while processing Polarion.")
                    ret_status = Ret.ERROR_ADAPTER_HANDLER_POLARION
                else:
                    # Save the output dictionary to a temporary file.
                    LOG.info("Saving output to a temporary file...")

                    # Get the output from the adapter.
                    processed_output = adapter.output

                    # Ensure the output always contains a date.
                    processed_output["date"] = datetime.datetime.now(
                    ).isoformat()

                    # Save the output to a temporary file.
                    if Ret.OK != _save_temp_file(output=processed_output):
                        ret_status = Ret.ERROR
                        LOG.error("Error while saving the temporary file.")
                    elif Ret.OK != _process_superset(adapter=adapter):
                        ret_status = Ret.ERROR_SUPERSET_UPLOAD
                        LOG.error("Error while processing Superset.")

        # Clean up the temporary directory if exists.
        shutil.rmtree(_TEMP_DIR_NAME, ignore_errors=True)

    return ret_status

################################################################################
# Main
################################################################################


if __name__ == "__main__":
    sys.exit(main())
