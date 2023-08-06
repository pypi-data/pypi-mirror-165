import math
from textwrap import dedent

import cupy as cp
import numpy as np

from .._shared.utils import _to_np_mode

try:
    # Device Attributes require CuPy > 6.0.b3
    d = cp.cuda.Device()
    cuda_MaxBlockDimX = d.attributes["MaxBlockDimX"]
    cuda_MaxGridDimX = d.attributes["MaxGridDimX"]
except (cp.cuda.runtime.CUDARuntimeError, AttributeError):
    # guess
    cuda_MaxBlockDimX = 1024
    cuda_MaxGridDimX = 2147483647


def get_hist_dtype(footprint_shape, force_int32=False):
    max_possible_histogram_value = math.prod(footprint_shape)

    if max_possible_histogram_value < 127 and not force_int32:
        return 'signed char', cp.int8
    else:
        return 'int', cp.int32


def gen_global_definitions(hist_int_t, hist_size=256, hist_size_coarse=8):

    if hist_size % hist_size_coarse != 0:
        raise ValueError(
            "`hist_size` must be a multiple of `hist_size_coarse`"
        )
    hist_size_fine = hist_size // hist_size_coarse
    log2_coarse = round(np.log2(hist_size_coarse))
    log2_fine = round(np.log2(hist_size_fine))

    global_defs = f"""
#define HIST_SIZE {hist_size}
#define HIST_SIZE_COARSE {hist_size_coarse}
#define HIST_SIZE_FINE {hist_size_fine}
#define HIST_INT_T {hist_int_t}
#define LOG2_COARSE {log2_coarse}
#define LOG2_FINE {log2_fine}
    """
    return global_defs


preamble_common = """

__device__ void histogramAddAndSubCoarse(HIST_INT_T* H, const HIST_INT_T* hist_colAdd, const HIST_INT_T* hist_colSub){
    int tx = threadIdx.x;
    if (tx<HIST_SIZE_COARSE){
        H[tx]+=hist_colAdd[tx]-hist_colSub[tx];
    }
}

__device__ void histogramMultipleAddCoarse(HIST_INT_T* H, const HIST_INT_T* hist_col, int histCount){
    int tx = threadIdx.x;
    if (tx<HIST_SIZE_COARSE){
        HIST_INT_T temp=H[tx];
        for(int i=0; i<histCount; i++)
            temp+=hist_col[(i<<LOG2_COARSE)+tx];
        H[tx]=temp;
    }
}

__device__ void histogramClearCoarse(HIST_INT_T* H){
    int tx = threadIdx.x;
    if (tx<HIST_SIZE_COARSE){
        H[tx]=0;
    }
}

__device__ void histogramAddCoarse(HIST_INT_T* H, const HIST_INT_T* hist_col){
    int tx = threadIdx.x;
    if (tx<HIST_SIZE_COARSE){
        H[tx]+=hist_col[tx];
    }
}

__device__ void histogramSubCoarse(HIST_INT_T* H, const HIST_INT_T* hist_col){
    int tx = threadIdx.x;
    if (tx<HIST_SIZE_COARSE){
        H[tx]-=hist_col[tx];
    }
}

__device__ void histogramAddFine(HIST_INT_T* H, const HIST_INT_T* hist_col){
    int tx = threadIdx.x;
    if (tx<HIST_SIZE_FINE){
        H[tx]+=hist_col[tx];
    }
}

__device__ void histogramAddAndSubFine(HIST_INT_T* H, const HIST_INT_T* hist_colAdd, const HIST_INT_T* hist_colSub){
    int tx = threadIdx.x;
    if (tx<HIST_SIZE_FINE){
        H[tx]+=hist_colAdd[tx]-hist_colSub[tx];
    }
}

__device__ void histogramClearFine(HIST_INT_T* H){
    int tx = threadIdx.x;
    if (tx<HIST_SIZE_FINE){
        H[tx]=0;
    }
}

__device__ void lucClearCoarse(int* luc){
    int tx = threadIdx.x;
    if (tx<HIST_SIZE_COARSE)
        luc[tx]=0;
}

"""  # noqa


