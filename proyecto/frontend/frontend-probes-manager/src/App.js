import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import ProbesMenu from './components/ProbesMenu';
import AddProbe from './components/AddProbe';
import ProbeDetails from './components/ProbeDetails';
import AddGroup from './components/AddGroup';
import ListGroups from './components/ListGroups';
import GroupDetails from './components/GroupDetails';
import ScanJobForm from './components/ScanJobForm';

function App() {
  return (
    <Router>
      <div style={styles.container}>
        <Routes>
          <Route path="/" element={
            <>
              <h1>Menú Principal</h1>
              <Link to="/probes-menu">
                <button style={styles.button}>Probes</button>
              </Link>
              <Link to="/probes-groups">
                <button style={styles.button}>Probes Groups</button>
              </Link>
            </>
          } />
          <Route path="/probes-menu" element={<ProbesMenu />} />
          <Route path="/add-probe" element={<AddProbe />} />
          <Route path="/probes-groups" element={<ListGroups />} />
          <Route path="/add-group" element={<AddGroup />} />
          <Route path="/probes/:id" element={<ProbeDetails />} />
          <Route path="/groups/:id" element={<GroupDetails />} />
          <Route path="/scan-job/:groupId/:jobId" element={<ScanJobForm />} />
        </Routes>
      </div>
    </Router>
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
  button: {
    padding: '10px 20px',
    fontSize: '16px',
    borderRadius: '5px',
    border: 'none',
    backgroundColor: '#007bff',
    color: 'white',
    cursor: 'pointer',
    margin: '10px',
  }
};

export default App;
