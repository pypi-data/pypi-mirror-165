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


# ---------------------------------------------------------------------

"""
Python API wrapper functions for femtoAPI 2.0 version.

See our `Command Reference`_ for full documentation.

.. _`Command Reference`: https://femtonics.atlassian.net/wiki/spaces/API2/pages/
    1448161785/The+FemtoAPI+command+reference

.. warning::
    Not final version, nor is it fully tested yet!!!

Usage notes:

    * The recommended way to obtain the FemtoAPI websocket object is via the
      context manager :func:`connection`.
    * Most of the API functions have an optional parameter ``required``.
      By default (``False``), failed operations return ``None`` (or in some
      cases, ``False``).
      This can be useful when the operation is allowed to fail, e.g. polling
      the API for new frames.
      When set to ``True``, failed operations raise an exception containing
      the original error code and message.
    * Logging actions can be configured via :attr:`log_command`,
      :attr:`log_error`, :attr:`log_info` and :attr:`log_debug`: they can be set
      to any function taking arbitrary number of arguments (e.g. :func:`print`).

.. [1] https://femtonics.atlassian.net/
    wiki/spaces/API2/pages/1448161792/Get-set+imaging+window+viewport+parameters
.. [2] https://femtonics.atlassian.net/wiki/spaces/API2/pages/1448161793/
    Get-set+ZStack+PMT+laser+intensity+device+depth+profile
.. [3] https://femtonics.atlassian.net/
    wiki/spaces/API2/pages/1448161795/Get-set+PMT+Laserintensity+device+values
.. [4] https://femtonics.atlassian.net/wiki/spaces/API2/pages/1448161813/
    Curve+operations#Curveoperations-writeCurve
"""

from __future__ import annotations

import json
import logging
import random
import shutil
import time
import typing as _t
from contextlib import contextmanager
from pathlib import Path

# noinspection PyPep8Naming
import PySide2.QtCore as _qtc  # Besides some usage, it needs to be imported to enable PyFemtoAPI

# noinspection PyPep8Naming
import femtoapi.PyFemtoAPI as _pfa  # Must be imported after PySide2!

from . import errors as _e

# Type aliases
_JsBool = str
_OptionalJsBool = str
_JsonDict = _t.Dict[str, _t.Any]
_SigSub = str
_Ignorable = _t.Any


DEFAULT_URL = 'ws://localhost:8888'
"""Default connection URL using local MESc instance."""


logger = logging.getLogger(__name__)

log_command = logger.debug
"""Set this to change logging output."""

log_error = logger.error
"""Set this to change logging output."""

log_debug = logger.debug
"""Set this to change logging output."""

log_info = print
"""Set this to change logging output."""

log_warning = logger.warning
"""Set this to change logging output."""


@contextmanager
def connection(url: str = DEFAULT_URL):
    """Context manager to create and close the connection with the API server.

    Example::

        with api.connection() as ws:
            api.login(ws, 'asd', '123')

    :param url: IP address and port of the server
    :return: FemtoAPI client object
    """
    ws = initConnection(url)
    try:
        yield ws
    finally:
        closeConnection(ws)


def initConnection(url: str = DEFAULT_URL) -> _pfa.APIWebSocketClient:
    """Creates the websocket object used in all communications with the API server
    returns the ws object which is used in all other functions.

    .. note::

        Prefer using :func:`connection`, to achieve automatic closing.

    :param url: IP address and port of the server
    :return: websocket connection object
    """
    ws = _pfa.APIWebSocketClient(url)
    if not ws:
        log_error('WebSocketHost could not be found?')
        raise _e.ConnectionFailed(url)
    timer = 0
    done = False
    while timer < 10:
        log_info('Trying to connect to server...')
        done = ws.connectToServer()
        if not done:
            time.sleep(1)
        else:
            break
        timer = timer + 1
    log_info(f"Connection initialized: '{done}'")
    if not done:
        raise _e.ConnectionFailed(url)
    return ws


def login(ws: _pfa.APIWebSocketClient, name: str, passw: str) -> bool:
    """Login to the API server.

    Login function was created for possible future use in the APIserver
    no check is implemented, does not need real name and password at the moment.

    :param ws: FemtoAPI client
    :param name: username
    :param passw: password
    :return: ``True`` if login was successful
    :raise ConnectionFailed: if login was not successful
    """
    timer = 0
    login_parser = None
    result_code = 0
    while timer < 10:
        log_info('Trying to login to server...')
        login_parser = ws.login(name, passw)
        result_code = login_parser.getResultCode()
        if result_code > 0:
            time.sleep(1)
        else:
            break
        timer = timer + 1
    if result_code > 0:
        log_error(login_parser.getErrorText())
        raise _e.ConnectionFailed(result_code, login_parser.getErrorText())
    else:
        log_info('Successful login to FemtoAPI server')
        return True


def closeConnection(ws: _pfa.APIWebSocketClient) -> None:
    """Closes the connection in the ws object.

    .. note::

        Prefer using :func:`connection`, to achieve automatic closing.

    :param ws: FemtoAPI client
    """
    ws.close()
    log_info('Connection closed')


def enableSignals(ws: _pfa.APIWebSocketClient, required: bool = False) -> _Ignorable:
    """Enables signals.

    :param ws: FemtoAPI client
    :param required: raise exception on failure
    """
    command = "FemtoAPITools.enableSignals('true')"
    return _execute_command(ws, command, required)


def isSignalEnabled(ws: _pfa.APIWebSocketClient, required: bool = False) -> bool:
    """Queries if signals are enabled.

    :param ws: FemtoAPI client
    :param required: raise exception on failure
    """
    command = 'FemtoAPITools.isSignalEnabled()'
    return not not _execute_command(ws, command, required)
    

def getFileList(
        ws: _pfa.APIWebSocketClient,
        sigSub: _SigSub = '',
        required: bool = False
) -> list[int] | None:
    """Returns a list of open files.

    :param ws: FemtoAPI client
    :param sigSub: ``'subscribe'``, ``'unsubscribe'`` or ``''``
    :param required: raise exception on failure
    :return: list of file handles
    """
    if not sigSub:
        command = 'FemtoAPIFile.getFileList()'
    else:
        command = f"FemtoAPIFile.getFileList('{sigSub}')"
    cmd_result = _execute_command(ws, command, required)
    return json.loads(cmd_result) if cmd_result else None


def getFileMetadata(
        ws: _pfa.APIWebSocketClient,
        handle: str | int,
        sigSub: _SigSub = '',
        required: bool = False
) -> _JsonDict | None:
    """Returns read-only file metadata.

    :param ws: FemtoAPI client
    :param handle: file handle
    :param sigSub: ``'subscribe'``, ``'unsubscribe'`` or ``''``
    :param required: raise exception on failure
    :return: ``dict`` of metadata
    """
    if not sigSub:
        command = f"FemtoAPIFile.getFileMetadata('{handle}')"
    else:
        command = f"FemtoAPIFile.getFileMetadata('{handle}', '{sigSub}')"
    cmd_result = _execute_command(ws, command, required)
    return json.loads(cmd_result) if cmd_result else None


def getSessionMetadata(
        ws: _pfa.APIWebSocketClient,
        handle: str,
        sigSub: _SigSub = '',
        required: bool = False
) -> _JsonDict | None:
    """Queries session metadata.

    :param ws: FemtoAPI client
    :param handle: session handle in format ``'<file_id>,<session_id>'``
    :param sigSub: ``'subscribe'``, ``'unsubscribe'`` or ``''``
    :param required: raise exception on failure
    :return: ``dict`` of metadata
    """
    if not sigSub:
        command = f"FemtoAPIFile.getSessionMetadata('{handle}')"
    else:
        command = f"FemtoAPIFile.getSessionMetadata('{handle}', '{sigSub}')"
    cmd_result = _execute_command(ws, command, required)
    return json.loads(cmd_result) if cmd_result else None


def setSessionMetadata(
        ws: _pfa.APIWebSocketClient,
        handle: str,
        jsonString: str,
        required: bool = False
) -> bool:
    """Sets session metadata (currently only ``'comment'``).

    :param ws: FemtoAPI client
    :param handle: session handle in format ``'<file_id>,<session_id>'``
    :param jsonString: must be the same format as the result of
        :func:`getSessionMetadata` with the proper modified values
    :param required: raise exception on failure
    :return: success
    """
    command = f"FemtoAPIFile.setSessionMetadata('{handle}', '{jsonString}')"
    return not not _execute_command(ws, command, required)


def getUnitMetadata(
        ws: _pfa.APIWebSocketClient,
        handle: str,
        jsonItemName: str,
        sigSub: _SigSub = '',
        required: bool = False
) -> _JsonDict | list[_JsonDict] | None:
    """Gets a section of metadata specified with the key ``jsonItemName``.

    :param ws: FemtoAPI client
    :param handle: unit handle in format ``'<file_id>,<session_id>,<unit_id>'``
    :param jsonItemName:
        one of the following in string::

            BaseUnitMetadata
            Roi
            ReferenceViewport
            Points
            Device
            AxisControl
            UserData
            Protocol
            AoSettings
            IntensityCompensationo
            CoordinateTuning
            MultiProtocolJson
            CurveInfo
            FullFrameparams
            ChannelInfo
            Modality
            CameraSettings
            BreakView

    :param sigSub: ``'subscribe'``, ``'unsubscribe'`` or ``''``
    :param required: raise exception on failure
    :return: JSON ``dict`` or `list` depending on the key
    """
    if not sigSub:
        command = f"FemtoAPIFile.getUnitMetadata('{handle}', '{jsonItemName}')"
    else:
        command = f"FemtoAPIFile.getUnitMetadata('{handle}', '{jsonItemName}', '{sigSub}')"
    cmd_result = _execute_command(ws, command, required)
    return json.loads(cmd_result) if cmd_result else None


