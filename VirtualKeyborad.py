from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Key, Controller
from time import sleep
from MyKey import MyKey
import cv2

### Initializing webCam object
cam = cv2.VideoCapture(0)

### Setting webCam resolution
camW = 640
camH = 480
cam.set(3, camW)
cam.set(4, camH)

### Instantiating from handDetector class with some detection confidence (detectionCon)
### Change detectionCon to change model's strictness of hand detection
detector = HandDetector(detectionCon=0.8)

### Accessing system keyboard
keyboard = Controller()

### Creating keyboard keys' objects
keys = MyKey.create_all()

### Initializing some variables
place_holder_text = ''
caps = False

while True:
    ### Reading from the webCam object
    success, img = cam.read()

    ### Detecting landmarks of hand
    img = detector.findHands(img)

    ### Drawing place holder and keyboard keys
    MyKey.draw_all(keys, img, place_holder_text)

    ### Getting landmarks' list and bounding box
    lmList, bboxInfo = detector.findPosition(img)

    ### Checking whether any hand in sight
    if lmList:
        for key in keys:
            x, y = key.position
            w, h = key.size

            ### Checking coordinates of index finger
            if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                ### Changing color of the hovered key and magnifying it
                key.draw(img, (180, 0, 180), hovered=1)

                ### Computing distance between tip of index finger and tip of middle finger
                length, _, _ = detector.findDistance(8, 12, img, draw=False)

                ### Checking whether fingers' tips are close enough to each other, in order to tap the hovered key
                if length < 30:
                    ### Changing color of the tapped key
                    key.draw(img, (0, 255, 0))

                    ### Checking the tapped key to type
                    if key.label == 'Space':
                        place_holder_text += ' '
                        keyboard.tap(Key.space)
                    elif key.label == 'CAPS':
                        caps = not caps
                        keyboard.tap(Key.caps_lock)
                    elif key.label == 'BKSP':
                        keyboard.tap(Key.backspace)
                        if place_holder_text:
                            place_holder_text = place_holder_text[:-1]
                        else:
                            place_holder_text = ''
                    else:
                        if caps:
                            place_holder_text += key.label.upper()
                            keyboard.tap(key.label.upper())
                        else:
                            place_holder_text += key.label.lower()
                            keyboard.tap(key.label.lower())

                    ### Waiting to prevent additional letters be typed
                    sleep(0.2)

    ### Showing the window
    cv2.imshow("Image", img)
    cv2.waitKey(1)
