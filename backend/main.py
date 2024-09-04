from helpers.analysis.fingerprinting import get_fingerprints
from helpers.analysis.sample import Sample
from helpers.analysis.snippet import Snippet
from helpers.analysis.spectrogram import Spectrogram
from helpers.database import setup_database
from helpers.initialize import initialize_database
from helpers import path

if __name__ == '__main__':
    candidate_samples = Snippet.load(path.get_content_path(
        "Waltz Op. 70 no. 1 in G flat major.ogg"
    )).identify_matching_samples()
    print("Sample matches:")
    for sample in candidate_samples:
        print(sample.title)