def gen_preamble_median(hist_size_coarse, hist_size_fine):
    n_log2_coarse = math.log2(hist_size_coarse)
    if hist_size_coarse < 2 or n_log2_coarse % 1.0 != 0:
        raise ValueError("hist_size_coarse must be a positive power of 2")

    n_log2_fine = math.log2(hist_size_fine)
    if hist_size_fine < 2 or n_log2_fine % 1.0 != 0:
        raise ValueError("hist_size_fine must be a positive power of 2")

    ops = """

        #define scanNeighbor(array, range, index, threadIndex)             \\
                {                                                          \\
                    HIST_INT_T v = 0;                                             \\
                    if (index <= threadIndex && threadIndex < range)       \\
                        v = array[threadIndex] + array[threadIndex-index]; \\
                    __syncthreads();                                       \\
                    if (index <= threadIndex && threadIndex < range)       \\
                        array[threadIndex] = v;                            \\
                }

        #define findMedian(array, range, threadIndex, result, count, position) \\
                if (threadIndex < range)                                       \\
                {                                                              \\
                    if (array[threadIndex+1] > position && array[threadIndex] <= position) \\
                    {                                                          \\
                        *result = threadIndex+1;                               \\
                        *count  = array[threadIndex];                          \\
                    }                                                          \\
                }

        __device__ void histogramMedianParCoarseLookupOnly(HIST_INT_T* H, HIST_INT_T* Hscan, const int medPos, int* retval, int* countAtMed){
            int tx=threadIdx.x;
            *retval=*countAtMed=0;
            if(tx<HIST_SIZE_COARSE){
                Hscan[tx]=H[tx];
            }
            __syncthreads();\n"""  # noqa

    for d in range(round(n_log2_coarse)):
        ops += f"""
            scanNeighbor(Hscan, {hist_size_coarse}, {2**d}, tx);
            __syncthreads();"""
    ops += f"""
            findMedian(Hscan, {hist_size_coarse - 1}, tx, retval, countAtMed, medPos);
        }}"""  # noqa

    ops += """

        __device__ void histogramMedianParFineLookupOnly(HIST_INT_T* H, HIST_INT_T* Hscan, const int medPos, int* retval, int* countAtMed){
            int tx=threadIdx.x;
            *retval=*countAtMed=0;
            if(tx<HIST_SIZE_FINE){
                Hscan[tx]=H[tx];
            }
            __syncthreads();\n"""  # noqa

    for d in range(round(n_log2_fine)):
        ops += f"""
            scanNeighbor(Hscan, {hist_size_fine}, {2**d}, tx);
            __syncthreads();"""
    ops += f"""
            findMedian(Hscan, {hist_size_fine - 1}, tx, retval, countAtMed, medPos);
        }}\n"""  # noqa

    return dedent(ops)


def gen_median_kernel_preamble(
    hist_int_t, hist_size=256, hist_size_coarse=8
):
    src = gen_global_definitions(
        hist_int_t,
        hist_size=hist_size,
        hist_size_coarse=hist_size_coarse,
    )
    src += preamble_common
    hist_size_fine = hist_size // hist_size_coarse
    src += gen_preamble_median(
        hist_size_coarse=hist_size_coarse, hist_size_fine=hist_size_fine
    )
    return src


