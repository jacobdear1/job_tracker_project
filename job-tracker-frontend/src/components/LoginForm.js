// handle user login and store the necessary JWT authorisation token locally 

import React, { useState } from 'react';
import api from '../api';

function LoginForm({ onLogin }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      //console.log(email);
      //console.log(password);
      
      // Create a FormData object and append form fields
      const formData = new FormData();
      formData.append('username', email);  // "username" is expected by OAuth2PasswordRequestForm
      formData.append('password', password);
      
      // Send the form data using the correct content type 'x-www-form-urlencoded'
      const response = await api.post('/token', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      });
  
      // Assuming the token is in response.data.access_token
      localStorage.setItem('token', response.data.access_token);
      onLogin();  // Notify parent that login was successful
    } catch (error) {
      setError('Invalid email or password');
    }
  };
  

  return (
    <div>
      <h2>Login</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <div>
          <label>Email</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit">Login</button>
      </form>
    </div>
  );
}

export default LoginForm;

