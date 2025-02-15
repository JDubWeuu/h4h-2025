import Image from "next/image";
import "./globals.css";
import { useState } from "react";

export default function Home() {
  const [text, setText] = useState("record");

  const clickButton = () => {
    newText = text === "record" ? "stop recording" : "record"
    setText(newText)
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
