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


"""Utils."""
from __future__ import annotations

import logging
import sys
import time
# noinspection PyPep8Naming
import PySide2.QtCore as _qtc

from . import api as _api


_log = logging.getLogger(__name__)


def waitForMeasurementStop(ws):
    logging.info("wait")
    state = _api.getMicroscopeState(ws)['microscopeState']
    if state == "Working":
        logging.info("Waiting for measurement to stop ...")
        while state == "Working":
            time.sleep(1)
            state = _api.getMicroscopeState(ws)['microscopeState']
    if state == "In an invalid state":
        logging.error("Microscope is in an invalid state! Testing cannot proceed. Restart might be needed.")
        sys.exit()
    if state == "Off":
        logging.error("Microscope is turned off! Testing cannot proceed. Hardver start needed..")
        sys.exit()
    if state == "Initializing":
        logging.info("Microscope is Initializing. Why it is in this state is a mystery ...  Testing will stop anyways.")
        sys.exit()
    if state == "Ready":
        return True
    else:
        return False


def isMeasurementRunning(ws):
    state = _api.getMicroscopeState(ws)['microscopeState']
    logging.info("Mic state is " + str(state))
    if state == "Working":
        return True
    elif state == "Ready":
        return False
    elif state == "Off":
        logging.error("Microscope is off!!")
        return False
    elif state == "Initializing":
        logging.info("Microscope is Initializing.")
        return False
    else:
        logging.error("Microscope is in an invalid state!")
        return False


def waitForAsyncCommand(ws, commandId):
    isPending = True
    time.sleep(0.5)
    while isPending:
        status = _api.getStatus(ws, commandId)
        isPending = status['isPending']


def qt_app_instance(*args, **kwargs) -> _qtc.QCoreApplication:
    """Gets the existing Qt application instance else creates one."""
    app = _qtc.QCoreApplication.instance()
    return _qtc.QCoreApplication(*args, **kwargs) if app is None else app
