import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

function ListGroups() {
  const [groups, setGroups] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchGroups = async () => {
      try {
        const response = await axios.get('http://localhost:8080/v1/probes-groups');
        if (response.status === 200) {
          setGroups(response.data);
        } else {
          setError('Error al obtener los grupos');
        }
      } catch (error) {
        setError(`Error de red al obtener los grupos: ${error.message}`);
      }
    };

    fetchGroups();
  }, []);

  return (
    <div style={styles.container}>
      <h1>Lista de Grupos de Sondas</h1>
      <Link to="/add-group"><button style={styles.addButton}>Añadir Grupo</button></Link>
      {error && <p style={styles.error}>{error}</p>}
      <ul style={styles.list}>
        {groups.map(group => (
          <li key={group.id} style={styles.listItem}>
            <Link to={`/groups/${group.id}`} style={styles.link}>{group.id} - {group.Name} </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}

const styles = {
  container: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    padding: '20px',
    fontFamily: 'Arial, sans-serif',
    width: '100%',
    maxWidth: '600px',
    margin: 'auto'
  },
  addButton: {
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
    width: '100%',
  },
  listItem: {
    padding: '10px',
    margin: '10px 0',
    backgroundColor: '#f8f9fa',
    borderRadius: '5px',
    border: '1px solid #ddd',
    textAlign: 'center',
    transition: 'background-color 0.3s, box-shadow 0.3s',
    ':hover': {
      backgroundColor: '#e8e8e8',
      boxShadow: '0 2px 5px rgba(0,0,0,0.2)'
    }
  },
  link: {
    textDecoration: 'none',
    color: '#007bff',
    fontWeight: 'bold',
    ':hover': {
      textDecoration: 'underline',
    }
  }
};

export default ListGroups;
