"""High-level convenience functions for frequent use cases,
using the low-level module :mod:`api`.
"""
from __future__ import annotations

import dataclasses as _dc
import json
import logging
import numpy as _np
import pathlib
import time
import typing as _t

# noinspection PyPep8Naming
import femtoapi.PyFemtoAPI as _pfa  # For type annotations only

from . import _mescfile as _mf

from .. import api as _api
from .. import errors as _err
from .. import utils as _utl

_log = logging.getLogger(__name__)


@_dc.dataclass
class MeasurementMeta:
    """Extended unit metadata."""
    unit: _mf.UnitMeta
    channels: list[_mf.ChannelMeta]
    viewports: list[_mf.Viewport]


class HighFemtoApi:
    """High-level API built on :mod:`api`, that produces and consumes
    :mod:`numpy` and regular Python objects instead of JSON
    and raw formats.
    """

    def __init__(self,
                 user_name: str = 'a',
                 password: str = 'b',
                 *,
                 url: str = _api.DEFAULT_URL,
                 sleep: float = 1.):
        self._app = _utl.qt_app_instance()
        self._ws = _api.initConnection(url)
        self._url = url
        _api.login(self._ws, user_name, password)
        time.sleep(sleep)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __del__(self):
        self.close()

    @property
    def ws(self) -> _pfa.APIWebSocketClient:
        """The websocket used for conection to FemtoAPI."""
        return self._ws

    @property
    def url(self) -> str:
        """The URL of the connected FemtoAPI."""
        return self._url

    def close(self):
        try:
            _api.closeConnection(self._ws)
        except AttributeError:
            pass

    def read_file_meta(self, file_handle: _mf.FileHandle) -> _mf.FileMeta:
        """Reads file metadata.

        Example use case: get the handles of available sessions.
        """
        file_tree = _api.getFileMetadata(self._ws, file_handle, required=True)
        file = _mf.FileMeta.from_tree(file_tree)
        return file

    def read_session_meta(self, session_handle: _mf.SessionHandle) -> _mf.SessionMeta:
        """Reads session metadata.

        Example use case: get all measurement unit handles in a session.
        """
        tree = _api.getSessionMetadata(self._ws, _mf.fmt_handle(session_handle), required=True)
        return _mf.SessionMeta.from_tree(tree)

    def read_unit_meta(self, unit_handle: _mf.UnitHandle) -> _mf.UnitMeta:
        """Reads a subset of the ``BaseUnitMetadata`` object.

        Example use case: get frame dimensions.
        """
        tree = _api.getUnitMetadata(
            self._ws, _mf.fmt_handle(unit_handle), 'BaseUnitMetadata', required=True)
        return _mf.UnitMeta.from_tree(unit_handle, tree)

    def read_ref_viewports(self, unit_handle: _mf.UnitHandle) -> list[_mf.Viewport]:
        """Reads the reference viewport for each layer.

        Example use case: get transformations for computing point coordinates.
        """
        tree = _api.getUnitMetadata(
            self._ws, _mf.fmt_handle(unit_handle), 'ReferenceViewport', required=True)
        return _mf.Viewport.from_tree(tree)

    def read_channels(self, unit_handle: _mf.UnitHandle) -> list[_mf.ChannelMeta]:
        """Reads all channels.

        Example use case: get lower an upper limit of pixel values.
        """
        tree = _api.getUnitMetadata(
            self._ws, _mf.fmt_handle(unit_handle), 'ChannelInfo', required=True)
        return _mf.ChannelMeta.from_tree(unit_handle, tree)

    def read_rois(self, unit_handle: _mf.UnitHandle) -> list[_mf.Roi]:
        """Reads regions of interests.

        Example use case: create a mask to crop a ROI from a downloaded frame.
        """
        tree = _api.getUnitMetadata(self._ws, _mf.fmt_handle(unit_handle), 'Roi', required=True)
        return _mf.Roi.from_tree(tree) if tree else []

    def write_rois(self,
                   unit_handle: _mf.UnitHandle,
                   rois: list[_mf.Roi] | dict[str, list[_mf.Roi]]) -> None:
        """Overwrites the ROIs stored in the specified unit.

        To keep the original ones, call :meth:`read_rois` to load them and
        pass the extended list to this function.

        Example use case: visualize contours found by image processing in
        the MESc GUI.

        :param unit_handle: measurement unit handle
        :param rois: list or groups of ROIs. This grouping has no effect in MESc.
        """
        if not isinstance(rois, dict):
            rois = {'a': rois}
        rois_json = json.dumps(_mf.Roi.groups_to_tree(rois))
        _api.setUnitMetadata(self._ws, _mf.fmt_handle(unit_handle), 'Roi', rois_json, required=True)

    def read_points(self, unit_handle: _mf.UnitHandle) -> dict[int, list[_mf.Point]]:
        """Reads point lists, grouped into point series.

        Example use case: measure distance of extracted image parts on a frame
        from a point marked on the GUI.

        .. note::
            Not finding points is not an error (returns an empty list), but
            not finding the unit (wrong handle) raises an exception.
        """
        tree = _api.getUnitMetadata(self._ws, _mf.fmt_handle(unit_handle), 'Points', required=True)
        return _mf.Point.from_tree(tree)

    def write_points(self,
                     unit_handle: _mf.UnitHandle,
                     points: list[_mf.Point] | dict[int, list[_mf.Point]]) -> None:
        """Overwrites the points stored in the specified unit.

        To keep the original ones, call :meth:`read_points` to load them and
        pass the extended list to this function.

        Example use case: visualize centroids found by image processing in
        the MESc GUI.

        :param unit_handle: measurement unit handle
        :param points: list or groups of points. :class:`dict` keys correspond
            to point groups (*Points* - *Point series 9*) in the MESc GUI.
            A simple :class:`list` of point is equivalent to group 0,
            i.e. *Points*.
        """
        if not isinstance(points, dict):
            points = {0: points}
        points_json = json.dumps(_mf.Point.groups_to_tree(points))
        _api.setUnitMetadata(
            self._ws, _mf.fmt_handle(unit_handle), 'Points', points_json, required=True)

    def wait_for_measurement(self, poll_s: float, timeout_s: int | None = None) -> None:
        """Waits until the microscope is in ``Working`` status.

        :param poll_s: delay between status checks in seconds
        :param timeout_s: timeout for getting ``Working`` status.
            If ``None``, it will wait indefinitely.
        :raise MicroscopeTimedOut: in case of timeout
        """
        t_0 = time.time()
        while True:
            if _utl.isMeasurementRunning(self._ws):
                break
            if timeout_s is not None and (t := (time.time() - t_0)) > timeout_s:
                raise _err.MicroscopeTimedOut(t, timeout_s)
            time.sleep(poll_s)

    def wait_for_n_frames(self,
                          unit_handle: _mf.UnitHandle,
                          n: int,
                          *,
                          poll_s: float = 1.,
                          timeout_s: int | None = None,
                          ) -> _mf.UnitMeta:
        """Waits until ``n`` frames are available in the specified unit.

        :param unit_handle: measurement unit handle
        :param n: number of frames required
        :param poll_s: time interval in seconds between repeated queries of
            movie dimensions
        :param timeout_s: timeout for getting ``Working`` status.
            If ``None``, it will wait indefinitely.
        :return: unit meta data containing the latest dimensions
        :raise MicroscopeTimedOut: in case of timeout
        """
        t_0 = time.time()
        while True:
            meta = self.read_unit_meta(unit_handle)
            if meta.n_frames >= n:
                return meta
            if timeout_s is not None and (t := (time.time() - t_0)) > timeout_s:
                raise _err.MicroscopeTimedOut(t, timeout_s)
            _log.info('Waiting...')
            time.sleep(poll_s)

    def find_file_by_path(self, path: str | pathlib.Path) -> _mf.FileMeta:
        """Reads the metadata of a file specified by file path."""
        path = _mf.fmt_path(path)
        handles = _api.getFileList(self.ws, required=True)
        if handles:
            for handle in handles[::-1]:
                meta = self.read_file_meta(handle)
                if meta.path == path:
                    return meta
        raise _err.NodeNotFound('file', path)

    def find_active_measurement(self, offline: bool = False) -> _mf.UnitMeta:
        """Finds the active measurement in the currently active file and
        session.

        :param offline: in case of offline processing, ignores whether the
            measure unit is being recorded
        :return: metadata for the active measurement in
            :class:`hi.MeasurementData`
        :raise NoMeasurementUnit: when the session is empty
        :raise FemtoApiWrapError: if an API operation fails
        :raise NodeNotFound: if none of the units are active
            (and not offline)
        """
        session_handle = _api.getCurrentSession(self._ws, required=True)
        tree = _api.getSessionMetadata(self._ws, session_handle, required=True)
        session = _mf.SessionMeta.from_tree(tree)
        if not session.unit_handles:
            raise _err.NoMeasurementUnit
        if offline:
            # Assume that we want the last one.
            # If we already knew the handle, why we would call this method? :)
            active_handle = session.unit_handles[-1]
            return self.read_unit_meta(active_handle)
        else:
            # Looking up the active one from backwards, as it is likely to be the last one.
            # This is to minimize the number of network queries.
            for handle in session.unit_handles[::-1]:
                unit = self.read_unit_meta(handle)
                if unit.being_recorded:
                    return unit
            raise _err.NodeNotFound('unit', 'being_recorded')

    def read_frames(
            self,
            channel_handle: _mf.ChannelHandle,
            from_dims: str | _t.Sequence,
            plus_dims: str | _t.Sequence,
            *,
            raw: bool
    ) -> _np.ndarray:
        """Reads 1 or more frames (or a slice thereof) from a channel.

        .. warning::

            If any of the dimensions is out of bounds, a smaller array will
            be returned. Please check ``shape``.

            ``dtype`` of the returned array can vary if ``raw=False``.

        :param channel_handle: channel handle
        :param from_dims: start position specifier (e.g. ``'0,0,0'``, ``(0, 0, 0)``
            or ``[0, 0, 0]``)
        :param plus_dims: offset of end position from ``from_dims``
            (e.g. ``'512,512,1'``, ``(512, 512, 1)`` or ``[512, 512, 1]``)
        :param raw: return raw frame (offset not compensated)
        :return: :class:`np.ndarray` with the frames.
        """
        if not isinstance(from_dims, str):
            from_dims = _mf.fmt_dims(tuple(from_dims))
        if not isinstance(plus_dims, str):
            plus_dims = _mf.fmt_dims(tuple(plus_dims))

        read = (_api.readRawChannelDataToClientsBlob if raw else
                _api.readChannelDataToClientsBlob)
        res = read(self._ws, _mf.fmt_handle(channel_handle), from_dims, plus_dims, required=True)
        _log.debug(f'Requested {from_dims}+{plus_dims}, got {res["result"]}')
        frames = _mf.channel_data_to_numpy(res)
        _log.debug(frames.shape)
        return frames

    def write_frames(self,
                     channel_handle: _mf.ChannelHandle,
                     from_dims: str | _t.Sequence,
                     frames: _np.ndarray,
                     *,
                     raw: bool) -> None:
        """Writes ``frames`` to the specified channel.

        .. warning:: Beware of data type
            It is the user's responsbility to make sure that ``frames.dtype``
            is of the channel's data type.
            No limit check, value rescaling or type cast is performed here.
            You can use :class:`hi.Channel` limit methods to get the
            allowed range and :attr:`hi.Channel.dtype` to cast the array.

        :param channel_handle: channel handle
        :param from_dims: starting position of value overwrite.
        :param frames: the array of frames or subslab to write
        :param raw: whether pixel data is raw.
            Depends on how you read or created the frames.
        """
        handle = _mf.fmt_handle(channel_handle)
        i_dim, j_dim, *n_frames = frames.shape
        from_dims = _mf.fmt_dims(from_dims)
        plus_dims = f'{i_dim},{j_dim},{n_frames[0] if n_frames else 1}'
        buffer = _mf.numpy_to_channel_data(frames)
        write = (_api.writeRawChannelDataFromAttachment if raw else
                 _api.writeChannelDataFromAttachment)
        write(self.ws, buffer, handle, from_dims, plus_dims, required=True)

    def online_frames(
            self,
            unit: _mf.UnitHandle | _mf.UnitMeta,
            channel: int,
            *,
            frame_0: int = 0,
            chunk_size: int = 1,
            poll_ms: int = 100,
            timeout_s: int = 60,
            raw: bool = False
    ) -> _t.Iterator[_np.ndarray]:
        """Loads frame one-by-one or polls MESc for new ones.

        :param unit: unit metadata or handle
        :param channel: channel index
        :param frame_0: index of the first frame of the iteration
        :param chunk_size: num of frames to get at the same time
        :param poll_ms: delay between querying metadata if no frames available
        :param timeout_s: timeout of waiting for new frames
        :param raw: return raw frame (offset not compensated)
        :return: generator of frame chunks, each (I × J × chunk_size)
        :raise NodeNotFound: if the channel doesn't exist
        """
        read = (_api.readRawChannelDataToClientsBlob if raw else
                _api.readChannelDataToClientsBlob)
        if isinstance(unit, tuple):
            unit_meta = self.read_unit_meta(unit)
        else:
            unit_meta = unit

        channels = self.read_channels(unit_meta.handle)
        if channel not in (ch.idx for ch in channels):
            raise _err.NodeNotFound('channel', channel)

        frame_shape = unit_meta.dims[:-1]
        frame_orig = [0] * (unit_meta.ndim - 1)
        ch_handle = _mf.fmt_handle((*unit_meta.handle, channel))
        plus_dims_handle = _mf.fmt_dims((*frame_shape, chunk_size))

        prev_n_frames = frame_0
        timeout_0 = time.time()
        while True:
            read_res = read(
                self._ws,
                ch_handle,
                _mf.fmt_dims((*frame_orig, prev_n_frames)),
                plus_dims_handle,
                required=False
            )
            if read_res:
                array = _mf.channel_data_to_numpy(read_res)
                prev_n_frames += chunk_size
                timeout_0 = time.time()
                yield array
            elif time.time() - timeout_0 > timeout_s:
                _log.warning(f'Polling timed out after {timeout_s} s')
                break
            else:
                time.sleep(poll_ms / 1000)

    def create_new_file(self, set_current: bool = True) -> _mf.SessionHandle:
        """Creates a new file with a new measurement session.

        :param set_current: sets the current session to the newly created one
        :return: session handle
        :raise FemtoApiWrapError: if the file creation failed
        """
        prev_session_id = None if set_current else _api.getCurrentSession(self._ws)
        status = _api.createNewFile(self._ws, required=True)
        if not status['succeeded']:
            raise _err.FemtoApiWrapError('createNewFile')
        file_id = _api.getFileList(self._ws, required=True)[-1]
        session_id = f'{file_id},0'
        if set_current:
            _api.setCurrentSession(self._ws, session_id, required=True)
            _log.info(f'Current session changed to {session_id}')
        else:
            _api.setCurrentSession(self._ws, prev_session_id, required=True)
            _log.info(f'Current session remained {prev_session_id}')
        return file_id, 0

    def create_time_series_unit(self,
                                shape: tuple[int, int, int],
                                viewport: _mf.Viewport,
                                tech_type: str,
                                *,
                                z0InMs: float = 0.,
                                zStepInMs: float = 1.
                                ) -> _mf.UnitHandle:
        """Creates a new time series measurement unit with
        :func:`api.createTimeSeriesMUnit`.

        :param shape: (I, J, n_frames) image resolution in pixels with initial
            number of frames
        :param viewport: viewport object
        :param tech_type: ``'resonant'``/``'galvo'``/``'AO'``/``'camera'``
        :param z0InMs: measurement start time offset in ms
        :param zStepInMs: frame duration time in ms (1/frame rate).
        :return: unit handle
        :raise FemtoApiWrapError: if the file creation failed
        """
        res = _api.createTimeSeriesMUnit(
            self._ws,
            xDim=shape[0],
            yDim=shape[1],
            taskXMLParameters=tech_type,
            viewportJson=json.dumps(viewport.to_tree()),
            z0InMs=z0InMs,
            zStepInMs=zStepInMs,
            zDimInitial=shape[2] or 1,
            required=True
        )
        if not res['succeeded']:
            raise _err.FemtoApiWrapError('createTimeSeriesMUnit')
        unit_handle = tuple(map(int, res['addedMUnitIdx'].split(',')))
        return unit_handle  # type: ignore

    def create_channel(self, unit_handle: _mf.UnitHandle, name: str) -> _mf.ChannelHandle:
        """Adds a new channel to the specified measurement unit.

        :param unit_handle: unit handle
        :param name: channel name to be displayed in MESc
        :return: handle of the new channel
        :raise FemtoApiWrapError: if channel creation failed
        """
        res = _api.addChannel(self._ws, _mf.fmt_handle(unit_handle), name, required=True)
        if not res['succeeded']:
            raise _err.FemtoApiWrapError('addChannel')
        channel_handle = tuple(map(int, res['addedChannelIdx'].split(',')))
        return channel_handle  # type: ignore

    def open_file(self, path: str | pathlib.Path) -> _mf.FileHandle:
        """Opens a file by path and returns its handle.

        :param path: file path
        :return: file handle
        """
        result = _api.openFilesAsync(self._ws, _mf.fmt_path(path))
        _utl.waitForAsyncCommand(self._ws, result['id'])
        state = _api.getChildTree(self._ws, required=True)
        handle = state['openedMEScFiles'][-1]['handle'][0]
        return handle

    def find_unit_by_type(self,
                          session_handle: _mf.SessionHandle,
                          tech_type: str,
                          method_type: str) -> _mf.UnitMeta:
        """Finds the firs tunit in a session that has the specified
        method and technology type.
        """
        if not session_handle:
            session_handle = _api.getCurrentSession(self._ws, required=True)
        tree = _api.getSessionMetadata(self._ws, _mf.fmt_handle(session_handle), required=True)
        session = _mf.SessionMeta.from_tree(tree)
        if not session.unit_handles:
            raise _err.NoMeasurementUnit

        for handle in session.unit_handles:
            unit = self.read_unit_meta(handle)
            if unit.method_type == method_type and unit.tech_type == tech_type:
                return unit
        raise _err.NodeNotFound(
            'unit', f'method_type == {method_type} and unit.tech_type == {tech_type}')

    def create_new_test_file(self) -> _mf.FileHandle:
        """Creates a new file and returns the file handle."""
        _api.createNewFile(self._ws, required=True)
        return _api.getFileList(self._ws, required=True)[-1]

    def close_all_files(self, save: bool) -> list[_mf.FileHandle]:
        """Closes all files opened in MESc.

        :param save: whether to save files before closing
        :return: list of closed file ids
        """
        handles = _api.getFileList(self._ws, required=True)
        close = _api.closeFileAndSaveAsync if save else _api.closeFileNoSaveAsync
        closed = []
        for handle in handles:
            result = close(self._ws, handle)
            fid = result['id']
            _log.info(fid)
            _utl.waitForAsyncCommand(self._ws, fid)
            closed.append(fid)
        return closed