rank_filter_kernel = """

extern "C" __global__
void cuRankFilterMultiBlock(unsigned char* src, unsigned char* dest, HIST_INT_T* histPar, HIST_INT_T* coarseHistGrid, int r0, int r1, int medPos_, int rows, int cols)
{
    __shared__ HIST_INT_T HCoarse[HIST_SIZE_COARSE];
    __shared__ HIST_INT_T HCoarseScan[HIST_SIZE_FINE];
    __shared__ HIST_INT_T HFine[HIST_SIZE_COARSE][HIST_SIZE_FINE];

    __shared__ int luc[HIST_SIZE_COARSE];

    __shared__ int firstBin, countAtMed, retval;

    // extract values from params array
    const int row_stride = cols;  // stride (in elements) along axis 0

    int extraRowThread = rows % gridDim.x;
    int doExtraRow = blockIdx.x < extraRowThread;
    int startRow = 0, stopRow = 0;
    int rowsPerBlock = rows/gridDim.x + doExtraRow;

    // The following code partitions the work to the blocks. Some blocks will do one row more
    // than other blocks. This code is responsible for doing that balancing
    if(doExtraRow){
        startRow=rowsPerBlock*blockIdx.x;
        stopRow=min(rows, startRow+rowsPerBlock);
    }
    else{
        startRow=(rowsPerBlock+1)*extraRowThread+(rowsPerBlock)*(blockIdx.x-extraRowThread);
        stopRow=min(rows, startRow+rowsPerBlock);
    }

    HIST_INT_T* hist = histPar + cols*HIST_SIZE*blockIdx.x;
    HIST_INT_T* histCoarse = coarseHistGrid + cols*HIST_SIZE_COARSE*blockIdx.x;

    if (blockIdx.x==(gridDim.x-1))
        stopRow=rows;
    __syncthreads();
    int initNeeded=0, initStartRow, initStopRow;
    HIST_INT_T initVal;

    if(blockIdx.x==0){
        initNeeded=1; initVal=r0+2; initStartRow=1;  initStopRow=r0;
    }
    else if (startRow<(r0+2)){
        initNeeded=1; initVal=r0+2-startRow; initStartRow=1; initStopRow=r0+startRow;
    }
    else{
        initNeeded=0; initVal=0; initStartRow=startRow-(r0+1);   initStopRow=r0+startRow;
    }
   __syncthreads();


    // In the original algorithm an initialization phase was required as part of the window was outside the
    // image. In this parallel version, the initializtion is required for all thread blocks that part
    // of the median filter is outside the window.
    // For all threads in the block the same code will be executed.
    if (initNeeded){
        for (int j=threadIdx.x; j<(cols); j+=blockDim.x){
            hist[j*HIST_SIZE + src[j]]=initVal;
            histCoarse[j*HIST_SIZE_COARSE + (src[j]>>LOG2_FINE)]=initVal;
        }
    }
    __syncthreads();

    // For all remaining rows in the median filter, add the values to the the histogram
    for (int j=threadIdx.x; j<cols; j+=blockDim.x){
        for(int i=initStartRow; i<initStopRow; i++){
            int pos=min(i,rows-1);
            hist[j*HIST_SIZE + src[pos * row_stride + j]]++;
            histCoarse[j*HIST_SIZE_COARSE + (src[pos * row_stride + j]>>LOG2_FINE)]++;
        }
    }
    __syncthreads();
     // Going through all the rows that the block is responsible for.
     int inc=blockDim.x*HIST_SIZE;
     int incCoarse=blockDim.x*HIST_SIZE_COARSE;
     for(int i=startRow; i< stopRow; i++){
         // For every new row that is started the global histogram for the entire window is restarted.

         histogramClearCoarse(HCoarse);
         lucClearCoarse(luc);
         // Computing some necessary indices
         int possub=max(0,i-r0-1),posadd=min(rows-1,i+r0);
         int histPos=threadIdx.x*HIST_SIZE;
         int histCoarsePos=threadIdx.x*HIST_SIZE_COARSE;
         // Going through all the elements of a specific row. Foeach histogram, a value is taken out and
         // one value is added.
         for (int j=threadIdx.x; j<cols; j+=blockDim.x){
            hist[histPos+ src[possub * row_stride + j] ]--;
            hist[histPos+ src[posadd * row_stride + j] ]++;
            histCoarse[histCoarsePos+ (src[possub * row_stride + j]>>LOG2_FINE) ]--;
            histCoarse[histCoarsePos+ (src[posadd * row_stride + j]>>LOG2_FINE) ]++;

            histPos+=inc;
            histCoarsePos+=incCoarse;
         }
        __syncthreads();

        histogramMultipleAddCoarse(HCoarse, histCoarse, 2*r1+1);
        int cols_m_1=cols-1;

        for(int j=r1;j<cols-r1;j++){
            int possub=max(j-r1, 0);
            int posadd=min(j+1+r1, cols_m_1);
            int medPos=medPos_;
            __syncthreads();

            histogramMedianParCoarseLookupOnly(HCoarse, HCoarseScan, medPos, &firstBin, &countAtMed);
            __syncthreads();

            int loopIndex = luc[firstBin];
            if (loopIndex <= (j-r1))
            {
                histogramClearFine(HFine[firstBin]);
                for ( loopIndex = j-r1; loopIndex < min(j+r1+1,cols); loopIndex++ ){
                    histogramAddFine(HFine[firstBin], hist+(loopIndex*HIST_SIZE+(firstBin<<LOG2_FINE) ) );
                }
            }
            else{
                for ( ; loopIndex < (j+r1+1);loopIndex++ ) {
                    histogramAddAndSubFine(HFine[firstBin],
                    hist+(min(loopIndex,cols_m_1)*HIST_SIZE+(firstBin<<LOG2_FINE) ),
                    hist+(max(loopIndex-2*r1-1,0)*HIST_SIZE+(firstBin<<LOG2_FINE) ) );
                    __syncthreads();
                }
            }
            __syncthreads();
            luc[firstBin] = loopIndex;

            int leftOver=medPos-countAtMed;
            if(leftOver>=0){
                histogramMedianParFineLookupOnly(HFine[firstBin], HCoarseScan, leftOver, &retval, &countAtMed);
            }
            else retval=0;
            __syncthreads();

            if (threadIdx.x==0){
                dest[i * row_stride + j]=(firstBin<<LOG2_FINE) + retval;
            }
            histogramAddAndSubCoarse(HCoarse, histCoarse+(int)(posadd<<LOG2_COARSE), histCoarse+(int)(possub<<LOG2_COARSE));

            __syncthreads();
        }
         __syncthreads();
    }
}
"""  # noqa


