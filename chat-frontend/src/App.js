import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import axios from 'axios';
import './App.css'; // Add this line
import Navbar from './components/navigation';
import logo from './logo.svg'; // Add this line
import Home from './components/Home';
import Contact from './components/contact';
import Chat from './components/chat';
import Login from './components/Login';
import Register from './components/Register';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const response = await axios.get('http://localhost:5000/check_auth', { withCredentials: true });
        if (response.data.message === "Authenticated") {
          setIsAuthenticated(true);
        }
      } catch (error) {
        console.error(error);
      }
    };
    checkAuth();
  }, []);

  return (
    <Router>
      <Navbar />
      <img src={logo} className="App-logo" alt="logo" /> {/* Add this line if you want to display the logo */}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/contact" element={<Contact />} />
        <Route
          path="/chat"
          element={isAuthenticated ? <Chat /> : <Navigate to="/login" />}
        />
        <Route path="/login" element={<Login setIsAuthenticated={setIsAuthenticated} />} />
        <Route path="/register" element={<Register />} />
      </Routes>
    </Router>
  );
}

export default App;