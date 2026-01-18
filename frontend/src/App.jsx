import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Landing from './pages/Landing/Landing'
import Sketchpad from './pages/Sketchpad/Sketchpad'
import ProjectGallery from './pages/ProjectGallery/ProjectGallery'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/sketchpad" element={<Sketchpad />} />
        <Route path="/gallery" element={<ProjectGallery />} />
      </Routes>
    </Router>
  )
}

export default App
