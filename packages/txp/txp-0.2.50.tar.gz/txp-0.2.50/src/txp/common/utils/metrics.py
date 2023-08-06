import logging

import numpy as np
import scipy.signal as signal
from scipy.integrate import cumtrapz
import sys


def peak(data):
    return np.absolute(data).max()


def rms(data):
    return np.sqrt(np.power(data, 2).mean())


def standard_deviation(data):
    return np.std(data)


def crest_factor(data):
    cf = peak(data) / rms(data)
    if np.isnan(cf):
        cf = sys.float_info.max
        logging.warning("crest factor to high returning maximum possible value")
    return cf


def get_psd(data, sampling_frequency, window="hanning"):
    bin_width = sampling_frequency / len(data)
    return signal.welch(data, fs=sampling_frequency, nperseg=sampling_frequency / bin_width, window=window, axis=0)


def integrate(y, x=None, sampling_frequency=1):
    if x is not None:
        return cumtrapz(y, x=x)
    else:
        return cumtrapz(y, dx=sampling_frequency)



