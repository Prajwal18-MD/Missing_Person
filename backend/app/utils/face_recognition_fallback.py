import cv2
import numpy as np
import os
from typing import List, Tuple, Optional
from PIL import Image
import pickle

class SimpleFaceRecognitionService:
    """Fallback face recognition service using OpenCV when dlib is not available"""
    
    def __init__(self, threshold: float = 0.6):
        self.threshold = float(os.getenv("FACE_MATCH_THRESHOLD", threshold))
        self.min_face_size = int(os.getenv("MIN_FACE_SIZE", 50))
        
        # Load OpenCV face detector
        try:
            self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        except:
            print("Warning: OpenCV face detector not available")
            self.face_cascade = None
    
    def extract_face_encoding(self, image_path: str) -> Optional[np.ndarray]:
        """Extract simple face features using OpenCV"""
        try:
            # Load image
            image = cv2.imread(image_path)
            if image is None:
                return None
            
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            if self.face_cascade is None:
                return None
                
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
            
            if len(faces) == 0:
                return None
            
            # Get the largest face
            largest_face = max(faces, key=lambda x: x[2] * x[3])
            x, y, w, h = largest_face
            
            # Check face size
            if w < self.min_face_size or h < self.min_face_size:
                return None
            
            # Extract face region and resize to standard size
            face_roi = gray[y:y+h, x:x+w]
            face_resized = cv2.resize(face_roi, (100, 100))
            
            # Create simple feature vector (histogram + edge features)
            hist = cv2.calcHist([face_resized], [0], None, [256], [0, 256])
            edges = cv2.Canny(face_resized, 50, 150)
            edge_hist = cv2.calcHist([edges], [0], None, [256], [0, 256])
            
            # Combine features
            features = np.concatenate([hist.flatten(), edge_hist.flatten()])
            
            # Normalize
            features = features / (np.linalg.norm(features) + 1e-7)
            
            return features
            
        except Exception as e:
            print(f"Error extracting face encoding: {e}")
            return None
    
    def extract_faces_from_video(self, video_path: str, output_dir: str) -> List[str]:
        """Extract faces from video frames"""
        try:
            cap = cv2.VideoCapture(video_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_interval = max(1, int(fps))  # Sample 1 frame per second
            
            frame_count = 0
            saved_faces = []
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                if frame_count % frame_interval == 0:
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    
                    if self.face_cascade is not None:
                        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
                        
                        for i, (x, y, w, h) in enumerate(faces):
                            if w >= self.min_face_size and h >= self.min_face_size:
                                # Extract face
                                face_image = frame[y:y+h, x:x+w]
                                
                                # Save face
                                face_filename = f"face_{frame_count}_{i}.jpg"
                                face_path = os.path.join(output_dir, face_filename)
                                cv2.imwrite(face_path, face_image)
                                saved_faces.append(face_path)
                
                frame_count += 1
            
            cap.release()
            return saved_faces
            
        except Exception as e:
            print(f"Error extracting faces from video: {e}")
            return []
    
    def compare_faces(self, known_encoding: np.ndarray, unknown_encoding: np.ndarray) -> float:
        """Compare two face encodings using cosine similarity"""
        try:
            # Cosine similarity
            dot_product = np.dot(known_encoding, unknown_encoding)
            norm_a = np.linalg.norm(known_encoding)
            norm_b = np.linalg.norm(unknown_encoding)
            
            if norm_a == 0 or norm_b == 0:
                return 0.0
            
            similarity = dot_product / (norm_a * norm_b)
            
            # Convert to 0-1 range
            similarity = (similarity + 1) / 2
            
            return float(similarity)
            
        except Exception as e:
            print(f"Error comparing faces: {e}")
            return 0.0
    
    def is_match(self, similarity_score: float) -> bool:
        """Determine if similarity score indicates a match"""
        return similarity_score >= self.threshold
    
    def serialize_encoding(self, encoding: np.ndarray) -> bytes:
        """Serialize face encoding for database storage"""
        return pickle.dumps(encoding)
    
    def deserialize_encoding(self, encoded_data: bytes) -> np.ndarray:
        """Deserialize face encoding from database"""
        return pickle.loads(encoded_data)
    
    def process_sighting_image(self, image_path: str, output_dir: str) -> List[str]:
        """Process a sighting image and extract all faces"""
        try:
            image = cv2.imread(image_path)
            if image is None:
                return []
            
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            if self.face_cascade is None:
                return []
            
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
            saved_faces = []
            
            for i, (x, y, w, h) in enumerate(faces):
                if w >= self.min_face_size and h >= self.min_face_size:
                    # Extract face
                    face_image = image[y:y+h, x:x+w]
                    
                    # Save face
                    face_filename = f"sighting_face_{i}.jpg"
                    face_path = os.path.join(output_dir, face_filename)
                    cv2.imwrite(face_path, face_image)
                    saved_faces.append(face_path)
            
            return saved_faces
            
        except Exception as e:
            print(f"Error processing sighting image: {e}")
            return []

# Try to import the advanced face recognition, fallback to simple version
try:
    from .face_recognition import FaceRecognitionService
    print("Using advanced face recognition (dlib)")
except ImportError:
    print("Using simple face recognition (OpenCV)")
    FaceRecognitionService = SimpleFaceRecognitionService