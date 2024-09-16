// add new job applications here using this component 

import React, { useState } from 'react';
import api from '../api';

const JobForm = ({ refreshApplications }) => {
  const [companyName, setCompanyName] = useState('');
  const [position, setPosition] = useState('');
  const [dateApplied, setDateApplied] = useState('');
  const [status, setStatus] = useState('Applied');
  const [notes, setNotes] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post('/applications/', {
        company_name: companyName,
        position,
        date_applied: dateApplied,
        status,
        notes,
      });
      refreshApplications();
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div>
      <h2>Add Job Application</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Company Name"
          value={companyName}
          onChange={(e) => setCompanyName(e.target.value)}
          required
        />
        <input
          type="text"
          placeholder="Position"
          value={position}
          onChange={(e) => setPosition(e.target.value)}
          required
        />
        <input
          type="date"
          value={dateApplied}
          onChange={(e) => setDateApplied(e.target.value)}
          required
        />
        <input
          type="text"
          placeholder="Status"
          value={status}
          onChange={(e) => setStatus(e.target.value)}
        />
        <textarea
          placeholder="Notes"
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
        />
        <button type="submit">Add Application</button>
      </form>
    </div>
  );
};

export default JobForm;
