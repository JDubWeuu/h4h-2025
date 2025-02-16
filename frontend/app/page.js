// components/AudioRecorder.js
"use client";
// import AudioRecorder from "./components/AudioRecorder";

import dynamic from "next/dynamic";


const AudioRecorder = dynamic(() => import("./components/AudioRecorder"), { ssr: false });

export default function Page() {
  
  return (
    <AudioRecorder />
  );
}