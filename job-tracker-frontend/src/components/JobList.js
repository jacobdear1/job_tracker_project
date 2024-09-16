// handles and displays all job listings, allowing for updates as well as deletions 

import React, { useState, useEffect } from 'react';
import api from '../api';

const JobList = () => {
  const [applications, setApplications] = useState([]);

  const fetchApplications = async () => {
    try {
      const response = await api.get('/applications/');
      setApplications(response.data);
    } catch (error) {
      console.log(error);
    }
  };

  const handleDelete = async (id) => {
    try {
      await api.delete(`/applications/${id}/`);
      fetchApplications();
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    fetchApplications();
  }, []);

  return (
    <div>
      <h2>Your Job Applications</h2>
      <ul>
        {applications.map((app) => (
          <li key={app.id}>
            <p><strong>Company:</strong> {app.company_name}</p>
            <p><strong>Position:</strong> {app.position}</p>
            <p><strong>Date Applied:</strong> {app.date_applied}</p>
            <p><strong>Status:</strong> {app.status}</p>
            <p><strong>Notes:</strong> {app.notes}</p>
            <button onClick={() => handleDelete(app.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default JobList;
