import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function AddGroup() {
  const [name, setName] = useState('');
  const [probes, setProbes] = useState([]);
  const [selectedProbes, setSelectedProbes] = useState([]);
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  // Cargar todas las sondas disponibles al cargar el componente
  useEffect(() => {
    const fetchProbes = async () => {
      try {
        const response = await axios.get('http://localhost:8080/v1/probes');
        if (response.status === 200) {
          setProbes(response.data);
        }
      } catch (error) {
        setMessage(`Error al cargar las sondas: ${error.message}`);
      }
    };

    fetchProbes();
  }, []);

  const handleAddGroup = async () => {
    const probeData = probes.filter(probe => selectedProbes.includes(probe.id));
    try {
      const response = await axios.post(`http://localhost:8080/v1/probes-groups?Nombre=${name}`, probeData);
      if (response.status === 200) {
        setMessage(`Grupo creado con éxito: ${response.data.id}`);
        setTimeout(() => navigate('/probes-groups'), 2000); // Redirige después de 2 segundos
      } else {
        setMessage('No se pudo registrar el grupo');
      }
    } catch (error) {
      setMessage(`Error al registrar el grupo: ${error.response?.data?.error || error.message}`);
    }
  };

  const handleSelectProbe = (probeId) => {
    const newSelection = selectedProbes.includes(probeId)
      ? selectedProbes.filter(id => id !== probeId)
      : [...selectedProbes, probeId];
    setSelectedProbes(newSelection);
  };

  return (
    <div style={styles.container}>
      <h1>Registrar Nuevo Grupo</h1>
      <input
        type="text"
        placeholder="Nombre del Grupo"
        value={name}
        onChange={(e) => setName(e.target.value)}
        style={styles.input}
      />
      <div>
        <h2>Seleccionar Sondas:</h2>
        {probes.map(probe => (
          <div key={probe.id}>
            <input
              type="checkbox"
              checked={selectedProbes.includes(probe.id)}
              onChange={() => handleSelectProbe(probe.id)}
            />
            {probe.Name}
          </div>
        ))}
      </div>
      <button onClick={handleAddGroup} style={styles.button}>Registrar Grupo</button>
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
    margin: '10px',
  },
  message: {
    marginTop: '20px',
    fontSize: '18px',
    color: '#333',
  }
};

export default AddGroup;
