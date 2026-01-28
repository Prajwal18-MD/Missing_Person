import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { casesAPI } from '../services/api';

const CreateCase = () => {
  const [formData, setFormData] = useState({
    name: '',
    address: '',
    aadhaar_number: '',
    email: '',
    phone: '',
    photo: null
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);
  const [preview, setPreview] = useState(null);
  
  const navigate = useNavigate();

  const handleChange = (e) => {
    if (e.target.name === 'photo') {
      const file = e.target.files[0];
      setFormData({
        ...formData,
        photo: file
      });
      
      // Create preview
      if (file) {
        const reader = new FileReader();
        reader.onloadend = () => {
          setPreview(reader.result);
        };
        reader.readAsDataURL(file);
      } else {
        setPreview(null);
      }
    } else {
      setFormData({
        ...formData,
        [e.target.name]: e.target.value
      });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    
    if (!formData.photo) {
      setError('Please upload a photo');
      return;
    }
    
    setLoading(true);

    try {
      const submitData = new FormData();
      submitData.append('name', formData.name);
      submitData.append('address', formData.address);
      submitData.append('aadhaar_number', formData.aadhaar_number);
      submitData.append('email', formData.email);
      submitData.append('phone', formData.phone);
      submitData.append('photo', formData.photo);

      await casesAPI.create(submitData);
      
      setSuccess('Missing person case created successfully!');
      setTimeout(() => {
        navigate('/my-cases');
      }, 2000);
    } catch (error) {
      setError(error.response?.data?.detail || 'Failed to create case');
    }
    
    setLoading(false);
  };

  return (
    <div className="form-container" style={{ maxWidth: '600px' }}>
      <h2 style={{ textAlign: 'center', marginBottom: '2rem' }}>Create Missing Person Case</h2>
      
      {error && (
        <div className="alert alert-error">
          {error}
        </div>
      )}
      
      {success && (
        <div className="alert alert-success">
          {success}
        </div>
      )}
      
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="name">Full Name *</label>
          <input
            type="text"
            id="name"
            name="name"
            className="form-control"
            value={formData.name}
            onChange={handleChange}
            required
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="address">Last Known Address</label>
          <textarea
            id="address"
            name="address"
            className="form-control"
            rows="3"
            value={formData.address}
            onChange={handleChange}
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="aadhaar_number">Aadhaar Number (Optional)</label>
          <input
            type="text"
            id="aadhaar_number"
            name="aadhaar_number"
            className="form-control"
            value={formData.aadhaar_number}
            onChange={handleChange}
            placeholder="Will be stored securely (hashed)"
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="email">Contact Email</label>
          <input
            type="email"
            id="email"
            name="email"
            className="form-control"
            value={formData.email}
            onChange={handleChange}
            placeholder="For receiving match alerts"
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="phone">Contact Phone</label>
          <input
            type="tel"
            id="phone"
            name="phone"
            className="form-control"
            value={formData.phone}
            onChange={handleChange}
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="photo">Recent Clear Photo *</label>
          <input
            type="file"
            id="photo"
            name="photo"
            className="form-control"
            accept="image/*"
            onChange={handleChange}
            required
          />
          <small style={{ color: '#666' }}>
            Upload a clear, recent photo showing the person's face clearly
          </small>
        </div>
        
        {preview && (
          <div className="form-group">
            <label>Photo Preview:</label>
            <div style={{ textAlign: 'center' }}>
              <img 
                src={preview} 
                alt="Preview" 
                style={{ 
                  maxWidth: '200px', 
                  maxHeight: '200px', 
                  border: '1px solid #ddd',
                  borderRadius: '4px'
                }} 
              />
            </div>
          </div>
        )}
        
        <button 
          type="submit" 
          className="btn btn-primary" 
          style={{ width: '100%' }}
          disabled={loading}
        >
          {loading ? 'Creating Case...' : 'Create Case'}
        </button>
      </form>
      
      <div className="alert alert-info" style={{ marginTop: '1rem' }}>
        <strong>Privacy Notice:</strong> All personal information is stored securely. 
        Aadhaar numbers are hashed and cannot be retrieved. Photos are used only for 
        facial recognition matching.
      </div>
    </div>
  );
};

export default CreateCase;