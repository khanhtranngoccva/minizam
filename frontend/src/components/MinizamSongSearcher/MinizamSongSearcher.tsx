import * as React from 'react';
import {produce} from "immer";
import {SearchResult} from "@/types/search";
import MinizamResultItem from "@/components/MinizamResultItem";
import {performSongSearch} from "@/helpers/search";
import * as Popover from "@radix-ui/react-popover";

interface SearchState {
    status: "stopped" | "searching" | "complete" | "error",
    results: SearchResult[],
}

interface InsertSearchResultAction {
    type: "insertResult",
    data: SearchResult,
}

interface ResetSearchAction {
    type: "reset",
}

interface StartSearchAction {
    type: "start",
}

interface CompleteSearchAction {
    type: "complete",
}

type SearchStateAction = InsertSearchResultAction | ResetSearchAction | CompleteSearchAction | StartSearchAction;

function searchStateReducer(state: SearchState, action: SearchStateAction) {
    return produce(state, function (draft) {
        switch (action.type) {
            case "reset":
                draft.status = "stopped";
                draft.results = [];
                break;
            case "start":
                draft.status = "searching";
                break;
            case "insertResult":
                let found = draft.results.find(result => result.id === action.data.id)
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
    audioElement: HTMLAudioElement,
    open: boolean,
}) {
    const [searchState, manageSearchState] = React.useReducer(
        searchStateReducer,
        {
            status: "stopped",
            results: [],
        },
    );

    // Should stop and reset the search every time the audio element changes.
    React.useEffect(() => {
        manageSearchState({
            type: "reset",
        });
    }, [props.audioElement]);

    // If the modal is open and the state is stopped, start the search automatically.
    React.useEffect(() => {
        if (props.open && searchState.status === "stopped") {
            manageSearchState({
                type: "start",
            });
        }
    }, [props.open, searchState.status]);

    // Should do search if the status is "searching" and stop all requests if the status is otherwise or component is
    // unmounted.
    React.useEffect(() => {
        if (searchState.status !== "searching") return;

        const abortController = new AbortController();

        async function doSearch() {
            const result = await performSongSearch({
                abortSignal: abortController.signal,
                audioElement: props.audioElement,
            });
            for (let resultItem of result) {
                manageSearchState({
                    type: "insertResult",
                    data: resultItem,
                });
            }
            manageSearchState({
                type: "complete"
            });
        }

        doSearch().then();

        return () => {
            abortController.abort();
        }
    }, [searchState.status, props.audioElement]);

    return <div
        className={"bg-white shadow-xl rounded-[8px] flex flex-col px-[8px] py-[12px] min-w-80 max-w-[25rem]"}>
        <h1 className={"font-[600] text-lg mb-2"}>
            {searchState.status === "complete"
                ? `${searchState.results.length} result(s) found.` :
                "Searching for songs..."}
        </h1>
        <div className={"h-[4px] bg-green-500 mx-[-8px]"}></div>
        <ul className={"flex flex-col gap-2 pt-2 max-h-[50vh] overflow-y-auto overflow-x-hidden"}>
            {searchState.results.map(item => {
                return <MinizamResultItem key={item.id} {...item}></MinizamResultItem>
            })}
        </ul>
    </div>
}

export default MinizamSongSearcher;