def setUnitMetadata(
        ws: _pfa.APIWebSocketClient,
        handle: str,
        jsonItemName: str,
        jsonString: str,
        required: bool = False
) -> bool:
    """Sets unit metadata.

    :param ws: FemtoAPI client
    :param handle: unit handle in format ``'<file_id>,<session_id>,<unit_id>'``
    :param jsonItemName: see at :func`getUnitMetadata`
    :param jsonString: must be the same format as the result of
        :func:`getUnitMetadata` with the proper modified values
    :param required: raise exception on failure
    :return: success
    """
    command = f"FemtoAPIFile.setUnitMetadata('{handle}', '{jsonItemName}', '{jsonString}')"
    return not not _execute_command(ws, command, required)


def getChildTree(
        ws: _pfa.APIWebSocketClient,
        handle: str = '',
        required: bool = False
) -> _JsonDict | None:
    """Returns information about the opened files.

    :param ws: FemtoAPI client
    :param handle: defines the range of data returned, can be empty,
        file level(``'10'``), session level(``'10,0'``) and
        munit level(``'10,0,0'``)
    :param required: raise exception on failure
    :return: tree as JSON ``dict``
    """
    command = f"FemtoAPIFile.getChildTree('{handle}')"
    cmd_result = _execute_command(ws, command, required)
    if cmd_result:
        log_debug('ChildTree acquired')
        return json.loads(cmd_result)
    else:
        return None


def getCurrentSession(
        ws: _pfa.APIWebSocketClient,
        sigSub: _SigSub = '',
        required: bool = False
) -> str | None:
    """Returns the handle of the current session.

    :param ws: FemtoAPI client
    :param sigSub: ``'subscribe'``, ``'unsubscribe'`` or ``''``
    :param required: raise exception on failure
    :return: handle in format ``'<file_id>,<session_id>'``
    """
    if not sigSub:
        command = 'FemtoAPIFile.getCurrentSession()'
    else:
        command = f"FemtoAPIFile.getCurrentSession('{sigSub}')"
    return _execute_command(ws, command, required)


def setCurrentSession(
        ws: _pfa.APIWebSocketClient,
        handle: str,
        required: bool = False
) -> bool:
    """Changes current session.

    :param ws: FemtoAPI client
    :param handle: in format ``'<file_id>,<session_id>'``
    :param required: raise exception on failure
    :return: success
    """
    command = f"FemtoAPIFile.setCurrentSession('{handle}')"
    return not not _execute_command(ws, command, required)

    
def getProcessingState(ws: _pfa.APIWebSocketClient, required: bool = False) -> _JsonDict | None:
    """
    .. deprecated:: 0.0.3
        Use :func:`getChildTree` instead.

    Returns a dictionary containing all data about the processing state
    """
    command = 'FemtoAPIFile.getProcessingState()'
    cmd_result = _execute_command(ws, command, required)
    return json.loads(cmd_result) if cmd_result else None

    
def getMicroscopeState(ws: _pfa.APIWebSocketClient, required: bool = False) -> _JsonDict | None:
    """Returns a dictionary containing data about the microscope state.

    Example::

        {'lastMeasurementError': '', 'microscopeState': 'Off'}

    :param ws: FemtoAPI client
    :param required: raise exception on failure
    :return: JSON ``dict``
    """
    command = 'FemtoAPIMicroscope.getMicroscopeState()'
    cmd_result = _execute_command(ws, command, required)
    return json.loads(cmd_result) if cmd_result else None


def getAcquisitionState(ws: _pfa.APIWebSocketClient, required: bool = False) -> _JsonDict | None:
    """Returns a dictionary containing all data about the processing state.

    .. note::
        Only input channels metadata information are get with this command,
        the output channel informations and much more regarding used waveforms,
        patterns, etc. can be get with the :func:`getActiveProtocol` command.

    :param ws: FemtoAPI client
    :param required: raise exception on failure
    :return: JSON ``dict``
    """
    command = 'FemtoAPIMicroscope.getAcquisitionState()'
    cmd_result = _execute_command(ws, command, required)
    return json.loads(cmd_result) if cmd_result else None


def startGalvoScanSnapAsync(ws: _pfa.APIWebSocketClient, required: bool = False) -> bool:
    """Starts a galvo XY scan snap asynchronously.

    :param ws: FemtoAPI client
    :param required: raise exception on failure
    :return: success
    """
    command = 'FemtoAPIMicroscope.startGalvoScanSnapAsync()'
    return not not _execute_command(ws, command, required)


def startGalvoScanAsync(ws: _pfa.APIWebSocketClient, required: bool = False) -> bool:
    """Starts a galvo XY scan asynchronously.

    :param ws: FemtoAPI client
    :param required: raise exception on failure
    :return: success
    """
    command = 'FemtoAPIMicroscope.startGalvoScanAsync()'
    return not not _execute_command(ws, command, required)


def stopGalvoScanAsync(ws: _pfa.APIWebSocketClient, required: bool = False) -> bool:
    """Stops a galvo XY scan asynchronously.

    :param ws: FemtoAPI client
    :param required: raise exception on failure
    :return: success
    """
    command = 'FemtoAPIMicroscope.stopGalvoScanAsync()'
    return not not _execute_command(ws, command, required)


def startResonantScanSnapAsync(ws: _pfa.APIWebSocketClient, required: bool = False) -> bool:
    """Starts a resonant scan snap asynchronously.

    :param ws: FemtoAPI client
    :param required: raise exception on failure
    :return: success
    """
    command = 'FemtoAPIMicroscope.startResonantScanSnapAsync()'
    return not not _execute_command(ws, command, required)


def startResonantScanAsync(ws: _pfa.APIWebSocketClient, required: bool = False) -> bool:
    """Starts a resonant scan asynchronously.

    :param ws: FemtoAPI client
    :param required: raise exception on failure
    :return: success
    """
    command = 'FemtoAPIMicroscope.startResonantScanAsync()'
    return not not _execute_command(ws, command, required)
    

def stopResonantScanAsync(ws: _pfa.APIWebSocketClient, required: bool = False) -> bool:
    """Stops a resonant scan asynchronously.

    :param ws: FemtoAPI client
    :param required: raise exception on failure
    :return: success
    """
    command = 'FemtoAPIMicroscope.stopResonantScanAsync()'
    return not not _execute_command(ws, command, required)


def createNewFile(ws: _pfa.APIWebSocketClient, required: bool = False) -> _JsonDict | None:
    """Creates a new, unnamed file, and sets it as the current file
    (i.e., the file where new measurements are placed).

    :param ws: FemtoAPI client
    :param required: raise exception on failure
    :return: JSON ``dict`` with keys ``'id'`` and ``'succeeded'``
    """
    command = 'FemtoAPIFile.createNewFile()'
    cmd_result = _execute_command(ws, command, required)
    return json.loads(cmd_result) if cmd_result else None


def saveFileAsync(
        ws: _pfa.APIWebSocketClient,
        handle: str | int = '',
        required: bool = False
) -> _JsonDict | None:
    """Save the current file or the file defined by handle.

    :param ws: FemtoAPI client
    :param handle: file handle
    :param required: raise exception on failure
    :return: JSON ``dict`` with keys ``'id'`` and ``'succeeded'``
    """
    command = f"FemtoAPIFile.saveFileAsync('{handle}')"
    cmd_result = _execute_command(ws, command, required)
    return json.loads(cmd_result) if cmd_result else None


def saveFileAsAsync(
        ws: _pfa.APIWebSocketClient,
        filePath: str,
        handle: str | int = '',
        overwrite: _JsBool = 'false',
        required: bool = False
) -> _JsonDict | None:
    """Save the current file as ``filepath`` or the file defined by ``handle``
    if given.

    :param ws: FemtoAPI client
    :param filePath: absolute path with forward slashes (``/``) only
    :param handle: file handle
    :param overwrite: ``'true'`` or ``'false'``
    :param required: raise exception on failure
    :return: JSON ``dict`` with keys ``'id'`` and ``'succeeded'``
    """
    command = f"FemtoAPIFile.saveFileAsAsync('{filePath}', '{handle}', {overwrite})"
    cmd_result = _execute_command(ws, command, required)
    return json.loads(cmd_result) if cmd_result else None
    

def closeFileNoSaveAsync(
        ws: _pfa.APIWebSocketClient,
        handle: str | int = '',
        required: bool = False
) -> _JsonDict | None:
    """Close the current file without saving or the file defined by ``handle``
    if given.

    :param ws: FemtoAPI client
    :param handle: file handle
    :param required: raise exception on failure
    :return: JSON ``dict`` with keys ``'id'`` and ``'succeeded'``
    """
    command = f"FemtoAPIFile.closeFileNoSaveAsync('{handle}')"
    cmd_result = _execute_command(ws, command, required)
    return json.loads(cmd_result) if cmd_result else None


def closeFileAndSaveAsync(
        ws: _pfa.APIWebSocketClient,
        handle: str = '',
        compress: _JsBool = 'false',
        required: bool = False
) -> _JsonDict | None:
    """Save and close the current file without saving or the file defined by
    ``handle`` if given.

    :param ws: FemtoAPI client
    :param handle: file handle
    :param compress: whether the file should be compressed if possible.
        ``'true'`` or ``'false'``
    :param required: raise exception on failure
    :return: JSON ``dict`` with keys ``'id'`` and ``'succeeded'``
    """
    command = f"FemtoAPIFile.closeFileAndSaveAsync('{handle}', '{handle}', {compress})"
    cmd_result = _execute_command(ws, command, required)
    return json.loads(cmd_result) if cmd_result else None


