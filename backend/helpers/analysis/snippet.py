import operator
from collections import OrderedDict
from helpers import path


class Snippet:
    def __init__(self, sha256):
        self.sha256 = sha256

    @property
    def path(self):
        return path.get_temp_path(f"{self.sha256}.wav")

    @staticmethod
    def load(infile, *_, slice_audio=None):
        from helpers.analysis.sample import load_audio
        buffer, sha256_hash = load_audio(infile, slice_audio=slice_audio)
        new_filename = f"{sha256_hash}.wav"
        new_file_path = path.get_temp_path(new_filename)
        with open(new_file_path, "wb") as f:
            f.write(buffer)
        return Snippet(sha256_hash)

    def identify_matching_samples(self):
        from helpers.analysis.sample import Sample
        from helpers.analysis.spectrogram import Spectrogram
        from helpers.analysis.fingerprinting import get_fingerprints, Fingerprint

        spectrogram = Spectrogram(self.path)
        raw_fingerprints = get_fingerprints(spectrogram)
        fingerprints = Fingerprint.search(raw_fingerprints[0:3])

        # Group matches
        matches = OrderedDict()
        for fingerprint in fingerprints:
            matches.setdefault(fingerprint.sample_id, 0)
            matches[fingerprint.sample_id] += 1

        sorted_matches = sorted(matches.items(), key=operator.itemgetter(1), reverse=True)
        top_match_ids = list(map(operator.itemgetter(0), sorted_matches[0:3]))
        return Sample.get_by_ids(top_match_ids)
