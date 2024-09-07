import * as React from 'react';
import {waitForAnimationFrame} from "@/helpers/animation";
import * as Popover from "@radix-ui/react-popover";
import MinizamSongSearcher from "@/components/MinizamSongSearcher";
import MinizamButton from "@/components/MinizamButton";
import {useElementPositionTopRight} from "@/hooks/useElementPosition";

function MinizamPopover(props: {
    audioElement: HTMLAudioElement
}) {
    const anchorRef = React.useRef<HTMLDivElement | null>(null);
    const [display, setDisplay] = React.useState(true);
    const [open, setOpen] = React.useState(false);

    useElementPositionTopRight(anchorRef, props.audioElement);

    if (!display) return null;

    return <div ref={anchorRef} className={"fixed hidden"}>
        <Popover.Root open={open} onOpenChange={(curState) => {
            setOpen(curState);
        }}>
            <MinizamButton setDisplay={setDisplay}></MinizamButton>
            <Popover.Portal>
                <Popover.Content sideOffset={4}>
                    <MinizamSongSearcher audioElement={props.audioElement} open={open}></MinizamSongSearcher>
                </Popover.Content>
            </Popover.Portal>
        </Popover.Root>
    </div>;
}

export default MinizamPopover;
