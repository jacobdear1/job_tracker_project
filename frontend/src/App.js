import './App.css';

import React, { useState, useEffect } from 'react';
import RegisterForm from './components/RegisterForm';
import LoginForm from './components/LoginForm';
import JobForm from './components/JobForm';
import JobList from './components/JobList';
import axios from 'axios';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(!!localStorage.getItem('token'));
  const [jobApplications, setJobApplications] = useState([]);

  // Fetch job applications from the backend API when logged in
  const fetchJobApplications = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('/job-applications/', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setJobApplications(response.data);
    } catch (error) {
      console.error('Error fetching job applications:', error);
    }
  };

  useEffect(() => {
    if (isLoggedIn) {
      fetchJobApplications();
    }
  }, [isLoggedIn]);

  const handleLogin = () => {
    setIsLoggedIn(true);
    fetchJobApplications(); // Fetch job applications after logging in
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsLoggedIn(false);
    setJobApplications([]); // Clear job applications on logout
  };

  return (
    <div className="App">
      {!isLoggedIn ? (
        <>
          <RegisterForm />
          <LoginForm onLogin={handleLogin} />
        </>
      ) : (
        <>
          <button onClick={handleLogout}>Logout</button>
          <JobForm refreshApplications={fetchJobApplications} />
          <JobList jobApplications={jobApplications} />
        </>
      )}
    </div>
  );
}

export default App;

