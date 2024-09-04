import decimal

import numpy as np
from scipy.spatial import distance
from helpers import database
from helpers.analysis.spectrogram import Spectrogram


class Fingerprint:
    def __init__(self, sample_id, offset, fingerprint, *_, _id=None):
        self.fingerprint = fingerprint
        self.sample_id = sample_id
        self.offset = offset
        self.id = _id

    @staticmethod
    def setup_table():
        with database.AtomicConnection() as _conn:
            _conn.cursor.execute("""CREATE TABLE IF NOT EXISTS fingerprints (
                id SERIAL PRIMARY KEY,
                sample_id SERIAL NOT NULL,
                "offset" INTEGER NOT NULL,
                fingerprint NUMERIC ARRAY NOT NULL,
                CONSTRAINT sample_id FOREIGN KEY (sample_id) REFERENCES samples(id)
            )""")

    @staticmethod
    def batch_insert(sample_id, raw_fingerprints):
        with database.AtomicConnection() as conn:
            conn.cursor.execute("""DELETE FROM fingerprints WHERE sample_id = %s""", [sample_id])
            with conn.cursor.copy("""COPY fingerprints (sample_id, "offset", fingerprint) FROM STDIN""") as copy:
                for offset, fingerprint in enumerate(raw_fingerprints):
                    copy.write_row([sample_id, offset, [decimal.Decimal(f) for f in fingerprint]])

    @staticmethod
    def search(input_raw_fingerprints):
        with database.AtomicConnection() as conn:
            query_result = conn.cursor.execute("""SELECT * FROM fingerprints""")
            for fingerprint_obj in query_result:
                database_fingerprint = Fingerprint(
                    fingerprint_obj["sample_id"],
                    fingerprint_obj["offset"],
                    fingerprint_obj["fingerprint"],
                    _id=fingerprint_obj["id"],
                )
                # TODO: Optimize using database algorithms and/or using a tree data structure. This is a prototype
                for input_raw_fingerprint in input_raw_fingerprints:
                    if match_fingerprints(input_raw_fingerprint, database_fingerprint.fingerprint):
                        yield database_fingerprint


def fingerprint_sample(sample):
    sample_spectrogram = Spectrogram(sample.path)
    sample_fingerprints = get_fingerprints(sample_spectrogram)

    Fingerprint.batch_insert(sample.id, sample_fingerprints)

    sample.is_processed = True
    sample.save()


# Credits: https://github.com/Lizzi-Busy/freezam
def get_fingerprints(spectrogram: Spectrogram):
    num_octaves = 8
    min_frequency = int((2 ** -(num_octaves + 1)) * (spectrogram.sample_rate / 2))
    fingerprints = []

    for octave in range(num_octaves):
        start = min_frequency * (2 ** octave) * 10
        end = min_frequency * (2 ** (octave + 1)) * 10

        sub_frequencies = spectrogram.frequencies[start:end]
        sub_spectrogram = spectrogram.spectrogram[start:end]

        sub_fingerprint = _get_fingerprint(sub_frequencies, sub_spectrogram)
        fingerprints.append(sub_fingerprint)

    # Fingerprint of each octave, consists of 8 elements. Need to transpose to procure fingerprint of all 8 octaves for
    # each window.
    return np.array(fingerprints).T


def _get_fingerprint(frequencies, spectrogram):
    max_frequency = max(frequencies)
    spectrogram_peaks = np.argmax(spectrogram, axis=0)
    fingerprints = frequencies[spectrogram_peaks] / max_frequency
    return np.array(fingerprints)


def match_fingerprints(f1, f2):
    tolerance = 0.01
    if len(f1) == len(f2):
        pairs = zip(f1, f2)
        dists = []
        for x, y in pairs:
            dists.append(distance.euclidean([float(x)], [float(y)]))
        if all([(d < tolerance) for d in dists]):
            return True
        return False
    else:
        raise Exception("expected equal fingerprint lengths")
