import hashlib
import io
import math
import random
import sys
import traceback

import pytest
from pydub import AudioSegment
from helpers import path
from helpers.analysis.sample import Sample
from helpers.analysis.snippet import Snippet

SNIPPET_LENGTH = 15
TEST_COUNT = 20


def create_snippet_from_file(filename):
    sample_data = AudioSegment.from_file(filename)

    # Ensure a 10 second snippet
    sample_slice_start = random.uniform(0, sample_data.duration_seconds - SNIPPET_LENGTH) * 1000
    sample_slice_end = sample_slice_start + SNIPPET_LENGTH * 1000
    sample_slice = sample_data[sample_slice_start:sample_slice_end]

    # Export and save
    buffer_io = io.BytesIO()
    sample_slice.export(buffer_io, format="wav")

    sample_slice_buffer = buffer_io.read()
    sample_slice_sha256 = hashlib.sha256(sample_slice_buffer).hexdigest()

    sample_slice_path = path.get_temp_path(f"{sample_slice_sha256}.wav")

    with open(sample_slice_path, "wb") as outfile:
        outfile.write(sample_slice_buffer)

    return sample_slice_path


def debug(e, sample, identified_samples, sample_slice_path):
    print(f"Current sample:", file=sys.stderr)
    print(sample, file=sys.stderr)

    print(f"Snippet path:", sample_slice_path, file=sys.stderr)

    print(f"Identified samples:", file=sys.stderr)
    for identified_sample in identified_samples:
        print(identified_sample, file=sys.stderr)

    print(f"Exception:", file=sys.stderr)
    print(e, file=sys.stderr)
    traceback.print_exception(e, file=sys.stderr)


# If multiple options are present, accuracy must be at least 70%
def test_randomized_identifications():
    samples = list(Sample.get_all())
    picked_samples = random.choices(samples, k=TEST_COUNT)

    passed_tests = 0

    for sample in picked_samples:
        identified_samples = []
        sample_slice_path = ""

        try:
            sample_slice_path = create_snippet_from_file(sample.path)
            identified_samples = list(Snippet.load(sample_slice_path).identify_matching_samples())
            assert len(identified_samples) > 0
            top_identified_sample = identified_samples[0]
            assert top_identified_sample.id == sample.id
        except Exception as e:
            debug(e, sample, identified_samples, sample_slice_path)
        else:
            passed_tests += 1

    print(f"Overall accuracy: {100 * passed_tests / len(picked_samples)}%")
    assert passed_tests > 0.7 * len(picked_samples)


# If multiple samples are presented to the user, accuracy must be at least 90%!
def test_randomized_identifications_with_list():
    samples = list(Sample.get_all())
    picked_samples = random.choices(samples, k=TEST_COUNT)

    passed_tests = 0

    for sample in picked_samples:
        identified_samples = []
        sample_slice_path = ""

        try:
            sample_slice_path = create_snippet_from_file(sample.path)
            identified_samples = list(Snippet.load(sample_slice_path).identify_matching_samples())
            assert len(identified_samples) > 0
            for identified_sample in identified_samples:
                if identified_sample.id == sample.id:
                    assert True
                    break
            else:
                assert False
        except Exception as e:
            debug(e, sample, identified_samples, sample_slice_path)
        else:
            passed_tests += 1

    print(f"Overall accuracy: {100 * passed_tests / len(picked_samples)}%")
    assert passed_tests > 0.90 * len(picked_samples)
