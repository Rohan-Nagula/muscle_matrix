import cv2
import mediapipe as mp
import numpy as np
import pyautogui

def pushup_exercise(num_reps):

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

    # Push-up counter
    pushup_counter = 0
    pushup_stage = None

    # Flag to indicate exercise completion
    exercise_complete = False

    # set up instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()

            # make detections
            results = pose.process(frame)

            # Extract Landmarks for Push-ups
            try:
                landmarks = results.pose_landmarks.landmark
                left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                                landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                            landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                            landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

                # Calculate angles for push-up form
                left_arm_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
                right_arm_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)

                # Visualize
                cv2.putText(frame, f"Left Arm: {int(left_arm_angle)}", tuple(np.multiply(left_elbow, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(frame, f"Right Arm: {int(right_arm_angle)}", tuple(np.multiply(right_elbow, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

                # Push-up counter logic
                if left_arm_angle > 160 and right_arm_angle > 160:
                    pushup_stage = "down"
                if left_arm_angle < 90 and right_arm_angle < 90 and pushup_stage == "down":
                    pushup_stage = "up"
                    pushup_counter += 1
                    print(f"Push-up Count: {pushup_counter}")

                # Display message for incorrect form only when exercise is not complete
                if not exercise_complete and (left_arm_angle < 20 or right_arm_angle < 20):
                    form_incorrect_msg = "INCORRECT FORM!"
                    text_size = cv2.getTextSize(form_incorrect_msg, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
                    text_x = int((frame.shape[1] - text_size[0]) / 2)
                    text_y = int((frame.shape[0] + text_size[1]) / 2)
                    
                    # Create a black rectangle as a background for the text
                    bottom_left_corner_x = text_x - 10
                    bottom_left_corner_y = text_y + 10
                    top_right_corner_x = text_x + text_size[0] + 10
                    top_right_corner_y = text_y - text_size[1] - 10
                    cv2.rectangle(frame, (bottom_left_corner_x, bottom_left_corner_y), (top_right_corner_x, top_right_corner_y), (0, 0, 0), -1)
                    
                    # Put the text on top of the rectangle
                    cv2.putText(frame, form_incorrect_msg, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

            except:
                pass

            # Status box
            color_rectangle = (10, 200, 200)
            color_text = (0, 0, 0)

            # Draw the rectangle for the push-up reps
            cv2.rectangle(frame, (0, 0), (200, 73), color_rectangle, -1)
            cv2.putText(frame, 'Total Reps', (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color_text, 1, cv2.LINE_AA)
            cv2.putText(frame, str(pushup_counter), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color_text, 2, cv2.LINE_AA)

            # Rendering dots
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(0, 0, 0), thickness=4, circle_radius=3),  # Black dots
                                    mp_drawing.DrawingSpec(color=(220, 128, 255), thickness=3, circle_radius=2))  # Light purple lines

            # Check if the push-up counter reaches the specified number of reps
            if not exercise_complete and pushup_counter >= num_reps:
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