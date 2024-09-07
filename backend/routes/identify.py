from urllib import request

import constants
from helpers.analysis.snippet import Snippet
from helpers.downloader import download_file
from server.response import json_resp
from server.server import app
from flask import request


@app.route('/identify/by_url', methods=['POST'])
def identify_by_url():
    audio_url = request.json["url"]
    audio_time = request.json["time"]

    downloaded_path = download_file(audio_url)
    samples = (Snippet
               .load(downloaded_path, slice_audio=(audio_time, audio_time + constants.WINDOW_DURATION + 5))
               .identify_matching_samples())
    result = []
    for sample in samples:
        result.append(sample.serialize())

    return json_resp(result)