def closeFileAndSaveAsAsync(
        ws: _pfa.APIWebSocketClient,
        filePath: str,
        handle: str = '',
        overwrite: _JsBool = 'false',
        compress: _JsBool = 'false',
        required: bool = False
) -> _JsonDict | None:
    """Save the current file as ``filepath`` or the file defined by ``handle``
    if given and close it.

    :param ws: FemtoAPI client
    :param filePath: absolute path with forward slashes (``/``) only
    :param handle: file handle
    :param overwrite: ``'true'`` or ``'false'``
    :param compress: whether the file should be compressed if possible.
        ``'true'`` or ``'false'``
    :param required: raise exception on failure
    :return: JSON ``dict`` with keys ``'id'`` and ``'succeeded'``
    """
    command = f"FemtoAPIFile.closeFileAndSaveAsAsync('{filePath}', '{handle}', {overwrite}, {compress})"
    cmd_result = _execute_command(ws, command, required)
    return json.loads(cmd_result) if cmd_result else None


def openFilesAsync(
        ws: _pfa.APIWebSocketClient,
        filePath: str,
        required: bool = False
) -> _JsonDict | None:
    """Opens one or more file(s) asynchronously.

    :param ws: FemtoAPI client
    :param filePath:  one or more full file path(s) in one unicode string(s),
        separated with semicolon within the string
    :param required: raise exception on failure
    :return: JSON ``dict`` with keys ``'id'`` and ``'succeeded'``
    """
    command = f"FemtoAPIFile.openFilesAsync('{filePath}')"
    cmd_result = _execute_command(ws, command, required)
    return json.loads(cmd_result) if cmd_result else None

    
def getImagingWindowParameters(
        ws: _pfa.APIWebSocketClient,
        mType: str = '',
        spaceName: str = '',
        required: bool = False
) -> _JsonDict | None:
    """Returns a dictionary containing data about the imaging window parameters
    the function will only return data about the measurement type defined in
    ``mType`` or all if undefined.

    :param ws: FemtoAPI client
    :param mType: ``'resonant'``, ``'galvo'``, or ``''``, in the latter case,
        both types are considered.
    :param spaceName: space name as string, if empty string is given,
        default space (``'space1'``) is considered.
    :param required: raise exception on failure
    :return: JSON ``dict`` with the following keys:

        * ``rotationQuaternion``
        * ``resolutionXLimits``
        * ``resolutionYLimits``

    """
    command = (f"FemtoAPIMicroscope.getImagingWindowParameters('{mType}', '{spaceName}')")
    cmd_result = _execute_command(ws, command, required)
    return json.loads(cmd_result) if cmd_result else None


def setImagingWindowParameters(
        ws: _pfa.APIWebSocketClient,
        jsonString: str,
        required: bool = False
) -> bool:
    """The input json format restrictions can be found in the function
    description on the FemtoAPI knowledgebase [1]_.

    :param ws: FemtoAPI client
    :param jsonString: JSON string with keys:

        * ``space``
        * ``measurementType``
        * ``resolution``
        * ``size``
        * ``transformation``

    :param required: raise exception on failure
    :return: success
    """
    command = f"FemtoAPIMicroscope.setImagingWindowParameters('{jsonString}')"
    return not not _execute_command(ws, command, required)


def getZStackLaserIntensityProfile(
        ws: _pfa.APIWebSocketClient,
        mType: str = '',
        spaceName: str = '',
        required: bool = False
) -> list[_JsonDict] | None:
    """Gets the Z-stack depth correction profile.

    :param ws: FemtoAPI client
    :param mType: defines the measurement type (resonant, galvo), all types if
        undefined
    :param spaceName: space name as string, if empty string is given,
        default space (``'space1'``) is considered.
    :param required: raise exception on failure
    :return: JSON ``list``
    """
    command = f"FemtoAPIMicroscope.getZStackLaserIntensityProfile('{mType}', '{spaceName}')"
    cmd_result = _execute_command(ws, command, required)
    return json.loads(cmd_result) if cmd_result else None


def setZStackLaserIntensityProfile(
        ws: _pfa.APIWebSocketClient,
        jsonString: str,
        required: bool = False
) -> bool:
    """The input json format restrictions can be found in the function
    description on the FemtoAPI knowledgebase [2]_.

    :param ws: FemtoAPI client
    :param jsonString: JSON array
    :param required: raise exception on failure
    :return: success
    """
    command = f"FemtoAPIMicroscope.setZStackLaserIntensityProfile('{jsonString}')"
    return not not _execute_command(ws, command, required)


def getAxisPositions(ws: _pfa.APIWebSocketClient, required: bool = False) -> list[_JsonDict] | None:
    """Get positions for all the axes.

    :param ws: FemtoAPI client
    :param required: raise exception on failure
    :return: JSON ``list``
    """
    command = "FemtoAPIMicroscope.getAxisPositions()"
    cmd_result = _execute_command(ws, command, required)
    return json.loads(cmd_result) if cmd_result else None


def getAxisPosition(
        ws: _pfa.APIWebSocketClient,
        axisName: str,
        posType: str = '',
        space: str = '',
        required: bool = False
) -> _JsonDict | None:
    """Get position of one specific axis.

    :param ws: FemtoAPI client
    :param axisName: name of a valid and configured axis
    :param posType:
    :param space: must be the name of the space for which the axis given by
        ``axisName`` is configured
    :param required: raise exception on failure
    :return: JSON ``dict``
    """
    command = f"FemtoAPIMicroscope.getAxisPosition('{axisName}', '{posType}', '{space}')"
    cmd_result = _execute_command(ws, command, required)
    return json.loads(cmd_result) if cmd_result else None


def isAxisMoving(
        ws: _pfa.APIWebSocketClient,
        axisName: str,
        required: bool = False
) -> bool:
    """Returns whether the objective is moving along the given axis.

    :param ws: FemtoAPI client
    :param axisName: must be a configured axis name
    :param required: raise exception on failure
    """
    command = f"FemtoAPIMicroscope.isAxisMoving('{axisName}')"
    return not not _execute_command(ws, command, required)


def doZero(
        ws: _pfa.APIWebSocketClient,
        axisName: str,
        spaceName: str = '',
        required: bool = False
) -> bool:
    """Used to set the axis relative position to 0.0, and set the
    labeling origin to the current absolute position.

    :param ws: FemtoAPI client
    :param axisName: must be configured axis name
    :param spaceName: must be the name of the space for which the axis given by
        ``axisName`` is configured
    :param required: raise exception on failure
    :return: success
    """
    command = f"FemtoAPIMicroscope.doZero('{axisName}', '{spaceName}')"
    return not not _execute_command(ws, command, required)


def setAxisPosition(
        ws: _pfa.APIWebSocketClient,
        axisName: str,
        newPosition: float,
        isRelativePosition: _JsBool = 'true',
        isRelativeToCurrentPosition: _JsBool = 'true',
        spaceName: str = '',
        required: bool = False
) -> bool:
    """Set an absolute or relative position of a configured axis.
    Only one axis can be set at once.

    :param ws: FemtoAPI client
    :param axisName: must be configured axis name
    :param newPosition: must be within the axis and threshold limits
    :param isRelativePosition: the given position is relative, otherwise it is
        considered as an absolute position
    :param isRelativeToCurrentPosition: the newPosition parameter means a
        relative position to the current position, otherwise it is relative
        to the labeling origin offset
    :param spaceName: empty string means default namespace
    :param required: raise exception on failure
    :return: success
    """
    command = (f"FemtoAPIMicroscope.setAxisPosition('{axisName}', {newPosition}, "
               f"{isRelativePosition}, {isRelativeToCurrentPosition}, '{spaceName}')")
    return not not _execute_command(ws, command, required)


def getPMTAndLaserIntensityDeviceValues(
        ws: _pfa.APIWebSocketClient,
        required: bool = False
) -> _JsonDict | None:
    """Returns a dictionary containing PMT/Laser intensity device values.

    :param ws: FemtoAPI client
    :param required: raise exception on failure
    :return: JSON ``dict``
    """
    command = 'FemtoAPIMicroscope.getPMTAndLaserIntensityDeviceValues()'
    cmd_result = _execute_command(ws, command, required)
    return json.loads(cmd_result) if cmd_result else None
    

def setPMTAndLaserIntensityDeviceValues(
        ws: _pfa.APIWebSocketClient,
        jsonString: str,
        required: bool = False
) -> bool:
    """The input json format restrictions can be found in the function
    description on the FemtoAPI knowledgebase [3]_.

    :param ws: FemtoAPI client
    :param jsonString: JSON array
    :param required: raise exception on failure
    :return: success
    """
    command = f"FemtoAPIMicroscope.setPMTAndLaserIntensityDeviceValues('{jsonString}')"
    return not not _execute_command(ws, command, required)


# TODO utolsó 3 paraméter változni fog!!!
def createTimeSeriesMUnit(
        ws: _pfa.APIWebSocketClient,
        xDim: int,
        yDim: int,
        taskXMLParameters: str,
        viewportJson: str,
        z0InMs: float = 0.0,
        zStepInMs: float = 1.0,
        zDimInitial: int = 1,
        required: bool = False
) -> _JsonDict | None:
    """Creates new measurement unit for galvo/resonant/AO fullframe scan
    time series measurement.

    :param ws: FemtoAPI client
    :param xDim: measurement image x resolution
    :param yDim: measurement image y resolution
    :param taskXMLParameters: previously measurementParamsXML for
        resonant/galvo/AO fullframe scan time series measurement.
        In MESc version 4.5 taskXMLParameters is replaced by a single string
        containing the scanning mode: ``'galvo'``, ``'resonant'``, ``'AO'``
    :param viewportJson: viewport for measurement
    :param z0InMs: Measurement start time offset in ms.
    :param zStepInMs: Frame duration time in ms (1/frame rate). Positive double
    :param zDimInitial: Number of frames to create in z dimension. Positive integer
    :param required: raise exception on failure
    :return: JSON ``dict`` with keys:

        * ``succeeded``
        * ``id``
        * ``addedMUnitIdx``
    """
    command = (f"FemtoAPIFile.createTimeSeriesMUnit({xDim}, {yDim}, '{taskXMLParameters}', "
               f"'{viewportJson}', {z0InMs}, {zStepInMs}, {zDimInitial})")
    cmd_result = _execute_command(ws, command, required)
    return json.loads(cmd_result) if cmd_result else None


