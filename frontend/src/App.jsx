import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Landing from './pages/Landing/Landing'
import Sketchpad from './pages/Sketchpad/Sketchpad'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/sketchpad" element={<Sketchpad />} />
      </Routes>
    </Router>
  )
}

export default App
