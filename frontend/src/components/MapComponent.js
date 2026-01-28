import React from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Fix for default markers
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

const MapComponent = ({ locations = [], center = [28.6139, 77.2090], zoom = 10 }) => {
  return (
    <div className="map-container">
      <MapContainer center={center} zoom={zoom} style={{ height: '100%', width: '100%' }}>
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        />
        {locations.map((location, index) => (
          <Marker key={index} position={[location.latitude, location.longitude]}>
            <Popup>
              <div>
                <strong>{location.name || 'Sighting Location'}</strong>
                <br />
                {location.timestamp && (
                  <>
                    Time: {new Date(location.timestamp).toLocaleString()}
                    <br />
                  </>
                )}
                {location.confidence_score && (
                  <>
                    Confidence: {(location.confidence_score * 100).toFixed(1)}%
                    <br />
                  </>
                )}
                Coordinates: {location.latitude.toFixed(6)}, {location.longitude.toFixed(6)}
              </div>
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
};

export default MapComponent;