import React, { useState } from "react";
import { useForm } from "react-hook-form";
import { toast } from "react-hot-toast";
import api from "../services/api";
import { useNavigate } from "react-router-dom";

const Register = () => {
  const [userType, setUserType] = useState("cliente");
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();
  const navigate = useNavigate();

  const handleUserTypeChange = (e) => setUserType(e.target.value);

  const onSubmit = async (data) => {
    // Crear un nuevo FormData
    const formData = new FormData();
  
    // Añadir los campos del formulario a FormData
    formData.append('rut', data.rut);
    formData.append('nombre', data.nombre);
    formData.append('email', data.email);
    formData.append('telefono', data.telefono);
    formData.append('password', data.password); 
    formData.append('tipo_usuario', userType); // Añadir el tipo de usuario
  
    // Si el usuario es trabajador y ha subido un CV, lo añadimos al FormData
    if (userType === 'trabajador' && data.archivo_cv && data.archivo_cv[0]) {
        formData.append('archivo_cv', data.archivo_cv[0]);
    }

    try {
      // Realizar la solicitud de registro al backend (Django)
      const response = await api.post('http://127.0.0.1:8000/servis_api/usuarios/register/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
  
      toast.success('Usuario registrado con éxito');

      navigate('/login');
      
    } catch (error) {
      console.log(error.response?.data || error.message);
      toast.error('Hubo un error al registrar el usuario');
    }
  };

  return (
    <div
      className="d-flex justify-content-center align-items-center"
      style={{ height: "100vh", backgroundColor: "#f8f9fa" }}
    >
      <div
        className="card p-4"
        style={{
          width: "400px",
          borderRadius: "10px",
          boxShadow: "0px 4px 8px rgba(0, 0, 0, 0.1)",
        }}
      >
        <h2 className="text-center mb-4 text-success">Registro de Usuario</h2>
        <form onSubmit={handleSubmit(onSubmit)}>
          <div className="mb-3">
            <label htmlFor="rut" className="form-label">
              RUT
            </label>
            <input
              id="rut"
              type="text"
              className="form-control"
              {...register("rut", { required: "Este campo es obligatorio" })}
            />
            {errors.rut && (
              <div className="text-danger">{errors.rut.message}</div>
            )}
          </div>

          <div className="mb-3">
            <label htmlFor="password" className="form-label">
              Contraseña
            </label>
            <input
              id="password"
              type="password"
              className="form-control"
              {...register("password", {
                required: "Este campo es obligatorio",
              })}
            />
            {errors.password && (
              <div className="text-danger">{errors.password.message}</div>
            )}
          </div>

          <div className="mb-3">
            <label htmlFor="nombre" className="form-label">
              Nombre
            </label>
            <input
              id="nombre"
              type="text"
              className="form-control"
              {...register("nombre", { required: "Este campo es obligatorio" })}
            />
            {errors.nombre && (
              <div className="text-danger">{errors.nombre.message}</div>
            )}
          </div>

          <div className="mb-3">
            <label htmlFor="email" className="form-label">
              Correo Electrónico
            </label>
            <input
              id="email"
              type="email"
              className="form-control"
              {...register("email", { required: "Este campo es obligatorio" })}
            />
            {errors.email && (
              <div className="text-danger">{errors.email.message}</div>
            )}
          </div>

          <div className="mb-3">
            <label htmlFor="telefono" className="form-label">
              Teléfono
            </label>
            <input
              id="telefono"
              type="text"
              className="form-control"
              {...register("telefono", {
                required: "Este campo es obligatorio",
              })}
            />
            {errors.telefono && (
              <div className="text-danger">{errors.telefono.message}</div>
            )}
          </div>

          <div className="mb-3">
            <label htmlFor="tipo_usuario" className="form-label">
              Tipo de Usuario
            </label>
            <select
              id="tipo_usuario"
              className="form-select"
              value={userType}
              onChange={handleUserTypeChange}
            >
              <option value="cliente">Cliente</option>
              <option value="trabajador">Trabajador</option>
            </select>
          </div>

          {userType === "trabajador" && (
            <div className="mb-3">
              <label htmlFor="archivo_cv" className="form-label">
                Subir CV (PDF/Word)
              </label>
              <input
                id="archivo_cv"
                type="file"
                className="form-control"
                accept=".pdf,.doc,.docx"
                {...register("archivo_cv")}
              />
            </div>
          )}

          <button type="submit" className="btn btn-success w-100">
            Registrar
          </button>
        </form>
      </div>
    </div>
  );
};

export default Register;
