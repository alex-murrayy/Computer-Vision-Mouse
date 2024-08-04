import cv2
import mediapipe as mp
import time
import numpy as np

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Initialize Video Capture
cap = cv2.VideoCapture(1)


# Function to calculate the Euclidean distance between two points
def euclidean_distance(point1, point2):
    return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

# Function to check if the index finger is moving
def is_finger_moving(current_positions, previous_positions, threshold=0.01):
    if previous_positions is None:
        return False
    
    # Calculate the distance between the current and previous positions of the index finger tip
    current_index_tip = current_positions[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    previous_index_tip = previous_positions[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    distance = euclidean_distance(current_index_tip, previous_index_tip)
    
    return distance > threshold
