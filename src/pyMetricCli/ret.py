"""This module contains general constants, used in all other modules."""

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

from enum import IntEnum

################################################################################
# Variables
################################################################################

################################################################################
# Classes
################################################################################


class Ret(IntEnum):
    """This type shall be used for return status information.
    """
    OK = 0
    ERROR = 1
    ERROR_ARGPARSE = 2  # Must be 2 to match the argparse error code.
    ERROR_INVALID_ARGUMENT = 3
    ERROR_ADAPTER_HANDLER_JIRA = 4
    ERROR_ADAPTER_HANDLER_POLARION = 5
    ERROR_SUPERSET_UPLOAD = 6
    ERROR_NOT_INSTALLED_JIRA = 7
    ERROR_NOT_INSTALLED_POLARION = 8
    ERROR_NOT_INSTALLED_SUPERSET = 9

################################################################################
# Functions
################################################################################

################################################################################
# Main
################################################################################
