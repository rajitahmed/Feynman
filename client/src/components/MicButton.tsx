import { useRef, useState } from "react";
import Button from "./Button.tsx";
import "./MicButton.css";

type MicButtonProps = {
  // Null when the mic is ready; otherwise what the kid is doing, shown on the disabled button.
  waitingLabel: string | null;
  onRecorded: (audioBase64: string) => void;
  onMicError: (error: unknown) => void;
};

function MicButton({ waitingLabel, onRecorded, onMicError }: MicButtonProps) {
  const [isRecording, setIsRecording] = useState(false);
  const recorderRef = useRef<MediaRecorder | null>(null);
  const isWaiting = waitingLabel !== null;

  async function startRecording() {
    try {
      const microphone = await navigator.mediaDevices.getUserMedia({
        audio: true,
      });
      const recorder = new MediaRecorder(microphone);
      const audioChunks: Blob[] = [];
      recorder.ondataavailable = (event) => audioChunks.push(event.data);
      recorder.onstop = () => {
        // Releasing the mic turns off the browser's recording indicator between answers.
        microphone.getTracks().forEach((track) => track.stop());
        const audio = new Blob(audioChunks, { type: recorder.mimeType });
        // Stays "recording" until the answer is handed over and the kid starts thinking,
        // so the mic never flashes back to ready and a second recording can't start early.
        readAsBase64(audio)
          .then(onRecorded, onMicError)
          .finally(() => setIsRecording(false));
      };
      recorder.start();
      recorderRef.current = recorder;
      setIsRecording(true);
    } catch (error) {
      onMicError(error);
    }
  }

  function stopRecording() {
    // A second tap before the hand-over is harmless: stopping an inactive recorder does nothing.
    recorderRef.current?.stop();
  }

  function chooseLabel() {
    if (waitingLabel !== null) {
      return waitingLabel;
    }
    return isRecording ? "Tap to send" : "Tap to talk";
  }

  return (
    <Button
      className={
        isRecording ? "mic-button mic-button--recording" : "mic-button"
      }
      aria-pressed={isRecording}
      disabled={isWaiting}
      onClick={isRecording ? stopRecording : startRecording}
    >
      <span aria-hidden="true">🎤</span>{" "}
      {/* Live, so screen readers hear "Pip is thinking…" without a second status line. */}
      <span aria-live="polite">{chooseLabel()}</span>
    </Button>
  );
}

function readAsBase64(audio: Blob): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      // A data URL reads "data:<type>;base64,<data>"; the server only wants the data.
      const [, base64Data] = String(reader.result).split(",");
      resolve(base64Data);
    };
    reader.onerror = () => reject(reader.error);
    reader.readAsDataURL(audio);
  });
}

export default MicButton;
