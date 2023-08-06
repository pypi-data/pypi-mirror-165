import math

import cupy


src = """

__device__ void histogramAddAndSub8(int* H, const int * hist_colAdd,const int * hist_colSub){
    int tx = threadIdx.x;
    if (tx<8){
        H[tx]+=hist_colAdd[tx]-hist_colSub[tx];
    }
}

__device__ void histogramMultipleAdd8(int* H, const int * hist_col,int histCount){
    int tx = threadIdx.x;
    if (tx<8){
        int temp=H[tx];
        for(int i=0; i<histCount; i++)
            temp+=hist_col[(i<<3)+tx];
        H[tx]=temp;
    }
}

__device__ void histogramClear8(int* H){
    int tx = threadIdx.x;
    if (tx<8){
        H[tx]=0;
    }
}

__device__ void histogramAdd8(int* H, const int * hist_col){
    int tx = threadIdx.x;
    if (tx<8){
        H[tx]+=hist_col[tx];
    }
}

__device__ void histogramSub8(int* H, const int * hist_col){
    int tx = threadIdx.x;
    if (tx<8){
        H[tx]-=hist_col[tx];
    }
}


__device__ void histogramAdd32(int* H, const int * hist_col){
    int tx = threadIdx.x;
    if (tx<32){
        H[tx]+=hist_col[tx];
    }
}

__device__ void histogramAddAndSub32(int* H, const int * hist_colAdd,const int * hist_colSub){
    int tx = threadIdx.x;
    if (tx<32){
        H[tx]+=hist_colAdd[tx]-hist_colSub[tx];
    }
}


__device__ void histogramClear32(int* H){
    int tx = threadIdx.x;
    if (tx<32){
        H[tx]=0;
    }
}

__device__ void lucClear8(int* luc){
    int tx = threadIdx.x;
    if (tx<8)
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

__device__ void histogramMedianPar8LookupOnly(int* H,int* Hscan, const int medPos,int* retval, int* countAtMed){
    int tx=threadIdx.x;
    *retval=*countAtMed=0;
    if(tx<8){
        Hscan[tx]=H[tx];
    }
    __syncthreads();
    scanNeighbor(Hscan, 8, 1, tx);
    __syncthreads();
    scanNeighbor(Hscan, 8, 2, tx);
    __syncthreads();
    scanNeighbor(Hscan, 8, 4, tx);
    __syncthreads();

    findMedian(Hscan, 7, tx, retval, countAtMed, medPos);
}

__device__ void histogramMedianPar32LookupOnly(int* H,int* Hscan, const int medPos,int* retval, int* countAtMed){
    int tx=threadIdx.x;
    *retval=*countAtMed=0;
    if(tx<32){
        Hscan[tx]=H[tx];
    }
    __syncthreads();
    scanNeighbor(Hscan, 32,  1, tx);
    __syncthreads();
    scanNeighbor(Hscan, 32,  2, tx);
    __syncthreads();
    scanNeighbor(Hscan, 32,  4, tx);
    __syncthreads();
    scanNeighbor(Hscan, 32,  8, tx);
    __syncthreads();
    scanNeighbor(Hscan, 32, 16, tx);
    __syncthreads();

    findMedian(Hscan, 31, tx, retval, countAtMed, medPos);
}


extern "C" __global__
void cuRankFilterMultiBlock(unsigned char* src, unsigned char* dest, int* histPar, int* coarseHistGrid, int r, int medPos_, int rows, int cols)
{
    __shared__ int HCoarse[8];
    __shared__ int HCoarseScan[32];
    __shared__ int HFine[8][32];

    __shared__ int luc[8];

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
        stopRow=min(rows, startRow+rowsPerBlock);
    }
    else{
        startRow=(rowsPerBlock+1)*extraRowThread+(rowsPerBlock)*(blockIdx.x-extraRowThread);
        stopRow=min(rows, startRow+rowsPerBlock);
    }

    int* hist = histPar + cols*256*blockIdx.x;
    int* histCoarse = coarseHistGrid + cols*8*blockIdx.x;

    if (blockIdx.x==(gridDim.x-1))
        stopRow=rows;
    __syncthreads();
    int initNeeded=0, initVal, initStartRow, initStopRow;

    if(blockIdx.x==0){
        initNeeded=1; initVal=r+2; initStartRow=1;  initStopRow=r;
    }
    else if (startRow<(r+2)){
        initNeeded=1; initVal=r+2-startRow; initStartRow=1; initStopRow=r+startRow;
    }
    else{
        initNeeded=0; initVal=0; initStartRow=startRow-(r+1);   initStopRow=r+startRow;
    }
    __syncthreads();


    // In the original algorithm an initialization phase was required as part of the window was outside the
    // image. In this parallel version, the initializtion is required for all thread blocks that part
    // of the median filter is outside the window.
    // For all threads in the block the same code will be executed.
    if (initNeeded){
        for (int j=threadIdx.x; j<(cols); j+=blockDim.x){
            hist[j*256+src[j]]=initVal;
            histCoarse[j*8+(src[j]>>5)]=initVal;
        }
    }
    __syncthreads();

    // For all remaining rows in the median filter, add the values to the the histogram
    for (int j=threadIdx.x; j<cols; j+=blockDim.x){
        for(int i=initStartRow; i<initStopRow; i++){
                int pos=::min(i,rows-1);
                hist[j*256 + src[pos * row_stride + j]]++;
                histCoarse[j*8 + (src[pos * row_stride + j]>>5)]++;
            }
    }
    __syncthreads();

    // Going through all the rows that the block is responsible for.
    int inc=blockDim.x*256;
    int incCoarse=blockDim.x*8;
    for(int i=startRow; i< stopRow; i++){
         // For every new row that is started the global histogram for the entire window is restarted.

         histogramClear8(HCoarse);
         lucClear8(luc);
         // Computing some necessary indices
         int possub=::max(0,i-r-1),posadd=::min(rows-1,i+r);
         int histPos=threadIdx.x*256;
         int histCoarsePos=threadIdx.x*8;
         // Going through all the elements of a specific row. Foeach histogram, a value is taken out and
         // one value is added.
         for (int j=threadIdx.x; j<cols; j+=blockDim.x){
            hist[histPos+ src[possub * row_stride + j] ]--;
            hist[histPos+ src[posadd * row_stride + j] ]++;
            histCoarse[histCoarsePos+ (src[possub * row_stride + j]>>5) ]--;
            histCoarse[histCoarsePos+ (src[posadd * row_stride + j]>>5) ]++;

            histPos+=inc;
            histCoarsePos+=incCoarse;
         }
        __syncthreads();

        histogramMultipleAdd8(HCoarse,histCoarse, 2*r+1);
        int cols_m_1=cols-1;

        for(int j=r;j<cols-r;j++){
            int possub=::max(j-r,0);
            int posadd=::min(j+1+r,cols_m_1);
            int medPos=medPos_;
            __syncthreads();

            histogramMedianPar8LookupOnly(HCoarse,HCoarseScan,medPos, &firstBin,&countAtMed);
            __syncthreads();

            int loopIndex = luc[firstBin];
            if (loopIndex <= (j-r))
            {
                histogramClear32(HFine[firstBin]);
                for ( loopIndex = j-r; loopIndex < min(j+r+1,cols); loopIndex++ ){
                    histogramAdd32(HFine[firstBin], hist+(loopIndex*256+(firstBin<<5) ) );
                }
            }
            else{
                for ( ; loopIndex < (j+r+1);loopIndex++ ) {
                    histogramAddAndSub32(HFine[firstBin],
                    hist+(::min(loopIndex,cols_m_1)*256+(firstBin<<5) ),
                    hist+(::max(loopIndex-2*r-1,0)*256+(firstBin<<5) ) );
                    __syncthreads();
                }
            }
            __syncthreads();
            luc[firstBin] = loopIndex;

            int leftOver=medPos-countAtMed;
            if(leftOver>=0){
                histogramMedianPar32LookupOnly(HFine[firstBin],HCoarseScan,leftOver,&retval,&countAtMed);
            }
            else retval=0;
            __syncthreads();

            if (threadIdx.x==0){
                dest[i * row_stride + j]=(firstBin<<5) + retval;
            }
            histogramAddAndSub8(HCoarse, histCoarse+(int)(posadd<<3),histCoarse+(int)(possub<<3));

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

    footprint = cp.ones((9, 9), dtype=cp.uint8)
    image = cp.array(skimage.data.camera(), dtype=cp.uint8)
    partitions = 128
    hist_size = 256
    hist_size_coarse = 8

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
            partitions = image.shape[0] // 2  # can be chosen

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
        kern(grid, block, (image, out, hist, coarse_hist, radii[0], med_pos, image.shape[0], image.shape[1]))

        out2 = cucim.skimage.filters.median(image, footprint, mode='mirror')
        fig, axes = plt.subplots(3, 1)
        axes[0].imshow(cp.asnumpy(out))
        axes[1].imshow(cp.asnumpy(out2))
        axes[2].imshow(cp.asnumpy(out2.astype(float) - out.astype(float)));
        plt.show()
        return out
