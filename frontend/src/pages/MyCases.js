import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { casesAPI } from '../services/api';

const MyCases = () => {
  const [cases, setCases] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchCases();
  }, []);

  const fetchCases = async () => {
    try {
      const response = await casesAPI.getAll();
      setCases(response.data);
    } catch (error) {
      setError('Failed to fetch cases');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (caseId) => {
    if (window.confirm('Are you sure you want to delete this case?')) {
      try {
        await casesAPI.delete(caseId);
        setCases(cases.filter(c => c.id !== caseId));
      } catch (error) {
        setError('Failed to delete case');
      }
    }
  };

  if (loading) {
    return <div className="loading">Loading your cases...</div>;
  }

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <h2>My Missing Person Cases</h2>
        <Link to="/create-case" className="btn btn-primary">
          Create New Case
        </Link>
      </div>

      {error && (
        <div className="alert alert-error">
          {error}
        </div>
      )}

      {cases.length === 0 ? (
        <div className="card">
          <div className="card-body" style={{ textAlign: 'center', padding: '3rem' }}>
            <h3>No cases found</h3>
            <p>You haven't created any missing person cases yet.</p>
            <Link to="/create-case" className="btn btn-primary">
              Create Your First Case
            </Link>
          </div>
        </div>
      ) : (
        <div className="grid grid-2">
          {cases.map(caseItem => (
            <div key={caseItem.id} className="card">
              <div className="card-header">
                <h3>{caseItem.name}</h3>
                <span className={`badge ${caseItem.is_found ? 'badge-success' : 'badge-warning'}`}>
                  {caseItem.is_found ? 'Found' : 'Active'}
                </span>
              </div>
              
              <div className="card-body">
                {caseItem.photo_path && (
                  <div style={{ textAlign: 'center', marginBottom: '1rem' }}>
                    <img 
                      src={`http://localhost:8000/${caseItem.photo_path}`}
                      alt={caseItem.name}
                      style={{ 
                        maxWidth: '150px', 
                        maxHeight: '150px', 
                        objectFit: 'cover',
                        borderRadius: '4px'
                      }}
                    />
                  </div>
                )}
                
                <div className="case-details">
                  {caseItem.address && (
                    <p><strong>Address:</strong> {caseItem.address}</p>
                  )}
                  {caseItem.email && (
                    <p><strong>Contact Email:</strong> {caseItem.email}</p>
                  )}
                  {caseItem.phone && (
                    <p><strong>Contact Phone:</strong> {caseItem.phone}</p>
                  )}
                  <p><strong>Created:</strong> {new Date(caseItem.created_at).toLocaleDateString()}</p>
                </div>
              </div>
              
              <div className="card-footer">
                <div style={{ display: 'flex', gap: '0.5rem' }}>
                  <button 
                    onClick={() => handleDelete(caseItem.id)}
                    className="btn btn-danger"
                    style={{ fontSize: '0.9rem', padding: '0.5rem 1rem' }}
                  >
                    Delete
                  </button>
                  {caseItem.is_found && (
                    <span style={{ 
                      color: '#27ae60', 
                      fontWeight: 'bold',
                      alignSelf: 'center'
                    }}>
                      ✓ Person Found
                    </span>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default MyCases;