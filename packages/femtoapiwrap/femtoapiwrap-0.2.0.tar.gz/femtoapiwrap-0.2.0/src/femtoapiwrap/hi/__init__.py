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

"""High-level utils for handling some common use cases of FemtoAPI,
built on the top of the low-leve API funcions of :mod:`femtoapiwrap.api`.
"""

# Types, constants, functions

from ._mescfile import (
    ChannelMeta,
    FileMeta,
    Point,
    Roi,
    SessionMeta,
    UnitMeta,
    Viewport,

    ZERO_ROT,
    ZERO_TRANSL,

    channel_data_to_numpy,
    find_measurements_by_method,
    fmt_dims,
    fmt_handle,
    fmt_path,
    numpy_to_channel_data,
    random_color,
    quat2rot,
)

from ._highapi import (
    HighFemtoApi,
    MeasurementMeta,
)

# Type aliases for typing annotations

from ._mescfile import (
    ChannelHandle,
    FileHandle,
    SessionHandle,
    UnitHandle,
)
