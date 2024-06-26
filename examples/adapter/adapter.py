
"""Project-Specific Adapter Module"""

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

from typing import Callable
import logging

################################################################################
# Variables
################################################################################

LOG = logging.getLogger(__name__)

################################################################################
# Classes
################################################################################


class Adapter:
    """
    Adapter class for handling different search results.
    """

    def handle_jira(self,
                    search_results: dict,
                    set_key_value_pair: Callable[[str, str], bool]) -> None:
        """
        Handles the JIRA search results.

        Args:
            search_results: The search results from the JIRA API.
            set_key_value_pair: The callback function to set 
                a key-value pair in the output dictionary.

        set_key_value_pair:
            Args:
                key: The key to set in the output dictionary.
                value: The value to set in the output dictionary.
            Returns:
                True if the key-value pair was set successfully, False otherwise.
        """
        LOG.info("Handling JIRA search results...")
        LOG.info(type(search_results))
        LOG.info(type(set_key_value_pair))

    def handle_polarion(self,
                        search_results: dict,
                        set_key_value_pair: Callable[[str, str], bool]) -> None:
        """
        Handles the Polarion search results.

        Args:
            search_results: The search results from the Polarion API.
            set_key_value_pair: The callback function to set 
                a key-value pair in the output dictionary.

        set_key_value_pair:
            Args:
                key: The key to set in the output dictionary.
                value: The value to set in the output dictionary.
            Returns:
                True if the key-value pair was set successfully, False otherwise.

        """
        LOG.info("Handling Polarion search results...")
        LOG.info(type(search_results))
        LOG.info(type(set_key_value_pair))

################################################################################
# Functions
################################################################################

################################################################################
# Main
################################################################################
