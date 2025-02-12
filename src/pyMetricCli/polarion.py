"""
Wrapper for the pyPolarionCli Tool.
"""

# BSD 3-Clause License
#
# Copyright (c) 2024 - 2025, NewTec GmbH
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
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
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

import os
import subprocess
import json
import logging

from pyProfileMgr.profile_mgr import ProfileMgr, ProfileType
from pyProfileMgr.ret import Ret


################################################################################
# Variables
################################################################################

LOG: logging.Logger = logging.getLogger(__name__)


################################################################################
# Classes
################################################################################


class Polarion:  # pylint: disable=too-few-public-methods
    """
    Wrapper for the pyPolarionCli Tool.
    """

    def __init__(self, polarion_config: dict) -> None:
        self.config = polarion_config
        self.is_installed = self.__check_if_is_installed()

    def __run_pypolarioncli(self, arguments) -> subprocess.CompletedProcess:
        """
        Wrapper to run pyPolarionCli command line.

        Args:
            arguments (list): List of arguments to pass to pyPolarionCli.

        Returns:
            subprocess.CompletedProcess[bytes]: The result of the command.
            Includes return code, stdout and stderr.
        """
        args = ["pyPolarionCli"]  # The executable to run.
        args.extend(arguments)  # Add the arguments to the command.

        return subprocess.run(args,
                              capture_output=True,
                              check=False,
                              shell=False)

    def __check_if_is_installed(self) -> bool:
        """
        Checks if the pyPolarionCli Tool is installed.

        Returns:
            bool: True if pyPolarionCli is installed, False otherwise.
        """
        # pylint: disable=duplicate-code
        is_installed = True
        try:
            ret = self.__run_pypolarioncli(["--help"])
            ret.check_returncode()
        except subprocess.CalledProcessError:
            print("pyPolarionCli is not installed!")
            is_installed = False
        return is_installed

    def search(self) -> dict:
        """
        Search in Polarion using the search command of pyPolarionCli.

        Returns:
            dict: Search results.
        """
        output = {}

        output_file_name = os.path.join(self.config['output'],
                                        f"{self.config['project']}_search_results.json")

        server: str
        username: str
        password: str
        token: str

        # Read credentials from the profile if a profile name has been given
        # in the 'polarion_config'.
        if "profile" in self.config:
            profile_mgr = ProfileMgr()
            ret_code = profile_mgr.load(self.config["profile"])
            if ret_code != Ret.CODE.RET_OK:
                print("Error loading profile:", self.config['profile'])
                return output

            # Check for profile type 'polarion'.
            if profile_mgr.get_type() != ProfileType.POLARION:
                print("The profile type is not 'polarion'.")
                return output

            server = profile_mgr.get_server_url()
            username = profile_mgr.get_user()
            password = profile_mgr.get_password()
            token = profile_mgr.get_api_token()
        # Else take credentials from the 'polarion_config'.
        else:
            server = self.config["server"]
            username = self.config["username"]
            password = self.config["password"]
            token = self.config["token"]

        command_list: list = []

        # Add token if available. pyPolarionCli will use it instead of the password if provided.
        if token:
            command_list += ["--token", token]
        else:
            command_list += ["--user", username,
                             "--password", password]

        command_list += ["--server", server,
                         "search",
                         "--project", self.config["project"],
                         "--output", self.config["output"],
                         "--query", self.config["query"]]

        for field in self.config["fields"]:
            command_list.append("--field")
            command_list.append(field)

        ret = self.__run_pypolarioncli(command_list)

        if 0 != ret.returncode:
            print("Error while running pyPolarionCli!")
            print(ret.stderr)
        else:

            try:
                with open(output_file_name, "r", encoding="utf-8") as file:
                    output = json.load(file)
            except Exception as e:  # pylint: disable=broad-except
                LOG.error(
                    "An error occurred loading the Polarion results from file: %s", e)

        return output


################################################################################
# Functions
################################################################################

################################################################################
# Main
################################################################################
