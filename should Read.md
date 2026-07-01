Backend Setup (FastAPI)

```bash
cd backend
python -m venv venv311
venv311\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload

Backend will run at:

http://127.0.0.1:8000

💻 Frontend Setup (React + Vite)
cd frontend
npm install
npm run dev

Frontend will run at:
http://localhost:5173

🔗 System Flow
Open frontend in browser
Allow webcam access
Show hand gesture
Frontend sends image to backend
Backend detects gesture using MediaPipe
Prediction is returned as text
Supported Gestures:
👋 Open palm → "Hello"
✊ Closed fist → "Bye"
👍 Thumb up → "Yes"
☝️ Index only → "No"
✌️ Index + middle → "Peace"
🤙 Thumb + pinky → "Call Me"
👌 Thumb + fingers closed → "OK"
🤟 Special combination → "I Love You"
🙌 Open palm → "Stop / Good / Please"
