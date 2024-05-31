import cv2
import mediapipe as mp
import numpy as np
import pyautogui

def lunges_exercise(num_reps):
        
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    def calculate_angle(a, b, c):
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)

        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)

        if angle > 180.0:
            angle = 360 - angle

        return angle


    # Get the screen dimensions
    screen_width, screen_height = pyautogui.size()

    # VIDEO FEED
    cap = cv2.VideoCapture(0)

    # Create a window with the desired dimensions
    window_width = int(screen_width * 0.50)  # 50% of the screen width
    window_height = int(screen_height * 0.65)  # 65% of the screen height
    cv2.namedWindow('Mediapipe Feed', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Mediapipe Feed', window_width, window_height)

    # Lunge counter
    left_lunge_counter = 0
    right_lunge_counter = 0
    lunge_stage = "center"

    # Flag to indicate exercise completion
    exercise_complete = False

    # set up instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()

            # make detections
            results = pose.process(frame)

            # Extract Landmarks for Lunges
            try:
                landmarks = results.pose_landmarks.landmark
                left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                            landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                            landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                            landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

                # Calculate angles for lunge form
                left_knee_angle = calculate_angle(left_hip, left_knee, left_ankle)
                right_knee_angle = calculate_angle(right_hip, right_knee, right_ankle)

                # Visualize
                cv2.putText(frame, f"Left Knee: {int(left_knee_angle)}", tuple(np.multiply(left_knee, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(frame, f"Right Knee: {int(right_knee_angle)}", tuple(np.multiply(right_knee, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

                # Lunge counter logic
                if left_knee_angle > 170 and right_knee_angle > 170:
                    lunge_stage = "center"
                elif left_knee_angle < 100 and right_knee_angle > 130 and lunge_stage == "center":
                    lunge_stage = "left"
                    left_lunge_counter += 1
                elif right_knee_angle < 100 and left_knee_angle > 130 and lunge_stage == "center":
                    lunge_stage = "right"
                    right_lunge_counter += 1
            except:
                pass
                
            # Status box
            color_rectangle = (10, 200, 200)
            color_text = (0, 0, 0)

            # Draw the rectangle for the left reps
            cv2.rectangle(frame, (0, 0), (200, 73), color_rectangle, -1)
            cv2.putText(frame, 'Left Reps', (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color_text, 1, cv2.LINE_AA)
            cv2.putText(frame, str(left_lunge_counter), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color_text, 2, cv2.LINE_AA)

            # Draw the rectangle for the right reps
            cv2.rectangle(frame, (205, 0), (405, 73), color_rectangle, -1)
            cv2.putText(frame, 'Right Reps', (215, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color_text, 1, cv2.LINE_AA)
            cv2.putText(frame, str(right_lunge_counter), (215, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color_text, 2, cv2.LINE_AA)

            # Rendering dots
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(0, 0, 0), thickness=4, circle_radius=3),  # Black dots
            mp_drawing.DrawingSpec(color=(220, 128, 255), thickness=3, circle_radius=2))  # Light purple lines

            # Check if the lunge counter reaches the specified number of reps
            if not exercise_complete and left_lunge_counter >= num_reps and right_lunge_counter >= num_reps:
                completion_message = "EXERCISE COMPLETED!"
                exercise_complete = True

            # Display "Exercise Complete" message
            if exercise_complete:
                text_size = cv2.getTextSize(completion_message, cv2.FONT_HERSHEY_TRIPLEX, 1, 2)[0]
                text_x = int((frame.shape[1] - text_size[0]) / 2)
                text_y = int((frame.shape[0] + text_size[1]) / 2)

                # Draw black background rectangle
                background_x1 = text_x - 10
                background_y1 = text_y - text_size[1] - 10
                background_x2 = text_x + text_size[0] + 10
                background_y2 = text_y + 10
                cv2.rectangle(frame, (background_x1, background_y1), (background_x2, background_y2), (0, 0, 0), -1)

                # Draw text
                cv2.putText(frame, completion_message, (text_x, text_y), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            cv2.imshow('Mediapipe Feed', frame)

            # Check if the user pressed 'q' to quit
            key = cv2.waitKey(10)
            if key & 0xFF == ord('x'):
                break

    cap.release()
    cv2.destroyAllWindows()