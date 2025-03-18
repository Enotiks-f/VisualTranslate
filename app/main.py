import cv2
import asyncio
import base64
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from app.processors.video_processor import VideoProcessor

app = FastAPI()

# Инициализируем VideoProcessor (добавь нужные аргументы)
video_processor = VideoProcessor(detector=None, translator=None)  # Укажи реальные объекты

@app.get("/")
async def get():
    with open("app/templates/index.html", "r", encoding="utf-8") as file:
        return HTMLResponse(file.read())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    cap = cv2.VideoCapture(0)  # Используем встроенную камеру по умолчанию

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Обработка кадра через VideoProcessor
            processed_frame = await video_processor.process_frame(frame)

            # Кодируем изображение в формат JPEG
            _, buffer = cv2.imencode('.jpg', processed_frame)
            frame_data = base64.b64encode(buffer).decode("utf-8")

            # Отправляем через WebSocket
            await websocket.send_text(frame_data)

            # Контроль частоты кадров
            await asyncio.sleep(0.01)  # Плавный вывод, настраиваем под нужный FPS

    except Exception as e:
        print(f"Ошибка WebSocket: {e}")

    finally:
        cap.release()
        await websocket.close()
