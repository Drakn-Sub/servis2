import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ServicesTable = () => {
    const [services, setServices] = useState([]);
    const [search, setSearch] = useState('');
    const [filter, setFilter] = useState(''); // Filtro por tipo de servicio

    useEffect(() => {
        axios.get(`/api/services?tipo_servicio=${filter}`)
            .then(response => setServices(response.data))
            .catch(error => console.error(error));
    }, [filter]);

    const handleContact = (serviceId) => {
        // Enviar notificación de solicitud de contacto al trabajador
        axios.post(`/api/contact/${serviceId}`)
            .then(response => alert('Solicitud enviada'))
            .catch(error => console.error(error));
    };

    return (
        <div>
            <input
                type="text"
                placeholder="Buscar servicio"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
            />
            <select onChange={(e) => setFilter(e.target.value)}>
                <option value="">Todos</option>
                <option value="Construcción">Construcción</option>
                <option value="Electricidad">Electricidad</option>
            </select>
            <table>
                <thead>
                    <tr>
                        <th>Nombre del Servicio</th>
                        <th>Precio</th>
                        <th>Calificación</th>
                        <th>Descripción</th>
                        <th>Trabajador</th>
                        <th>Horarios</th>
                        <th>Acción</th>
                    </tr>
                </thead>
                <tbody>
                    {services.filter(service => service.nombre.toLowerCase().includes(search.toLowerCase())).map(service => (
                        <tr key={service.id}>
                            <td>{service.nombre}</td>
                            <td>{service.precio}</td>
                            <td>{service.calificacion}</td>
                            <td><button onClick={() => alert(service.descripcion)}>Ver Descripción</button></td>
                            <td>{service.trabajador.nombre}</td>
                            <td>{service.horarios}</td>
                            <td><button onClick={() => handleContact(service.id)}>Contactar Trabajador</button></td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default ServicesTable;