def createZStackMUnit(
        ws: _pfa.APIWebSocketClient,
        xDim: int,
        yDim: int,
        zDim: int,
        taskXMLParameters: str,
        viewportJson: str,
        zStepInMicrons: float = 1.0,
        required: bool = False
) -> _JsonDict | None:
    """Creates a new Z-stack measurement unit.

    :param ws: FemtoAPI client
    :param xDim: measurement image x resolution
    :param yDim: measurement image y resolution
    :param zDim: number of Z planes
    :param taskXMLParameters: previously measurementParamsXML for
        resonant/galvo/AO fullframe scan time series measurement.
        In MESc version 4.5 taskXMLParameters is replaced by a single string
        containing the scanning mode: ``'galvo'``, ``'resonant'``, ``'AO'``
    :param viewportJson: viewport for measurement
    :param zStepInMicrons: Frame duration time in ms (1/frame rate). Positive double
    :param required: raise exception on failure
    :return: JSON ``dict`` with keys:

        * ``succeeded``
        * ``id``
        * ``addedMUnitIdx``
    """
    command = (f"FemtoAPIFile.createZStackMUnit({xDim}, {yDim}, {zDim}, '{taskXMLParameters}', "
               f"'{viewportJson}', {zStepInMicrons})")
    cmd_result = _execute_command(ws, command, required)
    return json.loads(cmd_result) if cmd_result else None


def createVolumeScanMUnit(
        ws: _pfa.APIWebSocketClient,
        xDim: int,
        yDim: int,
        zDim: int,
        tDim: int,
        technologyType: str,
        referenceViewportJson: str,
        required: bool = False
) -> _JsonDict | None:
    """Creates a new volume scan measurement unit.

    :param ws: FemtoAPI client
    :param xDim: measurement image x resolution
    :param yDim: measurement image y resolution
    :param zDim: number of Z planes
    :param tDim: number of frames to create
    :param technologyType: scanning mode, one of ``'galvo'``, ``'resonant'``, ``'AO'``
    :param referenceViewportJson: viewport for measurement
    :param required: raise exception on failure
    :return: JSON ``dict`` with keys:

        * ``succeeded``
        * ``id``
        * ``addedMUnitIdx``
    """
    command = (f"FemtoAPIFile.createVolumeScanMUnit({xDim}, {yDim}, {zDim}, {tDim}, "
               f"'{technologyType}', '{referenceViewportJson}')")
    cmd_result = _execute_command(ws, command, required)
    return json.loads(cmd_result) if cmd_result else None


def createMultiLayerMUnit(
        ws: _pfa.APIWebSocketClient,
        xDim: int,
        yDim: int,
        tDim: int,
        technologyType: str,
        referenceViewportJson: str,
        required: bool = False
) -> _JsonDict | None:
    """Creates a new multi-layer measurement unit.

    :param ws: FemtoAPI client
    :param xDim: measurement image x resolution
    :param yDim: measurement image y resolution
    :param tDim: number of frames to create
    :param technologyType: scanning mode, one of ``'galvo'``, ``'resonant'``, ``'AO'``
    :param referenceViewportJson: viewport for measurement
    :param required: raise exception on failure
    :return: JSON ``dict`` with keys:

        * ``succeeded``
        * ``id``
        * ``addedMUnitIdx``
    """
    command = (f"FemtoAPIFile.createMultiLayerMUnit({xDim}, {yDim}, {tDim}, "
               f"'{technologyType}', '{referenceViewportJson}')")
    cmd_result = _execute_command(ws, command, required)
    return json.loads(cmd_result) if cmd_result else None


# TODO utolsó 3 paraméter változni fog!!!
def createBackgroundFrame(
        ws: _pfa.APIWebSocketClient,
        xDim: int,
        yDim: int,
        technologyType: str,
        viewportJson: str,
        fileNodeDescriptor: str = '',
        z0InMs: float = 0.0,
        zStepInMs: float = 1.0,
        zDimInitial: int = 1,
        required: bool = False
) -> _JsonDict | None:
    """Creates new measurement session and a time series measurement unit in it
    with the specified technology type, and adds one (or optionally more)
    frame to it. This measurement session is special: it cannot be target of
    new measurements, and only multiROI images can be created in it.

    :param ws: FemtoAPI client
    :param xDim: measurement image x resolution
    :param yDim: measurement image y resolution
    :param technologyType: string, means the used technology for imaging,
        it can be ``'resonant'``, ``'galvo'``, or ``'AO'``.
    :param viewportJson: viewport for measurement.
    :param fileNodeDescriptor: string, descriptor of the file node in the MESc GUI,
        in which the new background session and unit will be created.
        If it is not given or empty string, current file is considered.
    :param z0InMs: Measurement start time offset in ms
    :param zStepInMs: Frame duration time in ms (1/frame rate). Positive double
    :param zDimInitial: Number of frames to create in z (time) dimension.
        Positive integer
    :param required: raise exception on failure
    :return: JSON ``dict``,
        e.g.::

            {'addedMUnitIdx': '11,1,0',
             'backgroundImagePath': '/MSession_1/MUnit_0',
             'id': '{aaa7bcbd-db5b-4b64-884b-da6c25a3f74a}',
             'succeeded': True}
    """
    command = (f"FemtoAPIFile.createBackgroundFrame({xDim}, {yDim}, '{technologyType}', "
               f"'{viewportJson}', '{fileNodeDescriptor}', {z0InMs}, {zStepInMs}, {zDimInitial})")
    cmd_result = _execute_command(ws, command, required)
    return json.loads(cmd_result) if cmd_result else None


def createBackgroundZStack(
        ws: _pfa.APIWebSocketClient,
        xDim: int,
        yDim: int,
        zDim: int,
        technologyType: str,
        viewportJson: str,
        fileNodeDescriptor: str = '',
        zStepInMicrons: float = 1.0,
        required: bool = False
) -> _JsonDict | None:
    """Creates new measurement session and a z-stack series measurement unit.

    :param ws: FemtoAPI client
    :param xDim: measurement image x resolution
    :param yDim: measurement image y resolution
    :param zDim: number of z planes
    :param technologyType: string, means the used technology for imaging,
        it can be ``'resonant'``, ``'galvo'``, or ``'AO'``.
    :param viewportJson: viewport for measurement.
    :param fileNodeDescriptor: string, descriptor of the file node in the MESc GUI,
        in which the new background session and unit will be created.
        If it is not given or empty string, current file is considered.
    :param zStepInMicrons: Step between z planes in um
    :param required: raise exception on failure
    :return: JSON ``dict``,
        e.g.::

            {'addedMUnitIdx': '11,1,1',
             'backgroundImagePath': '/MSession_1/MUnit_1',
             'id': '{7f3d629f-59f0-4a06-a5d6-6eb46bec9002}',
             'succeeded': True}
    """
    command = (f"FemtoAPIFile.createBackgroundZStack({xDim}, {yDim}, {zDim}, " 
               f"'{technologyType}', '{viewportJson}', '{fileNodeDescriptor}', {zStepInMicrons})")
    cmd_result = _execute_command(ws, command, required)
    return json.loads(cmd_result) if cmd_result else None


def createMultiROI2DMUnit(
        ws: _pfa.APIWebSocketClient,
        xDim: int,
        tDim: int,
        methodType: str,
        backgroundImagePath: str,
        deltaTInMs: float = 1.0,
        t0InMs: float = 0.0,
        required: bool = False
) -> _JsonDict | None:
    """Creates new MultiROI measurement unit.

    :param ws: FemtoAPI client
    :param xDim: measurement image x resolution
    :param tDim: number of timestamps
    :param methodType: 2D multiROI type, it can be ``'multiROIPointScan'``,
        ``'multiROILineScan'``, or ``'multiROIMultiLine'``
    :param backgroundImagePath: path of background image in the file
        (e.g. ``/MSession_0/MUnit_0`` )
    :param deltaTInMs: Frame duration time in ms (1/frame rate). Positive double
    :param t0InMs: Measurement start time offset in ms
    :param required: raise exception on failure
    :return: JSON ``dict``,
        e.g.::

            {'addedMUnitIdx': '11,1,1',
             'id': '{7f3d629f-59f0-4a06-a5d6-6eb46bec9002}',
             'succeeded': True}
    """
    command = (f"FemtoAPIFile.createMultiROI2DMUnit({xDim}, {tDim}, '{methodType}', "
               f"'{backgroundImagePath}', {deltaTInMs}, {t0InMs})")
    cmd_result = _execute_command(ws, command, required)
    return json.loads(cmd_result) if cmd_result else None


def createMultiROI3DMUnit(
        ws: _pfa.APIWebSocketClient,
        xDim: int,
        yDim: int,
        tDim: int,
        methodType: str,
        backgroundImagePath: str,
        deltaTInMs: float = 1.0,
        t0InMs: float = 0.0,
        required: bool = False
) -> _JsonDict | None:
    """Creates new MultiROI measurement unit.

    :param ws: FemtoAPI client
    :param xDim: measurement image x resolution
    :param yDim: measurement image y resolution
    :param tDim: number of timestamps
    :param methodType: 3D multiROI type, it can be ``'multiROIChessBoard'``,
        ``'multiROITransverseRibbonScan'``, ``'multiROILongitudinalRibbonScan'``
    :param backgroundImagePath: path of background image in the file
        (e.g. ``/MSession_0/MUnit_0``)
    :param deltaTInMs: Frame duration time in ms (1/frame rate). Positive double
    :param t0InMs: Measurement start time offset in ms
    :param required: raise exception on failure
    :return: JSON ``dict``,
        e.g.::

             {'addedMUnitIdx': '11,1,1',
             'id': '{7f3d629f-59f0-4a06-a5d6-6eb46bec9002}',
             'succeeded': True}
    """
    command = (f"FemtoAPIFile.createMultiROI3DMUnit({xDim}, {yDim}, {tDim}, "
               f"'{methodType}', '{backgroundImagePath}', {deltaTInMs}, {t0InMs})")
    cmd_result = _execute_command(ws, command, required)
    return json.loads(cmd_result) if cmd_result else None

    
