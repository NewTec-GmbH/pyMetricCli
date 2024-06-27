
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

import logging
from pyMetricCli.adapter_interface import AdapterInterface

################################################################################
# Variables
################################################################################

LOG = logging.getLogger(__name__)

################################################################################
# Classes
################################################################################


class Adapter(AdapterInterface):
    """
    Adapter class for handling different search results.
    """

    # Define the output dictionary
    # Must include all possible values.
    # Please make sure that the keys of the output dictionary are unique, regardless of their case.
    # In this example, Polarion Status has 2 possible values: "open" and "closed".
    output: dict = {
        "status_open": 0,
        "status_closed": 0
    }

    jira_config = {
        "server": "https://jira.example.com",
        "token": "",
        "filter": "",
        "max": "0",  # 0 gets all issues that match the filter.
        "fields": [],
        "full": False
    }

    polarion_config = {
        "username": "",
        "password": "",
        "server": "http://polarion.example.com/polarion",
        "project": "",
        "query": "HAS_VALUE:status",  # Query to get all work items with a status
        "fields": ["status"]  # Fields to include in the query
    }

    superset_config = {
        "server": "http://superset.example.com",
        "user": "",
        "password": "",
        "database": 0,  # Primary key of the database
        "table": "",
        "basic_auth": False,
        "no_ssl": False
    }

    def handle_jira(self, search_results: dict) -> bool:
        """
        Handles the JIRA search results.

        Args:
            search_results: The search results from the JIRA API.

        Returns:
            bool: True if the search results were handled successfully, False otherwise.
        """
        LOG.info("Handling JIRA search results...")
        LOG.info(search_results)
        return True

    def handle_polarion(self, search_results: dict) -> bool:
        """
        Handles the Polarion search results.

        Args:
            search_results: The search results from the Polarion API.

        Returns:
            bool: True if the search results were handled successfully, False otherwise.
        """
        LOG.info("Handling Polarion search results...")
        LOG.info(search_results)
        return True

################################################################################
# Functions
################################################################################

################################################################################
# Main
################################################################################
