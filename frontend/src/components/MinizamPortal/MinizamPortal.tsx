"use client";

import * as React from 'react';
import MinizamPopover from "@/components/MinizamPopover";

function forceUpdateReducer(state: number): number {
    return state++;
}

function MinizamPortal() {
    const [_, update] = React.useReducer(forceUpdateReducer, 0);

    // Live node list. Do not need to manipulate any further.
    const audioElements = document.querySelectorAll("audio");

    React.useEffect(() => {
        const observer = new MutationObserver(mutations => {
            for (let mutation of mutations) {
                if (mutation.target instanceof HTMLAudioElement) {
                    update();
                    break;
                }
            }
        });

        observer.observe(document.body, {childList: true});
        return () => {
            observer.disconnect();
        }
    }, []);

    return <>
        {Array.from(audioElements).map(element => {
            return <MinizamPopover key={element as any} audioElement={element}></MinizamPopover>
        })}
    </>
}

export default React.memo(MinizamPortal);
