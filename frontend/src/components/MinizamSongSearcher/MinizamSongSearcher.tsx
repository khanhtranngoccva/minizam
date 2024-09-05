import * as React from 'react';
import {produce} from "immer";
import {SearchResult} from "@/types/search";
import MinizamResultItem from "@/components/MinizamResultItem";
import {performSongSearch} from "@/helpers/search";

interface SearchState {
    status: "pending" | "searching" | "complete" | "error",
    results: SearchResult[],
}

interface InsertSearchResultAction {
    type: "insertResult",
    data: SearchResult,
}

interface ResetSearchAction {
    type: "reset",
}

interface CompleteSearchAction {
    type: "complete",
}

type SearchStateAction = InsertSearchResultAction | ResetSearchAction | CompleteSearchAction;

function searchStateReducer(state: SearchState, action: SearchStateAction) {
    return produce(state, function (draft) {
        switch (action.type) {
            case "reset":
                draft.status = "searching";
                draft.results = [];
                break;
            case "insertResult":
                let found = draft.results.find(result => result.id == action.data.id)
                if (found) {
                    Object.assign(found, action.data);
                } else {
                    draft.results.push(action.data);
                }
                return draft;
            case "complete":
                draft.status = "complete";
                break;
        }
    });
}

function MinizamSongSearcher(props: {
    audioElement: HTMLAudioElement
}) {
    const [searchState, manageSearchState] = React.useReducer(
        searchStateReducer,
        {
            status: "complete",
            results: [],
            // [{
            //     id: 1,
            //     album: "Chopin Complete Collection",
            //     title: "Ballade no. 1 - Op. 23.ogg",
            //     artist: "Frederic Chopin",
            //     image: "data:image/webp;base64,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",
            //     originalLink: null,
            //     audioTime: 0,
            // }]
        },
    );

    React.useEffect(() => {
        // Reset the search state.
        manageSearchState({
            type: "reset",
        });
    }, [props.audioElement]);

    React.useEffect(() => {
        if (searchState.status !== "searching") return;

        const abortController = new AbortController();

        async function doSearch() {
            const result = await performSongSearch({
                abortSignal: abortController.signal,
                audioElement: props.audioElement,
            });
        }

        doSearch().then();

        return () => {
            abortController.abort();
        }
    }, [searchState.status, props.audioElement]);

    return <div
        className={"bg-white shadow-xl rounded-[8px] flex flex-col px-[8px] py-[12px] min-w-80"}>
        <h1 className={"font-[600] text-lg mb-2"}>
            {searchState.status === "complete"
                ? `${searchState.results.length} result(s) found.` :
                "Searching for songs..."}
        </h1>
        <div className={"h-[4px] bg-green-500 mx-[-8px] max-h-[50vh] overflow-y-auto"}></div>
        <ul className={"flex flex-col gap-2 pt-2"}>
            {searchState.results.map(item => {
                return <MinizamResultItem key={item.id} {...item}></MinizamResultItem>
            })}
        </ul>
    </div>;
}

export default MinizamSongSearcher;
