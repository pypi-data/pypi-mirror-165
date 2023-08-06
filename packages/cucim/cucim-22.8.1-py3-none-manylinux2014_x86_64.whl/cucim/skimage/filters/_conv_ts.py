import math

import numpy as np
from cucim.skimage.filters._separable_filtering import _get_constants

shape = (102, 51)
src = np.zeros(shape, dtype=np.float32)
src[src.shape[0]//2, src.shape[1]//2] = 1
dst = np.empty_like(src)
kernel = np.ones((7, ), dtype=np.float32)

# def conv_temp(src, dst, kernel, anchor=None):

anchor = kernel.size // 2

block, patch_per_block, halo_size = get_constants(src.ndim, 0, kernel.size)

grid = (
    math.ceil(src.shape[1] / block[1]), math.ceil(src.shape[0] / block[0]), 1,
)

n_rows, n_cols = src.shape
kernel_size = kernel.size

blockdim_x, blockdim_y, blockdim_z = block
grid_x, grid_y, grid_z = grid
float_dtype = src.dtype

dst_shape = dst.shape
src = src.ravel()
dst = dst.ravel()
dst[:] = np.nan

for blockidx_x in range(grid_x):
    print(f"{blockidx_x=}")
    for blockidx_y in range(grid_y):
        print(f"{blockidx_y=}")
        smem = np.zeros(((patch_per_block + 2 * halo_size) * blockdim_y, blockdim_x), dtype=float_dtype)
        for threadidx_x in range(blockdim_x):
            print(f"{threadidx_x=}")
            for threadidx_y in range(blockdim_y):
                x = blockidx_x * blockdim_x + threadidx_x;
                if (x >= n_cols):
                    break
                yStart = blockidx_y * (blockdim_y * patch_per_block) + threadidx_y;

                # memory is contiguous along last (columns) axis
                row_stride = n_cols; # stride (in elements) along axis 0
                if (blockidx_y > 0):
                    #Upper halo
                    #pragma unroll
                    for j in range(halo_size):
                        print(f"row = {yStart - (halo_size - j) * blockdim_y}")
                        smem[threadidx_y + j * blockdim_y][threadidx_x] = (src[(yStart - (halo_size - j) * blockdim_y) * row_stride + x]);
                else:
                    # TODO, mode support: currently using replicate border condition
                    # Upper halo
                    #pragma unroll
                    for j in range(halo_size):
                        row = yStart - (halo_size - j) * blockdim_y;
                        if (row < 0):
                            row = 0
                        smem[threadidx_y + j * blockdim_y][threadidx_x] = (src[row * row_stride + x]);


                if (blockidx_y + 2 < grid_y):
                    #Main data
                    #pragma unroll
                    for j in range(patch_per_block):
                        smem[threadidx_y + halo_size * blockdim_y + j * blockdim_y][threadidx_x] = (src[(yStart + j * blockdim_y) * row_stride + x]);

                    #Lower halo
                    #pragma unroll
                    for j in range(halo_size):
                        smem[threadidx_y + (patch_per_block + halo_size) * blockdim_y + j * blockdim_y][threadidx_x] = (src[(yStart + (patch_per_block + j) * blockdim_y) * row_stride + x]);
                else:
                    # TODO, mode support: currently using replicate border condition

                    #Main data
                    #pragma unroll
                    for j in range(patch_per_block):
                        row = yStart + j * blockdim_y
                        if (row > n_rows - 1):
                            row = n_rows - 1;
                        smem[threadidx_y + halo_size * blockdim_y + j * blockdim_y][threadidx_x] = (src[row * row_stride + x]);

                    #Lower halo
                    #pragma unroll
                    for j in range(halo_size):
                        row = yStart + (patch_per_block + j) * blockdim_y;
                        if (row > n_rows - 1):
                            row = n_rows - 1
                        smem[threadidx_y + (patch_per_block + halo_size) * blockdim_y + j * blockdim_y][threadidx_x] = (src[row * row_stride + x])


                #pragma unroll
                for j in range(patch_per_block):
                    y = yStart + j * blockdim_y;

                    if (y < n_rows):
                        _sum = 0.0;

                        #pragma unroll
                        for k in range(kernel_size):
                            _sum = _sum + smem[threadidx_y + halo_size * blockdim_y + j * blockdim_y - anchor + k][threadidx_x] * kernel[k];

                        # TODO: replace with appropriate saturating cast to D for dst
                        dst[y * row_stride + x] = _sum;
dst = dst.reshape(shape)
assert not np.any(np.isnan(dst))


if False:

    import math

    import matplotlib.pyplot as plt
    import numpy as np
    from cucim.skimage.filters._separable_conv_shmem import get_constants

    shape = (256, 256)
    src = np.zeros(shape, dtype=np.float32)
    src[src.shape[0]//2, src.shape[1]//2] = 1
    dst = np.empty_like(src)
    dst[:] = np.nan
    kernel = np.ones((7, ), dtype=np.float32)

    # def conv_temp(src, dst, kernel, anchor=None):

    anchor = kernel.size // 2

    block, patch_per_block, halo_size = get_constants(src.ndim, 1, kernel.size)

    grid = (
        math.ceil(src.shape[1] / (block[0] * patch_per_block)), math.ceil(src.shape[0] / block[1]), 1,
    )
    print(f"{src.shape=}\n\t{block=}\n\t{grid=}\n\t{patch_per_block=}\n\t{halo_size=}")

    n_rows, n_cols = src.shape
    kernel_size = kernel.size

    blockdim_x, blockdim_y, blockdim_z = block
    grid_x, grid_y, grid_z = grid
    float_dtype = src.dtype
    bx = np.empty_like(dst)
    by = np.empty_like(dst)
    tx = np.empty_like(dst)
    ty = np.empty_like(dst)
    cnt = 0
    for blockidx_y in range(grid_y):
        for blockidx_x in range(grid_x):
            # print(f"\t{blockidx_y=},{blockidx_x=}")
            smem = np.zeros((blockdim_y, (patch_per_block + 2 * halo_size) * blockdim_x), dtype=float_dtype)
            for threadidx_y in range(blockdim_y):
                for threadidx_x in range(blockdim_x):
                    # print(f"\t\t{threadidx_y=}, {threadidx_x=}")

                    y = blockidx_y * blockdim_y + threadidx_y;
                    xStart = blockidx_x * (patch_per_block * blockdim_x) + threadidx_x;
                    if (y >= n_rows):
                        # print(f"\t\t\tskipped y: {y}")
                        continue  # break
                    for j in range(patch_per_block):
                        x = xStart + j * blockdim_x
                        if (x < n_cols):
                            dst[y, x] = cnt
                            bx[y, x] = blockidx_x
                            by[y, x] = blockidx_y
                            tx[y, x] = threadidx_x
                            ty[y, x] = threadidx_y
                            cnt += 1
                            # print(f"\t\t\t{(y, x)=}")
                        else:
                            continue  # break
                            # print(f"\t\t\tskipped x={x}")

    fig, axes = plt.subplots(1, 5)
    axes[0].imshow(dst)
    axes[1].imshow(bx)
    axes[1].set_title('blockIdx.x')
    axes[2].imshow(by)
    axes[2].set_title('blockIdx.y')
    axes[3].imshow(tx)
    axes[3].set_title('threadIdx.x')
    axes[4].imshow(ty)
    axes[4].set_title('threadIdx.y')
    plt.show()


    """ COLUMN FILTER """
    block, patch_per_block, halo_size = get_constants(src.ndim, 0, kernel.size)

    grid = (
        math.ceil(src.shape[1] / block[0]), math.ceil(src.shape[0] / (block[1] * patch_per_block)), 1,
    )
    print(f"{src.shape=}\n\t{block=}\n\t{grid=}\n\t{patch_per_block=}\n\t{halo_size=}")

    n_rows, n_cols = src.shape
    kernel_size = kernel.size

    blockdim_x, blockdim_y, blockdim_z = block
    grid_x, grid_y, grid_z = grid
    float_dtype = src.dtype

    bx = np.empty_like(dst)
    by = np.empty_like(dst)
    tx = np.empty_like(dst)
    ty = np.empty_like(dst)
    cnt = 0
    for blockidx_y in range(grid_y):
        for blockidx_x in range(grid_x):
            # print(f"\t{blockidx_y=},{blockidx_x=}")
            smem = np.zeros((blockdim_y, (patch_per_block + 2 * halo_size) * blockdim_x), dtype=float_dtype)
            for threadidx_y in range(blockdim_y):
                for threadidx_x in range(blockdim_x):
                    # print(f"\t\t{threadidx_y=}, {threadidx_x=}")

                    x = blockidx_x * blockdim_x + threadidx_x;
                    yStart = blockidx_y * (patch_per_block * blockdim_y) + threadidx_y;
                    if (x >= n_cols):
                        # print(f"\t\t\tskipped y: {y}")
                        continue  # break
                    for j in range(patch_per_block):
                        y = yStart + j * blockdim_y
                        if (y < n_rows):
                            dst[y, x] = cnt
                            bx[y, x] = blockidx_x
                            by[y, x] = blockidx_y
                            tx[y, x] = threadidx_x
                            ty[y, x] = threadidx_y
                            cnt += 1
                            #print(f"\t\t\t{(y, x)=}")
                        else:
                            continue  # break
                            #print(f"\t\t\tskipped x={x}")
    # plt.figure(); plt.imshow(dst); plt.show()

    fig, axes = plt.subplots(1, 5)
    axes[0].imshow(dst)
    axes[1].imshow(bx)
    axes[1].set_title('blockIdx.x')
    axes[2].imshow(by)
    axes[2].set_title('blockIdx.y')
    axes[3].imshow(tx)
    axes[3].set_title('threadIdx.x')
    axes[4].imshow(ty)
    axes[4].set_title('threadIdx.y')
    plt.show()

