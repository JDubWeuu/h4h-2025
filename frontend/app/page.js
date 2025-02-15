"use client"

import Image from "next/image";
import "./globals.css";
import { useState } from "react";

export default function Home() {
  const [text, setText] = useState("record");
  const [count, setCount] = useState(0);


  const clickButton = () => {
    if (count == 0) {
      setCount(count+1)
      speak()
    }
    if (newText == "record") {
      // create a websocket connection with backend to obtain voice of user
    }
    let newText = text === "record" ? "stop recording" : "record"
    setText(newText);
  }

  const speak = () => {
    const talk = new SpeechSynthesisUtterance("Hello there! I'm your flight booking assistant! How can I help you?");
    
    const voices = speechSynthesis.getVoices()
    talk.voice = voices[2];

    speechSynthesis.speak(talk);
  }
  return (
    <div>
      <h1>
        Blind Flights
      </h1>
      <main className="">
        <button onClick={clickButton}>
          {text}
        </button>
      </main>
      
      <button className="btn-88">
        <Image src="../public/testplane.svg" alt="Globe Icon" width={32} height={32} />

      </button>
    </div>
  );
}
