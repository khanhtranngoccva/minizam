import mimetypes
import os

import matplotlib
import numpy as np
from matplotlib import pyplot
from scipy.io import wavfile
from scipy import signal


class Spectrogram:
    def __init__(self, file_path):
        _, file_extension = os.path.splitext(file_path)
        reference_extension = mimetypes.guess_extension("audio/wav")
        if reference_extension != file_extension:
            raise Exception("Invalid extension for wav file")
        sample_rate, series = wavfile.read(file_path)
        # Merge left and right channels.
        self.series = np.mean(series, axis=1)
        self.sample_rate = sample_rate
        self.frequencies, self.segment_times, self.spectrogram = signal.spectrogram(
            self.series,
            fs=self.sample_rate,
            # Each segment is 10 seconds long, with a 9-second overlap.
            nperseg=10 * sample_rate,
            noverlap=9 * sample_rate,
            window="hamming",
        )

    def plot(self):
        pyplot.pcolormesh(self.segment_times, self.frequencies, self.spectrogram,
                          norm=matplotlib.colors.Normalize(0, 1))
        pyplot.ylabel('Frequency [Hz]')
        pyplot.xlabel('Time [sec]')
        pyplot.show()
