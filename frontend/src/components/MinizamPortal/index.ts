import dynamic from "next/dynamic";

export * from './MinizamPortal';
export default dynamic(() => import("./MinizamPortal"), {
    ssr: false
});