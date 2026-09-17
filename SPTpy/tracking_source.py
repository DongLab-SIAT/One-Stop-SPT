"""Persistent association between localization tables and original TIFF frames."""
import json
import os
from pathlib import Path
import tempfile

import numpy as np
import tifffile


def record_path(localization_path):
    return Path(localization_path).with_suffix('.sources.json')


def read_record(localization_path):
    path = record_path(localization_path)
    if not path.exists():
        return {}
    record = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(record, dict) or record.get('version') != 1:
        raise ValueError(f"Unsupported source association: {path}")
    return record


def source_candidates(localization_path, record):
    loc = Path(localization_path).resolve()
    candidates = []
    relative = record.get('relative_path')
    absolute = record.get('absolute_path')
    if isinstance(relative, str) and relative:
        candidates.append(loc.parent / relative)
    if isinstance(absolute, str) and absolute:
        candidates.append(Path(absolute))
    stem = loc.stem.removesuffix('_locs')
    for ext in ('.tif', '.tiff', '.TIF', '.TIFF'):
        candidates.append(loc.with_name(stem + ext))
    return list(dict.fromkeys(p.resolve() for p in candidates))


def save_record(localization_path, image_path, frame_base, source_frame_offset, frame_shape):
    loc = Path(localization_path).resolve()
    image = Path(image_path).resolve()
    record = {
        'version': 1,
        'relative_path': os.path.relpath(image, loc.parent),
        'absolute_path': str(image),
        'frame_base': int(frame_base),
        'source_frame_offset': int(source_frame_offset),
        'frame_shape': [int(v) for v in frame_shape],
    }
    target = record_path(loc)
    # Replace atomically so an interrupted write cannot leave partial JSON.
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=loc.parent,
                                         prefix=target.name + '.', suffix='.tmp', delete=False) as out:
            temporary = Path(out.name)
            json.dump(record, out, ensure_ascii=False, indent=2)
            out.write('\n')
        os.replace(temporary, target)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()
    return record


def normalize_frames(frames, frame_base):
    values = np.asarray(frames)
    if values.ndim != 1 or not values.size:
        raise ValueError('No localization points are available for tracking.')
    if frame_base not in (0, 1):
        raise ValueError('Frame numbering must start at 0 or 1.')
    if not np.isfinite(values).all() or np.any(values != np.floor(values)):
        raise ValueError('Localization frame numbers must be finite integers.')
    indices = values.astype(np.int64) - frame_base
    if np.any(indices < 0):
        raise ValueError('Localization frame numbers do not match the selected numbering.')
    return indices


def normalize_viewer_frame(frame_number, total_frames=None):
    """Return a one-based scalar frame number for image-stack navigation."""
    value = np.asarray(frame_number)
    if value.ndim != 0 or isinstance(frame_number, (bool, np.bool_)):
        raise ValueError('The current image frame must be one integer, not a localization frame array.')
    try:
        numeric = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError('The current image frame must be an integer.') from exc
    if not np.isfinite(numeric) or numeric != np.floor(numeric):
        raise ValueError('The current image frame must be an integer.')
    frame = int(numeric)
    if frame < 1:
        raise ValueError('The current image frame must be at least 1.')
    if total_frames is not None and frame > int(total_frames):
        raise IndexError(f'TIFF has {int(total_frames)} frames; requested frame {frame}.')
    return frame


def open_viewer_source(path):
    """Inspect a grayscale TIFF without decoding the complete image stack."""
    resolved = str(Path(path).resolve())
    with tifffile.TiffFile(resolved) as tif:
        series = tif.series[0]
        if series.keyframe.samplesperpixel != 1 or any(
            axis in 'CS' and size > 1 for axis, size in zip(series.axes, series.shape)
        ):
            raise ValueError('Select a grayscale TIFF stack, not a color image.')
        shape = tuple(int(size) for size in series.shape)
        stack_shape = (1,) + shape if len(shape) == 2 else shape
        if len(stack_shape) != 3 or not all(stack_shape):
            raise ValueError('Expected a grayscale TIFF with dimensions (frames, height, width).')
        stack = None
        if series.dataoffset is not None and series.keyframe.is_memmappable:
            stack = tifffile.memmap(resolved, series=0, mode='r')
            if stack.ndim == 2:
                stack = stack[np.newaxis, ...]
    return {
        'path': resolved,
        'stack': stack,
        'shape': stack_shape,
        'total_frames': stack_shape[0],
        'frame_shape': stack_shape[1:],
    }


def read_viewer_frame(source, frame_number):
    """Read one frame from an image-stack source using one-based numbering."""
    total_frames = int(source['total_frames'])
    frame = normalize_viewer_frame(frame_number, total_frames)
    index = frame - 1
    stack = source.get('stack')
    if stack is not None:
        image = np.asarray(stack[index])
    else:
        with tifffile.TiffFile(source['path']) as tif:
            image = tif.asarray(key=index, series=0)
    image = np.asarray(image)
    if image.ndim != 2 or image.shape != tuple(source['frame_shape']):
        raise ValueError(
            f"Decoded frame shape {image.shape} does not match TIFF metadata {tuple(source['frame_shape'])}."
        )
    return image


def load_validated_source(path, frames, frame_base, source_frame_offset=0, expected_shape=None):
    indices = normalize_frames(frames, frame_base)
    if (not isinstance(source_frame_offset, int) or isinstance(source_frame_offset, bool)
            or source_frame_offset < 0):
        raise ValueError('Invalid original TIFF starting frame in the source association.')
    with tifffile.TiffFile(path) as tif:
        # Series metadata can describe a contiguous stack even when later IFD
        # links cannot be traversed. Do not require every page directory to parse.
        series = tif.series[0]
        if series.keyframe.samplesperpixel != 1 or any(
            axis in 'CS' and size > 1 for axis, size in zip(series.axes, series.shape)
        ):
            raise ValueError('Select the original grayscale TIFF stack, not a color image.')
        shape = tuple(series.shape)
        stack_shape = (1,) + shape if len(shape) == 2 else shape
        if len(stack_shape) != 3 or not all(stack_shape):
            raise ValueError('Expected a grayscale TIFF with dimensions (frames, height, width).')
        if expected_shape is not None and stack_shape[1:] != tuple(expected_shape):
            raise ValueError(f'Image size mismatch: expected {tuple(expected_shape)}, got {stack_shape[1:]}.')
        required = int(indices.max()) + source_frame_offset + 1
        if required > stack_shape[0]:
            raise ValueError(f'TIFF has {stack_shape[0]} frames; these localizations require at least {required}.')

        if series.dataoffset is not None and series.keyframe.is_memmappable:
            # Map the existing file read-only; no writable or temporary TIFF copy.
            stack = tifffile.memmap(path, series=0, mode='r')
        else:
            # Compressed/non-contiguous TIFFs still use the normal decoder.
            stack = tif.asarray(series=0)
    if stack.ndim == 2:
        stack = stack[np.newaxis, ...]
    if stack.shape != stack_shape:
        raise ValueError(f'Decoded TIFF shape {stack.shape} does not match its metadata {stack_shape}.')
    return {'path': str(Path(path).resolve()), 'stack': stack,
            'frame_base': frame_base, 'source_frame_offset': source_frame_offset}
