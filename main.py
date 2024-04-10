import cv2
import mediapipe as mp
import pyautogui

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open video capture.")
    exit()

hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()

# Initialize variables
index_x, index_y, thumb_x, thumb_y = 0, 0, 0, 0

# Function to check if the cursor is inside the button region
def is_inside_button(x, y):
    return screen_width - 150 <= x <= screen_width and 0 <= y <= 150

# Function to draw the exit button
def draw_exit_button(frame):
    cv2.rectangle(frame, (screen_width - 150, 0), (screen_width, 150), (255, 0, 0), -1)
    cv2.putText(frame, 'Exit', (screen_width - 130, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab a frame")
        break

    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks
    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                if id == 8:  # Index finger tip
                    cv2.circle(frame, (x, y), 10, (0, 255, 255), -1)
                    index_x = x
                    index_y = y
                if id == 4:  # Thumb tip
                    cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)
                    thumb_x = x
                    thumb_y = y
            # Moved click and move actions outside the inner loop
            if abs(index_y - thumb_y) < 20:
                pyautogui.click()
                pyautogui.sleep(1)
            elif abs(index_y - thumb_y) < 100:
                pyautogui.moveTo(index_x, index_y)
            elif is_inside_button(index_x, index_y):
                if abs(index_y - thumb_y) < 100:
                    pyautogui.click()
                    pyautogui.sleep(1)
                    # Exit the program when the button is clicked
                    cap.release()
                    cv2.destroyAllWindows()
                    exit()

    # Draw exit button
    draw_exit_button(frame)

    cv2.imshow('Virtual Mouse', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
