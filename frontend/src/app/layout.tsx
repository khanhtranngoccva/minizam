import "./globals.css"
import React from "react";

export default function Layout(props: {
    children?: React.ReactNode
}) {
    return <html lang={"en"} className={"w-full flex flex-col min-h-screen m-0 relative bg-green-100"}>
    <body className={"w-full h-full m-0 px-8 py-4 flex-1 flex flex-col overflow-auto"}>
    {props.children}
    </body>
    </html>
}