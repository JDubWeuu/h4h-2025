import Image from "next/image";
import "./globals.css";
import React from "react";
import Navbar from "../components/Navbar";

export default function Home() {
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
