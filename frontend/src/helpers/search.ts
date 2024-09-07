import api from "@/helpers/api";
import {resolve} from "dns";
import {SearchResult} from "@/types/search";


export async function performSongSearch(params: {
    abortSignal?: AbortSignal,
    audioElement: HTMLAudioElement,
}) {
    const currentTime = params.audioElement.currentTime;
    const audioSrc = params.audioElement.src;

    const url = new URL(audioSrc, window.location.href);
    const searcher = new SongSearcher(params.abortSignal);

    if (url.protocol === "http:" || url.protocol === "https:") {
        return searcher.urlStrategy({
            url: url,
            currentTime: currentTime,
        });
    }

    return [];
}

class SongSearcher {
    _abortSignal?: AbortSignal;

    constructor(abortSignal?: AbortSignal) {
        this._abortSignal = abortSignal;
    }

    async urlStrategy(params: {
        url: URL,
        currentTime: number,
    }): Promise<SearchResult[]> {
        const samples = (await api.post<Api.Response<Api.Sample[]>>("/identify/by_url", {
            url: params.url,
            time: params.currentTime,
        }, {
            signal: this._abortSignal,
        })).data.data;
        return samples.map(sample => {
            return {
                album: sample.album,
                artist: sample.artist,
                title: sample.title,
                image: null,
                id: sample.id,
                audioTime: params.currentTime,
                originalLink: null,
            }
        });
    }
}