def createMultiROI4DMUnit(
        ws: _pfa.APIWebSocketClient,
        xDim: int,
        yDim: int,
        zDim: int,
        tDim: int,
        methodType: str,
        backgroundImagePath: str,
        deltaTInMs: float = 1.0,
        t0InMs: float = 0.0,
        required: bool = False
) -> _JsonDict | None:
    """Creates new MultiROI measurement unit.

    :param ws: FemtoAPI client
    :param xDim: measurement image x resolution
    :param yDim: measurement image y resolution
    :param zDim: measurement image z resolution
    :param tDim: number of timestamps
    :param methodType: 4D multiROI type, it can be ``'multiROIMultiCube'``,
        ``'multiROISnake'``
    :param backgroundImagePath: path of background image in the file
        (e.g. ``/MSession_0/MUnit_0``)
    :param deltaTInMs: Frame duration time in ms (1/frame rate). Positive double
    :param t0InMs: Measurement start time offset in ms
    :param required: raise exception on failure
    :return: JSON ``dict``,
        e.g.::

             {'addedMUnitIdx': '11,1,1',
             'id': '{7f3d629f-59f0-4a06-a5d6-6eb46bec9002}',
             'succeeded': True}
    """
    command = (f"FemtoAPIFile.createMultiROI4DMUnit({xDim}, {yDim}, {zDim}, {tDim}, "
               f"'{methodType}', '{backgroundImagePath}', {deltaTInMs}, {t0InMs})")
    cmd_result = _execute_command(ws, command, required)
    return json.loads(cmd_result) if cmd_result else None
    

def extendMUnit(
        ws: _pfa.APIWebSocketClient,
        mUnitHandle: str,
        countDims: str,
        required: bool = False
) -> _JsonDict | None:
    """Extends a measurement unit given by ``mUnitHandle`` with the number of
    frames ``countDims``.

    :param ws: FemtoAPI client
    :param mUnitHandle: unique index of a measurement unit converted to string,
        e.g. '23,0,1'.
    :param countDims: number of frames to extend the measurement unit with
    :param required: raise exception on failure
    :return: JSON ``dict``,
        e.g.::

            {'id': '{683fa0e8-0c55-4e1b-8854-7150cd2db42d}', 'succeeded': True}
    """
    command = f"FemtoAPIFile.extendMUnit('{mUnitHandle}', {countDims})"
    cmd_result = _execute_command(ws, command, required)
    return json.loads(cmd_result) if cmd_result else None


def deleteMUnit(
        ws: _pfa.APIWebSocketClient,
        mUnitHandle: str,
        required: bool = False
) -> _JsonDict | None:
    """Deletes a measurement unit from a .mesc file.

    :param ws: FemtoAPI client
    :param mUnitHandle: unit handle in format e.g. ``'23,0,1``
    :param required: raise exception on failure
    :return: JSON ``dict``,
        e.g.::

            {'deletedMUnitIdx': '11,0,3',
             'id': '{c808840f-882c-4b6a-8d8b-fc34120f3a92}',
             'succeeded': True}
    """
    command = f"FemtoAPIFile.deleteMUnit('{mUnitHandle}')"
    cmd_result = _execute_command(ws, command, required)
    return json.loads(cmd_result) if cmd_result else None


def copyMUnit(
        ws: _pfa.APIWebSocketClient,
        sourceMUnitHandle: str,
        destMSessionHandle: str,
        bCopyChannelContents: _JsBool = 'true',
        required: bool = False
) -> _JsonDict | None:
    """Copies the source measurement unit to the requested measurement session
    (or group).

    :param ws: FemtoAPI client
    :param sourceMUnitHandle: is the measurementunit handle of the source
    :param destMSessionHandle: is the session handle of the destination
    :param bCopyChannelContents: if true, channel contents of measurement unit
        will be copied too. Otherwise, channel data values are 0.
    :param required: raise exception on failure
    :return: JSON ``dict``,
        e.g.::

            {'copiedMUnitIdx': '11,0,4', 'id': '{4c4bb735-85dd-4c03-9f10-fd3a440f8a65}', 'succeeded': True}
    """
    command = (f"FemtoAPIFile.copyMUnit('{sourceMUnitHandle}', "
               f"'{destMSessionHandle}', {bCopyChannelContents})")
    cmd_result = _execute_command(ws, command, required)
    return json.loads(cmd_result) if cmd_result else None


def moveMUnit(
        ws: _pfa.APIWebSocketClient,
        sourceMUnitHandle: str,
        destMSessionHandle: str,
        required: bool = False
) -> _JsonDict | None:
    """Moves the source measurement unit to the requested measurement session
    (or group).  The content of the channels always moved.

    :param ws: FemtoAPI client
    :param sourceMUnitHandle: is the measurementunit handle of the source
    :param destMSessionHandle: is the sessionhandle of the destination
    :param required: raise exception on failure
    :return: JSON ``dict``,
        e.g.::

            {'id': '{be390ea7-e6a6-4c55-9584-61b77b9b66ff}', 'movedMUnitIdx': '11,0,5', 'succeeded': True}
    """
    command = f"FemtoAPIFile.moveMUnit('{sourceMUnitHandle}', '{destMSessionHandle}')"
    cmd_result = _execute_command(ws, command, required)
    return json.loads(cmd_result) if cmd_result else None

    
def addChannel(
        ws: _pfa.APIWebSocketClient,
        mUnitHandle: str,
        channelName: str | int,
        compressionPreset: int = 0,
        required: bool = False
) -> _JsonDict | None:
    """Adds a new channel to the measurement unit with the given channel name.

    :param ws: FemtoAPI client
    :param mUnitHandle: unit handle, e.g. ``'23,1,1'``
    :param channelName: channel name
    :param compressionPreset: Compression preset value (integer).
        Currently available presets:

        * 0=NoCompression
        * 1=Preset1: ZLib, compression level=2
        * 2=Preset2: ZLib, compression level=9
        * 3=Preset3: BLOSC
        * 4=Preset4: SZip
    :param required: raise exception on failure
    :return: JSON ``dict``,
        e.g.::

            {'addedChannelIdx': '11,0,1,0',
             'id': '{568dfe0c-b2a8-428c-b84c-b9d27515cbf8}',
             'succeeded': True}
    """
    command = f"FemtoAPIFile.addChannel('{mUnitHandle}', '{channelName}', '{compressionPreset}')"
    cmd_result = _execute_command(ws, command, required)
    return json.loads(cmd_result) if cmd_result else None


def deleteChannel(
        ws: _pfa.APIWebSocketClient,
        channelHandle: str,
        required: bool = False
) -> _JsonDict | None:
    """Removes the specified channel.

    :param ws: FemtoAPI client
    :param channelHandle: channel handle, e.g. ``'23,0,0,0'``
    :param required: raise exception on failure
    :return: JSON ``dict``,
        e.g.::

            {'id': '{99e0895d-d7b7-4125-8497-f8458994b893}', 'succeeded': True}
    """
    command = f"FemtoAPIFile.deleteChannel('{channelHandle}')"
    cmd_result = _execute_command(ws, command, required)
    return json.loads(cmd_result) if cmd_result else None


def addLastFrameToMSession(
        ws: _pfa.APIWebSocketClient,
        destMSessionHandle: str = '',
        space: str = '',
        required: bool = False
) -> str | None:
    """Creates a new MUnit in the given MSession, and adds the frame on the
    immediate window (last frame of a measurement/live or snap) to it.

    :param ws: FemtoAPI client
    :param destMSessionHandle: session handle, e.g. ``'23,0'``
    :param space: space name
    :param required: raise exception on failure
    :return: node descriptor of the created measurement unit containing the immediate image
    """
    command = f"FemtoAPIFile.addLastFrameToMSession('{destMSessionHandle}', '{space}')"
    return _execute_command(ws, command, required)


def sendFileToClientsBlob(
        ws: _pfa.APIWebSocketClient,
        sPathAndFileName: str,
        required: bool = False
) -> int | None:
    """Sends file.

    :param ws: FemtoAPI client
    :param sPathAndFileName: full path
    :param required: raise exception on failure
    :return: the file size if file found, None if filepath is not valid
    """
    command = f"FemtoAPIFile.sendFileToClientsBlob('{sPathAndFileName}')"
    return _execute_command(ws, command, required)


def saveAttachmentToFile(
        ws: _pfa.APIWebSocketClient,
        sPathAndFileName: str,
        required: bool = False
) -> bool:
    """If there is data attached to the websocket session it is gonna be saved
    as the given file.
    :func:`APIWebSocketClient.uploadAttachment` function can be used for
    ataching data to the websocket session.
    No data means empty file.
    """
    command = f"FemtoAPIFile.saveAttachmentToFile('{sPathAndFileName}')"
    cmd_result = _execute_command(ws, command, required)
    return cmd_result is not None

    
def modifyConversion(
        ws: _pfa.APIWebSocketClient,
        sConversionName: str,
        dScale: float,
        dOffset: float,
        bSave: _JsBool = 'false',
        required: bool = False
) -> bool:
    """Modifies conversion in MESc conversion manager to the given value,
    which can be saved to file if requested.

    :param ws: FemtoAPI client
    :param sConversionName: name of the conversion, as it can be seen
        in MESc conversion manager.
    :param dScale: the new scale to set
    :param dOffset: the new offset to set
    :param bSave: if true, the conversion is saved to disk if it has been modified.
        Otherwise, the specified conversion modified only in memory.
    :param required: raise exception on failure
    :return: success
    """
    command = (f"FemtoAPIFile.modifyConversion('{sConversionName}', '{dScale}', "
               f"'{dOffset}', {bSave})")
    return not not _execute_command(ws, command, required)


