"""Shared intensity preprocessing for GUI and notebook segmentation."""
import numpy as np

def to_uint8_view(img):
    arr = np.asarray(img, dtype=np.float64)
    finite = np.isfinite(arr)
    out = np.zeros(arr.shape, dtype=np.uint8)
    if not finite.any():
        return out
    values = arr[finite]
    v1, v2 = np.percentile(values, (1, 99))
    if v2 <= v1:
        v1, v2 = float(values.min()), float(values.max())
    if v2 <= v1:
        return out  # 恒定图像没有对比度，避免除零。
    out[finite] = np.clip((values - v1) * 255.0 / (v2 - v1), 0, 255).astype(np.uint8)
    return out
