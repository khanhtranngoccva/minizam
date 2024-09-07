import * as React from "react";
import {waitForAnimationFrame} from "@/helpers/animation";

export function useElementPositionTopRight(anchorRef: React.RefObject<HTMLDivElement | null>, element: HTMLElement) {
    React.useEffect(() => {
        if (!anchorRef.current) return;
        let doLoop = true;

        const anchor = anchorRef.current!;

        async function track() {
            anchor.style.display = "flex";
            while (doLoop) {
                const boundingBox = element.getBoundingClientRect();
                anchor.style.left = boundingBox.left + boundingBox.width + "px";
                anchor.style.top = boundingBox.top - 8 + "px";
                await waitForAnimationFrame();
            }
        }

        track().then();

        return () => {
            doLoop = false;
        }
    }, [anchorRef, element]);
}