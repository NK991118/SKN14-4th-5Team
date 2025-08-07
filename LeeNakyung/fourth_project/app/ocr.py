from paddleocr import PaddleOCR
import numpy as np
from PIL import Image
import io

ocr_model = None

def get_ocr_model():
    global ocr_model
    if ocr_model is None:
        print("PaddleOCR 모델을 로딩합니다...")
        ocr_model = PaddleOCR(lang='korean',
                               use_doc_orientation_classify=False,
                               use_doc_unwarping=False,
                               use_textline_orientation=False)
        print("✅ PaddleOCR 모델 로딩 완료!")
    return ocr_model

def process_image_to_text(image_file):

    try:

        image_bytes = image_file.read()

        image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        
        np_array = np.array(image)

        result = ocr_model.predict(np_array)

        if not result or not result[0]:
            return "이미지에서 텍스트를 추출하지 못했습니다."

        return "".join(result[0]['rec_texts'])

    except Exception as e:
        print(f"[OCR-ERROR] 처리 중 예상치 못한 오류 발생: {e}")
        return f"OCR 처리 중 오류가 발생했습니다: {e}"