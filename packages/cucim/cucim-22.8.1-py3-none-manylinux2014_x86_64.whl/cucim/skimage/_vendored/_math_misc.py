"""A vendored subset of cupy._math.misc"""


def _fftconv_faster(x, h, mode):
    """
    .. seealso:: :func: `scipy.signal._signaltools._fftconv_faster`

    """
    # TODO(Dahlia-Chehata): replace with GPU-based constants.
    return True


def _choose_conv_method(in1, in2, mode):
    if in1.ndim != 1 or in2.ndim != 1:
        raise NotImplementedError('Only 1d inputs are supported currently')

    if in1.dtype.kind in 'bui' or in2.dtype.kind in 'bui':
        return 'direct'

    if _fftconv_faster(in1, in2, mode):
        return 'fft'

    return 'direct'