def saveVarToFile(
        ws: _pfa.APIWebSocketClient,
        jsValue: _t.Any,
        pathAndFileName: str,
        required: bool = False
) -> int | None:
    command = f"FemtoAPIFile.saveVarToFile({jsValue}, '{pathAndFileName}')"
    log_command(command)
    return _execute_command(ws, command, required)
    

def getStatus(
        ws: _pfa.APIWebSocketClient,
        sCommandID: str | None = None,
        required: bool = False
) -> _JsonDict | None:
    """If ``sCommand`` is defined the function will get the status of the
    assyncronous file operation represented by the given ID. **not tested**

    If ``sCommand`` is not given the function will return information about
    the currently opened files.

    :param ws: FemtoAPI client
    :param sCommandID: command ID from file operation return value
    :param required: raise exception on failure
    :return: JSON ``dict``,

        e.g.::

            {'lastFileOpenError': {'commandID': '', 'error': []}, 'openedFilesStatus': []}
    """
    if sCommandID:
        command = f"FemtoAPIFile.getStatus('{sCommandID}')"
    else:
        command = f"FemtoAPIFile.getStatus()"
    cmd_result = _execute_command(ws, command, required)
    return json.loads(cmd_result) if cmd_result else None
    

def curveInfo(
        ws: _pfa.APIWebSocketClient,
        mUnitHandle: str,
        curveIdx: int,
        required: bool = False
) -> _JsonDict | None:
    """Returns information about the selected curve

    :param ws: FemtoAPI client
    :param mUnitHandle: unit handle, e.g. ``'23,1,1'``
    :param curveIdx: curve index
    :param required: raise exception on failure
    :return: see :func:`writeCurve`
    """
    command = f"FemtoAPIFile.curveInfo('{mUnitHandle}', '{curveIdx}')"
    cmd_result = _execute_command(ws, command, required)
    return json.loads(cmd_result) if cmd_result else None


def readCurve(
        ws: _pfa.APIWebSocketClient,
        mUnitHandle: str,
        curveIdx: int,
        vectorFormat: _OptionalJsBool = '',
        forceDouble: _OptionalJsBool = '',
        required: bool = False
) -> _JsonDict | None:
    """Reads a curve and returns curve data as attachment.

    :param ws: FemtoAPI client
    :param mUnitHandle: unit handle, e.g. ``'23,1,1'``
    :param curveIdx: curve index
    :param vectorFormat: ``'true'``, ``'false'`` or ``''``.
        If ``'true'``, the RLE and equidistant curve data is extracted to
        vectors.
    :param forceDouble: ``'true'``, ``'false'`` or ``''``.
        If ``'true'``, the uint16 output data samples are converted to double
        samples.
    :param required: raise exception on failure
    :return: a dictionary with 2 elements

    ``'Result'``
        contains data about the specified curve
    ``'BinaryData'``
        a dictionary with 2 elements:
        - ``'xData'`` is a list with the x data of the curve
        - ``'yData'`` is a list with the y data of the curve
        the elements of these 2 list make up data pairs (xData[0] - yData[0], xData[1] - yData[1], etc.)
    """
    command = (f"FemtoAPIFile.readCurve('{mUnitHandle}', '{curveIdx}', "
               f"'{vectorFormat}', '{forceDouble}')")
    log_command(command)
    simple_cmd_parser = ws.sendJSCommand(command)
    # log_debug(simple_cmd_parser.hasBinaryParts())
    result_code = simple_cmd_parser.getResultCode()
    if result_code > 0:
        message = simple_cmd_parser.getErrorText()
        log_error(f'Return code: {result_code}')
        log_error(message)
        if required:
            raise _e.FemtoApiWrapError(result_code, message)
        return None
    else:
        cmd_result = {}
        result = json.loads(simple_cmd_parser.getJSEngineResult())
        cmd_result.update({"Result": result})
        data_size = result['size']
        x_type = result['xType']
        y_type = result['yType']
        x_data_type = result['xDataType']
        y_data_type = result['yDataType']
        # SOMETHING NEEDS DOING

        x_data = []
        y_data = []
        curve_data = {"xData": x_data, "yData": y_data}

        raw_data = _qtc.QByteArray()
        for parts in simple_cmd_parser.getPartList():
            print(parts.size())
            raw_data.append(parts)

            if x_type == 'vector':
                x_size = data_size
            else:
                x_size = 2

            stream = _qtc.QDataStream(parts)
            stream.setByteOrder(_qtc.QDataStream.ByteOrder.LittleEndian)
            cntr = 0
            while not stream.atEnd():
                if cntr < x_size:
                    if x_data_type == 'double':
                        tmp_data = stream.readDouble()
                        curve_data["xData"].append(tmp_data)
                    else:
                        tmp_data = stream.readUInt16()
                        curve_data["xData"].append(tmp_data)
                else:
                    if y_type == 'rle':
                        if y_data_type == 'double':
                            # RLE esetén első minden páratlan sorszámú érték 32 bites
                            tmp_data = stream.readUInt32()
                            curve_data["yData"].append(tmp_data)
                            tmp_data = stream.readDouble()
                            curve_data["yData"].append(tmp_data)
                        else:
                            tmp_data = stream.readUInt32()
                            curve_data["yData"].append(tmp_data)
                            tmp_data = stream.readUInt16()
                            curve_data["yData"].append(tmp_data)
                    else:
                        if y_data_type == 'double':
                            tmp_data = stream.readDouble()
                            curve_data["yData"].append(tmp_data)
                        else:
                            tmp_data = stream.readUInt16()
                            curve_data["yData"].append(tmp_data)
                cntr += 1

        """
        for parts in simpleCmdParser.getPartList():
        size = int(parts.size() / 2)
        binaryDataX = QByteArray()
        binaryDataY = QByteArray()
        binaryDataX.append(parts[:size])
        binaryDataY.append(parts[size:])

        stream = QDataStream(binaryDataX)
        stream.setByteOrder(QDataStream.ByteOrder.LittleEndian)
        while not stream.atEnd():
            floatData = stream.readDouble()
            curveData["xData"].append(floatData) 
        stream = QDataStream(binaryDataY)
        stream.setByteOrder(QDataStream.ByteOrder.LittleEndian)
        while not stream.atEnd():
            floatData = stream.readDouble()
            curveData["yData"].append(floatData)
        print( "Binary part with size: " + str(parts.size()))
        """
        cmd_result.update({'CurveData': curve_data})
        return cmd_result

    
def deleteCurve(
        ws: _pfa.APIWebSocketClient,
        mUnitHandle: str,
        curveIdx: int,
        required: bool = False
) -> bool:
    """Deletes a curve.

    :param ws: FemtoAPI client
    :param mUnitHandle: unit handle, e.g. ``'23,1,1'``
    :param curveIdx: curve index
    :param required: raise exception on failure
    :return: success
    """
    command = f"FemtoAPIFile.deleteCurve('{mUnitHandle}', '{curveIdx}')"
    return not not _execute_command(ws, command, required)


# will change
def writeCurve(
        ws: _pfa.APIWebSocketClient,
        buffer: _qtc.QByteArray,
        mUnitHandle: str,
        size: int,
        name: str,
        xType: str,
        xDataType: str,
        yType: str,
        yDataType: str,
        optimize: _OptionalJsBool = '',
        required: bool = False
) -> _JsonDict | None:
    """Adds a new curve.

    Parameter info on Confluence -> API2.0 [4]_.

    :param ws: FemtoAPI client
    :param buffer: byte array containing the data
    :param mUnitHandle: unit handle, e.g. ``'23,1,1'``
    :param size: count of the samples (x=y) to insert to the new curve
    :param name: curve name
    :param xType: value can be one of the followings:
        ``'equidistant'``: input data is represented as equidistant values, i.e the first value and the step are provided
        ``'vector'``: input data is a vector of x values
    :param xDataType: value can be one of the followings:
        ``'double'``: input data is represented in IEEE 754 64-bit floating point type
        ``'uint16'``: input data is represented in 16-bit unsigned integers
    :param yType: value can be one of the followings:
        ``'rle'``: input data is run-length encoded, i.e pairs of repetition count and value are provided
        ``'vector'``: input data is a vector of y values
    :param yDataType: same as xDataType
    :param optimize: ``'true'``, ``'false'`` or ``''``,
        flags whether the provided data is wanted to be analyzed for possible
        compressions (encode x as equidistant or y as rle if it provides a
        smaller size)
    :param required: raise exception on failure
    :return: JSON ``dict`` containing ``'success'``
    """
    ws.uploadAttachment(buffer)
    command = (f"FemtoAPIFile.writeCurve('{mUnitHandle}', '{size}', '{name}', "
               f"'{xType}', '{xDataType}', '{yType}', '{yDataType}', '{optimize}')")
    cmd_result = _execute_command(ws, command, required)
    return json.loads(cmd_result) if cmd_result else None


# not working !! fix needed
def appendToCurve(
        ws: _pfa.APIWebSocketClient,
        buffer: _qtc.QByteArray,
        mUnitHandle: str,
        curveIdx: int,
        size: int,
        xType: str,
        xDataType: str,
        yType: str,
        yDataType: str,
        required: bool = False
) -> bool:
    """Appends data to a curve.

    See :func:`writeCurve` for parameters.

    :return: success
    """
    ws.uploadAttachment(buffer)
    command = (f"FemtoAPIFile.appendToCurve('{mUnitHandle}', '{curveIdx}', "
               f"'{size}', '{xType}', '{xDataType}', '{yType}', '{yDataType}')")
    log_command(command)
    return not not _execute_command(ws, command, required)


