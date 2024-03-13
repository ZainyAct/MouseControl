from operator import index
import cv2
import mediapipe
import pyautogui
from threading import Thread

class HandTracker:
    def __init__(self, capture_fps=60):
        self.capture_hands = mediapipe.solutions.hands.Hands()
        self.drawing_option = mediapipe.solutions.drawing_utils
        self.screen_width, self.screen_height = pyautogui.size()
        self.camera = cv2.VideoCapture(0)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # Set frame width to 1280 pixels
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)   # Set frame height to 720 pixels
        self.camera.set(cv2.CAP_PROP_FPS, capture_fps)    # Set frame rate
        self.stopped = False

    def start(self):
        Thread(target=self.track_hands, args=()).start()
        return self

    def track_hands(self):
        while not self.stopped:
            _, image = self.camera.read()
            image_height, image_width, _ = image.shape
            image = cv2.flip(image, 1)
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            output_hands = self.capture_hands.process(rgb_image)
            all_hands = output_hands.multi_hand_landmarks


            if all_hands:
                for hand in all_hands:
                    self.drawing_option.draw_landmarks(image, hand)
                    one_hand_landmarks = hand.landmark

                    ring_finger = one_hand_landmarks[16]
                    thumb_finger = one_hand_landmarks[8]
                    index_finger = one_hand_landmarks[4]
                    middle_finger = one_hand_landmarks[12]
                    pinky_finger = one_hand_landmarks[20]

                    for id, lm in enumerate(one_hand_landmarks):
                        
                        x = int(lm.x * image_width)
                        y = int(lm.y * image_height)

                        if id == 8: #Index Finger
                            mouse_x = int(self.screen_width / image_width * x)
                            mouse_y = int(self.screen_height / image_height * y)
                            pyautogui.moveTo(mouse_x, mouse_y)

                            cv2.circle(image, (x, y), 10, (0, 255, 255))
                            x1 = x
                            y1 = y

                        if id == 4: #Thumb
                            cv2.circle(image, (x, y), 10, (0, 255, 255))
                            x2 = x
                            y2 = y
                            

                        if id == 12: #Middle
                            cv2.circle(image, (x, y), 10, (0, 255, 255))
                            x3 = x
                            y3 = y 

                        if id == 16: #Ring
                            cv2.circle(image, (x, y), 10, (0, 255, 255))
                            x4 = x
                            y4 = y 

                        
                        if id == 20: #Pinky
                            cv2.circle(image, (x, y), 10, (0, 255, 255))
                            x5 = x
                            y5 = y 

                        if id == 0: #Palm Base
                            cv2.circle(image, (x, y), 10, (255, 0, 255))
                            x6 = x
                            y6 = y 
                            
                            
                def calc_dist(x,y):
                    return cv2.sqrt(x**2, y**2)

                    

                def single_click():
                    singClick = y2 - y1
                    if singClick < 40:
                        
                        return True


                #doubClick = y3 - y1

                #if singClick < 40:
                #    pyautogui.click()

                #if doubClick < 40:
                #    pyautogui.doubleClick()

            cv2.imshow("Hand Mouse Tracker", image)
            key = cv2.waitKey(100)

            if key == 27:
                self.stop()

    def stop(self):
        self.stopped = True
        self.camera.release()
        cv2.destroyAllWindows()

# Create and start the hand tracker
hand_tracker = HandTracker(capture_fps=60).start()
