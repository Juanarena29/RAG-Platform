import { BrowserRouter, Route, Routes } from 'react-router-dom'
import LandingPage from './LandingPage.jsx'
import ChatPage from './ChatPage.jsx'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/chat" element={<ChatPage />} />
      </Routes>
    </BrowserRouter>
  )
}
