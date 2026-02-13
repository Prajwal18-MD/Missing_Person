import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../utils/AuthContext';

const Navbar = () => {
  const { isAuthenticated, isAdmin, user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <nav className="navbar">
      <Link to="/" className="navbar-brand">
        Missing Person Detection
      </Link>

      <div className="navbar-nav">
        <Link to="/" className="nav-link">Home</Link>
        <Link to="/upload-sighting" className="nav-link">Report Sighting</Link>

        {isAuthenticated ? (
          <>
            <Link to="/create-case" className="nav-link">Create Case</Link>
            <Link to="/my-cases" className="nav-link">My Cases</Link>
            {isAdmin && (
              <Link to="/admin" className="nav-link">Admin Dashboard</Link>
            )}
            <span className="nav-link" style={{ cursor: 'default' }}>
              👤 {user?.email?.split('@')[0] || 'User'}
            </span>
            <button
              onClick={handleLogout}
              className="nav-link btn-danger"
              style={{
                background: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
                border: 'none',
                cursor: 'pointer',
                color: 'white'
              }}
            >
              Logout
            </button>
          </>
        ) : (
          <>
            <Link to="/login" className="nav-link">Login</Link>
            <Link to="/register" className="nav-link">Register</Link>
          </>
        )}
      </div>
    </nav>
  );
};

export default Navbar;