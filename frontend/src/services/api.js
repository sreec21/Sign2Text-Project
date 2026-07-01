import axios from 'axios'

const API_URL = 'http://127.0.0.1:8000'

export async function predictImage(image) {
  const response = await axios.post(`${API_URL}/predict`, {
    image,
  })

  return response.data.prediction
}