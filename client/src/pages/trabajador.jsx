import React, { useState } from 'react';
import axios from 'axios';
import Navbar from '../components/NavbarTrabajador';
import PublicarServicio from '../components/PublicarServicio';

const Trabajador = () => {
  const [message, setMessage] = useState('');
  const [menuOpen, setMenuOpen] = useState(false);

  const handleSubmit = (serviceData) => {
    axios.post('http://localhost:8000/crear-servicio', serviceData, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
      }
    })
    .then(response => {
      setMessage('Servicio publicado con éxito!');
    })
    .catch(error => {
      setMessage('Hubo un error al publicar el servicio.');
      console.error("Error al publicar el servicio:", error);
    });
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    window.location.href = '/';  // Redirigir a la página de inicio
  };

  return (
    <div className="container mt-5">
      <Navbar onLogout={handleLogout} />
      <h1 className="text-center text-success mb-4">Publicar Servicio</h1>
      <PublicarServicio onSubmit={handleSubmit} message={message} />
    </div>
  );
};

export default Trabajador;
