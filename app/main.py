import warnings
import asyncio
from app.uti.YandexCloudTokenManager import YandexCloudTokenManager
from app.uti.translate import Translator
from app.uti.yolo_detector import ObjectDetector
from app.uti.video_processor import VideoProcessor


warnings.filterwarnings("ignore", category=FutureWarning)
token_maneger = YandexCloudTokenManager()
token = token_maneger.get_token()


async def main():
    translator = Translator(iam_token=token, folder_id="b1goq174dg5prud37cui")
    detector = ObjectDetector()
    processor = VideoProcessor(detector, translator)

    await processor.run()

if __name__ == "__main__":
    asyncio.run(main())
