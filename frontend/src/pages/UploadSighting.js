import React, { useState } from 'react';
import { sightingsAPI } from '../services/api';

const UploadSighting = () => {
  const [formData, setFormData] = useState({
    file: null,
    latitude: '',
    longitude: '',
    location_name: ''
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);
  const [preview, setPreview] = useState(null);
  const [gettingLocation, setGettingLocation] = useState(false);

  const handleChange = (e) => {
    if (e.target.name === 'file') {
      const file = e.target.files[0];
      setFormData({
        ...formData,
        file: file
      });
      
      // Create preview for images
      if (file && file.type.startsWith('image/')) {
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

  const getCurrentLocation = () => {
    setGettingLocation(true);
    
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setFormData({
            ...formData,
            latitude: position.coords.latitude.toString(),
            longitude: position.coords.longitude.toString()
          });
          setGettingLocation(false);
        },
        (error) => {
          setError('Failed to get current location. Please enter manually.');
          setGettingLocation(false);
        }
      );
    } else {
      setError('Geolocation is not supported by this browser.');
      setGettingLocation(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    
    if (!formData.file) {
      setError('Please select a file to upload');
      return;
    }
    
    setLoading(true);

    try {
      const submitData = new FormData();
      submitData.append('file', formData.file);
      
      if (formData.latitude) {
        submitData.append('latitude', formData.latitude);
      }
      if (formData.longitude) {
        submitData.append('longitude', formData.longitude);
      }
      if (formData.location_name) {
        submitData.append('location_name', formData.location_name);
      }

      await sightingsAPI.upload(submitData);
      
      setSuccess('Sighting uploaded successfully! Our system will process it and check for matches.');
      
      // Reset form
      setFormData({
        file: null,
        latitude: '',
        longitude: '',
        location_name: ''
      });
      setPreview(null);
      
      // Reset file input
      document.getElementById('file').value = '';
      
    } catch (error) {
      setError(error.response?.data?.detail || 'Failed to upload sighting');
    }
    
    setLoading(false);
  };

  return (
    <div className="form-container" style={{ maxWidth: '600px' }}>
      <h2 style={{ textAlign: 'center', marginBottom: '2rem' }}>Report a Sighting</h2>
      
      <div className="alert alert-info" style={{ marginBottom: '2rem' }}>
        <strong>Help find missing persons!</strong> Upload photos or videos of people you've seen. 
        Our system will automatically check for matches with missing persons and alert their families.
      </div>
      
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
          <label htmlFor="file">Photo or Video *</label>
          <input
            type="file"
            id="file"
            name="file"
            className="form-control"
            accept="image/*,video/*"
            onChange={handleChange}
            required
          />
          <small style={{ color: '#666' }}>
            Supported formats: JPEG, PNG for images; MP4, AVI, MOV for videos
          </small>
        </div>
        
        {preview && (
          <div className="form-group">
            <label>Preview:</label>
            <div style={{ textAlign: 'center' }}>
              <img 
                src={preview} 
                alt="Preview" 
                style={{ 
                  maxWidth: '300px', 
                  maxHeight: '300px', 
                  border: '1px solid #ddd',
                  borderRadius: '4px'
                }} 
              />
            </div>
          </div>
        )}
        
        <div className="form-group">
          <label htmlFor="location_name">Location Name</label>
          <input
            type="text"
            id="location_name"
            name="location_name"
            className="form-control"
            value={formData.location_name}
            onChange={handleChange}
            placeholder="e.g., Central Park, Mumbai Railway Station"
          />
        </div>
        
        <div className="grid grid-2">
          <div className="form-group">
            <label htmlFor="latitude">Latitude</label>
            <input
              type="number"
              id="latitude"
              name="latitude"
              className="form-control"
              value={formData.latitude}
              onChange={handleChange}
              step="any"
              placeholder="e.g., 28.6139"
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="longitude">Longitude</label>
            <input
              type="number"
              id="longitude"
              name="longitude"
              className="form-control"
              value={formData.longitude}
              onChange={handleChange}
              step="any"
              placeholder="e.g., 77.2090"
            />
          </div>
        </div>
        
        <div style={{ textAlign: 'center', marginBottom: '1rem' }}>
          <button 
            type="button"
            onClick={getCurrentLocation}
            className="btn btn-secondary"
            disabled={gettingLocation}
          >
            {gettingLocation ? 'Getting Location...' : 'Use Current Location'}
          </button>
        </div>
        
        <button 
          type="submit" 
          className="btn btn-primary" 
          style={{ width: '100%' }}
          disabled={loading}
        >
          {loading ? 'Uploading...' : 'Upload Sighting'}
        </button>
      </form>
      
      <div className="alert alert-info" style={{ marginTop: '1rem' }}>
        <strong>Privacy:</strong> Your uploads help find missing persons. Location data helps 
        track movement patterns. All data is processed securely and used only for matching purposes.
      </div>
    </div>
  );
};

export default UploadSighting;