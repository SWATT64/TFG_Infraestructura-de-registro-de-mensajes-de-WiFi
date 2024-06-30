import React, { useEffect, useState, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

function ProbeDetails() {
  const { id } = useParams();
  const [probe, setProbe] = useState(null);
  const [currentWork, setCurrentWork] = useState('');  // Nuevo estado para el trabajo actual
  const [error, setError] = useState('');
  const [updateMessage, setUpdateMessage] = useState('');
  const navigate = useNavigate();

  const fetchProbeDetails = useCallback(async () => {
    try {
      const response = await fetch(`http://localhost:8080/v1/probes/${id}`);
      if (!response.ok) {
        setError('Error al obtener los detalles de la sonda');
        return;
      }
      const data = await response.json();
      setProbe(data);
  
      const workResponse = await fetch(`http://localhost:8080/v1/probes/${id}/current-job`);
      if (!workResponse.ok) {
        setCurrentWork(null);
        return;
      }
      const workData = await workResponse.json();
      setCurrentWork(workData);
    } catch (error) {
      setError('Error de red al obtener los detalles de la sonda');
    }
  }, [id]);
  
  

  useEffect(() => {
    fetchProbeDetails();
  }, [fetchProbeDetails]);

  const handleUpdate = async () => {
    try {
      const response = await fetch(`http://localhost:8080/v1/probes/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ id: probe.id, Name: probe.Name, LastRecordedIP: probe.LastRecordedIP }),
      });
      if (response.ok) {
        setUpdateMessage('Sonda actualizada correctamente');
        fetchProbeDetails();
      } else {
        setUpdateMessage('Error al actualizar la sonda');
      }
    } catch (error) {
      setUpdateMessage('Error de red al actualizar la sonda');
    }
  };

  const handleDelete = async () => {
    try {
      const response = await fetch(`http://localhost:8080/v1/probes/${id}`, {
        method: 'DELETE',
      });
      if (response.ok) {
        navigate('/probes-menu');
      } else {
        setError('Error al eliminar la sonda');
      }
    } catch (error) {
      setError('Error de red al eliminar la sonda');
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setProbe((prevProbe) => ({
      ...prevProbe,
      [name]: value,
    }));
  };

  const handleClose = () => {
    navigate('/probes-menu');
  };

  if (!probe) {
    return <p>Cargando...</p>;
  }

  return (
    <div style={styles.container}>
      <h1>Detalles de la Sonda</h1>
      {error && <p style={styles.error}>{error}</p>}
      {updateMessage && <p style={styles.updateMessage}>{updateMessage}</p>}
      <div style={styles.details}>
        <p><strong>ID:</strong> {probe.id}</p>
        <p>
          <strong>Nombre:</strong>
          <input
            type="text"
            name="Name"
            value={probe.Name}
            onChange={handleChange}
            style={styles.input}
          />
        </p>
        <p>
          <strong>Última IP registrada:</strong>
          <input
            type="text"
            name="LastRecordedIP"
            value={probe.LastRecordedIP}
            onChange={handleChange}
            style={styles.input}
          />
        </p>
        <p><strong>En uso:</strong> {probe.InUse ? 'Sí' : 'No'}</p>
        {currentWork ? (
          <div style={styles.currentWork}>
            <h2>Trabajando actualmente en:</h2>
            {currentWork.Job.Status && <p><strong>Status:</strong> {currentWork.Job.Status}</p>}
            {currentWork.Job.group_id && <p><strong>Grupo:</strong> {currentWork.Job.group_id}</p>}
            {currentWork.Job.BSSID && <p><strong>BSSID:</strong> {currentWork.Job.BSSID}</p>}
            {currentWork.Job.ESSID && <p><strong>ESSID:</strong> {currentWork.Job.ESSID}</p>}
            {currentWork.Job.Channel && <p><strong>Channel:</strong> {currentWork.Job.Channel}</p>}
            {currentWork.Job.IP && <p><strong>IP:</strong> {currentWork.Job.IP}</p>}
            {currentWork.Job.WaveLenght && <p><strong>WaveLenght:</strong> {currentWork.Job.WaveLenght}</p>}
            {currentWork.Job.created_at && <p><strong>Created At:</strong> {new Date(currentWork.Job.created_at).toLocaleString()}</p>}
          </div>
        ) : <p>No hay trabajo asignado actualmente.</p>}
      </div>
      <button onClick={handleUpdate} style={styles.button}>Actualizar</button>
      <button onClick={handleDelete} style={{ ...styles.button, backgroundColor: '#dc3545' }}>Eliminar</button>
      <button onClick={handleClose} style={styles.button}>Cerrar</button>
    </div>
  );
  
}

const styles = {
  currentWork: {
    backgroundColor: '#f0f0f0',
    padding: '10px',
    borderRadius: '5px',
    margin: '10px 0',
    textAlign: 'left',
  },
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
    backgroundColor: '#007bff',
    color: 'white',
    cursor: 'pointer',
    margin: '10px',
  },
  error: {
    color: 'red',
    marginBottom: '20px',
  },
  updateMessage: {
    color: 'green',
    marginBottom: '20px',
  },
  details: {
    textAlign: 'left',
    marginBottom: '20px',
  },
  input: {
    width: '100%',
    padding: '10px',
    margin: '5px 0',
    fontSize: '16px',
    borderRadius: '5px',
    border: '1px solid #ccc',
  }
};

export default ProbeDetails;
