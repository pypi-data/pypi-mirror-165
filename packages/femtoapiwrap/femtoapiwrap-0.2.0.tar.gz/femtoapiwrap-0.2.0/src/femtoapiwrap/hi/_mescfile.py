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
MESc data structure handling.
"""
from __future__ import annotations  # TODO: to be removed from Python 3.9

import dataclasses as _dc
import functools as _ft
import logging
import numpy as _np
# noinspection PyPep8Naming
import PySide2.QtCore as _qtc
import pathlib
import scipy.spatial.transform as _st
import typing as _t
import upolygon as _poly
import uuid

from .. import errors as _err


_log = logging.getLogger(__name__)

FileHandle = int
"""Type alias for file handles."""

SessionHandle = _t.Tuple[int, int]
"""Type alias for session handles."""

UnitHandle = _t.Tuple[int, int, int]
"""Type alias for measurement unit handles."""

ChannelHandle = _t.Tuple[int, int, int, int]
"""Type alias for channel handles."""


def quat2rot(quat: _t.Sequence[float]) -> _st.Rotation:
    """Converts a 4-element array to a rotation object.

    :param quat: the 4 quaternion values
    :return: rotation object
    """
    return _st.Rotation.from_quat(quat)


ZERO_ROT: _st.Rotation = quat2rot([0., 0., 0., 1.])
""":class:`scipy.spatial.transform.Rotation` object representing no rotation"""

ZERO_TRANSL: _np.ndarray = _np.array([0., 0., 0.])
"""Zero 3D translation"""


@_dc.dataclass
class FileMeta:
    """File metadata."""

    JSON_VERSION: _t.ClassVar[str] = '2'
    """Supported JSON format version"""

    handle: FileHandle
    """Handle"""

    path: str
    """Full path of the MESc file"""

    uuid: str
    """UUID"""

    session_handles: list[SessionHandle]
    """Handles of contained sessions, each in format ``(<file_id>, <session_id>)``"""

    @classmethod
    def from_tree(cls, tree: dict[str, _t.Any]) -> FileMeta:
        """Parses the output of :func:`api.getFileMetadata`.

        :param tree: :class:`dict` loaded from JSON
        :return: object with a subset of metadata
        :raise NoMetaData: if ``tree`` is empty
        :raise UnsupportedVersion: if ``tree`` is not of the expected format
        """
        if not tree:
            raise _err.NoMetaData
        if (version := tree['formatVersion']) != cls.JSON_VERSION:
            raise _err.UnsupportedVersion('formatVersion', version, cls.JSON_VERSION)
        path = tree['path']
        try:
            path = fmt_path(tree['path'])
        except OSError:
            # Falls here in case of no-yet-saved files
            pass
        return cls(
            handle=tree['handle'][0],
            path=path,
            uuid=tree['uuid'],
            session_handles=list(map(tuple, tree['sessionHandles']))
        )


@_dc.dataclass
class SessionMeta:
    """Metadata of measurement sessions."""

    JSON_VERSION: _t.ClassVar[str] = '2'
    """Supported JSON format version"""

    handle: SessionHandle
    """Handle in format ``(<file_id>, <session_id>)``"""

    unit_handles: list[UnitHandle]
    """Measurement unit handles"""

    uuid: str
    """UUID"""

    comment: str
    """Comment"""

    @classmethod
    def from_tree(cls, tree: dict[str, _t.Any]) -> SessionMeta:
        """Extracts ROIs from the metadata object from::

            api.getSessionMetadata(ws, handle)

        :param tree: metadata object
        :returns: list of :class:`Roi`
        :raise NoMetaData: if ``tree`` is empty
        :raise UnsupportedVersion: if ``tree`` is not of the expected format
        """
        if not tree:
            raise _err.NoMetaData
        if (version := tree['formatVersion']) != cls.JSON_VERSION:
            raise _err.UnsupportedVersion('session.formatVersion', version, cls.JSON_VERSION)
        return cls(
            handle=tuple(tree['handle']),
            unit_handles=list(map(tuple, tree['unitHandles'])),
            uuid=tree['uuid'],
            comment=tree['comment'],
        )


@_dc.dataclass
class ChannelMeta:
    """Metadata of measurement channels."""

    idx: int
    """Index within the measurement unit"""

    offset: float
    """Offset of measured pixel values"""

    handle: ChannelHandle
    """Handle in format ``(<file_id>,<session_id>,<unit_id>,<idx>)``"""

    dtype: _t.Type[_np.uint16] | _t.Type[_np.double]
    """:mod:`numpy` data type of channel data"""

    raw_limits: tuple[int, int] = (0, 2**16 - 1)
    """Raw limits. Set only when loaded from metadata"""

    scale: float = -1
    """Scale"""

    name: str = ''

    @classmethod
    def from_tree(cls, unit_handle: UnitHandle, tree: list[dict[str, _t.Any]]) -> list[ChannelMeta]:
        """Parses the result of :func:`api.getUnitMetadata` to get measurement
        metadata.

        :param unit_handle: measurement unit handle (not contained in ``tree``)
        :param tree: :class:`list` loaded from JSON
        :return: object with a subset of metadata
        :raise NoMetaData: if ``tree`` is empty
        """
        if not tree:
            raise _err.NoMetaData
        return [cls(
            idx=(idx := subtree['channelIdx']),
            handle=unit_handle + (idx,),
            dtype=_np.uint16 if subtree['dataType'] == 'uint16' else _np.double,
            offset=(conv := subtree['conversion'])['offset'],
            raw_limits=tuple(conv['limits']),
            scale=conv['scale'],
            name=subtree['name'],
        ) for subtree in tree]

    @property
    def lower_limit(self):
        """Lowest allowed value"""
        return min(self.scale * self.raw_limits[0] + self.offset,
                   self.scale * self.raw_limits[1] + self.offset)

    @property
    def upper_limit(self):
        """Highest allowed value + 1"""
        return max(self.scale * self.raw_limits[0] + self.offset,
                   self.scale * self.raw_limits[1] + self.offset)

    @property
    def raw_lower_limit(self):
        """Lowest allowed raw value"""
        return min(self.raw_limits)

    @property
    def raw_upper_limit(self):
        """Highest allowed raw value + 1"""
        return max(self.raw_limits)


@_dc.dataclass
class UnitMeta:
    """Metadata of measurement units"""

    handle: UnitHandle
    """Handle in format ``(<file_id>,<session_id>,<unit_id>)``"""

    method_type: str
    """Measurement method. Currently ``timeSeries`` is supported"""

    tech_type: str
    """Technology type, eg. ``'aO'``"""

    dims: tuple[int, int] | tuple[int, int, int] | tuple[int, int, int, int]
    """Sizes of the measurement data array.
    For ``timeSeries``, X × Y × n_frames.
    For ``volumeScan``, X × Y × Z × n_frames.
    """

    pixel_sizes: list[tuple[float, float, float]]
    """Pixel sizes for each layer, where *z* size is 0 when not applicable"""

    labeling_origin: tuple[float, float, float]
    """Labeling origin"""

    min_z: float = 0.
    """The first layers perpendicular distance from the viewport."""

    max_z: float = 0.
    """The last layers perpendicular distance from the viewport."""

    uuid: str = ''
    """UUID"""

    comment: str = ''
    """Comment"""

    being_recorded: bool = False
    """Recording is currently in progress"""

    @property
    def n_frames(self) -> int:
        """Number of frames"""
        return self.dims[-1]

    @property
    def frame_shape(self) -> tuple[int, int]:
        """Shape of a frame, as per :mod:`numpy`"""
        return self.dims[:2]

    @property
    def ndim(self) -> int:
        """Dimension of the measurement array"""
        return len(self.dims)

    @property
    def session_handle(self) -> SessionHandle:
        """Handle of the parent session"""
        return self.handle[:2]

    @classmethod
    def from_tree(cls, handle: UnitHandle, tree: dict[str, _t.Any]) -> UnitMeta:
        """Parses the result of :func:`api.getUnitMetadata` to get measurement
        metadata.

        :param handle: measurement unit handle (not contained in ``tree``)
        :param tree: :class:`dict` loaded from JSON
        :return: object with a subset of metadata
        :raise NoMetaData: if ``tree`` is empty
        """
        if not tree:
            raise _err.NoMetaData

        return cls(
            handle=handle,
            method_type=tree['methodType'],
            tech_type=tree['technologyType'],
            dims=tuple(tree['logicalDimSizes']),
            pixel_sizes=list(zip(x := tree['pixelSizeX'],
                                 tree['pixelSizeY'],
                                 tree['pixelSizeZ'] or ([0] * len(x)))),
            labeling_origin=tuple(tree['labelingOrigin']),
            min_z=tree.get('minZ', 0.),
            max_z=tree.get('maxZ', 0.),
            uuid=tree['uuid'],
            comment=tree['comment'],
            being_recorded=tree['isBeingRecorded'],
        )

    def from_dims(self, *, frame: int = 0) -> tuple[int, ...]:
        """Constructs a tuple of indices to specify a starting point for
        :func:`femtoapiwrap.api.readRawChannelDataToClientsBlob` or
        :func:`femtoapiwrap.api.readChannelDataToClientsBlob`.

        :param frame: index of the first frame to include
        :raise InvalidDimension: when out of bounds
        """
        if not (0 <= frame <= self.n_frames):
            raise _err.InvalidDimension('frame', frame, (0, self.n_frames))
        return *([0] * (self.ndim - 1)), frame

    def plus_dims(self, *, n_frames: int = None, d_coords: _t.Sequence[int] = None) -> tuple[int, ...]:
        """Constructs a tuple of indices to specify an end point for
        :func:`femtoapiwrap.api.readRawChannelDataToClientsBlob` or
        :func:`femtoapiwrap.api.readChannelDataToClientsBlob`.

        :param n_frames: number of frames to include, None means all
        :param d_coords: coordinate deltas to specify the end of a selection
        :raise InvalidDimension: when out of bounds
        """
        n_frames = n_frames or self.n_frames
        if not (0 <= n_frames <= self.n_frames):
            raise _err.InvalidDimension('n_frames', n_frames, (0, self.n_frames))
        if d_coords is None:
            d_coords = self.dims[:-1]
        elif (len(d_coords) != self.ndim - 1 or
              any(0 > c or c > d for c, d in zip(d_coords, self.dims[:-1]))):
            raise _err.InvalidDimension('d_coords', d_coords, (0, self.dims[:-1]))
        return *d_coords, n_frames

    def array_shape(self, *, n_frames: int) -> tuple[int, ...]:
        """Array shape for an array with a sequence of full frames.

        :param n_frames: number of frames to include
        """
        return self.plus_dims(n_frames=n_frames)

    def pixel_size(self, layer_index: int) -> tuple[float, float]:
        """Pixel size in micrometers, for X × Y × T data.

        .. warning::
            Will be deprecated.

        :param layer_index: index of layer (and viewport) to use
        """
        return self.pixel_sizes[layer_index][:2]


@_dc.dataclass
class Roi:
    """Region of Interest"""

    JSON_VERSION: _t.ClassVar[int] = 2
    """Supported JSON format version"""

    label: str
    """Label displayed on GUI"""

    viewport_index: int
    """Index of the viewport on which the ROI lives"""

    viewport_rot: _st.Rotation
    """Rotation applied to the viewport"""

    viewport_transl: _np.ndarray
    """Translation applied to the viewport"""

    type: str
    """Type; ``rectangleXY``/``polygonXY``/``regularPolygonXY``"""

    vertices: _np.ndarray
    """N×2 array of 2D coordinates of the vertices. Must be a closed loop"""

    @classmethod
    def from_px_coords(cls,
                       pixel_coords: _t.Sequence[tuple[int, int]] | _np.ndarray,
                       pixel_size: tuple[float, float] | _np.ndarray,
                       viewport: Viewport,
                       label: str,
                       ) -> Roi:
        """Creates a polygon ROI from the vertices given in pixel coordinates.

        :param pixel_coords: list of (i, j) coordinates of the vertices
        :param pixel_size: pixel size in micrometers
        :param viewport: viewport object from MESc
        :param label: label to be displayed in MESc
        """
        vertices = _np.array(pixel_coords)
        vertices = vertices[~_np.isnan(vertices).any(axis=1)]
        # ROI must be a closed loop
        if not _np.all(vertices[0] == vertices[-1]):
            vertices = _np.vstack((vertices, vertices[0]))
        vertices = cls._px2vp_coord(vertices, pixel_size)

        return Roi(
            label=label,
            viewport_index=viewport.layer_idx,
            viewport_rot=viewport.rot,
            viewport_transl=viewport.transl,
            type='polygonXY',
            vertices=_np.array(vertices),
        )

    @classmethod
    def from_tree(cls, tree: dict[str, _t.Any]) -> list[Roi]:
        """Extracts ROIs from the metadata object from::

            api.getUnitMetadata(ws, mUnit, 'Roi')

        :param tree: metadata object
        :returns: list of :class:`Roi`
        :raise NoMetaData: if ``tree`` is empty
        :raise UnsupportedVersion: if ``tree`` is not of the expected format
        """
        if not tree:
            raise _err.NoMetaData
        if version := tree['roiFormatVersion'] != cls.JSON_VERSION:
            raise _err.UnsupportedVersion('roiFormatVersion', version, cls.JSON_VERSION)
        rois = tree['rois']
        return [cls(
            label=roi['label'],
            viewport_index=roi['refViewportIndex'],
            viewport_rot=quat2rot(roi['refViewportGeomTrans']['roiGeomTransRotXYZW']),
            viewport_transl=_np.array(roi['refViewportGeomTrans']['roiGeomTransTransl'], dtype=_np.float32),
            type=roi['type'],
            vertices=_np.array(roi['vertices'])
        ) for roi in rois]

    def to_tree(self,
                layer_idx: int = 0,
                *,
                first_z: int = 0,
                last_z: int = 0) -> dict[str, _t.Any]:
        """Converts the object to JSON dict.

        :param layer_idx: layer or viewport index
        :param first_z: value for ``firstZPlane`` JSON attribute
        :param last_z: value for ``lastZPlane`` JSON attribute
        """
        if self.type not in ('polygonXY', 'rectangleXY'):
            raise NotImplementedError(f'{self.type} not supported')
        return {
            'color': random_color(),
            'firstZPlane': first_z,
            'label': self.label,
            'lastZPlane': last_z,
            'refViewportGeomTrans': {
                'roiGeomTransRotXYZW': self.viewport_rot.as_quat().tolist(),
                'roiGeomTransTransl': self.viewport_transl.tolist()
            },
            'refViewportIndex': layer_idx,
            'roiCoordinateSystem': 'referenceViewport',
            'roiJsonFormatVersion': self.JSON_VERSION,
            'role': 'standard',
            'type': self.type,
            'uniqueID': f'{{{uuid.uuid4()}}}',
            'vertices': self.vertices.tolist(),
        }

    def to_px_coords(self,
                     pixel_size: tuple[float, float] | _np.ndarray
                     ) -> _np.ndarray:
        """Transforms vertices to pixel coordinates.

        :param pixel_size: pixel size in micrometers
        :return: n_vertices × 2 array of (i, j) coordinates
        """
        # Remove last element as it is only for closing the loop
        return self._vp2px_coord(self.vertices[:-1], pixel_size)

    @classmethod
    def groups_to_tree(cls, roi_groups: dict[str, list[Roi]]) -> dict[str, _t.Any]:
        """Converts grouped ROI objects to JSON dict, ready to be passed as::

            api.setUnitMetadata(ws, mUnit, 'Roi', json.dumps(tree))

        Groups are not preserved in the output: they can be marked with color and label.
        """
        return {
            'roiFormatVersion': cls.JSON_VERSION,
            'rois': [roi.to_tree()
                     for roi_group in roi_groups.values()
                     for roi in roi_group]
        }

    def draw_to_mask(self,
                     mask: _np.ndarray,
                     pixel_size: tuple[float, float],
                     true_value: _t.Any = 1) -> None:
        """Fills pixels belonging to the ROI.

        :param mask: an image of the same size as a frame
        :param pixel_size: scaling factors
        :param true_value: value assigned to the pixels contained in the ROI
        """
        px_vertices = self.to_px_coords(pixel_size)
        # upolygon works with (x, y) coordinates
        # Overshoot is not a problem, then the roi will be cropped
        _poly.draw_polygon(mask, [px_vertices[:, [1, 0]].ravel().tolist()], true_value)

    @staticmethod
    def _px2vp_coord(
            px_coords: _np.ndarray,
            px_size: tuple[float, float] | _np.ndarray,
    ) -> _np.ndarray:
        scale = _np.array(px_size, dtype=float)
        return px_coords * scale

    @staticmethod
    def _vp2px_coord(
            vp_coords: _np.ndarray,
            px_size: tuple[float, float] | _np.ndarray,
    ) -> _np.ndarray:
        scale = _np.array(px_size, dtype=float)
        return (vp_coords / scale).astype(int)


@_dc.dataclass
class Point:
    """Point object from ``Points`` unit metadata"""

    JSON_VERSION: _t.ClassVar[int] = 2
    """Supported JSON format version"""

    pos: _np.ndarray
    """*x*, *y*, *z* coordinates"""

    color: str | None = None
    """Color code in ARGB hexa format"""
    
    visible: bool = True
    """Visible in MESc"""

    @classmethod
    def from_tree(cls, tree: dict[str, _t.Any]) -> dict[int, list[Point]]:
        """Extracts point groups from the metadata object from::

            api.getUnitMetadata(ws, mUnit, 'Points')

        :param tree: metadata object
        :returns: list of :class:`Point`
        :raise NoMetaData: if ``tree`` is empty
        :raise UnsupportedVersion: if ``tree`` is not of the expected format
        """
        if not tree:
            raise _err.NoMetaData
        if (version := tree['pointsFormatVersion']) != cls.JSON_VERSION:
            raise _err.UnsupportedVersion('pointsFormatVersion', version, cls.JSON_VERSION)
        return {
            group['index']: [cls(
                pos=_np.array(p['position']),
                color=p['color'],
                visible=p['visible'],
            ) for p in group['points']]
            for group in tree['group']
        }

    @classmethod
    def from_px_coords(cls,
                       pixel_coords: tuple[int, int] | _np.ndarray,
                       pixel_size: tuple[float, float] | _np.ndarray,
                       viewport: Viewport,
                       color: str | None = None,
                       visible: bool = True,
                       ) -> Point:
        """Transforms a point from pixel coordinates to a point in viewport
        coordinates.

        :param pixel_coords: *i* and *j* coordinates
        :param pixel_size: pixel size in micrometers
        :param viewport: viewport object from MESc
        :param color: color code in ARGB hexa format
        :param visible: visible in MESc
        """
        return cls(
            pos=cls._transform_point(pixel_coords, pixel_size, viewport),
            color=color,
            visible=visible
        )

    @staticmethod
    def _transform_point(
            pixel_coords: tuple[int, int] | _np.ndarray,
            pixel_size: tuple[float, float] | _np.ndarray,
            viewport: Viewport,
    ) -> _np.ndarray:
        scale = _np.array([pixel_size[0], pixel_size[1], 0], dtype=float)
        v = _np.array([pixel_coords[0], pixel_coords[1], 0], dtype=float)
        v *= scale
        v = viewport.rot.apply(v)
        v += viewport.transl
        return v

    def to_tree(self):
        """Converts the object to JSON dict"""
        return {
            'color': self.color or random_color(),
            'position': self.pos.tolist(),
            'visible': self.visible
        }
    
    @classmethod
    def groups_to_tree(cls, point_groups: dict[int, list[Point]]) -> dict[str, _t.Any]:
        """Converts grouped point objects to JSON dict, ready to be passed as:

            api.setUnitMetadata(ws, mUnit, 'Points', json.dumps(tree))

        :param point_groups: lists of points under integer keys corresponding to
            the predefined point series of MESc
        :raise InvalidPointGroup: if the group key is not among the
            predefined ones
        """
        if bad_i := [i for i in point_groups.keys() if i < 0 or i > 9]:
            raise _err.InvalidPointGroup(bad_i)
        return {
            'group': [
                {
                    'index': i,
                    'points': [p.to_tree() for p in points]
                } for i, points in point_groups.items()
            ],
            'pointsFormatVersion': cls.JSON_VERSION,
            'show': True,
            'showInDepth': True,
            'showNumbering': False
        }


@_dc.dataclass
class Viewport:
    """Viewport object of `ReferenceViewport` and ROI metadata"""

    JSON_VERSION: _t.ClassVar[int] = 1
    """Supported JSON format version"""

    rot: _st.Rotation
    """3D rotation"""

    transl: _np.ndarray
    """3D translation"""

    height: float
    """Height in micrometers"""

    width: float
    """Width in micrometers"""

    layer_idx: int = 0
    """Index of the corresponding layer. Set only when loaded from metadata"""

    @classmethod
    def from_tree(cls, subtree: dict[str, _t.Any]) -> list[Viewport]:
        """Extracts reference viewports from the metadata object from::

            api.getUnitMetadata(ws, mUnit, 'ReferenceViewport')

        :param subtree: metadata object
        :returns: list of :class:`Viewport`
        :raise NoMetaData: if ``tree`` is empty
        :raise UnsupportedVersion: if ``tree`` is not of the expected format
        """
        if not subtree:
            raise _err.NoMetaData
        if (version := subtree['referenceViewportFormatVersion']) != cls.JSON_VERSION:
            raise _err.UnsupportedVersion(
                'referenceViewportFormatVersion', version, cls.JSON_VERSION)
        viewports = subtree['viewports']
        return [cls(
            layer_idx=i,
            rot=quat2rot(vp['geomTransRot']),
            transl=_np.array(vp['geomTransTransl'], dtype=_np.float32),
            height=vp['height'],
            width=vp['width']
        ) for i, vp in enumerate(viewports)]

    def to_tree(self, self_only: bool = False) -> dict[str, _t.Any]:
        """Converts the object to MESc JSON format.

        :param self_only: generate without the outer scope of the JSON
        :return: JSON dict
        """
        self_tree = {
            'geomTransRot': self.rot.as_quat().tolist(),
            'geomTransTransl': self.transl.tolist(),
            'height': self.height,
            'width': self.width
        }
        if self_only:
            return self_tree
        else:
            return {
                'referenceViewportFormatVersion': 1,
                'viewports': [self_tree]
            }


def find_measurements_by_method(
        session_tree: dict[str, _t.Any],
        method_type: str
) -> list[UnitHandle]:
    """Parses the result of :func:`api.getChildTree` on a session to get the
    measurement units with the given method.

    :param session_tree: output of :func:`api.getChildTree`
    :param method_type: method type as written in the JSON
    :return: all conforming unit metadata
    :raise NoMeasurementUnit: if the session contains no units
    """
    if not session_tree or not (ms := session_tree['measurements']):
        raise _err.NoMeasurementUnit
    return [tuple(m['handle']) for m in ms if m['methodType'] == method_type]


_DTYPE_MAP = {'uInt16': _np.uint16,
              'double': _np.double}


def channel_data_to_numpy(response: dict) -> _np.ndarray:
    """
    Format binary data to multidimensional array.

    Uses the metadata returned by ``read(Raw)ChannelDataToClientsBlob``,
    so the ``dtype`` of the result depends on the API call.

    :param response: Femto API response
    :return: :class:`np.ndarray`
    """
    raw_data = response['data']
    meta = response['result']
    dtype = _DTYPE_MAP[meta['channelDataType']]
    dims = tuple(meta['size'])
    return _np.frombuffer(raw_data, dtype=dtype).reshape(dims, order='F')


def numpy_to_channel_data(a: _np.ndarray) -> _qtc.QByteArray:
    """Converts a ``numpy`` array into the format required by Femto API."""
    return _qtc.QByteArray(a.tobytes(order='F'))


_RNG = _np.random.default_rng(12345)


def random_color(rng: _np.random.Generator | None = None) -> str:
    """Generates a lighter colour that is more visible in the MESc GUI"""
    rng = _RNG if rng is None else rng
    r = 128 + int(rng.integers(128))
    g = 128 + int(rng.integers(128))
    b = 128 + int(rng.integers(128))
    return f'#ff{r:02x}{g:02x}{b:02x}'


@_ft.lru_cache(100)
def fmt_handle(ids: tuple[int, ...]) -> str:
    """Converts a tuple of numeric ids of files, sessions, units, channels
    to the format expected by Femto API.

    :param ids: IDs
    :returns: handle
    """
    return ','.join(map(str, ids))


@_ft.lru_cache(100)
def fmt_dims(dims: _t.Sequence[int | None]) -> str:
    """Converts a tuple of numeric indices to the format expected by
    Femto API.

    :param dims: indices; may contain trailing ``None`` s
    :returns: handle
    """
    return ','.join(str(d) for d in dims if d is not None)


def fmt_path(path: str | pathlib.Path) -> str:
    """Converts file paths to the format expected by the API."""
    return pathlib.Path(path).resolve().as_posix()
