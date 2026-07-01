import { useRef, useState } from "react";
import Webcam from "react-webcam";

function WebcamCapture() {
  const webcamRef = useRef(null);
  const [result, setResult] = useState("");

  const captureAndPredict = async () => {
    const imageSrc = webcamRef.current.getScreenshot();

    const response = await fetch("http://127.0.0.1:8000/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        image: imageSrc,
      }),
    });

    const data = await response.json();

    // Show exactly what backend sends
    setResult(data.prediction);
  };

  return (
    <div>
      <Webcam
        ref={webcamRef}
        screenshotFormat="image/jpeg"
        width={640}
        height={480}
      />

      <br />
      <button onClick={captureAndPredict}>Predict Sign</button>

      <h2>{result}</h2>
    </div>
  );
}

export default WebcamCapture;