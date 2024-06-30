import React, { useEffect, useState, useCallback } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

function ProbesMenu() {
  const [probes, setProbes] = useState([]);
  const [error, setError] = useState('');
  const [filterName, setFilterName] = useState('');
  const [isActiveOnly, setIsActiveOnly] = useState(false); // Estado para la casilla de verificación

  const fetchProbes = useCallback(async () => {
    try {
      const queryParams = new URLSearchParams();
      if (filterName) queryParams.append('Nombre', filterName);
      if (isActiveOnly) queryParams.append('is_active', true); // Agregar solo si isActiveOnly es true

      const response = await axios.get(`http://localhost:8080/v1/probes?${queryParams.toString()}`);
      if (response.status === 200) {
        setProbes(response.data);
      } else {
        setError('Error al obtener las sondas');
      }
    } catch (error) {
      setError('Error de red al obtener las sondas');
    }
  }, [filterName, isActiveOnly]);  // Incluir isActiveOnly en las dependencias

  useEffect(() => {
    fetchProbes();
  }, [fetchProbes]);

  return (
    <div style={styles.container}>
      <h1>Gestión de Sondas</h1>
      <input
        type="text"
        placeholder="Filtrar por nombre"
        value={filterName}
        onChange={e => setFilterName(e.target.value)}
        style={styles.input}
      />
      <label style={styles.label}>
        <input
          type="checkbox"
          checked={isActiveOnly}
          onChange={e => setIsActiveOnly(e.target.checked)}
          style={styles.checkbox}
        />
        Mostrar solo activas
      </label>
      <Link to="/add-probe">
        <button style={styles.button}>Añadir Sonda</button>
      </Link>
      {error && <p style={styles.error}>{error}</p>}
      <ul style={styles.list}>
        {probes.map((probe) => (
          <li key={probe.id} style={styles.listItem}>
            <Link to={`/probes/${probe.id}`}>{probe.id} - {probe.Name}</Link>
          </li>
        ))}
      </ul>
    </div>
  );
}

// Estilos incluidos en el componente, incluyendo estilos para la checkbox y la etiqueta
const styles = {
  container: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    height: '100vh',
    fontFamily: 'Arial, sans-serif'
  },
  button: {
    padding: '10px 20px',
    fontSize: '16px',
    borderRadius: '5px',
    border: 'none',
    backgroundColor: '#28a745',
    color: 'white',
    cursor: 'pointer',
    marginBottom: '20px',
  },
  error: {
    color: 'red',
    marginBottom: '20px',
  },
  list: {
    listStyleType: 'none',
    padding: 0,
    width: '80%',
    maxWidth: '600px',
  },
  listItem: {
    padding: '10px',
    margin: '10px 0',
    backgroundColor: '#f8f9fa',
    borderRadius: '5px',
    border: '1px solid #ddd',
  },
  input: {
    padding: '10px',
    marginBottom: '20px',
    width: '300px',
    borderRadius: '5px',
    border: '1px solid #ccc',
  },
  label: {
    marginBottom: '20px',
  },
  checkbox: {
    marginRight: '5px',
  }
};

export default ProbesMenu;
