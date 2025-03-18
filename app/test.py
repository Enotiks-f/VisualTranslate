import warnings
import asyncio
from app.uti.translate import Translator
from app.detectors.yolo_detector import ObjectDetector
from app.processors.video_processor import VideoProcessor


warnings.filterwarnings("ignore", category=FutureWarning)

async def main():
    translator = Translator(iam_token="t1.9euelZqJjZyTj8eTlZaJj8-Jxs2ZzO3rnpWalY6PyMqTzcvJnZyQjonKlZvl8_ctNRhB-e8FCnos_N3z921jFUH57wUKeiz8zef1656VmsmKys-Xxo3Nls7MzM7Ll5uL7_zF656VmsmKys-Xxo3Nls7MzM7Ll5uL.G0STGyQRMSEZpEYiDIRDngY4Jj03FM3PXoSCWui9WDse_CKvkhW_3E3F9r6PXlfMxZU1bw7MX8NyUf3hjXQ0Cw", folder_id="b1goq174dg5prud37cui")
    detector = ObjectDetector()
    processor = VideoProcessor(detector, translator)

    await processor.run()

if __name__ == "__main__":
    asyncio.run(main())
