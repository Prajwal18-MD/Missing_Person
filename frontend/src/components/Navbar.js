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
        Missing Person Detection System
      </Link>
      
      <ul className="navbar-nav">
        <li>
          <Link to="/" className="nav-link">Home</Link>
        </li>
        <li>
          <Link to="/upload-sighting" className="nav-link">Report Sighting</Link>
        </li>
        
        {isAuthenticated ? (
          <>
            <li>
              <Link to="/create-case" className="nav-link">Create Case</Link>
            </li>
            <li>
              <Link to="/my-cases" className="nav-link">My Cases</Link>
            </li>
            {isAdmin && (
              <li>
                <Link to="/admin" className="nav-link">Admin Dashboard</Link>
              </li>
            )}
            <li>
              <span className="nav-link">Welcome, {user?.email}</span>
            </li>
            <li>
              <button onClick={handleLogout} className="nav-link" style={{background: 'none', border: 'none', cursor: 'pointer'}}>
                Logout
              </button>
            </li>
          </>
        ) : (
          <>
            <li>
              <Link to="/login" className="nav-link">Login</Link>
            </li>
            <li>
              <Link to="/register" className="nav-link">Register</Link>
            </li>
          </>
        )}
      </ul>
    </nav>
  );
};

export default Navbar;