def getFocusingModes(
        ws: _pfa.APIWebSocketClient,
        spaceName: str = '',
        required: bool = False
) -> list[str] | None:
    """Gets the available (configured) focusing modes for the specified space
    in json array, as it can be seen in the MESc GUI.

    :param ws: FemtoAPI client
    :param spaceName: if empty, ``'space1'`` is considered
    :param required: raise exception on failure
    :return: list of focusing modes
    """
    command = f"FemtoAPIMicroscope.getFocusingModes('{spaceName}')"
    log_command(command)
    cmd_result = _execute_command(ws, command, required)
    return json.loads(cmd_result) if cmd_result else None

    
def setFocusingMode(
        ws: _pfa.APIWebSocketClient,
        sfocusingMode: str,
        spaceName: str = '',
        required: bool = False
) -> bool:
    """Switches to the given focusing mode ``focusingMode``, if it is valid.

    :param ws: FemtoAPI client
    :param sfocusingMode: valid values are obtained by the output of
        :func:`getFocusingModes` command
    :param spaceName: if empty, ``'space1'`` is considered
    :param required: raise exception on failure
    :return: success
    """
    command = f"FemtoAPIMicroscope.setFocusingMode('{sfocusingMode}', '{spaceName}')"
    return not not _execute_command(ws, command, required)


def getActiveProtocol(ws: _pfa.APIWebSocketClient, required: bool = False) -> _JsonDict | None:
    """Reads the active protocol.

    :param ws: FemtoAPI client
    :param required: raise exception on failure
    :return: JSON ``dict``
        containing:

            * currently active user waveforms, channels, and patterns
            * which waveform is currently set to be displayed on which channels
            * display order and timing of the waveforms
            * pattern metadata: path description, path order, cycle time, etc.

        e.g.::

            {'beginCut': 0, 'lastModified': '2022-08-01T09:31:09',
            'measurementLength': 0, 'modifiedBy': '', 'name': '',
            'protocolId': '', 'runtimeUniqueIndex': '', 'timelines': [],
            'version': ''}
    """
    command = 'FemtoAPIMicroscope.getActiveProtocol()'
    cmd_result = _execute_command(ws, command, required)
    return json.loads(cmd_result) if cmd_result else None


def setActiveTaskAndSubTask(
        ws: _pfa.APIWebSocketClient,
        taskName: str,
        subTaskName: str = 'timeSeries',
        required: bool = False
) -> bool:
    """Sets the given measurement task and subtask.

    :param ws: FemtoAPI client
    :param taskName: ``'resonant'`` or ``'galvo'``
    :param subTaskName: ``'timeSeries'``, ``'zStack'`` or ``'volumeScan'``
        If not given, timeseries measurement will be selected on the MESc GUI
        by default.
    :param required: raise exception on failure
    :return: success
    """
    command = f"FemtoAPIMicroscope.setActiveTaskAndSubTask( '{taskName}', '{subTaskName}')"
    return not not _execute_command(ws, command, required)


def getCommandSetVersion(ws: _pfa.APIWebSocketClient, required: bool = False) -> str:
    """Gets the version of the FemtoAPI API command set (Microscope namespace).

    :param ws: FemtoAPI client
    :param required: raise exception on failure
    :return: e.g. ``'2.0.0'``
    """
    command = 'FemtoAPIMicroscope.getCommandSetVersion()'
    return _execute_command(ws, command, required)


def getCommandSetVersionProcessing(ws: _pfa.APIWebSocketClient, required: bool = False) -> str:
    """Gets the version of the FemtoAPI API command set (File namespace).

    :param ws: FemtoAPI client
    :param required: raise exception on failure
    :return: e.g. ``'2.0.0'``
    """
    command = 'FemtoAPIFile.getCommandSetVersion()'
    return _execute_command(ws, command, required)


def getLastCommandError(ws: _pfa.APIWebSocketClient, required: bool = False) -> _JsonDict | None:
    """Gets the error information of the last issued command (Microscope namespace).

    :param ws: FemtoAPI client
    :param required: raise exception on failure
    :return: If no error happened, ``None``; otherwise a JSON ``dict`` with
        keys ``'errorCode'`` and ``'errorText'``.
    """
    command = 'FemtoAPIMicroscope.getLastCommandError()'
    simple_cmd_parser = ws.sendJSCommand(command)
    result_code = simple_cmd_parser.getResultCode()
    if result_code > 0:
        return {
            'errorCode': result_code,
            'errorText': simple_cmd_parser.getErrorText()
        }
    else:
        if required:
            raise _e.FemtoApiWrapError
        return None


def getLastCommandErrorProcessing(
        ws: _pfa.APIWebSocketClient,
        required: bool = False
) -> _JsonDict | None:
    """Gets the error information of the last issued command (File namespace).

    :param ws: FemtoAPI client
    :param required: raise exception on failure
    :return: If no error happened, ``None``; otherwise a JSON ``dict``,
        e.g.::

            {'errorCode': 17201,
             'errorText': 'Code: 17201. Measurement session item is invalid! Error type: eUnknownError'}
    """
    command = 'FemtoAPIFile.getLastCommandError()'
    simple_cmd_parser = ws.sendJSCommand(command)
    result_code = simple_cmd_parser.getResultCode()
    if result_code > 0:
        return {
            'errorCode': result_code,
            'errorText': simple_cmd_parser.getErrorText()
        }
    else:
        if required:
            raise _e.FemtoApiWrapError
        return None


def setMeasurementDuration(
        ws: _pfa.APIWebSocketClient,
        duration: float,
        taskName: str = '',
        spaceName: str = '',
        required: bool = False
) -> bool:
    """Sets measurement duration for the given task and space.

    :param ws: FemtoAPI client
    :param duration: measurement duration
    :param taskName: ``'resonant'``, ``'galvo'``, or ``''``
    :param spaceName: space name as string, if empty string is given,
        default space (``'space1'``) is considered.
    :param required: raise exception on failure
    :return: success
    """
    command = (f"FemtoAPIMicroscope.setMeasurementDuration({duration}, "
               f"'{taskName}', '{spaceName}')")
    return not not _execute_command(ws, command, required)


def readRawChannelDataToClientsBlob(
        ws: _pfa.APIWebSocketClient,
        handle: str,
        fromDims: str,
        countDims: str,
        filePath: str | None = None,
        required: bool = False
) -> _JsonDict | None:
    """Transfers raw binary data to the FemtoAPI client as a binary blob.

    :param ws: FemtoAPI client
    :param handle: channel handle, e.g. ``'52,0,1,1'``
    :param fromDims: a string enumerating the starting indices of a
        sub-hyperrectangle of a multidimensional data array.
        For example, in a 3-dimensional data array, '256,0,10' means index 256
        in the first dimension, index 0 in the second dimension, and index 10
        in the third dimension. Note that all indices are zero-based.
    :param countDims: a string enumerating the dimensions of a
        sub-hyperrectangle of a multidimensional data array.
        For example, in a three-dimensional data array, '512,512,10' means
        512 pixels in the first and second dimensions, and 10 frames in the
        third dimension.
    :param filePath: optional parameter, default ``None``.
        If defined, binary data will be writen in the given file, return value
        is ``True`` if successfull or ``False`` is failed
        If filePath not defined, binary data will be written in ``QByteArray``
        and put into the result.
    :param required: raise exception on failure
    :return: JSON ``dict``,
        e.g.::

            {'data': <QByteArray>,
            'result': {'size': [100, 200, 10],
                       'channelDataType': 'double'}}
    """
    command = (f"FemtoAPIFile.readRawChannelDataToClientsBlob('{handle}', "
               f"'{fromDims}', '{countDims}')")
    return _read_channel_data(ws, command, filePath, required)


def readChannelDataToClientsBlob(
        ws: _pfa.APIWebSocketClient,
        handle: str,
        fromDims: str,
        countDims: str,
        filePath: str | None = None,
        required: bool = False
) -> _JsonDict | None:
    """The converted binary data is transferred from the server to the FemtoAPI
    client as a binary blob.

    See :func:`readRawChannelDataToClientsBlob` for parameters and return value.
    """
    command = f"FemtoAPIFile.readChannelDataToClientsBlob('{handle}', '{fromDims}', '{countDims}')"
    return _read_channel_data(ws, command, filePath, required)


def _read_channel_data(
        ws: _pfa.APIWebSocketClient,
        command: str,
        file_path: str | None,
        required: bool = False
) -> _JsonDict | None:
    log_command(command)
    simple_cmd_parser = ws.sendJSCommand(command)
    result_code = simple_cmd_parser.getResultCode()
    if result_code > 0:
        message = simple_cmd_parser.getErrorText()
        log_error(f'Return code: {result_code}')
        log_error(message)
        if required:
            raise _e.FemtoApiWrapError(result_code, message)
        return None
    else:
        cmd_result = {}
        result = json.loads(simple_cmd_parser.getJSEngineResult())
        # log_debug ("readRawChannelDataToClientsBlob result: " + result)
        cmd_result.update({'result': result})
        if file_path:
            binary_data = _qtc.QByteArray()
            for parts in simple_cmd_parser.getPartList():
                binary_data.append(parts)
            # log_debug("Res type: " + str(type(binaryData)) + ", Res size: "  + str(binaryData.size()))
            tmp = binary_data.data()
            with open(file_path, 'wb') as f:
                f.write(tmp)
            return cmd_result
        else:
            binary_data = _qtc.QByteArray()
            for parts in simple_cmd_parser.getPartList():
                binary_data.append(parts)
                # log_debug( "Binary part sizes: " + str(parts.size()))
            cmd_result.update({'data': binary_data})
            return cmd_result


