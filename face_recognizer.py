from train import *


class FaceRecognizer:
    def __init__(self) -> None:
        super().__init__()
        self.encodings = None
        self.names = None

    def trainModel(self):
        self.names, self.encodings = loadEncodings()

    def findMatch(self, rgb_small_frame, face_locations):
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(self.encodings, face_encoding)
            name = "Unknown"
            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = self.names[first_match_index]
            face_names.append(name)
        return face_names