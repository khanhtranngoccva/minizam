import pytest
import numpy as np
from helpers import path
from helpers.analysis.fingerprinting import get_fingerprints
from helpers.analysis.spectrogram import Spectrogram


def test_fingerprint():
    spectrogram = Spectrogram(path.get_content_path("A Tender Feeling.wav"))
    fingerprints = get_fingerprints(spectrogram)[0]
    fingerprints_reference = [
        np.float64(0.6158323632130385),
        np.float64(0.6015125072716696),
        np.float64(0.8077929630706601),
        np.float64(0.9613315888937345),
        np.float64(0.606148702667345),
        np.float64(0.5410807078745594),
        np.float64(0.5709769436217955),
        np.float64(0.5033839333569528)
    ]

    for i in range(8):
        reference_element = fingerprints_reference[i]
        computed_element = fingerprints[i]
        assert computed_element == reference_element

    print(fingerprints_reference)
