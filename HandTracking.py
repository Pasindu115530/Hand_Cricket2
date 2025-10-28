import cv2
import mediapipe as mp
import time
import math
from mediapipe.python.solutions.hands_connections import HAND_CONNECTIONS


def calculate_distance(p1, p2):

    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)


cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils

cTime = 0
pTime = 0

array = []
generate_array = []


FINGER_TIPS = [8, 12, 16, 20]
FINGER_KNUCKLES = [5, 9, 13, 17]


while True:
    success, img = cap.read()
    if not success:
        break

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    gesture_label = ""
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            landmarks = handLms.landmark


            index_is_up = landmarks[8].y < landmarks[6].y and landmarks[8].y < landmarks[5].y
            middle_is_up = landmarks[12].y < landmarks[10].y and landmarks[12].y < landmarks[9].y
            ring_is_up = landmarks[16].y < landmarks[14].y and landmarks[16].y < landmarks[13].y
            pinky_is_up = landmarks[20].y < landmarks[18].y and landmarks[20].y < landmarks[17].y

            index_is_down = landmarks[8].y > landmarks[6].y
            middle_is_down = landmarks[12].y > landmarks[10].y
            ring_is_down = landmarks[16].y > landmarks[14].y
            pinky_is_down = landmarks[20].y > landmarks[18].y

            thumb_is_dis = landmarks[17].x - landmarks[5].x
            thumb_is_dis_with_17 = landmarks[17].x - landmarks[4].x
            thumb_is_in = abs(thumb_is_dis) > abs(thumb_is_dis_with_17) #4
            thumb_is_out = abs(thumb_is_dis) < abs(thumb_is_dis_with_17) #5




            thumb_is_up = landmarks[4].y < landmarks[0].y

            thumb_index_dist = calculate_distance(landmarks[4], landmarks[5])
            wrist_index_dist = calculate_distance(landmarks[0], landmarks[5])


            thumb_is_bent = thumb_index_dist < (wrist_index_dist * 1.5)
            thumb_is_bent_opp = thumb_index_dist > (wrist_index_dist * 1.5)


            result_1_1 = index_is_up and middle_is_down and ring_is_down and pinky_is_down and thumb_is_in
            result_1_2 = index_is_down and middle_is_up and ring_is_down and pinky_is_down and thumb_is_in
            result_1_3 = index_is_down and middle_is_down and ring_is_up and pinky_is_down and thumb_is_in
            result_1_4 = index_is_down and middle_is_down and ring_is_down and pinky_is_up and thumb_is_in

            result_2_1 = index_is_up and middle_is_up and ring_is_down and pinky_is_down and thumb_is_in
            result_2_2 = index_is_up and middle_is_down and ring_is_up and pinky_is_down and thumb_is_in
            result_2_3 = index_is_up and middle_is_down and ring_is_down and pinky_is_up and thumb_is_in
            result_2_4 = index_is_down and middle_is_up and ring_is_up and pinky_is_down and thumb_is_in
            result_2_5 = index_is_down and middle_is_up and ring_is_down and pinky_is_up and thumb_is_in
            result_2_6 = index_is_down and middle_is_down and ring_is_up and pinky_is_up and thumb_is_in
            result_2_7 = index_is_up and middle_is_down and ring_is_down and pinky_is_down and thumb_is_out
            result_2_8 = index_is_down and middle_is_up and ring_is_down and pinky_is_down and thumb_is_out
            result_2_9 = index_is_down and middle_is_down and ring_is_up and pinky_is_down and thumb_is_out
            result_2_10 = index_is_down and middle_is_down and ring_is_down and pinky_is_up and thumb_is_out

            result_3_1 = index_is_up and middle_is_up and ring_is_up and pinky_is_down and thumb_is_in
            result_3_2 = index_is_up and middle_is_up and ring_is_down and pinky_is_up and thumb_is_in
            result_3_3 = index_is_up and middle_is_down and ring_is_up and pinky_is_up and thumb_is_in
            result_3_4 = index_is_down and middle_is_up and ring_is_up and pinky_is_up and thumb_is_in
            result_3_5 = index_is_up and middle_is_up and ring_is_down and pinky_is_down and thumb_is_out
            result_3_6 = index_is_up and middle_is_down and ring_is_up and pinky_is_down and thumb_is_out
            result_3_7 = index_is_up and middle_is_down and ring_is_down and pinky_is_up and thumb_is_out
            result_3_8 = index_is_down and middle_is_up and ring_is_up and pinky_is_down and thumb_is_out
            result_3_9 = index_is_down and middle_is_up and ring_is_down and pinky_is_up and thumb_is_out
            result_3_10 = index_is_down and middle_is_down and ring_is_up and pinky_is_up and thumb_is_out


            result_4_1 = index_is_up and middle_is_up and ring_is_up and pinky_is_up and thumb_is_in
            result_4_2 = index_is_down and middle_is_up and ring_is_up and pinky_is_up and thumb_is_out
            result_4_3 = index_is_up and middle_is_down and ring_is_up and pinky_is_up and thumb_is_out
            result_4_4 = index_is_up and middle_is_up and ring_is_down and pinky_is_up and thumb_is_out
            result_4_5 = index_is_up and middle_is_up and ring_is_up and pinky_is_down and thumb_is_out
            result_5_1 = index_is_up and middle_is_up and ring_is_up and pinky_is_up and thumb_is_out

            result_6_1 = (index_is_down and middle_is_down and ring_is_down and pinky_is_down and thumb_is_out)


            if result_1_1 or result_1_2 or result_1_3 or result_1_4:
                gesture_label = "Gesture: Number 1"
                array.append(1)
            if result_2_1 or result_2_2 or result_2_3 or result_2_4 or result_2_5 or result_2_6 or result_2_7 or result_2_8 or result_2_9 or result_2_10:
                gesture_label = "Gesture: Number 2"
                array.append(2)
            if result_3_1 or result_3_2 or result_3_3 or result_3_4 or result_3_5 or result_3_6 or result_3_7 or result_3_8 or result_3_9 or result_3_10:
                gesture_label = "Gesture: Number 3"
                array.append(3)
            if result_4_1 or result_4_2 or result_4_3 or result_4_4 or result_4_5:
                gesture_label = "Gesture: Number 4"
                array.append(4)
            if result_5_1:
                gesture_label = "Gesture: Number 5"
                array.append(5)
            if result_6_1:
                gesture_label = "Gesture: Number 6"
                array.append(6)

            # --- Draw Landmarks ---
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

            # --- Thumb Distance Visualization ---
            h, w, c = img.shape
            x4, y4 = int(landmarks[4].x * w), int(landmarks[4].y * h)
            x5, y5 = int(landmarks[5].x * w), int(landmarks[5].y * h)

            cv2.line(img, (x4, y4), (x5, y5), (255, 255, 0), 2)
            cv2.putText(img, f"{thumb_index_dist:.2f}", (x5 + 10, y5 - 10),
                        cv2.FONT_HERSHEY_PLAIN, 1.2, (0, 255, 255), 2)

            # Optional: Draw wrist-to-index reference distance
            x0, y0 = int(landmarks[0].x * w), int(landmarks[0].y * h)
            cv2.line(img, (x0, y0), (x5, y5), (0, 255, 255), 1)

    # --- Draw Gesture Label ---
    if gesture_label:
        cv2.putText(img, gesture_label, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

    # --- FPS ---
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (18, 70), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
    if 0xFF == ord('s'):


    cv2.imshow('Hand Gesture Recognizer', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
