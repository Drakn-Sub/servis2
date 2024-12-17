import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Navbar from '../components/NavbarCliente';
import TablaServicios from '../components/TablaServicios';

const Cliente = () => {
  const [servicios, setServicios] = useState([]);
  const [loading, setLoading] = useState(true);
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    axios.get('http://localhost:8000/servis_api/usuarios/servicios/', {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      }
    })
    .then(response => {
      setServicios(response.data);
      setLoading(false);
    })
    .catch(error => {
      console.error("Hubo un error al obtener los servicios:", error);
      setLoading(false);
    });
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    window.location.href = '/';  // Redirigir a la página de inicio
  };

  if (loading) {
    return <div>Cargando servicios...</div>;
  }

  return (
    <div className="container mt-5">
      <Navbar onLogout={handleLogout} />
      <h1>Servicios Disponibles</h1>
      <TablaServicios servicios={servicios} />
    </div>
  );
};

export default Cliente;
