import torch

class ObjectDetector:
    def __init__(self, model_name='yolov5s'):
        self.model = torch.hub.load('ultralytics/yolov5', model_name)

    def detect(self, frame):
        results = self.model(frame)
        return results
