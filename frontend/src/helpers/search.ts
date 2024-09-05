import {SearchResult} from "@/types/search";

export async function performSongSearch(params: {
    abortSignal: AbortSignal,
    audioElement: HTMLAudioElement,
}) {
    const currentTime = params.audioElement.currentTime;
    const audioSrc = params.audioElement.src;

    const url = new URL(audioSrc, window.location.href);
    const searcher = new SongSearcher(params.abortSignal);


    if (url.protocol === "http:" || url.protocol === "https:") {
        return searcher.urlStrategy({
            src: url,
            currentTime: currentTime,
        });
    }

    return null;
}

class SongSearcher {
    _abortSignal: AbortSignal;

    constructor(abortSignal: AbortSignal) {
        this._abortSignal = abortSignal;
    }

    async urlStrategy(params: {
        src: URL,
        currentTime: number,
    }) {
        console.log(params.src, params.currentTime);
    }
}