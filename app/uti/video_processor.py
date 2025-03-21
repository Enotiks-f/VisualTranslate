import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy as np

class VideoProcessor:
    def __init__(self, detector, translator):
        self.detector = detector
        self.translator = translator
        self.click_x, self.click_y = -1, -1
        self.selected_label = None
        self.translated_label = None

    def click_event(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.click_x, self.click_y = x, y
            print(f"Клик по координатам: ({x}, {y})")

    def draw_text_with_pillow(self, frame, text, x, y, font_size=32, color=(0, 255, 0), bg_color=(0, 0, 0), padding=5):
        self.font_path = "C:/Users/titov/AppData/Local/Microsoft/Windows/Fonts/DejaVuSans.ttf"
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(image)
        draw = ImageDraw.Draw(pil_image)
        font = ImageFont.truetype(self.font_path, font_size)
        bbox = draw.textbbox((x, y), text, font=font)
        text_width = bbox[2] - bbox[0] + 2 * padding
        text_height = bbox[3] - bbox[1] + 2 * padding

        draw.rectangle(
            [(x, y), (x + text_width, y + text_height)],
            fill=bg_color
        )

        draw.text((x + padding, y + padding), text, font=font, fill=color)
        frame = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        return frame

    async def process_frame(self, frame):
        height, width, _ = frame.shape
        box_size = int(min(width, height) * 0.7)
        x1_center = (width - box_size) // 2
        y1_center = (height - box_size) // 2
        x2_center = x1_center + box_size
        y2_center = y1_center + box_size

        cv2.rectangle(frame, (x1_center, y1_center), (x2_center, y2_center), (255, 255, 255), 2)

        results = self.detector.detect(frame)
        translation_position = (width // 2 - 100, height - 50)

        for det in results.pred[0]:
            x1, y1, x2, y2, conf, cls = det
            label = results.names[int(cls)]
            translated_label = await self.translator.translate(label, "ru")

            if x1 <= self.click_x <= x2 and y1 <= self.click_y <= y2:
                print(f"Объект '{label}' выбран!")
                self.selected_label = label
                self.selected_coords = (x1, y1, x2, y2)
                self.translated_label = await self.translator.translate(label, "cv")
                print(f"Переведенное название: {self.translated_label}")
                self.click_x, self.click_y = -1, -1

            if x1_center <= x1 <= x2_center and y1_center <= y1 <= y2_center:
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 1)
                frame = self.draw_text_with_pillow(frame, translated_label, int(x1), int(y1) - 30)

        if self.selected_label and self.translated_label:
            frame = self.draw_text_with_pillow(
                frame,
                f"{await self.translator.translate(self.selected_label, 'ru')} - {self.translated_label}",
                *translation_position, color=(255, 0, 0)
            )

        return frame

    async def run(self):
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FPS, 30)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        cv2.namedWindow("Detected Objects with Click")
        cv2.setMouseCallback("Detected Objects with Click", self.click_event)

        while True:
            ret, frame = cap.read()
            frame = cv2.flip(frame, 1)
            if not ret:
                break

            frame = await self.process_frame(frame)
            cv2.imshow("Detected Objects with Click", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
