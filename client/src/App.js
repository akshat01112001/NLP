import React from 'react'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import Login from './components/login'
import Signup from './components/signup'
import Profile from './components/profile'

const App = () => {
  return (
    <Router>
      <Routes>
        <Route exact path="/signin" element={<Login />} />
        <Route exact path="/signup" element={<Signup />} />
        <Route exact path="/profile" element={<Profile />} />
        
      </Routes>
    </Router>
  )
}

export default App
