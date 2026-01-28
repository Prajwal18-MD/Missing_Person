import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../utils/AuthContext';

const Home = () => {
  const { isAuthenticated } = useAuth();

  return (
    <div>
      <div className="card">
        <div className="card-body" style={{ textAlign: 'center', padding: '3rem' }}>
          <h1 style={{ marginBottom: '1rem', color: '#2c3e50' }}>
            Missing Person Detection System
          </h1>
          <p style={{ fontSize: '1.2rem', color: '#666', marginBottom: '2rem' }}>
            Help find missing persons using advanced facial recognition technology
          </p>
          
          <div className="grid grid-2" style={{ maxWidth: '600px', margin: '0 auto' }}>
            <Link to="/upload-sighting" className="btn btn-primary" style={{ padding: '1rem' }}>
              Report a Sighting
            </Link>
            {isAuthenticated ? (
              <Link to="/create-case" className="btn btn-success" style={{ padding: '1rem' }}>
                Create Missing Person Case
              </Link>
            ) : (
              <Link to="/register" className="btn btn-success" style={{ padding: '1rem' }}>
                Register to Create Case
              </Link>
            )}
          </div>
        </div>
      </div>

      <div className="grid grid-3" style={{ marginTop: '2rem' }}>
        <div className="card">
          <div className="card-body">
            <h3 style={{ marginBottom: '1rem', color: '#3498db' }}>Report Sightings</h3>
            <p>
              Upload photos or videos of people you've seen. Our system will automatically 
              check for matches with missing persons.
            </p>
          </div>
        </div>
        
        <div className="card">
          <div className="card-body">
            <h3 style={{ marginBottom: '1rem', color: '#27ae60' }}>Create Cases</h3>
            <p>
              Register missing persons with their photos. Our facial recognition system 
              will monitor all sightings for potential matches.
            </p>
          </div>
        </div>
        
        <div className="card">
          <div className="card-body">
            <h3 style={{ marginBottom: '1rem', color: '#e74c3c' }}>Get Alerts</h3>
            <p>
              Receive instant email notifications when potential matches are found, 
              including location and confidence scores.
            </p>
          </div>
        </div>
      </div>

      <div className="card" style={{ marginTop: '2rem' }}>
        <div className="card-body">
          <h2 style={{ marginBottom: '1rem' }}>How It Works</h2>
          <div className="grid grid-2">
            <div>
              <h4>1. Upload Missing Person Photo</h4>
              <p>Create a case with a clear photo of the missing person.</p>
              
              <h4>2. Community Reports Sightings</h4>
              <p>Anyone can upload photos/videos of people they've seen.</p>
            </div>
            <div>
              <h4>3. AI Matches Faces</h4>
              <p>Our system automatically compares faces using advanced recognition.</p>
              
              <h4>4. Instant Alerts</h4>
              <p>Get notified immediately when potential matches are found.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;