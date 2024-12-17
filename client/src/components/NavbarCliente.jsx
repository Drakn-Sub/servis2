import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
    return (
        <nav className="navbar">
            <div className="navbar-container">
                <Link to="/profile">Mi Perfil</Link>
                <button onClick={handleLogout}>Cerrar Sesión</button>
            </div>
        </nav>
    );

    function handleLogout() {
        // Aquí se manejaría el cierre de sesión, eliminando el token JWT, por ejemplo.
        window.location.href = "/login"; // Redirigir a la página de login
    }
};

export default Navbar;