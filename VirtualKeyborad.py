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
sym_dict = {'1': '!',
            '2': '@',
            '3': '#',
            '4': '$',
            '5': '%',
            '6': '^',
            '7': '&',
            '8': '*',
            '9': '(',
            '0': ')',
            '-': '_',
            '=': '+',
            '[': '{',
            ']': '}',
            ';': ':',
            '\'': '"',
            '\\': '|',
            ',': '<',
            '.': '>',
            '/': '?'}
place_holder_text = ''
shift = False

while True:
    ### Reading from the webCam object
    success, img = cam.read()

    ### Detecting landmarks of hand
    img = detector.findHands(img)

    ### Drawing place holder and keyboard keys
    MyKey.draw_all(keys, img, place_holder_text, shift)

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

                ### Computing distance between index fingertip and middle fingertip
                length, _, _ = detector.findDistance(8, 12, img, draw=False)

                ### Checking whether fingertips are close enough to each other, in order to tap the hovered key
                if length < 30:
                    ### Changing color of tapped key
                    key.draw(img, (0, 255, 0))

                    label = key.label

                    ### Checking the tapped key to type
                    if label == 'Space':
                        keyboard.tap(Key.space)
                        place_holder_text += ' '
                    elif label == 'Shift':
                        shift = not shift
                    elif label == 'BKSP':
                        keyboard.tap(Key.backspace)
                        place_holder_text = place_holder_text[:-1] if place_holder_text else ''
                    elif shift:
                        with keyboard.pressed(Key.shift):
                            keyboard.tap(label.lower())
                            place_holder_text += sym_dict[label.lower()] if label.lower() in sym_dict.keys()\
                                else label.upper()
                    else:
                        keyboard.tap(label.lower())
                        place_holder_text += label.lower()

                    ### Waiting to prevent additional letters be typed
                    sleep(0.2)

    ### Showing the window
    cv2.imshow("Virtual Keyboard", img)
    cv2.waitKey(1)
