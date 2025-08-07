from paddleocr import PaddleOCR
import numpy as np
from PIL import Image
import io

# PaddleOCR 모델을 초기화해. 이 과정은 서버가 시작될 때 딱 한 번만 실행되는 게 좋아.
# use_angle_cls=True와 lang='korean' 옵션은 한글 인식률을 높이는 데 중요해.
print("글자 방향 탐지(use_angle_cls=True) 기능이 포함된 PaddleOCR 모델을 로딩합니다...")
ocr_model = PaddleOCR(use_angle_cls=True, lang='korean')
print("✅ PaddleOCR 모델 로딩 완료!")


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
        result = ocr_model.ocr(np_array, cls=True)

        # 5. 결과가 없거나 비어있는 경우를 대비한 방어 코드.
        if not result or not result[0]:
            return "이미지에서 텍스트를 추출하지 못했습니다."

        # 6. 추출된 텍스트만 뽑아서 하나의 문자열로 합쳐서 반환해.
        text_lines = [line[1][0] for line in result[0]]
        return "\n".join(text_lines)

    except Exception as e:
        # 에러가 발생하면 터미널에 로그를 남기고, 사용자에게 보여줄 메시지를 반환해.
        print(f"[OCR-ERROR] 처리 중 예상치 못한 오류 발생: {e}")
        return f"OCR 처리 중 오류가 발생했습니다: {e}"