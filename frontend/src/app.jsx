import WebcamCapture from './components/WebcamCapture'

function App() {
  return (
    <div style={{ textAlign: 'center', marginTop: '20px' }}>
      <h1>Sign2Text</h1>
      <p>Sign Language to Text Converter</p>
      <WebcamCapture />
    </div>
  )
}

export default App