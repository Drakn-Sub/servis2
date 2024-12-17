import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Register from './pages/register';
import Login from './pages/login';
import Cliente from './pages/cliente';
import Trabajador from './pages/trabajador';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route path="/cliente" element={<Cliente />} />
        <Route path="/trabajador" element={<Trabajador />} />
      </Routes>
    </Router>
  );
}

export default App;
