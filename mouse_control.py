import cv2
import mediapipe
import pyautogui
from threading import Thread

class HandTracker:
    def __init__(self):
        self.capture_hands = mediapipe.solutions.hands.Hands()
        self.drawing_option = mediapipe.solutions.drawing_utils
        self.screen_width, self.screen_height = pyautogui.size()
        self.camera = cv2.VideoCapture(0)
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
                    for id, lm in enumerate(one_hand_landmarks):
                        x = int(lm.x * image_width)
                        y = int(lm.y * image_height)

                        if id == 8:
                            mouse_x = int(self.screen_width / image_width * x)
                            mouse_y = int(self.screen_height / image_height * y)
                            cv2.circle(image, (x, y), 10, (0, 255, 255))
                            pyautogui.moveTo(mouse_x, mouse_y)
                            x1 = x
                            y1 = y

                        if id == 4:
                            x2 = x
                            y2 = y
                            cv2.circle(image, (x, y), 10, (0, 255, 255))

                        if id == 12:
                            x3 = x
                            y3 = y
                            cv2.circle(image, (x, y), 10, (0, 255, 255))

                singClick = y2 - y1
                doubClick = y3 - y1

                if singClick < 20:
                    pyautogui.click()

                if doubClick < 20:
                    pyautogui.doubleClick()

            cv2.imshow("Hand Mouse Tracker", image)
            key = cv2.waitKey(100)

            if key == 27:
                self.stop()

    def stop(self):
        self.stopped = True
        self.camera.release()
        cv2.destroyAllWindows()

# Create and start the hand tracker
hand_tracker = HandTracker().start()
