import * as React from 'react';
import {FaMusic, FaXmark} from "react-icons/fa6";
import * as Popover from "@radix-ui/react-popover";

function MinizamButton(props: {
    setDisplay: (arg: boolean) => void
}) {
    return <div
        className={"absolute right-0 bottom-0 p-[4px] bg-white rounded-[8px] flex items-center gap-[4px]"}>
        <Popover.Trigger asChild={true}>
            <button
                title={"What song am I hearing?"}
                className={"bg-green-500 rounded-[4px] w-6 h-6 flex-1 aspect-square flex gap-[4px] justify-center items-center"}>
                <FaMusic className={"text-white"}></FaMusic>
            </button>
        </Popover.Trigger>
        <button
            onClick={() => {
                props.setDisplay(false);
            }}
            className={"bg-gray-200 rounded-[4px] w-6 h-6 flex-1 aspect-square flex gap-[4px] justify-center items-center"}>
            <FaXmark className={"text-black"}></FaXmark>
        </button>
    </div>;
}

export default React.memo(MinizamButton);
