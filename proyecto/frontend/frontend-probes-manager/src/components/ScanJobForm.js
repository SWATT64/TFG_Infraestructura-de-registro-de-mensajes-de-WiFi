import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams, useNavigate } from 'react-router-dom';
import { useFormik } from 'formik';
import * as Yup from 'yup';

const ScanJobForm = () => {
  const { groupId, jobId } = useParams();
  const navigate = useNavigate();
  const [networks, setNetworks] = useState([]);
  const [fields, setFields] = useState({ bssid: [], essid: [], security: [], channel: [] });
  const [loading, setLoading] = useState(true);
  const [jobSubmitted, setJobSubmitted] = useState(null);

  useEffect(() => {
    const fetchNetworks = async () => {
      setLoading(true);
      try {
        const url = `http://localhost:8080/v1/probes-groups/${groupId}/jobs/${jobId}/monitorize`;
        const response = await axios.get(url, {
          headers: {
            'Accept': 'application/json'
          }
        });
        if (response.status === 200) {
          const networksData = response.data.networks.map(network => ({
            bssid: network.BSSID.trim(), // Limpieza de espacios extra
            channel: network.Channel.trim(),
            essid: network.ESSID.trim(),
            security: network.Security.trim(),
          }));
          setNetworks(networksData);
          setFields({
            bssid: getAllOptions(networksData, 'bssid'),
            essid: getAllOptions(networksData, 'essid'),
            security: getAllOptions(networksData, 'security'),
            channel: getAllOptions(networksData, 'channel')
          });
        } else {
          console.error('Error fetching networks:', response.status);
        }
      } catch (error) {
        console.error('Error fetching networks:', error);
      } finally {
        setLoading(false);
      }
    };
    
    const getAllOptions = (data, field) => {
      return [...new Set(data.map(item => item[field.toLowerCase()]))].filter(Boolean); // Ajuste a minúsculas
    };
    
    fetchNetworks();
  }, [groupId, jobId]);

  const formik = useFormik({
    initialValues: {
      bssid: '',
      essid: '',
      security: '',
      channel: '',
      WaveLength: '',  // Nuevo campo
      cswitch: '',    // New field
      wildcard: '',   // New field
      ChannelMode: '', // New field
      band: '',       // New field
      associated_clients: false // New field
    },
    validationSchema: Yup.object({
      bssid: Yup.string(),
      essid: Yup.string(),
      security: Yup.string(),
      channel: Yup.number().integer(),
      WaveLength: Yup.string(),
      cswitch: Yup.number().integer(),
      wildcard: Yup.string()
      .matches(/^(FF|00)(:(FF|00)){5}$/, { message: "Wildcard must be in format FF:FF:FF:FF:FF:FF or 00:00:00:00:00:00" }),
      ChannelMode: Yup.string(),
      band: Yup.string(),
      associated_clients: Yup.boolean()
    }),
    onSubmit: (values) => {
      const jobData = {
        Job: {
          BSSID: values.bssid || undefined,
          ESSID: values.essid || undefined,
          Channel: values.channel ? parseInt(values.channel, 10) : undefined,
          WaveLenght: values.WaveLength || undefined,
          Status: "scan",  // Assuming 'scan' is the default status if not provided
          band: values.band || undefined,
          cswitch: values.cswitch ? parseInt(values.channel, 10): undefined,
          security: values.security || undefined,
          wildcard: values.wildcard || undefined,
          associated_clients: values.associated_clients,
          ChannelMode: values.ChannelMode || undefined
        }
      };

      const url = `http://localhost:8080/v1/probes-groups/${groupId}/jobs`; // Adjust URL as needed
      axios.post(url, jobData)
        .then(response => {
          console.log('Job created successfully:', response);
          setJobSubmitted(true); // Handle the successful submission state
          setTimeout(() => {
            navigate(`/groups/${groupId}`); // Navigate after submission
          }, 3000);
        })
        .catch(error => {
          console.error('Error submitting job:', error);
        });
    }
  });

  const handleBandChange = (e) => {
    const { value, checked } = e.target;
    let newBand = formik.values.band;
    if (checked) {
      if (!newBand.includes(value)) {
        newBand += value;
      }
    } else {
      newBand = newBand.replace(value, '');
    }
    formik.setFieldValue('band', newBand);
  };

  useEffect(() => {
    setFields({
      bssid: getFilteredOptions('bssid', formik.values),
      essid: getFilteredOptions('essid', formik.values),
      security: getFilteredOptions('security', formik.values),
      channel: getFilteredOptions('channel', formik.values)
    });
  }, [formik.values]);


  const getFilteredOptions = (field, values) => {
    field = field.toLowerCase(); // Ajuste para comparación de campos
    return networks
      .filter(network => {
        return (!values.bssid || network.bssid === values.bssid) &&
               (!values.essid || network.essid === values.essid) &&
               (!values.security || network.security === values.security) &&
               (!values.channel || network.channel === values.channel);
      })
      .map(network => network[field])
      .filter((value, index, self) => value && self.indexOf(value) === index);
  };


  if (loading) {
    return <p>Loading...</p>;
  }

  return (
    <div>
      <h1>Assign Scan Job</h1>
      <form onSubmit={formik.handleSubmit}>
        <div style={styles.formControl}>
          <label htmlFor="bssid">BSSID:</label>
          <select
            id="bssid"
            name="bssid"
            onChange={formik.handleChange}
            value={formik.values.bssid}
            onBlur={formik.handleBlur}
            style={styles.select}
          >
            <option value="">All BSSIDs</option>
            {fields.bssid.map((bssid, index) => (
              <option key={index} value={bssid}>{bssid}</option>
            ))}
          </select>
        </div>
        <div style={styles.formControl}>
          <label htmlFor="essid">ESSID:</label>
          <select
            id="essid"
            name="essid"
            onChange={formik.handleChange}
            value={formik.values.essid}
            onBlur={formik.handleBlur}
            style={styles.select}
          >
            <option value="">All ESSIDs</option>
            {fields.essid.map((essid, index) => (
              <option key={index} value={essid}>{essid}</option>
            ))}
          </select>
        </div>

        <div style={styles.formControl}>
          <label htmlFor="security">Security:</label>
          <select
            id="security"
            name="security"
            onChange={formik.handleChange}
            value={formik.values.security}
            onBlur={formik.handleBlur}
            style={styles.select}
          >
            <option value="">All Security Types</option>
            {fields.security.map((security, index) => (
              <option key={index} value={security}>{security}</option>
            ))}
          </select>
        </div>

        <div style={styles.formControl}>
          <label htmlFor="channel">Channel:</label>
          <select
            id="channel"
            name="channel"
            onChange={formik.handleChange}
            value={formik.values.channel}
            onBlur={formik.handleBlur}
            style={styles.select}
          >
            <option value="">All Channels</option>
            {fields.channel.map((channel, index) => (
              <option key={index} value={channel}>{channel}</option>
            ))}
          </select>
        </div>

        <div style={styles.formControl}>
          <label htmlFor="WaveLength">WaveLength:</label>
          <select
            id="WaveLength"
            name="WaveLength"
            onChange={formik.handleChange}
            value={formik.values.WaveLength}
            onBlur={formik.handleBlur}
            style={styles.select}
          >
            <option value="">Select WaveLength</option>
            <option value="2.4 GHz">2.4 GHz</option>
            <option value="5 GHz">5 GHz</option>
          </select>
        </div>
        <div style={styles.formControl}>
        <label htmlFor="ChannelMode">Channel Mode:</label>
        <select
          id="ChannelMode"
          name="ChannelMode"
          onChange={formik.handleChange}
          value={formik.values.ChannelMode}
          style={styles.select}
        >
          <option value="">Select Channel Mode</option>
          <option value="ht20">HT20</option>
          <option value="ht40-">HT40-</option>
          <option value="ht40+">HT40+</option>
        </select>
      </div>
      <div style={styles.formControl}>
        <label htmlFor="cswitch">Channel Switch:</label>
        <select
          id="cswitch"
          name="cswitch"
          onChange={formik.handleChange}
          value={formik.values.cswitch}
          style={styles.select}
        >
          <option value="">Select Switch Method</option>
          <option value="0">0</option>
          <option value="1">1</option>
          <option value="2">2</option>
        </select>
      </div>
      <div>
        <label htmlFor="wildcard">Netmask: </label>
        <input
          id="wildcard"
          name="wildcard"
          type="text"
          onChange={formik.handleChange}
          value={formik.values.wildcard}
          list="wildcardOptions"
        />
        <datalist id="wildcardOptions">
          <option value="FF:FF:FF:FF:FF:FF">FF:FF:FF:FF:FF:FF</option>
          <option value="00:00:00:00:00:00">00:00:00:00:00:00</option>
          <option value="FF:FF:00:FF:00:00">FF:FF:00:FF:00:00</option>
          <option value="00:FF:FF:00:FF:FF">00:FF:FF:00:FF:FF</option>
        </datalist>
      </div>
      <br />
      <div style={styles.formControl}>
        <label htmlFor="band">Band:</label>
        <div>
          <label htmlFor="band_a">
            <input
              id="band_a"
              name="band_a"
              type="checkbox"
              value="a"
              onChange={handleBandChange}
              checked={formik.values.band.includes('a')}
            /> A (5 GHz)
          </label>
        </div>
        <div>
          <label htmlFor="band_b">
            <input
              id="band_b"
              name="band_b"
              type="checkbox"
              value="b"
              onChange={handleBandChange}
              checked={formik.values.band.includes('b')}
            /> B (2.4 GHz)
          </label>
        </div>
        <div>
          <label htmlFor="band_g">
            <input
              id="band_g"
              name="band_g"
              type="checkbox"
              value="g"
              onChange={handleBandChange}
              checked={formik.values.band.includes('g')}
            /> G (2.4 GHz)
          </label>
        </div>
      </div>
      <div style={styles.formControl}>
        <label htmlFor="associated_clients">Show Associated Clients:</label>
        <input
          id="associated_clients"
          name="associated_clients"
          type="checkbox"
          onChange={formik.handleChange}
          checked={formik.values.associated_clients}
          style={styles.checkbox}
        />
      </div>
        <button type="submit" style={styles.button}>Submit</button>
      </form>
      {jobSubmitted && (
        <div style={styles.message}>
          Trabajo de escaneo asignado correctamente.
        </div>
      )}
    </div>
  );
};

const styles = {
  formControl: {
    marginBottom: '15px'
  },
  select: {
    width: '100%',
    padding: '8px',
    margin: '8px 0',
    display: 'inline-block',
    border: '1px solid #ccc',
    borderRadius: '4px',
    boxSizing: 'border-box'
  },
  button: {
    width: '100%',
    backgroundColor: '#4CAF50',
    color: 'white',
    padding: '14px 20px',
    margin: '8px 0',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer'
  },
  message: {
    marginTop: '20px',
    padding: '10px',
    backgroundColor: '#dff0d8',
    color: '#3c763d',
    borderRadius: '4px',
    textAlign: 'center'
  }
};

export default ScanJobForm;
