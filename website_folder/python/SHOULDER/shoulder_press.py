import cv2
import mediapipe as mp
import numpy as np
import pyautogui


def shoulder_press_exercise(num_reps):
        
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

    # curl counters
    left_counter = 0
    right_counter = 0
    left_stage = None
    right_stage = None

    # Flag to indicate exercise completion
    exercise_complete = False

    # set up instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()

            # make detections
            results = pose.process(frame)

            # Extract Landmarks for Left Bicep
            try:
                left_landmarks = results.pose_landmarks.landmark
                left_shoulder = [left_landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                left_landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                left_elbow = [left_landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                            left_landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                left_wrist = [left_landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                            left_landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                left_hip = [left_landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                            left_landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]

                # Function
                left_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
                left_angle2 = calculate_angle(left_hip, left_shoulder, left_elbow)

                # Visualize
                cv2.putText(frame, f"Left: {int(left_angle)}", tuple(np.multiply(left_elbow, [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)


                # Curl counter logic
                if left_angle > 110 and left_angle2 > 80:
                    left_stage = "up"
                if left_angle < 90 and left_angle2 < 80 and left_stage == "up":
                    left_stage = "down"
                    left_counter += 1
                    print(f"Left Shoulder Count: {left_counter}")

                # Display message for incorrect form only when exercise is not complete
                if not exercise_complete and left_angle2 < 65:
                    leftarmmsg = "INCORRECT FORM!"
                    text_size = cv2.getTextSize(leftarmmsg, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
                    text_x = int((frame.shape[1] - text_size[0]) / 2)
                    text_y = int((frame.shape[0] + text_size[1]) / 2)
                    
                    # Create a black rectangle as a background for the text
                    bottom_left_corner_x = text_x - 10
                    bottom_left_corner_y = text_y + 10
                    top_right_corner_x = text_x + text_size[0] + 10
                    top_right_corner_y = text_y - text_size[1] - 10
                    cv2.rectangle(frame, (bottom_left_corner_x, bottom_left_corner_y), (top_right_corner_x, top_right_corner_y), (0, 0, 0), -1)
                    
                    # Put the text on top of the rectangle
                    cv2.putText(frame, leftarmmsg, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

            except:
                pass

            # Extract Landmarks for Right Bicep
            try:
                right_landmarks = results.pose_landmarks.landmark
                right_shoulder = [right_landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                                right_landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                right_elbow = [right_landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                                right_landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                right_wrist = [right_landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                                right_landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                right_hip = [right_landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                            right_landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]

                # Function
                right_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
                right_angle2 = calculate_angle(right_hip, right_shoulder, right_elbow)

                # Visualize
                cv2.putText(frame, f"Right: {int(right_angle)}", tuple(np.multiply(right_elbow, [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

                # Curl counter logic
                if right_angle > 110 and right_angle2 > 80:
                    right_stage = "up"
                if right_angle < 90 and right_angle2 < 80 and right_angle2 > 50 and right_stage == "up":
                    right_stage = "down"
                    right_counter += 1
                    print(f"Right Shoulder Count: {right_counter}")

                # Display message for incorrect form only when exercise is not complete
                if not exercise_complete and right_angle2 < 65:
                    rightarmmsg = "FORM INCORRECT!"
                    text_size = cv2.getTextSize(rightarmmsg, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
                    text_x = int((frame.shape[1] - text_size[0]) / 2)
                    text_y = int((frame.shape[0] + text_size[1]) / 2)
                    
                    # Create a black rectangle as a background for the text
                    bottom_left_corner_x = text_x - 10
                    bottom_left_corner_y = text_y + 10
                    top_right_corner_x = text_x + text_size[0] + 10
                    top_right_corner_y = text_y - text_size[1] - 10
                    cv2.rectangle(frame, (bottom_left_corner_x, bottom_left_corner_y), (top_right_corner_x, top_right_corner_y), (0, 0, 0), -1)
                    
                    # Put the text on top of the rectangle
                    cv2.putText(frame, rightarmmsg, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

            except:
                pass

            # Status box
            color_rectangle = (10, 200, 200)
            color_text = (0, 0, 0)

            # Draw the rectangle for the left reps
            cv2.rectangle(frame, (0, 0), (200, 73), color_rectangle, -1)
            cv2.putText(frame, 'Left Reps', (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color_text, 1, cv2.LINE_AA)
            cv2.putText(frame, str(left_counter), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color_text, 2, cv2.LINE_AA)

            # Draw the rectangle for the right reps
            cv2.rectangle(frame, (205, 0), (405, 73), color_rectangle, -1)
            cv2.putText(frame, 'Right Reps', (215, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color_text, 1, cv2.LINE_AA)
            cv2.putText(frame, str(right_counter), (215, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color_text, 2, cv2.LINE_AA)

            # Rendering dots
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(0, 0, 0), thickness=4, circle_radius=3),  # Black dots
            mp_drawing.DrawingSpec(color=(220, 128, 255), thickness=3, circle_radius=2))  # Light purple lines

            # Check if both left and right counters reach the specified number of reps
            if not exercise_complete and left_counter >= num_reps and right_counter >= num_reps:
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