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

    def set_click_coordinates(self, x, y):
        """Устанавливает координаты клика (из веб-интерфейса)"""
        self.click_x, self.click_y = x, y
        print(f"Клик по координатам: ({x}, {y})")

    def draw_text_with_pillow(self, frame, text, x, y, font_path, font_size=32, color=(0, 255, 0)):
        """Рисует текст с использованием Pillow на кадре OpenCV"""
        self.font_path = "C:/Users/titov/AppData/Local/Microsoft/Windows/Fonts/DejaVuSans.ttf"
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(image)

        # Создаем объект для рисования текста
        draw = ImageDraw.Draw(pil_image)
        font = ImageFont.truetype(self.font_path, font_size)

        # Рисуем текст
        draw.text((x, y), text, font=font, fill=color)

        # Преобразуем изображение обратно в формат OpenCV
        frame = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        return frame

    async def process_frame(self, frame):
        """Обрабатывает кадр и добавляет разметку"""
        results = self.detector.detect(frame)

        # Отображаем ранее выбранный объект, если есть
        if self.selected_label and self.translated_label:
            frame = self.draw_text_with_pillow(frame, self.translated_label, 50, 50, self.font_path, 32)

        for det in results.pred[0]:
            x1, y1, x2, y2, conf, cls = det
            label = results.names[int(cls)]

            # Рисуем рамку и текст
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 1)
            cv2.putText(frame, f"{label} ({conf:.2f})", (int(x1), int(y1) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            # Проверяем, попал ли клик в объект
            if x1 <= self.click_x <= x2 and y1 <= self.click_y <= y2:
                print(f"Объект '{label}' выбран!")
                self.selected_label = label
                self.translated_label = await self.translator.translate(label)
                print(f"Переведенное название: {self.translated_label}")
                # Сбрасываем координаты клика после обработки
                self.click_x, self.click_y = -1, -1

        return frame