def readRawChannelDataJSON(
        ws: _pfa.APIWebSocketClient,
        handle: str,
        fromDims: str,
        countDims: str,
        required: bool = False
) -> list[int] | None:
    """The server sends the requested raw image data as a JSON string to the
    FemtoAPI client.

    See :func:`readRawChannelDataToClientsBlob` for parameters.

    :return: 1D list of raw values
    """
    command = f"FemtoAPIFile.readRawChannelDataJSON('{handle}', '{fromDims}', '{countDims}')"
    cmd_result = _execute_command(ws, command, required)
    return json.loads(cmd_result) if cmd_result else None


def readChannelDataJSON(
        ws: _pfa.APIWebSocketClient,
        handle: str,
        fromDims: str,
        countDims: str,
        required: bool = False
) -> list[int] | None:
    """The server sends the requested converted image data as a JSON string to
    the FemtoAPI client.

    See :func:`readRawChannelDataToClientsBlob` for parameters.

    :return: 1D list of converted values
    """
    command = f"FemtoAPIFile.readChannelDataJSON('{handle}', '{fromDims}', '{countDims}')"
    cmd_result = _execute_command(ws, command, required)
    return json.loads(cmd_result) if cmd_result else None

    
def readRawChannelData(
        ws: _pfa.APIWebSocketClient,
        varName: str,
        handle: str,
        fromDims: str,
        countDims: str,
        required: bool = False
) -> bool:
    """Reads raw channel data on the server side to a JavaScript variable.

    See :func:`readRawChannelDataToClientsBlob` for parameters.

    :return: success
    """
    command = (f"var {varName} = "
               f"FemtoAPIFile.readRawChannelData('{handle}', '{fromDims}', '{countDims}')")
    return not not _execute_command(ws, command, required, just_true=True)


def readChannelData(
        ws: _pfa.APIWebSocketClient,
        varName: str,
        handle: str,
        fromDims: str,
        countDims: str,
        required: bool = False
) -> bool:
    """Reads converted channel data on the server side into a JavaScript variable.

    See :func:`readRawChannelDataToClientsBlob` for parameters.

    :return: success
    """
    command = (f"var {varName} = "
               f"FemtoAPIFile.readChannelData('{handle}', '{fromDims}', '{countDims}')")
    return not not _execute_command(ws, command, required, just_true=True)
    

def writeRawChannelData(
        ws: _pfa.APIWebSocketClient,
        varName: str,
        handle: str,
        fromDims: str,
        countDims: str,
        required: bool = False
) -> bool:
    """Writes raw channel data from the variable to the specified
    sub-hyperrectangle.

    See :func:`readRawChannelDataToClientsBlob` for parameters.

    :return: success
    """
    command = (f"FemtoAPIFile.writeRawChannelData({varName}, '{handle}', "
               f"'{fromDims}', '{countDims}')")
    return not not _execute_command(ws, command, required)
    

def writeChannelData(
        ws: _pfa.APIWebSocketClient,
        varName: str,
        handle: str,
        fromDims: str,
        countDims: str,
        required: bool = False
) -> bool:
    """Writes converted channel data from the variable to the specified
    sub-hyperrectangle.

    See :func:`readRawChannelDataToClientsBlob` for parameters.

    :return: success
    """
    command = (f"FemtoAPIFile.writeChannelData({varName}, '{handle}', "
               f"'{fromDims}', '{countDims}')")
    return not not _execute_command(ws, command, required)

    
def writeRawChannelDataFromAttachment(
        ws: _pfa.APIWebSocketClient,
        buffer: _qtc.QByteArray,
        handle: str,
        fromDims: str,
        countDims: str,
        required: bool = False
) -> bool:
    """Writes the specified raw data from an attached binary data file.

    :param ws: FemtoAPI client
    :param buffer:
    :param handle: channel handle, e.g. ``'52,0,1,1'``
    :param fromDims: a string enumerating the starting indices of a
        sub-hyperrectangle of a multidimensional data array.
        For example, in a 3-dimensional data array, '256,0,10' means index 256
        in the first dimension, index 0 in the second dimension, and index 10
        in the third dimension. Note that all indices are zero-based.
    :param countDims: a string enumerating the dimensions of a
        sub-hyperrectangle of a multidimensional data array.
        For example, in a three-dimensional data array, '512,512,10' means
        512 pixels in the first and second dimensions, and 10 frames in the
        third dimension.
    :param required: raise exception on failure
    :return: success
    """
    command = (f"FemtoAPIFile.writeRawChannelDataFromAttachment('{handle}', "
               f"'{fromDims}', '{countDims}')")
    ws.uploadAttachment(buffer)
    return not not _execute_command(ws, command, required)


def writeChannelDataFromAttachment(
        ws: _pfa.APIWebSocketClient,
        buffer: _qtc.QByteArray,
        handle: str,
        fromDims: str,
        countDims: str,
        required: bool = False
) -> bool:
    """Writes the specified converted data from an attached binary data file.

    See :func:`writeRawChannelData` for parameters.

    :return: success
    """
    command = f"FemtoAPIFile.writeChannelDataFromAttachment('{handle}', '{fromDims}', '{countDims}')"
    ws.uploadAttachment(buffer)
    return not not _execute_command(ws, command, required)


def getTmpTiff(
        ws: _pfa.APIWebSocketClient,
        uId: str,
        filePath: Path,
        required: bool = False
) -> bool:
    """The command sends the exported file metadata as a binary file, if exists.

    :param ws: FemtoAPI client
    :param uId: id from :func:`tiffExport`
    :param filePath: path to save the result
    :param required: raise exception on failure
    :return: success
    """
    command = f"FemtoAPIFile.getTmpTiff('{uId}')"
    log_command(command)
    simple_cmd_parser = ws.sendJSCommand(command)
    result_code = simple_cmd_parser.getResultCode()
    if result_code > 0:
        message = simple_cmd_parser.getErrorText()
        log_error(f'Return code: {result_code}')
        log_error(message)
        if required:
            raise _e.FemtoApiWrapError(result_code, message)
        return False
    else:
        result = simple_cmd_parser.getJSEngineResult()
        log_debug(f'getTiff result: {result}')
        cmd_result = _qtc.QByteArray()
        for parts in simple_cmd_parser.getPartList():
            cmd_result.append(parts)
        with open(Path(filePath), 'wb') as f:
            f.write(cmd_result.data())
        return True


def tiffExport(
        ws: _pfa.APIWebSocketClient,
        filePath: str,
        handle: str,
        applyLut: _JsBool,
        channelList: str = '',
        compressed: _OptionalJsBool = 'true',
        breakView: _OptionalJsBool = 'false',
        exportRawData: _OptionalJsBool = 'false',
        startTimeSlice: str = '',  # TODO maybe int
        endTimeSlice: str = '',  # TODO maybe int
        required: bool = False
) -> bool:
    """Creates an .ome.tiff file synchonized way.

    :param ws: FemtoAPI client
    :param filePath: file path
    :param handle: unit handle, e.g. ``'23,0,1'``
    :param applyLut: ``'true'`` or ``'false'``
    :param channelList: optional list of channel indices, separated by space
        converted to a string, e.g. ``'0,1'``
    :param compressed: ``'true'``, ``'false'`` or ``''``
    :param breakView: ``'true'``, ``'false'`` or ``''``
    :param exportRawData: ``'true'``, ``'false'`` or ``''``
    :param startTimeSlice: start time
    :param endTimeSlice: end time
    :param required: raise exception on failure
    :return: JSON ``dict``
    """
    file_path = Path(filePath)
    log_debug(file_path)
    if not file_path.parent.exists():
        log_error(message := 'tiffExport error: Filepath directory does not exists.')
        if required:
            raise _e.FemtoApiWrapError(message)
        return False
    rndm = random.randrange(0, 1000000)
    uid = 'tmptif_' + str(rndm)
    command = (f"FemtoAPIFile.createTmpTiff('{uid}', '{handle}', {applyLut}, "
               f"'{channelList}', {compressed}, {breakView}, {exportRawData}, "
               f"{startTimeSlice}, {endTimeSlice})")
    log_command(command)
    simple_cmd_parser = ws.sendJSCommand(command)
    result_code = simple_cmd_parser.getResultCode()
    if result_code > 0:
        log_error(f'Return code: {result_code}')
        log_error(message := simple_cmd_parser.getErrorText())
        if required:
            raise _e.FemtoApiWrapError(result_code, message)
        return False
    else:
        create_tiff_res = simple_cmd_parser.getJSEngineResult()
        log_debug(f'createTmpTiff result: {create_tiff_res}')
        cmd_result = _qtc.QByteArray()
        for parts in simple_cmd_parser.getPartList():
            cmd_result.append(parts)
        tmp = cmd_result.data()
        m_data_file = Path(file_path.parent, f'{file_path.name}.metadata.txt')
        with open(m_data_file, 'wb') as f:
            f.write(tmp)
        if ws.getUrl().toString == 'ws://localhost:8888':
            tmp_path = Path(create_tiff_res['tmp'])
            shutil.move(tmp_path, file_path)
            result = None
        else:
            result = getTmpTiff(ws, uid, file_path)
        return result
   

def _execute_command(
        ws: _pfa.APIWebSocketClient,
        command: str,
        required: bool,
        just_true: bool = False) -> _t.Any:
    log_command(command)
    simple_cmd_parser = ws.sendJSCommand(command)
    result_code = simple_cmd_parser.getResultCode()
    if result_code > 0:
        message = simple_cmd_parser.getErrorText()
        if required:
            log_error(f'Return code: {result_code}')
            log_error(message)
            raise _e.FemtoApiWrapError(result_code, message)
        else:
            log_warning(f'Return code: {result_code}')
            log_warning(message)
            return None
    else:
        if just_true:
            # Some commands return None even on success.
            # This way we can transform it to a truthy value
            return True
        return simple_cmd_parser.getJSEngineResult()
