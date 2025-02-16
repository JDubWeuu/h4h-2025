"use client";

import { useEffect, useState } from "react";
import { useReactMediaRecorder } from "react-media-recorder";

export default function AudioRecorder() {
  const [text, setText] = useState("Record");
  const [speech, setSpeech] = useState("");
  const { status, startRecording, stopRecording, mediaBlobUrl } =
    useReactMediaRecorder({
      audio: {
        sampleRate: 48000, // Increase to 48kHz for better quality
        echoCancellation: true, // Reduce echo
        noiseSuppression: true, // Reduce background noise
      },
      blobPropertyBag: { type: "audio/wav" },
    });

    useEffect(()=>{
    const talk = new SpeechSynthesisUtterance(
      speech
    );
    const voices = speechSynthesis.getVoices();
    talk.voice = voices[0];
    speechSynthesis.speak(talk);
    },[speech]);


  const [isUploading, setIsUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState("");

  const clickButton = () => {
    if (status !== "recording") {
      startRecording();
      setText("Stop Recording");
      setUploadStatus("");
    } else {
      stopRecording();
      setText("Record");
    }
  };

  const sendWavToBackend = async (blobUrl) => {
    try {
      setIsUploading(true);
      setUploadStatus("Preparing audio data...");

      // Fetch the blob from the blob URL
      const response = await fetch(blobUrl);
      const blob = await response.blob();

      // Convert audio to actual WAV format
      const audioContext = new (window.AudioContext ||
        window.webkitAudioContext)();
      const arrayBuffer = await blob.arrayBuffer();
      const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);

      // Create WAV file
      const wavBlob = await convertToWav(audioBuffer);

      setUploadStatus("Sending to server...");

      // Send to backend
      const formData = new FormData();
      formData.append("file", wavBlob, "recording.wav");

      const res = await fetch("http://127.0.0.1:8000/send/wav", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        throw new Error(`Server responded with status: ${res.status}`);
      }

      const data = await res.json();
      console.log("Backend response:", data);
      setUploadStatus("Upload successful!");
      setSpeech(data.message.content);
      // Cleanup
      audioContext.close();
    } catch (error) {
      console.error("Error sending WAV to backend:", error);
      setUploadStatus(`Error: ${error.message}`);
    } finally {
      setIsUploading(false);
    }
  };

  // Function to convert AudioBuffer to WAV format
  const convertToWav = (audioBuffer) => {
    const numOfChannels = audioBuffer.numberOfChannels;
    const sampleRate = audioBuffer.sampleRate;
    const length = audioBuffer.length * numOfChannels * 2;
    const buffer = new ArrayBuffer(44 + length);
    const view = new DataView(buffer);

    // Write WAV header
    // "RIFF" identifier
    writeString(view, 0, "RIFF");
    // File length minus RIFF identifier length and file description length
    view.setUint32(4, 36 + length, true);
    // "WAVE" identifier
    writeString(view, 8, "WAVE");
    // "fmt " chunk identifier
    writeString(view, 12, "fmt ");
    // Chunk length
    view.setUint32(16, 16, true);
    // Sample format (raw)
    view.setUint16(20, 1, true);
    // Channel count
    view.setUint16(22, numOfChannels, true);
    // Sample rate
    view.setUint32(24, sampleRate, true);
    // Byte rate (sample rate * block align)
    view.setUint32(28, sampleRate * numOfChannels * 2, true);
    // Block align (channel count * bytes per sample)
    view.setUint16(32, numOfChannels * 2, true);
    // Bits per sample
    view.setUint16(34, 16, true);
    // "data" chunk identifier
    writeString(view, 36, "data");
    // Chunk length
    view.setUint32(40, length, true);

    // Write audio data
    const offset = 44;
    const channels = [];
    for (let i = 0; i < numOfChannels; i++) {
      channels.push(audioBuffer.getChannelData(i));
    }

    let index = 0;
    for (let i = 0; i < audioBuffer.length; i++) {
      for (let channel = 0; channel < numOfChannels; channel++) {
        const sample = Math.max(-1, Math.min(1, channels[channel][i]));
        view.setInt16(
          offset + index,
          sample < 0 ? sample * 0x8000 : sample * 0x7fff,
          true
        );
        index += 2;
      }
    }

    return new Blob([buffer], { type: "audio/wav" });
  };

  // Helper function to write strings to DataView
  const writeString = (view, offset, string) => {
    for (let i = 0; i < string.length; i++) {
      view.setUint8(offset + i, string.charCodeAt(i));
    }
  };

  useEffect(() => {
    if (mediaBlobUrl) {
      sendWavToBackend(mediaBlobUrl);
    }
  }, [mediaBlobUrl]);

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Audio Recorder</h1>
      <button
        onClick={clickButton}
        disabled={isUploading}
        className={`bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mb-4 ${
          isUploading ? "opacity-50 cursor-not-allowed" : ""
        }`}
      >
        {text}
      </button>
      <div className="space-y-4">
        {uploadStatus && (
          <p
            className={`text-sm ${
              uploadStatus.includes("Error") ? "text-red-600" : "text-gray-600"
            }`}
          >
            {uploadStatus}
          </p>
        )}
        {mediaBlobUrl && (
          <div>
            <p className="text-sm text-gray-600 mb-2">Recording:</p>
            <audio src={mediaBlobUrl} controls className="w-full" />
          </div>
        )}
      </div>
    </div>
  );
}
