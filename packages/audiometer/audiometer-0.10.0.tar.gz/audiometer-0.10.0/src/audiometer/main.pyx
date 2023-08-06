import cython
import pydub.utils

from libc.math cimport exp, fabs, fmax


cdef float INTEGRATION_TIME = 0.3 / 2
cdef int AMPLITUDE_COEFFICIENT = 2
cdef int RMS_AMPLITUDE_BONUS = 10


@cython.boundscheck(False)
@cython.wraparound(False)
def calculate_rms(segment):
    cdef:
        object samples = segment.get_array_of_samples()
        int sample_rate = segment.frame_rate
        float max_amplitude = segment.max_possible_amplitude
        int channels = segment.channels
        float decay_const = exp(-1 / sample_rate / INTEGRATION_TIME)
        float update_ratio = 1 - decay_const
        int i
        int sample_idx
        float sample
        float max_rms
        float channel_max_rms
        float cur_rms

    max_rms = 0
    for i in range(channels):
        channel_max_rms = 0
        cur_rms = 0
        channel_samples = samples[i::channels]
        for sample_idx in range(len(channel_samples)):
            sample = fabs(channel_samples[sample_idx] / max_amplitude)
            cur_rms = (cur_rms * decay_const) + (sample * sample * update_ratio)
            channel_max_rms = fmax(channel_max_rms, cur_rms)

        max_rms = max(max_rms, channel_max_rms)

    result = pydub.utils.ratio_to_db(max_rms * AMPLITUDE_COEFFICIENT, using_amplitude=False)
    return round(result, 1)
