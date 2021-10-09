from cvzone import cornerRect
import cv2

class MyKey:
    def __init__(self, position, label, size=(40, 40), text_indent=(8, 30)):
        self.position = position
        self.label = label
        self.size = size
        self.text_indent = text_indent

    def draw(self, img, color=(255, 0, 255), hovered=0):
        margin = 3

        x, y = self.position
        w, h = self.size
        i_x, i_y = self.text_indent

        cornerRect(img, (x, y, w, h), 10, rt=0)
        cv2.rectangle(img, (x - margin * hovered, y - margin * hovered),
                      (x + w + margin * hovered, y + h + margin * hovered), color, cv2.FILLED)
        cv2.putText(img, self.label, (x + i_x, y + i_y), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

    @staticmethod
    def create_all():
        labels = [['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '[', ']'],
                ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';', '\'', '\\'],
                ['Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/']]

        keys = []

        for i in range(len(labels)):
            for j, label in enumerate(labels[i]):
                keys.append(MyKey((50 * j + 25, 50 * i + 10), label))

        keys.append(MyKey((525, 110), 'CAPS', (90, 40), (5, 30)))
        keys.append(MyKey((25, 160), 'Space', (490, 40), (200, 30)))
        keys.append(MyKey((525, 160), 'BKSP', (90, 40), (5, 30)))

        return keys

    @staticmethod
    def draw_all(keys, img, place_holder_text):
        for key in keys:
            key.draw(img)

        cv2.rectangle(img, (25, 210), (615, 250), (130, 0, 130), cv2.FILLED)
        cv2.putText(img, place_holder_text, (30, 240), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
