import math

import cupy as cp
import matplotlib.pyplot as plt

from cucim.skimage.filters._separable_filtering import _get_separable_conv_kernel
from cucim.skimage.filters._separable_filtering import get_constants

d = cp.cuda.Device()

# src = cp.zeros((768*4, 512*4), dtype=cp.float32)
# src = cp.zeros((768*4, 512*4), dtype=cp.float32)
src = cp.zeros((16, 16), dtype=cp.float32)
src[src.shape[0]//2, src.shape[1]//2] = 1
# kernel = cp.ones((15, ), dtype=cp.float32)
kernel = cp.array([1, 2, 3, 4, 5], dtype=cp.float32)
anchor = kernel.size // 2
# fig, axes = plt.subplots(1, 2)
patch_per_block = 4
for axis in [0]:
    block, patch_per_block, halo_size = get_constants(src.ndim, axis, kernel.size, anchor, patch_per_block=patch_per_block)
    print(f"{halo_size=}")
    conv_axis_kernel, block, patch_per_block = _get_separable_conv_kernel(
        kernel.size,
        axis=axis,
        ndim=src.ndim,
        image_c_type='float',
        kernel_c_type='float',
        output_c_type='float',
        anchor=anchor,
        patch_per_block=patch_per_block)
    print(f"shared_size_bytes = {conv_axis_kernel.shared_size_bytes}")
    print(f"num_regs = {conv_axis_kernel.num_regs}")

    if axis == 0:
        # column filter
        grid = (
            math.ceil(src.shape[1] / block[0]),
            math.ceil(src.shape[0] / (block[1] * patch_per_block)),
            1,
        )
    elif axis == 1:
        # row filter
        grid = (
            math.ceil(src.shape[1] / (block[0] * patch_per_block)),
            math.ceil(src.shape[0] / block[1]),
            1,
        )
    # out = k(src, kernel, anchor, dst, size=src.size)
    dst = cp.empty_like(src)
    conv_axis_kernel(grid, block, (src, dst, kernel, anchor, src.shape[0], src.shape[1]))
    # axes[axis].imshow(cp.asnumpy(dst))
# plt.show()
