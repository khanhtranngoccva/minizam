import * as React from 'react';
import {waitForAnimationFrame} from "@/helpers/animation";
import {FaMusic, FaXmark} from "react-icons/fa6";
import * as Popover from "@radix-ui/react-popover";
import MinizamSongSearcher from "@/components/MinizamSongSearcher";

function MinizamButton(props: {
    audioElement: HTMLAudioElement
}) {
    const anchorRef = React.useRef<HTMLDivElement | null>(null);
    const [display, setDisplay] = React.useState(true);

    React.useEffect(() => {
        if (!anchorRef.current) return;
        let doLoop = true;

        const anchor = anchorRef.current!;

        async function track() {
            anchor.style.display = "flex";
            while (doLoop) {
                const boundingBox = props.audioElement.getBoundingClientRect();
                anchor.style.left = boundingBox.left + boundingBox.width + "px";
                anchor.style.top = boundingBox.top - 8 + "px";
                await waitForAnimationFrame();
            }
        }

        track().then();

        return () => {
            doLoop = false;
        }
    }, [props.audioElement]);

    if (!display) return null;

    return <div ref={anchorRef} className={"fixed hidden"}>
        <Popover.Root>
            <Popover.Trigger asChild={true}>
                <div
                    className={"absolute right-0 bottom-0 p-[4px] bg-white rounded-[8px] flex items-center gap-[4px]"}>
                    <button
                        title={"What song am I hearing?"}
                        className={"bg-green-500 rounded-[4px] w-6 h-6 flex-1 aspect-square flex gap-[4px] justify-center items-center"}>
                        <FaMusic className={"text-white"}></FaMusic>
                    </button>
                    <button
                        onClick={() => {
                            setDisplay(false);
                        }}
                        className={"bg-gray-200 rounded-[4px] w-6 h-6 flex-1 aspect-square flex gap-[4px] justify-center items-center"}>
                        <FaXmark className={"text-black"}></FaXmark>
                    </button>
                </div>
            </Popover.Trigger>
            <Popover.Portal>
                <Popover.Content sideOffset={4}>
                    <MinizamSongSearcher audioElement={props.audioElement}></MinizamSongSearcher>
                </Popover.Content>
            </Popover.Portal>
        </Popover.Root>
    </div>;
}

export default React.memo(MinizamButton);
