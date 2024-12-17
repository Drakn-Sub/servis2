import React from "react";
import { useForm } from "react-hook-form";
import { toast } from "react-hot-toast";
import api from "../services/api";
import { useNavigate } from "react-router-dom";

const Login = () => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();
  const navigate = useNavigate();

  const onSubmit = async (data) => {
    console.log(data);
    try {
      // Aquí estamos enviando el objeto 'data' directamente a la API
      const response = await api.post("login/", {
        rut: data.rut,
        password: data.password,
      });
      console.log("tipo_usuario:", response.data.tipo_usuario);
      localStorage.setItem("access", response.data.access);
      if (response.data.tipo_usuario === "cliente") {
        navigate("/cliente");
      } else if (response.data.tipo_usuario === "trabajador") {
        navigate("/trabajador");
      }
    } catch (error) {
      console.error(error.response ? error.response.data : error); // Ver detalles completos de la respuesta
      toast.error("Hubo un error al intentar iniciar sesión");
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
        <h2 className="text-center mb-4 text-success">Iniciar sesión</h2>
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

          <button type="submit" className="btn btn-success w-100">
            Iniciar sesión
          </button>
        </form>
      </div>
    </div>
  );
};

export default Login;
