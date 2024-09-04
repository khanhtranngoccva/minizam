import os

from helpers.analysis.fingerprinting import get_fingerprints, Fingerprint, fingerprint_sample
from helpers.analysis.sample import Sample
from helpers import path
from helpers.analysis.spectrogram import Spectrogram


def initialize_database():
    for parent, dirs, files in os.walk(path.get_content_path()):
        for file in files:
            file_path = os.path.join(parent, file)
            sample = Sample.load(file_path, require_metadata=False)
            sample.save()

            fingerprint_sample(sample)
            print(f"Successfully inserted sample {file_path}")
