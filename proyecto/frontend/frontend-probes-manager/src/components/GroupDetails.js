import React, { useEffect, useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import axios from 'axios';

function GroupDetails() {
  const navigate = useNavigate();
  const { id } = useParams();
  const [group, setGroup] = useState(null);
  const [probes, setProbes] = useState([]);
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isAssigningJob, setIsAssigningJob] = useState(false);
  const [monitoringMessage, setMonitoringMessage] = useState('');
  const [stopMessage, setStopMessage] = useState('');
  const [currentJobIndex, setCurrentJobIndex] = useState(0);




  useEffect(() => {
    const fetchGroupDetails = async () => {
      try {
        const groupResponse = await axios.get(`http://localhost:8080/v1/probes-groups/${id}`);
        const probesResponse = await Promise.all(groupResponse.data.probes_id.map(probeId =>
          axios.get(`http://localhost:8080/v1/probes/${probeId}`)
        ));
        const jobsResponse = await axios.get(`http://localhost:8080/v1/probes-groups/${id}/jobs`);

        if (groupResponse.status === 200) {
          setGroup(groupResponse.data);
          setProbes(probesResponse.map(response => response.data));
          setJobs(jobsResponse.data);
        } else {
          console.error('Failed to fetch group details');
        }
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setLoading(false);
      }
    };
      

    fetchGroupDetails();
  }, [id]);


  const handleMonitorize = async () => {
    const jobData = {
      Job: {
        Status: "monitorize"
      }
    };
  
    try {
      const response = await axios.post(`http://localhost:8080/v1/probes-groups/${id}/jobs`, jobData);
  
      if (response.status === 200) {
        // Feedback positivo y actualización de la UI
        console.log('Trabajo de monitorización asignado correctamente.');
        setMonitoringMessage('Proceso de monitorización activado!');
        setTimeout(() => {
          setMonitoringMessage('');
          fetchJobs(); // Actualiza la lista de trabajos después de un tiempo
        }, 3000);
      } else {
        console.error('Error al asignar el trabajo de monitorización');
      }
    } catch (error) {
      console.error('Error al enviar la solicitud de monitorización:', error);
    }
  };
  const fetchJobs = async () => {
    try {
      const response = await axios.get(`http://localhost:8080/v1/probes-groups/${id}/jobs`);
      if (response.status === 200) {
        setJobs(response.data); // Asumiendo que la API devuelve la lista de trabajos directamente
      } else {
        console.log('Error fetching jobs');
      }
    } catch (error) {
      console.error('Error: ', error);
    }
  };
    
  const handleStopJob = async () => {
    const jobData = {
      Job: {
        Status: "stop"
      }
    };
  
    try {
      const response = await axios.post(`http://localhost:8080/v1/probes-groups/${id}/jobs`, jobData);
  
      if (response.status === 200) {
        // Feedback positivo y actualización de la UI
        console.log('Trabajo parado correctamente.');
        setStopMessage('Trabajo parado correctamente');
        setTimeout(() => {
          setStopMessage('');
          fetchJobs(); // Actualiza la lista de trabajos después de un tiempo
        }, 3000);
      } else {
        console.error('Error al asignar el trabajo de parada');
      }
    } catch (error) {
      console.error('Error al enviar la solicitud de parada:', error);
    }
  };
  const goToNextJob = () => {
    setCurrentJobIndex(prevIndex => (prevIndex + 1) % jobs.length); // Asegura que el índice se reinicie al final
  };
  
  const goToPreviousJob = () => {
    setCurrentJobIndex(prevIndex => (prevIndex - 1 + jobs.length) % jobs.length); // Asegura que el índice sea cíclico
  };

  const handleNavigate = (id2) => {
    console.log('ID=', id)
    navigate(`/scan-job/${id}/${id2}`);
  };
  
  

  const StatusIndicator = ({ isActive }) => {
    const style = {
      height: '10px',
      width: '10px',
      borderRadius: '50%',
      backgroundColor: isActive ? 'green' : 'red',
      display: 'inline-block',
      marginLeft: '5px'
    };

    const tooltipText = isActive ? "Activo" : "Parado";

    return <span style={style} title={tooltipText} />;
  };

  const handleAssignNewJob = async () => {
      setIsAssigningJob(true);
    };

  
    if (loading) {
      return <p>Loading...</p>;
  }

  return (
    <div style={styles.container}>

      <h1 style={styles.header}>Detalles del Grupo</h1>
      {group && (
        <div style={styles.groupDetails}>
          <h2>{group.id} - {group.Name}</h2>
          <p>{group.is_active ? 'Estado: Activo' : 'Estado: Inactivo'}</p>
          <h3>Sondas en el Grupo:</h3>

          {probes.map(probe => (
            <div key={probe.id} style={styles.probeDetail}>
              {probe.id} - {probe.Name}
              <Link to={`/probes/${probe.id}`} style={styles.detailsLink}>Ver Detalles</Link>
            </div>
          ))}

          <h3>Trabajos Realizados:</h3>
          <div style={styles.jobsContainer}>

          {
            jobs.length > 0 ? (
                <div style={styles.jobViewer}>

                    <button onClick={goToPreviousJob} style={styles.navButton}>&lt;</button>
                    <div style={styles.jobDetail}>
                    <p><strong>ID:</strong> {jobs[currentJobIndex].Job.JobID}</p>
                    {jobs[currentJobIndex].Job.BSSID && <p><strong>BSSID:</strong> {jobs[currentJobIndex].Job.BSSID}</p>}
                    {jobs[currentJobIndex].Job.ESSID && <p><strong>ESSID:</strong> {jobs[currentJobIndex].Job.ESSID}</p>}
                    {jobs[currentJobIndex].Job.Channel && <p><strong>Channel:</strong> {jobs[currentJobIndex].Job.Channel}</p>}
                    {jobs[currentJobIndex].Job.IP && <p><strong>IP:</strong> {jobs[currentJobIndex].Job.IP}</p>}
                    {jobs[currentJobIndex].Job.WaveLenght && <p><strong>WaveLenght:</strong> {jobs[currentJobIndex].Job.WaveLenght}</p>}
                    <p><strong>Status:</strong> {jobs[currentJobIndex].Job.Status} <StatusIndicator isActive={jobs[currentJobIndex].Job.is_active} /></p>
                    {jobs[currentJobIndex].Job.created_at && <p><strong>Created At:</strong> {new Date(jobs[currentJobIndex].Job.created_at).toLocaleString()}</p>}
                    {jobs[currentJobIndex].URL?.URL && (
                    <a href={jobs[currentJobIndex].URL.URL} style={styles.downloadLink} target="_blank" rel="noopener noreferrer">Descargar Trabajo</a>
                    )}
                    </div>
                    <button onClick={goToNextJob} style={styles.navButton}>&gt;</button>
                </div>
            ) : <p>No jobs found for this group.</p>}


          </div>
          {!monitoringMessage && !isAssigningJob && (
            <>
                <button onClick={handleStopJob} style={styles.button}>Parar Trabajo</button>
                <button onClick={handleAssignNewJob} style={styles.button}>Asignar Nuevo Trabajo</button>
                <p>{stopMessage}</p>
            </>
            )}

            {isAssigningJob && (
            <>
                <p style={styles.monitoringMessage}>{monitoringMessage}</p>
                <button onClick={   handleMonitorize} style={styles.button}>Monitorizar</button>
                <button onClick={() => handleNavigate(jobs[currentJobIndex].Job.JobID)} style={styles.button}>Escanear</button>

            </>
            )}

            {monitoringMessage && !isAssigningJob && (
                <p style={styles.monitoringMessage}>{monitoringMessage}</p>
            )}
        </div>
      )}
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
        width: '100%', // Asegura que el contenedor use el ancho disponible.
        overflow: 'auto' // Asegura que el contenido sea accesible con scroll si es necesario.
      },
    monitoringMessage: {
        color: 'green',
        fontSize: '16px',
        marginBottom: '10px',
      },
    header: {
      color: '#007bff',
      marginBottom: '20px',
      fontSize: '24px', 
    },
    groupDetails: {
      width: '90%',
      maxWidth: '960px',
      padding: '20px',
      margin: '10px 0',
      border: '1px solid #ccc',
      borderRadius: '5px',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'flex-start',
    },
    downloadLink: {
        color: '#007bff',
        textDecoration: 'none',
        fontWeight: 'bold',
        marginTop: '10px',
        display: 'inline-block',
      },
    probeDetail: {
      margin: '10px 0',
      padding: '10px',
      borderBottom: '1px solid #ddd',
      width: '97%', 
    },
    detailsLink: {
      marginLeft: '10px',
      color: '#007bff',
      textDecoration: 'none'
    },
    jobsContainer: {
        width: '97%', // Mantiene el ancho del contenedor padre.
        border: '1px solid #ccc',
        padding: '10px',
        marginBottom: '10px', // Añade un margen inferior para separación visual.
      },
    jobViewer: {
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between'
      },
      jobDetail: {
        flex: 1,
        padding: '10px'
      },
      navButton: {
        cursor: 'pointer'
      },
    workSection: {
      width: '90%',
      marginTop: '20px',
      display: 'flex',
      flexDirection: 'column', 
      alignItems: 'center', 
      padding: '10px',
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
    }
  };
  
  

export default GroupDetails;
