import cv2
import mediapipe as mp
import numpy as np
import pyttsx3
import time
import pyttsx3

engine = pyttsx3.init()

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


def calculate_angle(a, b, c):
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle


cap = cv2.VideoCapture(0)

# curl counter variables
counter1 = 0
counter2 = 0
counter3 = 0
counter4 = 0
f = 0
crct = 0
c = 1
t = 0
stage = 'none'

import pyttsx3  # import the library


def voiceChange():
    eng = pyttsx3.init()  # initialize an instance
    engine.setProperty("rate", 130)
    voice = eng.getProperty('voices')  # get the available voices
    # eng.setProperty('voice', voice[0].id) #set the voice to index 0 for male voice
    eng.setProperty('voice', voice[1].id)  # changing voice to index 1 for female voice
    eng.say(
        "Welcome to pose detection. Let us practice the Warrior pose!! Please make sure your full body is visible inside the frame! once timer starts inhale and exhale calmly")
    eng.runAndWait()  # run and process the voice command


if __name__ == "__main__":
    voiceChange()

## Setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Make detection
        results = pose.process(image)

        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark

            # Get coordinates
            re = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                  landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            rs = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                  landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            rh = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]

            le = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                  landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            ls = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                  landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            lh = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]

            lk = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                  landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
            la = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                  landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
            lh = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]

            rk = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            ra = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                  landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            rh = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]

            # Calculate angle
            angle = calculate_angle(re, rs, rh)
            ANGLE = calculate_angle(le, ls, lh)
            rightleg = calculate_angle(rh, rk, ra)
            leftleg = calculate_angle(rh, rk, ra)

            # Visualize angle

            cv2.putText(image, str(angle),
                        tuple(np.multiply(rs, [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                        )

            cv2.putText(image, str(ANGLE),
                        tuple(np.multiply(ls, [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                        )

            cv2.putText(image, str(rightleg),
                        tuple(np.multiply(rk, [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                        )

            cv2.putText(image, str(leftleg),
                        tuple(np.multiply(lk, [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                        )

            # welocme
            # eng.say("Welocme!! Let us practice the Warrior pose!! Please make sure your full body is visible inside the frame!") #say method for passing text to be spoken

            # counter logic

            # eng.say("Welocme!! Let us practice the Warrior pose!! Please make sure your full body is visible inside the frame!")

            if angle > 100:
                counter1 = " lower your right arm"
                c = c + 1
                print(counter1, c)
                if (c % 60 == 0):
                    engine.say("lower your right arm")
                    engine.runAndWait()
            if angle < 65:
                counter1 = "raise your right arm"
                c = c + 1
                print(counter1, c)
                if (c % 60 == 0):
                    engine.say("raise your right arm")
                    engine.runAndWait()
            if (angle >= 65 and angle <= 100):
                counter1 = "Right arm correct!"
                c = c + 1
                t = t + 1
                print(counter1)
            # if(c%30==0):
            #    engine.say("right arm correct")
            # engine.runAndWait()

            if (angle >= 65 and angle <= 100):
                if ANGLE > 105:
                    counter2 = " lower your left arm"
                    c = c + 1
                    print(counter2, c)
                    if (c % 60 == 0):
                        engine.say("lower your left arm")
                        engine.runAndWait()

                if ANGLE < 65:
                    counter2 = "raise your left arm"
                    c = c + 1
                    print(counter2, c)
                    if (c % 60 == 0):
                        engine.say("raise your left arm")
                        engine.runAndWait()

                if (ANGLE >= 65 and ANGLE <= 105):
                    counter2 = "Left arm correct!"
                    c = c + 1
                    t = t + 1
                    print(counter2, c)

            if (ANGLE >= 65 and ANGLE <= 105):

                if leftleg > 145:
                    counter3 = "Bend your right knee "
                    c = c + 1
                    print(counter3, c)
                    if (c % 60 == 0):
                        engine.say("Bend your right knee")
                        engine.runAndWait()

                if leftleg < 80:
                    counter2 = "Right knee bent too much"
                    c = c + 1
                    print(counter3, c)
                    if (c % 60 == 0):
                        engine.say("Right knee bent too much")
                        engine.runAndWait()

                if (leftleg >= 80 and leftleg <= 145):
                    counter3 = "Rightknee correct"
                    c = c + 1
                    t = t + 1
                    print(counter3, c)
                    if (t >= 3):
                        if (c % 30 == 0):
                            engine.say("Right knee correct")
                            engine.say("Congragulations! pose done correctly. Now try and hold posture for 3 counts.")
                            engine.runAndWait()


                            def countdown(t):
                                while t > 0:
                                    engine.say(t)
                                    engine.runAndWait()
                                    t -= 1
                                    time.sleep(1)
                                    engine.runAndWait()


                            countdown(3)
                            engine.say("Thank you. Stay healthy!")
                            t = 0

            # if (leftleg>=80 and leftleg<=145):

            # if rightleg > 280:
            # counter4 = "Bend your left knee "
            # c=c+1
            # print(counter4,c)
            # if(c%60==0):
            # engine.say("Bend your left knee")
            # engine.runAndWait()

            # if rightleg < 130 :
            # counter4="leftt knee bent too much"
            # c=c+1
            # print(counter4,c)
            # if(c%60==0):
            # engine.say("leftt knee bent too much")
            # engine.runAndWait()

            # if (rightleg>=130 and leftleg<=280):
            # counter3="Leftknee correct"
            # c=c+1
            # print(counter3,c)



        except:
            pass

        # Rep data
        # cv2.putText(image, 'Feedback:', (15,12),
        #           cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,255), 1, cv2.LINE_AA)
        cv2.putText(image, str(counter1),
                    (15, 12),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(image, str(counter2),
                    (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(image, str(counter3),
                    (5, 120),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2, cv2.LINE_AA)

        # cv2.putText(image, str(counter4),
        #  (0,200),
        # cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 2, cv2.LINE_AA)
        # @cv2.putText(image, str(crct),
        #   (250,250),
        #  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2, cv2.LINE_AA)

        # Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                  mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                  )

        cv2.imshow('Mediapipe Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
