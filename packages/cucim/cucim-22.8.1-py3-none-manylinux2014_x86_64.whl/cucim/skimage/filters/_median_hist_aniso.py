import math

import cupy


src = """

#define HIST_SIZE_COARSE 8
#define HIST_SIZE_FINE 32
#define HIST_SIZE 256
#define LOG2_COARSE 3
#define LOG2_FINE 5


__device__ void histogramAddAndSubCoarse(int* H, const int * hist_colAdd,const int * hist_colSub){
    int tx = threadIdx.x;
    if (tx<HIST_SIZE_COARSE){
        H[tx]+=hist_colAdd[tx]-hist_colSub[tx];
    }
}

__device__ void histogramMultipleAddCoarse(int* H, const int * hist_col,int histCount){
    int tx = threadIdx.x;
    if (tx<HIST_SIZE_COARSE){
        int temp=H[tx];
        for(int i=0; i<histCount; i++)
            temp+=hist_col[(i<<LOG2_COARSE)+tx];
        H[tx]=temp;
    }
}

__device__ void histogramClearCoarse(int* H){
    int tx = threadIdx.x;
    if (tx<HIST_SIZE_COARSE){
        H[tx]=0;
    }
}

__device__ void histogramAddCoarse(int* H, const int * hist_col){
    int tx = threadIdx.x;
    if (tx<HIST_SIZE_COARSE){
        H[tx]+=hist_col[tx];
    }
}

__device__ void histogramSubCoarse(int* H, const int * hist_col){
    int tx = threadIdx.x;
    if (tx<HIST_SIZE_COARSE){
        H[tx]-=hist_col[tx];
    }
}


__device__ void histogramAddFine(int* H, const int * hist_col){
    int tx = threadIdx.x;
    if (tx<HIST_SIZE_FINE){
        H[tx]+=hist_col[tx];
    }
}

__device__ void histogramAddAndSubFine(int* H, const int * hist_colAdd,const int * hist_colSub){
    int tx = threadIdx.x;
    if (tx<HIST_SIZE_FINE){
        H[tx]+=hist_colAdd[tx]-hist_colSub[tx];
    }
}


__device__ void histogramClearFine(int* H){
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

#define scanNeighbor(array, range, index, threadIndex)             \
{                                                          \
    int v = 0;                                             \
    if (index <= threadIndex && threadIndex < range)       \
        v = array[threadIndex] + array[threadIndex-index]; \
    __syncthreads();                                       \
    if (index <= threadIndex && threadIndex < range)       \
        array[threadIndex] = v;                            \
}
#define findMedian(array, range, threadIndex, result, count, position) \
if (threadIndex < range)                                       \
{                                                              \
    if (array[threadIndex+1] > position && array[threadIndex] <= position) \
    {                                                          \
        *result = threadIndex+1;                               \
        *count  = array[threadIndex];                          \
    }                                                          \
}

__device__ void histogramMedianParCoarseLookupOnly(int* H,int* Hscan, const int medPos,int* retval, int* countAtMed){
    int tx=threadIdx.x;
    *retval=*countAtMed=0;
    if(tx<HIST_SIZE_COARSE){
        Hscan[tx]=H[tx];
    }
    __syncthreads();
    scanNeighbor(Hscan, HIST_SIZE_COARSE, 1, tx);
    __syncthreads();
    scanNeighbor(Hscan, HIST_SIZE_COARSE, 2, tx);
    __syncthreads();
    scanNeighbor(Hscan, HIST_SIZE_COARSE, 4, tx);
    __syncthreads();

    findMedian(Hscan, HIST_SIZE_COARSE - 1, tx, retval, countAtMed, medPos);
}

__device__ void histogramMedianParFineLookupOnly(int* H,int* Hscan, const int medPos,int* retval, int* countAtMed){
    int tx=threadIdx.x;
    *retval=*countAtMed=0;
    if(tx<HIST_SIZE_FINE){
        Hscan[tx]=H[tx];
    }
    __syncthreads();
    scanNeighbor(Hscan, HIST_SIZE_FINE,  1, tx);
    __syncthreads();
    scanNeighbor(Hscan, HIST_SIZE_FINE,  2, tx);
    __syncthreads();
    scanNeighbor(Hscan, HIST_SIZE_FINE,  4, tx);
    __syncthreads();
    scanNeighbor(Hscan, HIST_SIZE_FINE,  8, tx);
    __syncthreads();
    scanNeighbor(Hscan, HIST_SIZE_FINE, 16, tx);
    __syncthreads();

    findMedian(Hscan, HIST_SIZE_FINE - 1, tx, retval, countAtMed, medPos);
}


extern "C" __global__
void cuRankFilterMultiBlock(unsigned char* src, unsigned char* dest, int* histPar, int* coarseHistGrid, int r0, int r1, int medPos_, int rows, int cols)
{
    __shared__ int HCoarse[HIST_SIZE_COARSE];
    __shared__ int HCoarseScan[HIST_SIZE_FINE];
    __shared__ int HFine[HIST_SIZE_COARSE][HIST_SIZE_FINE];

    __shared__ int luc[HIST_SIZE_COARSE];

    __shared__ int firstBin, countAtMed, retval;

    const int row_stride = cols;  // stride (in elements) along axis 0

    int extraRowThread = rows % gridDim.x;
    int doExtraRow = blockIdx.x < extraRowThread;
    int startRow = 0, stopRow = 0;
    int rowsPerBlock = rows/gridDim.x + doExtraRow;

    // The following code partitions the work to the blocks. Some blocks will do one row more
    // than other blocks. This code is responsible for doing that balancing
    if(doExtraRow){
        startRow=rowsPerBlock*blockIdx.x;
        stopRow=::min(rows, startRow+rowsPerBlock);
    }
    else{
        startRow=(rowsPerBlock+1)*extraRowThread+(rowsPerBlock)*(blockIdx.x-extraRowThread);
        stopRow=::min(rows, startRow+rowsPerBlock);
    }

    int* hist = histPar + cols*HIST_SIZE*blockIdx.x;
    int* histCoarse = coarseHistGrid + cols*HIST_SIZE_COARSE*blockIdx.x;

    if (blockIdx.x==(gridDim.x-1))
        stopRow=rows;
    __syncthreads();
    int initNeeded=0, initVal, initStartRow, initStopRow;

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
                int pos=::min(i,rows-1);
                hist[j*HIST_SIZE+src[pos * row_stride + j]]++;
                histCoarse[j*HIST_SIZE_COARSE+(src[pos * row_stride + j]>>LOG2_FINE)]++;
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
         int possub=::max(0,i-r0-1),posadd=::min(rows-1,i+r0);
         int histPos=threadIdx.x*HIST_SIZE;
         int histCoarsePos=threadIdx.x*HIST_SIZE_COARSE;
         // Going through all the elements of a specific row. Foeach histogram, a value is taken out and
         // one value is added.
         for (int j=threadIdx.x; j<cols; j+=blockDim.x){
            hist[histPos + src[possub * row_stride + j]]--;
            hist[histPos + src[posadd * row_stride + j]]++;
            histCoarse[histCoarsePos + (src[possub * row_stride + j]>>LOG2_FINE)]--;
            histCoarse[histCoarsePos + (src[posadd * row_stride + j]>>LOG2_FINE)]++;

            histPos+=inc;
            histCoarsePos+=incCoarse;
         }
        __syncthreads();

        histogramMultipleAddCoarse(HCoarse,histCoarse, 2*r1+1);
        int cols_m_1=cols-1;

         for(int j=r1;j<cols-r1;j++){
            int possub=::max(j-r1,0);
            int posadd=::min(j+1+r1,cols_m_1);
            int medPos=medPos_;
            __syncthreads();

            histogramMedianParCoarseLookupOnly(HCoarse,HCoarseScan,medPos, &firstBin,&countAtMed);
            __syncthreads();

            int loopIndex = luc[firstBin];
            if (loopIndex <= (j-r1))
            {
                histogramClearFine(HFine[firstBin]);
                for ( loopIndex = j-r1; loopIndex < ::min(j+r1+1,cols); loopIndex++ ){
                    histogramAddFine(HFine[firstBin], hist+(loopIndex*HIST_SIZE+(firstBin<<LOG2_FINE) ) );
                }
            }
            else{
                for ( ; loopIndex < (j+r1+1);loopIndex++ ) {
                    histogramAddAndSubFine(HFine[firstBin],
                    hist+(::min(loopIndex,cols_m_1)*HIST_SIZE+(firstBin<<LOG2_FINE) ),
                    hist+(::max(loopIndex-2*r1-1,0)*HIST_SIZE+(firstBin<<LOG2_FINE) ) );
                    __syncthreads();
                }
            }
            __syncthreads();
            luc[firstBin] = loopIndex;

            int leftOver=medPos-countAtMed;
            if(leftOver>=0){
                histogramMedianParFineLookupOnly(HFine[firstBin],HCoarseScan,leftOver,&retval,&countAtMed);
            }
            else retval=0;
            __syncthreads();

            if (threadIdx.x==0){
                dest[i * row_stride + j]=(firstBin<<LOG2_FINE) + retval;
            }
            histogramAddAndSubCoarse(HCoarse, histCoarse+(int)(posadd<<LOG2_COARSE),histCoarse+(int)(possub<<LOG2_COARSE));

            __syncthreads();
        }
         __syncthreads();
    }
}
"""


