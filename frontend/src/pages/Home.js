import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../utils/AuthContext';

const Home = () => {
  const { isAuthenticated } = useAuth();

  return (
    <div>
      {/* Hero Section */}
      <div className="card" style={{ 
        background: 'linear-gradient(135deg, rgba(255, 255, 255, 0.98) 0%, rgba(255, 255, 255, 0.95) 100%)',
        marginBottom: '3rem',
        border: '2px solid rgba(255, 255, 255, 0.6)'
      }}>
        <div className="card-body" style={{ 
          textAlign: 'center', 
          padding: '4rem 3rem',
          background: 'linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%)'
        }}>
          <div style={{ 
            fontSize: '3.5rem', 
            marginBottom: '1rem',
            filter: 'drop-shadow(0 4px 8px rgba(0,0,0,0.1))'
          }}>
            🔍
          </div>
          <h1 style={{ 
            marginBottom: '1.5rem', 
            fontSize: '3rem',
            fontWeight: '800',
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            backgroundClip: 'text',
            fontFamily: "'Outfit', sans-serif",
            letterSpacing: '-1px'
          }}>
            Missing Person Detection System
          </h1>
          <p style={{ 
            fontSize: '1.4rem', 
            color: '#718096', 
            marginBottom: '3rem',
            maxWidth: '800px',
            margin: '0 auto 3rem',
            lineHeight: '1.8',
            fontWeight: '500'
          }}>
            Reunite families using cutting-edge facial recognition AI. 
            Every sighting matters, every match brings hope.
          </p>
          
          <div className="grid grid-2" style={{ 
            maxWidth: '700px', 
            margin: '0 auto',
            gap: '1.5rem'
          }}>
            <Link 
              to="/upload-sighting" 
              className="btn btn-primary" 
              style={{ 
                padding: '1.3rem 2rem',
                fontSize: '1.1rem',
                fontWeight: '700'
              }}
            >
              📸 Report a Sighting
            </Link>
            {isAuthenticated ? (
              <Link 
                to="/create-case" 
                className="btn btn-success" 
                style={{ 
                  padding: '1.3rem 2rem',
                  fontSize: '1.1rem',
                  fontWeight: '700'
                }}
              >
                ➕ Create Missing Person Case
              </Link>
            ) : (
              <Link 
                to="/register" 
                className="btn btn-success" 
                style={{ 
                  padding: '1.3rem 2rem',
                  fontSize: '1.1rem',
                  fontWeight: '700'
                }}
              >
                🚀 Register to Create Case
              </Link>
            )}
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div style={{ marginBottom: '2rem' }}>
        <h2 style={{ 
          textAlign: 'center', 
          marginBottom: '2.5rem',
          fontSize: '2.5rem',
          fontWeight: '700',
          color: 'white',
          textShadow: '0 2px 8px rgba(0,0,0,0.2)',
          fontFamily: "'Outfit', sans-serif"
        }}>
          How We Help
        </h2>
        <div className="grid grid-3">
          <div className="card" style={{
            background: 'linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%), rgba(255, 255, 255, 0.98)',
            border: '2px solid rgba(102, 126, 234, 0.3)'
          }}>
            <div className="card-body" style={{ textAlign: 'center', padding: '2.5rem 2rem' }}>
              <div style={{ fontSize: '3.5rem', marginBottom: '1.5rem' }}>📸</div>
              <h3 style={{ 
                marginBottom: '1.2rem', 
                fontSize: '1.5rem',
                fontWeight: '700',
                color: '#667eea',
                fontFamily: "'Outfit', sans-serif"
              }}>
                Report Sightings
              </h3>
              <p style={{ 
                lineHeight: '1.8', 
                color: '#4a5568',
                fontSize: '1.05rem'
              }}>
                Upload photos or videos of people you've seen. Our AI system will automatically 
                check for matches with missing persons in real-time.
              </p>
            </div>
          </div>
          
          <div className="card" style={{
            background: 'linear-gradient(135deg, rgba(79, 172, 254, 0.15) 0%, rgba(0, 242, 254, 0.15) 100%), rgba(255, 255, 255, 0.98)',
            border: '2px solid rgba(79, 172, 254, 0.3)'
          }}>
            <div className="card-body" style={{ textAlign: 'center', padding: '2.5rem 2rem' }}>
              <div style={{ fontSize: '3.5rem', marginBottom: '1.5rem' }}>👤</div>
              <h3 style={{ 
                marginBottom: '1.2rem', 
                fontSize: '1.5rem',
                fontWeight: '700',
                color: '#00f2fe',
                fontFamily: "'Outfit', sans-serif"
              }}>
                Create Cases
              </h3>
              <p style={{ 
                lineHeight: '1.8', 
                color: '#4a5568',
                fontSize: '1.05rem'
              }}>
                Register missing persons with their photos. Our advanced facial recognition 
                continuously monitors all sightings for potential matches.
              </p>
            </div>
          </div>
          
          <div className="card" style={{
            background: 'linear-gradient(135deg, rgba(250, 112, 154, 0.15) 0%, rgba(254, 225, 64, 0.15) 100%), rgba(255, 255, 255, 0.98)',
            border: '2px solid rgba(250, 112, 154, 0.3)'
          }}>
            <div className="card-body" style={{ textAlign: 'center', padding: '2.5rem 2rem' }}>
              <div style={{ fontSize: '3.5rem', marginBottom: '1.5rem' }}>🔔</div>
              <h3 style={{ 
                marginBottom: '1.2rem', 
                fontSize: '1.5rem',
                fontWeight: '700',
                color: '#fa709a',
                fontFamily: "'Outfit', sans-serif"
              }}>
                Get Instant Alerts
              </h3>
              <p style={{ 
                lineHeight: '1.8', 
                color: '#4a5568',
                fontSize: '1.05rem'
              }}>
                Receive immediate email notifications when potential matches are found, 
                complete with location data and confidence scores.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* How It Works Section */}
      <div className="card" style={{
        background: 'linear-gradient(135deg, rgba(255, 255, 255, 0.98) 0%, rgba(255, 255, 255, 0.95) 100%)',
        border: '2px solid rgba(255, 255, 255, 0.6)'
      }}>
        <div className="card-body" style={{ padding: '3rem' }}>
          <h2 style={{ 
            marginBottom: '3rem', 
            textAlign: 'center',
            fontSize: '2.5rem',
            fontWeight: '700',
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            backgroundClip: 'text',
            fontFamily: "'Outfit', sans-serif"
          }}>
            How It Works
          </h2>
          <div className="grid grid-2" style={{ gap: '3rem' }}>
            <div style={{ 
              padding: '2rem',
              borderRadius: '16px',
              background: 'linear-gradient(135deg, rgba(102, 126, 234, 0.08) 0%, rgba(118, 75, 162, 0.08) 100%)',
              border: '2px solid rgba(102, 126, 234, 0.2)'
            }}>
              <div style={{ display: 'flex', alignItems: 'center', marginBottom: '1.5rem' }}>
                <div style={{ 
                  fontSize: '2.5rem', 
                  marginRight: '1rem',
                  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                  width: '60px',
                  height: '60px',
                  borderRadius: '16px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: 'white',
                  fontWeight: '800',
                  fontFamily: "'Outfit', sans-serif"
                }}>
                  1
                </div>
                <h4 style={{ fontSize: '1.3rem', fontWeight: '700', color: '#2d3748' }}>
                  Upload Missing Person Photo
                </h4>
              </div>
              <p style={{ fontSize: '1.05rem', lineHeight: '1.8', color: '#4a5568', marginLeft: '76px' }}>
                Create a case with a clear photo of the missing person and relevant details. 
                Our system creates a facial signature for matching.
              </p>
            </div>

            <div style={{ 
              padding: '2rem',
              borderRadius: '16px',
              background: 'linear-gradient(135deg, rgba(79, 172, 254, 0.08) 0%, rgba(0, 242, 254, 0.08) 100%)',
              border: '2px solid rgba(79, 172, 254, 0.2)'
            }}>
              <div style={{ display: 'flex', alignItems: 'center', marginBottom: '1.5rem' }}>
                <div style={{ 
                  fontSize: '2.5rem', 
                  marginRight: '1rem',
                  background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
                  width: '60px',
                  height: '60px',
                  borderRadius: '16px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: 'white',
                  fontWeight: '800',
                  fontFamily: "'Outfit', sans-serif"
                }}>
                  2
                </div>
                <h4 style={{ fontSize: '1.3rem', fontWeight: '700', color: '#2d3748' }}>
                  Community Reports Sightings
                </h4>
              </div>
              <p style={{ fontSize: '1.05rem', lineHeight: '1.8', color: '#4a5568', marginLeft: '76px' }}>
                Anyone can upload photos or videos of people they've seen in public places. 
                Every submission helps expand our search network.
              </p>
            </div>

            <div style={{ 
              padding: '2rem',
              borderRadius: '16px',
              background: 'linear-gradient(135deg, rgba(240, 147, 251, 0.08) 0%, rgba(245, 87, 108, 0.08) 100%)',
              border: '2px solid rgba(240, 147, 251, 0.2)'
            }}>
              <div style={{ display: 'flex', alignItems: 'center', marginBottom: '1.5rem' }}>
                <div style={{ 
                  fontSize: '2.5rem', 
                  marginRight: '1rem',
                  background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
                  width: '60px',
                  height: '60px',
                  borderRadius: '16px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: 'white',
                  fontWeight: '800',
                  fontFamily: "'Outfit', sans-serif"
                }}>
                  3
                </div>
                <h4 style={{ fontSize: '1.3rem', fontWeight: '700', color: '#2d3748' }}>
                  AI Matches Faces
                </h4>
              </div>
              <p style={{ fontSize: '1.05rem', lineHeight: '1.8', color: '#4a5568', marginLeft: '76px' }}>
                Our advanced AI automatically compares every sighting with all active cases 
                using state-of-the-art facial recognition technology.
              </p>
            </div>

            <div style={{ 
              padding: '2rem',
              borderRadius: '16px',
              background: 'linear-gradient(135deg, rgba(250, 112, 154, 0.08) 0%, rgba(254, 225, 64, 0.08) 100%)',
              border: '2px solid rgba(250, 112, 154, 0.2)'
            }}>
              <div style={{ display: 'flex', alignItems: 'center', marginBottom: '1.5rem' }}>
                <div style={{ 
                  fontSize: '2.5rem', 
                  marginRight: '1rem',
                  background: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
                  width: '60px',
                  height: '60px',
                  borderRadius: '16px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: 'white',
                  fontWeight: '800',
                  fontFamily: "'Outfit', sans-serif"
                }}>
                  4
                </div>
                <h4 style={{ fontSize: '1.3rem', fontWeight: '700', color: '#2d3748' }}>
                  Instant Alerts Sent
                </h4>
              </div>
              <p style={{ fontSize: '1.05rem', lineHeight: '1.8', color: '#4a5568', marginLeft: '76px' }}>
                Get notified immediately when potential matches are found with location, 
                timestamp, and confidence score to help reunite families faster.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Call to Action */}
      <div style={{ 
        textAlign: 'center', 
        marginTop: '4rem',
        padding: '3rem',
        background: 'rgba(255, 255, 255, 0.95)',
        borderRadius: '24px',
        border: '2px solid rgba(255, 255, 255, 0.6)',
        boxShadow: '0 16px 48px rgba(0, 0, 0, 0.2)'
      }}>
        <h2 style={{ 
          fontSize: '2.2rem',
          fontWeight: '700',
          marginBottom: '1.5rem',
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          backgroundClip: 'text',
          fontFamily: "'Outfit', sans-serif"
        }}>
          Every Second Counts
        </h2>
        <p style={{ 
          fontSize: '1.2rem',
          color: '#4a5568',
          marginBottom: '2rem',
          maxWidth: '700px',
          margin: '0 auto 2rem',
          lineHeight: '1.8'
        }}>
          Join our community in making a difference. Together, we can bring families back together.
        </p>
        <Link 
          to="/upload-sighting" 
          className="btn btn-primary" 
          style={{ 
            padding: '1.3rem 3rem',
            fontSize: '1.2rem',
            fontWeight: '700'
          }}
        >
          Get Started Now →
        </Link>
      </div>
    </div>
  );
};

export default Home;