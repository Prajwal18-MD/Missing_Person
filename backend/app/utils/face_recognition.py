# Try to import face_recognition library, fallback to OpenCV if not available
try:
    import face_recognition
    import cv2
    import numpy as np
    import os
    from typing import List, Tuple, Optional
    from PIL import Image
    import pickle
    FACE_RECOGNITION_AVAILABLE = True
except ImportError:
    import cv2
    import numpy as np
    import os
    from typing import List, Tuple, Optional
    from PIL import Image
    import pickle
    FACE_RECOGNITION_AVAILABLE = False
    print("Warning: face_recognition library not available, using OpenCV fallback")

class FaceRecognitionService:
    def __init__(self, threshold: float = 0.6):
        self.threshold = float(os.getenv("FACE_MATCH_THRESHOLD", threshold))
        self.min_face_size = int(os.getenv("MIN_FACE_SIZE", 50))
        
        if not FACE_RECOGNITION_AVAILABLE:
            # Initialize OpenCV face detector as fallback
            try:
                self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            except:
                self.face_cascade = None
    
    def extract_face_encoding(self, image_path: str) -> Optional[np.ndarray]:
        """Extract face encoding from an image"""
        if FACE_RECOGNITION_AVAILABLE:
            return self._extract_face_encoding_dlib(image_path)
        else:
            return self._extract_face_encoding_opencv(image_path)
    
    def _extract_face_encoding_dlib(self, image_path: str) -> Optional[np.ndarray]:
        """Extract face encoding using dlib (advanced)"""
        try:
            # Load image
            image = face_recognition.load_image_file(image_path)
            
            # Find face locations
            face_locations = face_recognition.face_locations(image)
            
            if not face_locations:
                return None
            
            # Get face encodings
            face_encodings = face_recognition.face_encodings(image, face_locations)
            
            if not face_encodings:
                return None
            
            # Return the first face encoding
            return face_encodings[0]
            
        except Exception as e:
            print(f"Error extracting face encoding with dlib: {e}")
            return None
    
    def _extract_face_encoding_opencv(self, image_path: str) -> Optional[np.ndarray]:
        """Extract simple face features using OpenCV (fallback)"""
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
            
            # Create simple feature vector
            hist = cv2.calcHist([face_resized], [0], None, [256], [0, 256])
            features = hist.flatten()
            
            # Normalize
            features = features / (np.linalg.norm(features) + 1e-7)
            
            return features
            
        except Exception as e:
            print(f"Error extracting face encoding with OpenCV: {e}")
            return None
    
    def extract_faces_from_video(self, video_path: str, output_dir: str) -> List[str]:
        """Extract faces from video frames and save them"""
        if FACE_RECOGNITION_AVAILABLE:
            return self._extract_faces_from_video_dlib(video_path, output_dir)
        else:
            return self._extract_faces_from_video_opencv(video_path, output_dir)
    
    def _extract_faces_from_video_dlib(self, video_path: str, output_dir: str) -> List[str]:
        """Extract faces using dlib (advanced)"""
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
                    # Convert BGR to RGB
                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    
                    # Find faces
                    face_locations = face_recognition.face_locations(rgb_frame)
                    
                    for i, face_location in enumerate(face_locations):
                        top, right, bottom, left = face_location
                        
                        # Check face size
                        face_width = right - left
                        face_height = bottom - top
                        
                        if face_width >= self.min_face_size and face_height >= self.min_face_size:
                            # Extract face
                            face_image = rgb_frame[top:bottom, left:right]
                            
                            # Save face
                            face_filename = f"face_{frame_count}_{i}.jpg"
                            face_path = os.path.join(output_dir, face_filename)
                            
                            # Convert to PIL and save
                            pil_image = Image.fromarray(face_image)
                            pil_image.save(face_path)
                            saved_faces.append(face_path)
                
                frame_count += 1
            
            cap.release()
            return saved_faces
            
        except Exception as e:
            print(f"Error extracting faces from video with dlib: {e}")
            return []
    
    def _extract_faces_from_video_opencv(self, video_path: str, output_dir: str) -> List[str]:
        """Extract faces using OpenCV (fallback)"""
        try:
            cap = cv2.VideoCapture(video_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_interval = max(1, int(fps))
            
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
            print(f"Error extracting faces from video with OpenCV: {e}")
            return []
    
    def compare_faces(self, known_encoding: np.ndarray, unknown_encoding: np.ndarray) -> float:
        """Compare two face encodings and return similarity score"""
        if FACE_RECOGNITION_AVAILABLE:
            return self._compare_faces_dlib(known_encoding, unknown_encoding)
        else:
            return self._compare_faces_opencv(known_encoding, unknown_encoding)
    
    def _compare_faces_dlib(self, known_encoding: np.ndarray, unknown_encoding: np.ndarray) -> float:
        """Compare faces using dlib (advanced)"""
        try:
            # Calculate face distance (lower is better)
            face_distance = face_recognition.face_distance([known_encoding], unknown_encoding)[0]
            
            # Convert to similarity score (higher is better)
            similarity = 1 - face_distance
            
            return float(similarity)
            
        except Exception as e:
            print(f"Error comparing faces with dlib: {e}")
            return 0.0
    
    def _compare_faces_opencv(self, known_encoding: np.ndarray, unknown_encoding: np.ndarray) -> float:
        """Compare faces using cosine similarity (fallback)"""
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
            print(f"Error comparing faces with OpenCV: {e}")
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
        if FACE_RECOGNITION_AVAILABLE:
            return self._process_sighting_image_dlib(image_path, output_dir)
        else:
            return self._process_sighting_image_opencv(image_path, output_dir)
    
    def _process_sighting_image_dlib(self, image_path: str, output_dir: str) -> List[str]:
        """Process sighting using dlib (advanced)"""
        try:
            # Load image
            image = face_recognition.load_image_file(image_path)
            
            # Find face locations
            face_locations = face_recognition.face_locations(image)
            
            saved_faces = []
            
            for i, face_location in enumerate(face_locations):
                top, right, bottom, left = face_location
                
                # Check face size
                face_width = right - left
                face_height = bottom - top
                
                if face_width >= self.min_face_size and face_height >= self.min_face_size:
                    # Extract face
                    face_image = image[top:bottom, left:right]
                    
                    # Save face
                    face_filename = f"sighting_face_{i}.jpg"
                    face_path = os.path.join(output_dir, face_filename)
                    
                    # Convert to PIL and save
                    pil_image = Image.fromarray(face_image)
                    pil_image.save(face_path)
                    saved_faces.append(face_path)
            
            return saved_faces
            
        except Exception as e:
            print(f"Error processing sighting image with dlib: {e}")
            return []
    
    def _process_sighting_image_opencv(self, image_path: str, output_dir: str) -> List[str]:
        """Process sighting using OpenCV (fallback)"""
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
            print(f"Error processing sighting image with OpenCV: {e}")
            return []