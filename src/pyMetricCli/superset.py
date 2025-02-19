"""
Wrapper for the pySupersetCli Tool.
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

import subprocess
import logging

from pyProfileMgr.profile_data import ProfileType
from pyProfileMgr.profile_mgr import ProfileMgr
from pyProfileMgr.ret import Ret


################################################################################
# Variables
################################################################################

LOG: logging.Logger = logging.getLogger(__name__)


################################################################################
# Classes
################################################################################


class Superset:  # pylint: disable=too-few-public-methods
    """
    Wrapper for the pySupersetCli Tool.
    """

    def __init__(self, superset_config: dict) -> None:
        self.config = superset_config
        self.is_installed = self._check_if_is_installed()

    def _run_pysupersetcli(self, arguments) -> subprocess.CompletedProcess:
        """
        Wrapper to run pySupersetCli command line.

        Args:
            arguments (list): List of arguments to pass to pySupersetCli.

        Returns:
            subprocess.CompletedProcess[bytes]: The result of the command.
            Includes return code, stdout and stderr.
        """
        # pylint: disable=duplicate-code
        args = ["pySupersetCli"]  # The executable to run.
        args.extend(arguments)  # Add the arguments to the command.
        return subprocess.run(args,
                              capture_output=True,
                              check=False,
                              shell=False)

    def _check_if_is_installed(self) -> bool:
        """
        Checks if the pySupersetCli Tool is installed.

        Returns:
            bool: True if pySupersetCli is installed, False otherwise.
        """
        is_installed = True
        try:
            ret = self._run_pysupersetcli(["--help"])
            ret.check_returncode()
        except subprocess.CalledProcessError:
            print("pySupersetCli is not installed!")
            is_installed = False
        return is_installed

    def upload(self, input_file) -> int:
        """
        Upload to Superset using the upload command of pySupersetCli.

        Args:
            input_file (str): Path to JSON file which shall be uploaded.

        Returns:
            int: Return Code of the command.
        """

        server: str
        username: str
        password: str

        # Read credentials from the profile if a profile name has been given
        # in the 'superset_config'.
        # pylint: disable=R0801
        if "profile" in self.config:
            profile_mgr = ProfileMgr()
            ret_code = profile_mgr.load(self.config["profile"])
            if ret_code != Ret.CODE.RET_OK:
                print("Error loading profile:", self.config['profile'])
                return -1

            # Check for profile type 'superset'.
            if profile_mgr.loaded_profile.type != ProfileType.SUPERSET:
                print("The profile type is not 'superset'.")
                return -1

            server = profile_mgr.loaded_profile.server_url
            username = profile_mgr.loaded_profile.user
            password = profile_mgr.loaded_profile.password
        # Else take credentials from the 'superset_config'.
        else:
            server = self.config["server"]
            username = self.config["username"]
            password = self.config["password"]

        command_list: list = ["--verbose",
                              "--server", server,
                              "--user", username,
                              "--password", password]

        if self.config.get("basic_auth") is True:
            command_list.append("--basic_auth")

        if self.config.get("no_ssl") is True:
            command_list.append("--no_ssl")

        LOG.info("Uploading file: %s", input_file)

        command_list.extend(["upload",
                             "--database", self.config["database"],
                             "--table", self.config["table"],
                             "--file", input_file
                             ])
        ret = self._run_pysupersetcli(command_list)

        if 0 != ret.returncode:
            LOG.error("Error while uploading: %s", ret.stderr)

        return ret.returncode


################################################################################
# Functions
################################################################################

################################################################################
# Main
################################################################################
