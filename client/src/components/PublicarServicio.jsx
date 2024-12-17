import React, { useState } from 'react';
import axios from 'axios';

const PublishService = () => {
    const [nombre, setNombre] = useState('');
    const [precio, setPrecio] = useState('');
    const [descripcion, setDescripcion] = useState('');
    const [horarios, setHorarios] = useState('');
    const [categoria, setCategoria] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        const serviceData = {
            nombre,
            precio,
            descripcion,
            horarios,
            categoria,
        };

        axios.post('http://127.0.0.1:8000/servis_api/usuarios/crear-servicio/', serviceData)
            .then(response => alert('Servicio publicado'))
            .catch(error => console.error(error));
    };

    return (
        <div>
            <h2>Publicar Servicio</h2>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="Nombre del Servicio"
                    value={nombre}
                    onChange={(e) => setNombre(e.target.value)}
                />
                <input
                    type="text"
                    placeholder="Precio"
                    value={precio}
                    onChange={(e) => setPrecio(e.target.value)}
                />
                <textarea
                    placeholder="Descripción"
                    value={descripcion}
                    onChange={(e) => setDescripcion(e.target.value)}
                />
                <input
                    type="text"
                    placeholder="Horarios Disponibles"
                    value={horarios}
                    onChange={(e) => setHorarios(e.target.value)}
                />
                <select onChange={(e) => setCategoria(e.target.value)}>
                    <option value="">Seleccionar Categoría</option>
                    <option value="Construcción">Construcción</option>
                    <option value="Electricidad">Electricidad</option>
                </select>
                <button type="submit">Publicar</button>
            </form>
        </div>
    );
};

export default PublishService;
