# c:/Workspaces/Personal_Anything/3rd_to_4th/fourth_project/app/ocr.py

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
    """
    업로드된 이미지 파일(in-memory file)을 받아서 텍스트를 추출하는 함수.
    """
    try:
        # 1. Django가 전달해준 이미지 파일을 읽어서 바이트(bytes) 형태로 변환해.
        image_bytes = image_file.read()

        # 2. 바이트 데이터를 Pillow 라이브러리를 사용해 이미지 객체로 열고,
        #    안정적인 처리를 위해 RGB 형식으로 변환해.
        image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        
        # 3. 이미지를 numpy 배열로 변환해. PaddleOCR이 처리할 수 있는 형태야.
        np_array = np.array(image)

        # 4. OCR 모델을 실행해서 텍스트를 추출해!
        #    result 구조: [[[[좌표], ('텍스트', 정확도)], ...]]
        result = get_ocr_model().predict(np_array)

        # 5. 결과가 없거나 비어있는 경우를 대비한 방어 코드.
        if not result or not result[0]:
            return "이미지에서 텍스트를 추출하지 못했습니다."

        # 6. 추출된 텍스트만 뽑아서 하나의 문자열로 합쳐서 반환해.
        # text_lines = [line[1][0] for line in result[0]]
        return "".join(result[0]['rec_texts'])

    except Exception as e:
        # 에러가 발생하면 터미널에 로그를 남기고, 사용자에게 보여줄 메시지를 반환해.
        print(f"[OCR-ERROR] 처리 중 예상치 못한 오류 발생: {e}")
        return f"OCR 처리 중 오류가 발생했습니다: {e}"