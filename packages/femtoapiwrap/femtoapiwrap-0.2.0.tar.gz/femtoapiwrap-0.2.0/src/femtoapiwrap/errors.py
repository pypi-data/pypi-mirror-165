# Copyright ©2021. Femtonics Ltd. (Femtonics). All Rights Reserved.
# Permission to use, copy, modify this software and its documentation for educational,
# research, and not-for-profit purposes, without fee and without a signed licensing agreement, is
# hereby granted, provided that the above copyright notice, this paragraph and the following two
# paragraphs appear in all copies, modifications, and distributions. Contact info@femtonics.eu
# for commercial licensing opportunities.
#
# IN NO EVENT SHALL FEMTONICS BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL,
# INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS, ARISING OUT OF
# THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF FEMTONICS HAS BEEN
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# FEMTONICS SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE. THE SOFTWARE AND ACCOMPANYING DOCUMENTATION, IF ANY, PROVIDED
# HEREUNDER IS PROVIDED "AS IS". FEMTONICS HAS NO OBLIGATION TO PROVIDE
# MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.


"""
Errors.
"""

import typing as _t


class FemtoApiWrapError(IOError):
    """Base exception for this package."""
    pass


class ConnectionFailed(FemtoApiWrapError, IOError):
    """Connection to MESc or login failed."""
    pass


class MicroscopeTimedOut(FemtoApiWrapError, TimeoutError):
    """Cannot find microscope in the requested state within the specified time."""
    def __init__(self, time_passed, timeout):
        super().__init__(f'Operation timed out ({time_passed:.2f} > {timeout:.2f})')


class NodeNotFound(FemtoApiWrapError):
    """Cannot find a node (file, session, unit) that meets the conditions."""
    def __init__(self, what, key):
        super().__init__(f'Node ({what}, {key}) not found')


class MEScFileError(FemtoApiWrapError):
    """Base class for errors during MESc data structure processing."""


class NoMetaData(MEScFileError):
    """The raw metadata object is not provided / empty."""
    def __init__(self):
        super().__init__('Metadata could not be read. '
                         'Bad unithandle given or something else went wrong ...')


class NoMeasurementUnit(MEScFileError):
    """The session does not contain units."""
    def __init__(self):
        super().__init__('The current session has no measurement units.')


class InvalidMeasurementType(MEScFileError):
    """Unexpected measurement type encountered."""
    def __init__(self, bad_type: str):
        """
        :param bad_type: the invalid measurement type
        """
        super().__init__('Bad measurement type! Invalid file or newer/unexpected type.', bad_type)


class InvalidDimension(MEScFileError, IndexError):
    """Invalid / out of bounds index or dimension provided."""
    def __init__(self, what: str, bad: _t.Any, good: _t.Any):
        """
        :param what: name of the parameter / value
        :param bad: the bad value
        :param good: the good values
        """
        super().__init__('Dimension out of bounds', what, bad, good)


class InvalidPointGroup(MEScFileError, KeyError):
    """Got a point group index not supported by MESc"""
    def __init__(self, what: _t.Sequence[int]):
        """
        :param what: parameter values
        """
        super().__init__('Point group indices must be in [0; 9]', what)


class UnsupportedVersion(MEScFileError, NotImplementedError):
    """The version found in the data structure being processed is not
    supported by the current function."""
    def __init__(self, what: str, version: _t.Any, supported: _t.Any, *args):
        """
        :param what: which (sub-)structure is being processed
        :param version: the version found
        :param supported: supported version(s)
        :param args: additional info
        """
        super().__init__(f'Unsupported version for {what}: {version}. '
                         f'Supported: {supported}', *args)