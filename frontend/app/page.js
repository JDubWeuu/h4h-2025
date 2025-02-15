"use client";

import Image from "next/image";
import "./globals.css";
import React from "react";
import Navbar from "../components/Navbar";
import { useEffect, useState, useRef } from "react";


export default function Home() {
  const [text, setText] = useState("record");
  const [audioStream, setAudioStream] = useState(null);
  const [count, setCount] = useState(0);
  const socketRef = useRef(null);
  const mediaRecorderRef = useRef(null);

  useEffect(() => {
    // const ws = new WebSocket("http://localhost:3000/ws/audio");
    socketRef.current = new WebSocket("ws://localhost:3000/ws/audio");
    socketRef.current.binaryType = "arraybuffer";

    socketRef.current.onopen = () => {
      console.log("WebSocket connected");
    };

    socketRef.current.onmessage = (event) => {
      console.log("Received from backend:", event.data);
    };

    socketRef.current.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    socketRef.current.onclose = () => {
      console.log("WebSocket connection closed");
    };
  }, [])

  const clickButton = async () => {
    if (count == 0) {
      setCount(count + 1);
      speak();
    }
    if (text == "record") {
      // create a websocket connection with backend to obtain voice of user
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          audio: true,
        });
        setAudioStream(stream);
        const mediaRecorder = new MediaRecorder(stream);
        mediaRecorderRef.current = mediaRecorder;

        mediaRecorder.ondataavailable = (event) => {
          if (event.data && event.data.size > 0) {
            if (
              socketRef.current &&
              socketRef.current.readyState === WebSocket.OPEN
            ) {
              socketRef.current.send(event.data);
              console.log("Sent audio chunk:", event.data);
            }
          }
        };
        mediaRecorder.start(100);
      } catch (error) {
        console.error(error);
      }
    } else {
      // end the websocket connection
     if (audioStream) {
       const tracks = audioStream.getTracks();
       for (let track of tracks) {
         track.stop();
         console.log(`Stopped track: ${track.kind}`);
       }
       setAudioStream(null);
     }
    }
    let newText = text === "record" ? "stop recording" : "record";
    setText(newText);
  };

  const speak = () => {
    const talk = new SpeechSynthesisUtterance(
      "Hello there! I'm your flight booking assistant! How can I help you?"
    );

    const voices = speechSynthesis.getVoices();
    talk.voice = voices[2];

    speechSynthesis.speak(talk);
  };
  return (
    <div>
      <Navbar/> 
      
      <div className="container">
        <div className="text-left">
          <h2>Welcome to Visionary, your Virtual Flight Assistant!</h2>
          <p>short description or purpose. Click the button on the right to begin.</p>
        </div>

        <div>
          <a /*RECORD BUTTON*/
            className="btn-88"
            href="https://google.com"
            target="_blank"
            rel="noopener noreferrer"
          >
            <Image
              src="/globe.svg"
              alt="Record button"
              width={60}
              height={60}
            />
          </a>
        </div>

      </div>

      <div>
        <p>Recording time: </p>
      </div>

    </div>
  );
}
