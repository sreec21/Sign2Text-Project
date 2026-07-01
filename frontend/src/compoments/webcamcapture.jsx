import { useRef, useState } from 'react'
import Webcam from 'react-webcam'

function WebcamCapture() {
  const webcamRef = useRef(null)
  const [result, setResult] = useState('')

  const capture = () => {
    const imageSrc = webcamRef.current.getScreenshot()
    console.log(imageSrc)
    setResult('HELLO')
  }

  return (
    <div>
      <Webcam
        ref={webcamRef}
        audio={false}
        screenshotFormat="image/jpeg"
        width={500}
        height={375}
      />

      <br />

      <button onClick={capture}>
        Predict Sign
      </button>

      <div
        style={{
          marginTop: '20px',
          fontSize: '24px',
          fontWeight: 'bold'
        }}
      >
        {result}
      </div>
    </div>
  )
}

export default WebcamCapture