# @cp.memoize(for_each_device=True)
def _get_median_rawkernel(hist_int_t, hist_size=256, hist_size_coarse=8):
    preamble = gen_median_kernel_preamble(
        hist_int_t,
        hist_size=hist_size,
        hist_size_coarse=hist_size_coarse,
    )
    name = (
        f"cuRankFilterMultiBlock_{hist_int_t}_{hist_size}_{hist_size_coarse}"
    )
    return cp.RawKernel(
        code=preamble + rank_filter_kernel,
        name=name,
    )


def _can_use_histogram_based_median(image, footprint):
    """Validate compatibility with histogram-based median.

    Parameters
    ----------
    image : cupy.ndarray
        The image to filter.
    footprint : cupy.ndarray
        The filter footprint.

    Returns
    -------
    compatible : bool
        Indicates whether the provided image and footprint are compatible with
        the histogram-based median.
    reason : str
        Description of the reason for the incompatibility
    """
    # only 2D uint8 images are supported
    if image.ndim != 2:
        return False, "only 2D images are supported"
    if image.dtype != np.uint8:
        return False, "only 8-bit unsigned images are supported"

    # only odd-sized footprints are supported
    if not all(s % 2 == 1 for s in footprint.shape):
        return False, "footprint must have odd size on both axes"

    if any(s == 1 for s in footprint.shape):
        return False, "footprint must have size >= 3"

    # footprint radius can't be larger than the image
    # TODO: need to check if we need this exact restriction
    #       (may be specific to OpenCV's boundary handling)
    radii = tuple(s // 2 for s in footprint.shape)
    if any(r > s for r, s in zip(radii, image.shape)):
        return False, "footprint half-width cannot exceed the image extent"

    # only fully populated footprint is supported
    if not np.all(footprint):  # synchronizes!
        return False
    return True, "footprint must be 1 everywhere"


def _median_hist(image, footprint, output=None, mode='mirror', cval=0):

    if output is not None:
        raise NotImplementedError("TODO")

    compatible_image, reason = _can_use_histogram_based_median(
        image, footprint
    )
    if not compatible_image:
        raise ValueError(reason)

    if not image.flags.c_contiguous:
        image = cp.ascontiguousarray(image)

    radii = tuple(s // 2 for s in footprint.shape)
    med_pos = footprint.size // 2

    n_rows, n_cols = image.shape[:2]

    hist_size = 256  # hardcoded in OpenCV -> corresponds to uint8 dtype
    hist_size_coarse = 8  # hardcoded in OpenCV -> each coarse bin will cover a range of 32 values  # noqa

    partitions = 128
    if partitions > image.shape[0]:
        partitions = n_rows // 2  # can be chosen
    grid = (partitions, 1, 1)
    block = (32, 1, 1)  # TODO: always keep this at 32 to match warp size?

    hist_int_t, _ = get_hist_dtype(footprint.shape)
    kern = _get_median_rawkernel(
        hist_int_t,
        hist_size=hist_size,
        hist_size_coarse=hist_size_coarse,
    )

    autopad = True
    # don't have to pad along columns if mode is already 'nearest'
    pad_both_axes = mode != 'nearest'
    if autopad:
        if pad_both_axes:
            npad = tuple((r, r) for r in radii)
        else:
            npad = ((0, 0),) * (image.ndim - 1) + ((radii[-1], radii[-1]),)
        mode = _to_np_mode(mode)
        if mode == 'constant':
            pad_kwargs = dict(mode=mode, constant_values=cval)
        else:
            pad_kwargs = dict(mode=mode)
        image = cp.pad(image, npad, **pad_kwargs)
        # must update n_rows, n_cols after padding!
        n_rows, n_cols = image.shape[:2]

    out = cp.empty_like(image)
    _, hist_dtype = get_hist_dtype(footprint.shape)
    hist = cp.zeros((n_cols * hist_size * partitions,), hist_dtype)
    coarse_hist = cp.zeros(
        (n_cols * hist_size_coarse * partitions,), hist_dtype
    )
    kern(
        grid,
        block,
        (
            image, out, hist, coarse_hist, radii[0], radii[1], med_pos,
            image.shape[0], image.shape[1],
        ),
    )
    if autopad:
        if pad_both_axes:
            out_sl = tuple(slice(r, -r) for r in radii)
            out = out[out_sl]
        else:
            out = out[..., radii[-1]:-radii[-1]]
    return out
