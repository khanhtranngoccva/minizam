import Image from "next/image";
import DemoAudio from "@/components/DemoAudio";
import MinizamManager from "@/components/MinizamPortal";

export default function Home() {
    return (
        <main className="flex h-full flex-col items-center justify-between p-24">
            {/* Do not mess with this component! Should demonstrate the ability to create a button on the fly. */}
            <DemoAudio></DemoAudio>
            <MinizamManager></MinizamManager>
        </main>
    );
}
