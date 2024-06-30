import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

function AddProbe() {
  const [nombre, setNombre] = useState('');
  const [ip, setIp] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const handleRegister = async () => {
    try {
      const response = await axios.post('http://localhost:8080/v1/probes', null, {
        params: { Nombre: nombre, IP: ip }
      });

      if (response.status === 200) {
        setMessage(`Sonda registrada con ID: ${response.data.id}`);
        setTimeout(() => navigate('/probes-menu'), 2000); // Redirige después de 2 segundos
      }
    } catch (error) {
      setMessage(`Error al registrar la sonda: ${error.response?.data?.error || error.message}`);
    }
  };

  return (
    <div style={styles.container}>
      <h1>Registrar Nueva Sonda</h1>
      <input
        type="text"
        placeholder="Nombre"
        value={nombre}
        onChange={(e) => setNombre(e.target.value)}
        style={styles.input}
      />
      <input
        type="text"
        placeholder="IP"
        value={ip}
        onChange={(e) => setIp(e.target.value)}
        style={styles.input}
      />
      <button onClick={handleRegister} style={styles.button}>Registrar</button>
      {message && <p style={styles.message}>{message}</p>}
    </div>
  );
}

const styles = {
  container: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    height: '100vh',
    fontFamily: 'Arial, sans-serif'
  },
  input: {
    width: '300px',
    padding: '10px',
    margin: '10px 0',
    fontSize: '16px',
    borderRadius: '5px',
    border: '1px solid #ccc',
  },
  button: {
    padding: '10px 20px',
    fontSize: '16px',
    borderRadius: '5px',
    border: 'none',
    backgroundColor: '#28a745',
    color: 'white',
    cursor: 'pointer',
  },
  message: {
    marginTop: '20px',
    fontSize: '18px',
    color: '#333',
  }
};

export default AddProbe;
