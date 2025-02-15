import Image from "next/image";
import "./globals.css";

export default function Home() {
  return (
    <div>
      <h1>
        Blind Flights
      </h1>
      
      
      <button className="btn-88">
        <Image src="../public/testplane.svg" alt="Globe Icon" width={32} height={32} />

      </button>
    </div>
  );
}
