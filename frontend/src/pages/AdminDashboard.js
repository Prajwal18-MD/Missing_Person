import React, { useState, useEffect } from 'react';
import { adminAPI } from '../services/api';
import MapComponent from '../components/MapComponent';

const AdminDashboard = () => {
  const [stats, setStats] = useState(null);
  const [cases, setCases] = useState([]);
  const [matches, setMatches] = useState([]);
  const [selectedCase, setSelectedCase] = useState(null);
  const [locationHistory, setLocationHistory] = useState([]);
  const [activeTab, setActiveTab] = useState('overview');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [statsRes, casesRes, matchesRes] = await Promise.all([
        adminAPI.getStats(),
        adminAPI.getAllCases(),
        adminAPI.getAllMatches()
      ]);
      
      setStats(statsRes.data);
      setCases(casesRes.data);
      setMatches(matchesRes.data);
    } catch (error) {
      setError('Failed to fetch dashboard data');
    } finally {
      setLoading(false);
    }
  };

  const handleMarkFound = async (caseId) => {
    if (window.confirm('Are you sure you want to mark this person as found?')) {
      try {
        await adminAPI.markFound(caseId);
        fetchData(); // Refresh data
      } catch (error) {
        setError('Failed to mark person as found');
      }
    }
  };

  const handleVerifyMatch = async (matchId, verified) => {
    try {
      await adminAPI.updateMatch(matchId, { verified });
      fetchData(); // Refresh data
    } catch (error) {
      setError('Failed to update match');
    }
  };

  const handleViewLocationHistory = async (caseId) => {
    try {
      const response = await adminAPI.getLocationHistory(caseId);
      setLocationHistory(response.data);
      setSelectedCase(cases.find(c => c.id === caseId));
    } catch (error) {
      setError('Failed to fetch location history');
    }
  };

  if (loading) {
    return <div className="loading">Loading dashboard...</div>;
  }

  return (
    <div>
      <h2 style={{ marginBottom: '2rem' }}>Admin Dashboard</h2>

      {error && (
        <div className="alert alert-error">
          {error}
        </div>
      )}

      {/* Navigation Tabs */}
      <div style={{ marginBottom: '2rem', borderBottom: '1px solid #ddd' }}>
        <div style={{ display: 'flex', gap: '1rem' }}>
          {['overview', 'cases', 'matches', 'locations'].map(tab => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              style={{
                padding: '0.5rem 1rem',
                border: 'none',
                background: activeTab === tab ? '#3498db' : 'transparent',
                color: activeTab === tab ? 'white' : '#333',
                borderRadius: '4px 4px 0 0',
                cursor: 'pointer'
              }}
            >
              {tab.charAt(0).toUpperCase() + tab.slice(1)}
            </button>
          ))}
        </div>
      </div>

      {/* Overview Tab */}
      {activeTab === 'overview' && stats && (
        <div>
          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-number">{stats.total_cases}</div>
              <div className="stat-label">Total Cases</div>
            </div>
            <div className="stat-card">
              <div className="stat-number">{stats.active_cases}</div>
              <div className="stat-label">Active Cases</div>
            </div>
            <div className="stat-card">
              <div className="stat-number">{stats.found_cases}</div>
              <div className="stat-label">Found Cases</div>
            </div>
            <div className="stat-card">
              <div className="stat-number">{stats.total_sightings}</div>
              <div className="stat-label">Total Sightings</div>
            </div>
            <div className="stat-card">
              <div className="stat-number">{stats.total_matches}</div>
              <div className="stat-label">Total Matches</div>
            </div>
            <div className="stat-card">
              <div className="stat-number">{stats.pending_matches}</div>
              <div className="stat-label">Pending Verification</div>
            </div>
          </div>
        </div>
      )}

      {/* Cases Tab */}
      {activeTab === 'cases' && (
        <div>
          <h3>All Missing Person Cases</h3>
          <div className="table-container" style={{ overflowX: 'auto' }}>
            <table className="table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Status</th>
                  <th>Created</th>
                  <th>Contact</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {cases.map(caseItem => (
                  <tr key={caseItem.id}>
                    <td>{caseItem.name}</td>
                    <td>
                      <span className={`badge ${caseItem.is_found ? 'badge-success' : 'badge-warning'}`}>
                        {caseItem.is_found ? 'Found' : 'Active'}
                      </span>
                    </td>
                    <td>{new Date(caseItem.created_at).toLocaleDateString()}</td>
                    <td>{caseItem.email || caseItem.phone || 'N/A'}</td>
                    <td>
                      <div style={{ display: 'flex', gap: '0.5rem' }}>
                        {!caseItem.is_found && (
                          <button
                            onClick={() => handleMarkFound(caseItem.id)}
                            className="btn btn-success"
                            style={{ fontSize: '0.8rem', padding: '0.25rem 0.5rem' }}
                          >
                            Mark Found
                          </button>
                        )}
                        <button
                          onClick={() => handleViewLocationHistory(caseItem.id)}
                          className="btn btn-secondary"
                          style={{ fontSize: '0.8rem', padding: '0.25rem 0.5rem' }}
                        >
                          View Locations
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Matches Tab */}
      {activeTab === 'matches' && (
        <div>
          <h3>Face Recognition Matches</h3>
          <div className="table-container" style={{ overflowX: 'auto' }}>
            <table className="table">
              <thead>
                <tr>
                  <th>Missing Person</th>
                  <th>Confidence</th>
                  <th>Location</th>
                  <th>Date</th>
                  <th>Verified</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {matches.map(match => (
                  <tr key={match.id}>
                    <td>{match.case.name}</td>
                    <td>{(match.confidence_score * 100).toFixed(1)}%</td>
                    <td>
                      {match.sighting.location_name || 
                       (match.sighting.latitude && match.sighting.longitude ? 
                        `${match.sighting.latitude.toFixed(4)}, ${match.sighting.longitude.toFixed(4)}` : 
                        'Unknown')}
                    </td>
                    <td>{new Date(match.created_at).toLocaleDateString()}</td>
                    <td>
                      <span className={`badge ${match.verified ? 'badge-success' : 'badge-warning'}`}>
                        {match.verified ? 'Verified' : 'Pending'}
                      </span>
                    </td>
                    <td>
                      {!match.verified && (
                        <div style={{ display: 'flex', gap: '0.5rem' }}>
                          <button
                            onClick={() => handleVerifyMatch(match.id, true)}
                            className="btn btn-success"
                            style={{ fontSize: '0.8rem', padding: '0.25rem 0.5rem' }}
                          >
                            Verify
                          </button>
                          <button
                            onClick={() => handleVerifyMatch(match.id, false)}
                            className="btn btn-danger"
                            style={{ fontSize: '0.8rem', padding: '0.25rem 0.5rem' }}
                          >
                            Reject
                          </button>
                        </div>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Locations Tab */}
      {activeTab === 'locations' && (
        <div>
          <h3>Location History</h3>
          {selectedCase ? (
            <div>
              <h4>Locations for: {selectedCase.name}</h4>
              {locationHistory.length > 0 ? (
                <>
                  <MapComponent 
                    locations={locationHistory}
                    center={[locationHistory[0].latitude, locationHistory[0].longitude]}
                  />
                  <div className="table-container" style={{ marginTop: '1rem', overflowX: 'auto' }}>
                    <table className="table">
                      <thead>
                        <tr>
                          <th>Location</th>
                          <th>Coordinates</th>
                          <th>Confidence</th>
                          <th>Timestamp</th>
                        </tr>
                      </thead>
                      <tbody>
                        {locationHistory.map(location => (
                          <tr key={location.id}>
                            <td>{location.location_name || 'Unknown'}</td>
                            <td>{location.latitude.toFixed(6)}, {location.longitude.toFixed(6)}</td>
                            <td>{location.confidence_score ? (location.confidence_score * 100).toFixed(1) + '%' : 'N/A'}</td>
                            <td>{new Date(location.timestamp).toLocaleString()}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </>
              ) : (
                <p>No location history found for this case.</p>
              )}
            </div>
          ) : (
            <p>Select a case from the Cases tab to view location history.</p>
          )}
        </div>
      )}
    </div>
  );
};

export default AdminDashboard;