import cv2
import mediapipe as mp
import pyautogui
import MouseController

# Initialize smoothing variables
previous_x, previous_y = None, None
smoothing_factor = .30  # Adjust this for more or less smoothing

# Initialize Mediapipe Hands and Drawing modules
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
controller = MouseController.MouseController()
chosen_hand = "Right"

# Initialize Video Capture
cap = cv2.VideoCapture(1)

def recognize_gesture(hand_landmarks, image):
    h, w, c = image.shape
    wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
    thumb_cmc = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC]
    thumb_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP]
    thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
    index_pip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP]
    index_dip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP]
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
    middle_pip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP]
    middle_dip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP]
    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP]
    ring_pip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP]
    ring_dip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_DIP]
    ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP]
    pinky_pip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP]
    pinky_dip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_DIP]
    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

    #TODO: Figure out how to make scrolling good

    if isScrolling(index_tip.x, index_tip.y,  index_dip.x, index_dip.y, index_pip.y, middle_tip.x, middle_tip.y, middle_dip.x, middle_dip.y, middle_pip.y, pinky_tip.y, pinky_dip.y, pinky_pip.y, ring_tip.y, ring_dip.y, ring_pip.y) == True: 
        return "Scrolling"
    if isLeftClicking(thumb_tip.y, index_tip.y) == True:
        return "Left Click"
    if isRightClicking(thumb_tip.y, middle_tip.y) == True:
        return "Right Click"
    return "N/A"


def isLeftClicking(thumb_tip, index_tip):
    distance = abs(thumb_tip - index_tip)

    if distance < 0.05:
        return True
    return False

# TODO: Make right clicking more accurrate
def isRightClicking(thumb_tip, middle_tip): 
    distance = abs(thumb_tip - middle_tip)

    if distance < 0.05: 
        return True  
    return False

def isScrolling(index_tip_x, index_tip_y,  index_dip_x, index_dip_y, index_pip_y, middle_tip_x, middle_tip_y, middle_dip_x, middle_dip_y, middle_pip_y, pinky_tip, pinky_dip, pinky_pip, ring_tip, ring_dip, ring_pip):
        diff_tip = abs(index_tip_x - middle_tip_x)
        diff_dip = abs(index_dip_x - middle_dip_x)
 
        isRingLower = False 
        isPinkyLower = False
        isIndexAbove = False
        isMiddleAbove = False

        if pinky_tip > pinky_pip and pinky_dip > pinky_pip:
            isPinkyLower = True
        elif pinky_tip < pinky_pip and pinky_dip < pinky_pip:
            isPinkyLower = False

        if ring_tip > ring_pip:
            isRingLower = True
        elif ring_tip < ring_pip and ring_dip < ring_pip:
            isRingLower = False

        if index_tip_y < index_pip_y and index_dip_y < index_pip_y:
            isIndexAbove = True
        elif index_tip_y > index_pip_y and index_dip_y > index_pip_y:
            isIndexAbove = False

        if middle_tip_y < middle_pip_y and middle_dip_y < middle_pip_y:
            isMiddleAbove = True
        elif middle_tip_y > middle_pip_y and middle_dip_y > middle_pip_y:
            isMiddleAbove = False

        #TODO: Add it so that the pinky and ring tip need to be less than middle and index mcp
        if diff_tip < 0.05 and diff_dip < 0.05 and isPinkyLower == True and isRingLower == True and isIndexAbove == True and isMiddleAbove == True: 
            return True
        return False

with mp_hands.Hands(
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7) as hands:

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        # Flip the image horizontally for a later selfie-view display
        # Convert the BGR image to RGB
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        
        # Process the image and find hands
        results = hands.process(image)

        # Convert the image color back to BGR
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Draw hand landmarks
        if results.multi_hand_landmarks:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                # Check if the detected hand matches the chosen hand
                if handedness.classification[0].label == chosen_hand:
                    # Draw the hand landmarks on the image
                    mp_drawing.draw_landmarks(
                        image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    
                # Draw dots and lines manually
                    for landmark in hand_landmarks.landmark:
                        # Get the landmark coordinates
                        h, w, c = image.shape
                        cx, cy = int(landmark.x * w), int(landmark.y * h)
                        
                        # Draw a circle at each landmark
                        cv2.circle(image, (cx, cy), 5, (0, 0, 255), -1)

                    # Draw lines between the landmarks
                    for connection in mp_hands.HAND_CONNECTIONS:
                        start_idx = connection[0]
                        end_idx = connection[1]
                        start = hand_landmarks.landmark[start_idx]
                        end = hand_landmarks.landmark[end_idx]
                        start_point = (int(start.x * w), int(start.y * h))
                        end_point = (int(end.x * w), int(end.y * h))
                        cv2.line(image, start_point, end_point, (0, 0, 0), 2)

                # # TODO: FIND A WAY TO MAKE THE MOUSE TRACKING GOOD
                # # NOTE: Mouse Tracking
                # # Moving pointer
                scaling_factor = 6.0
                index_tip_x = (hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x + hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].x) / 2
                index_tip_y = (hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].y + hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y) / 2
               
                # Get screen dimensions
                screen_width, screen_height = pyautogui.size()

                # Convert normalized coordinates to screen coordinates
                x = int((index_tip_x * screen_width - (screen_width * .5)) * scaling_factor) - screen_width
                y = int((index_tip_y * screen_height - (screen_height * .7)) * scaling_factor)

                # Apply smoothing
                if previous_x is not None and previous_y is not None:
                    x = int(previous_x * (1 - smoothing_factor) + x * smoothing_factor)
                    y = int(previous_y * (1 - smoothing_factor) + y * smoothing_factor)

                # Move the mouse
                pyautogui.moveTo(x, y)

                # Store current position for smoothing
                previous_x, previous_y = x, y

                # Mouse Functions
                gesture = recognize_gesture(hand_landmarks, image)
                if gesture == "Left Click":
                     controller.click()

                scroll_direction = -10
                if gesture == "Scrolling":
                    controller.scroll(scroll_direction)

                    

                cv2.putText(image, gesture, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 200, 200), 2, cv2.LINE_AA)

        # Display the image
        cv2.imshow('Hand Tracking', image)

        # Exit when 'q' is pressed
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()