def _get_median_rawkernel(footprint_shape, hist_size=256, hist_size_coarse=8):
    return cp.RawKernel(
        code=src,
        name="cuRankFilterMultiBlock"
    )


if False:
    import cupy as cp
    import matplotlib.pyplot as plt
    import skimage.data
    import cucim.skimage.filters

    footprint = cp.ones((5, 15), dtype=cp.uint8)
    image = cp.array(skimage.data.camera()[:340, :420], dtype=cp.uint8)

    def _median(image, footprint=None, partitions=None):

        if not image.flags.c_contiguous:
            image = cp.ascontiguousarray(image)

        if not all(s % 2 == 1 for s in footprint.shape):
            raise ValueError("footprint must have odd size along all axes")

        radii = tuple(s // 2 for s in footprint.shape)
        med_pos = footprint.size // 2

        row_stride = image.shape[1]

        # info = cupy.array((n_signals, n_samples) + x.shape, dtype=index_dtype)
        # info = cp.array(radii + (med_pos,) + image.shape + (row_stride,), dtype=cp.int32)

        # TODO: need to check if we need this exact restriction
        #       likely this one corresponds specifically to OpenCV's boundary handling
        if any(r > s for r, s in zip(radii, image.shape)):
            raise ValueError("footprint radius cannot exceed the image size")

        hist_size = 256  # hardcoded in OpenCV -> corresponds to uint8 dtype
        hist_coarse_size = 8  # hardcoded in OpenCV -> each coarse bin will cover a range of 32 values
        if partitions is None:
            partitions = n_rows // 2  # can be chosen

        # TODO: just drop the unused first dimension (it is present due to OpenCV's 2D GpuMat)
        n_cols = image.shape[1]

        # call a RawKernel with
        grid = (partitions, 1, 1)
        block = (32, 1, 1)  # TODO: always keep this at 32 to match warp size?

        kern = _get_median_rawkernel(
            footprint.shape,
            hist_size=hist_size,
            hist_size_coarse=hist_size_coarse,
        )

        out = cp.empty_like(image)
        hist = cp.zeros((n_cols * hist_size * partitions,), cp.int32);
        coarse_hist = cp.zeros((n_cols * hist_coarse_size * partitions,), cp.int32);
        kern(grid, block, (image, out, hist, coarse_hist, radii[0], radii[1], med_pos, image.shape[0], image.shape[1]))

        out2 = cucim.skimage.filters.median(image, footprint, mode='mirror')
        fig, axes = plt.subplots(3, 1)
        axes[0].imshow(cp.asnumpy(out))
        axes[1].imshow(cp.asnumpy(out2))
        axes[2].imshow(cp.asnumpy(out2.astype(float) - out.astype(float)));
        plt.show()

        return out
