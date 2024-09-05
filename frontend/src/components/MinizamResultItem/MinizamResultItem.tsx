import * as React from 'react';
import {SearchResult} from "@/types/search";
import * as nodeCrypto from "crypto";
import Image from "next/image";

function MinizamResultItem(props: SearchResult) {
    const titleSeed = props.title ?? crypto.randomUUID();
    const titleSeedHash = nodeCrypto.createHash("md5").update(titleSeed).digest().toString("hex");
    const defaultColor = "#" + titleSeedHash.slice(0, 6);
    const sampleTitle = props.title ?? "Unknown Title";
    const sampleArtist = props.artist ?? "Unknown Artist(s)";
    const sampleAlbum = props.album ?? "Unknown Album";

    return <li className={"flex gap-2"}>
        <div
            className={"max-w-32 min-w-16 max-h-32 min-h-16 w-[8vmin] h-[8vmin] flex-0 aspect-square overflow-hidden rounded-[8px] relative"}>
            {
                props.image
                    ? <Image className={"object-cover"} fill={true} src={props.image!}
                             alt={sampleTitle}></Image>
                    : <div className={"w-full h-full"}
                           style={{
                               background: defaultColor
                           }}></div>
            }
        </div>
        <div className={"flex flex-col gap-1 flex-1"}>
            <h2 className={"font-[500] text-base"}>{sampleTitle}</h2>
            <span className={"text-[0.75rem]"}>{sampleArtist}</span>
            <span className={"text-[0.75rem]"}>{sampleAlbum}</span>
        </div>
    </li>;
}

export default React.memo(MinizamResultItem);
