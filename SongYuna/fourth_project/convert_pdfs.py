# c:/Workspaces/Personal_Anything/3rd_to_4th/fourth_project/convert_pdfs.py (새 파일)

import os
import fitz  # PyMuPDF 라이브러리야. PDF를 다루는 아주 강력한 도구!
import json

# 원본 PDF 파일들이 있는 폴더 경로
PDF_SOURCE_DIR = os.path.join('static', 'pdf')

# 변환된 이미지들을 저장할 폴더 경로
IMAGE_OUTPUT_DIR = os.path.join('static', 'images', 'pdf_pages')

# 각 문제에 대한 정보를 담고 있는 config.py 파일 경로
CONFIG_FILE_PATH = os.path.join('app', 'config.py')

def convert_all_pdfs():
    print("PDF를 이미지로 변환하는 작업을 시작합니다...")

    # 이미지 저장 폴더가 없으면 새로 만들어줘.
    os.makedirs(IMAGE_OUTPUT_DIR, exist_ok=True)

    # config.py를 읽어서 UNIVERSITY_DATA 딕셔너리를 가져와야 해.
    # 하지만 직접 import하기보다, 파일로 읽어서 처리하는 게 더 안전해.
    # 여기서는 간단하게 파일 경로만 가지고 작업할게.

    # PDF_SOURCE_DIR 안에 있는 모든 파일과 폴더를 순회해.
    for root, _, files in os.walk(PDF_SOURCE_DIR):
        for filename in files:
            # PDF 파일이 아니면 건너뛰어.
            if not filename.lower().endswith('.pdf'):
                continue

            # 원본 PDF 파일의 전체 경로
            pdf_path = os.path.join(root, filename)
            
            # PDF 파일 이름에서 확장자(.pdf)를 뺀 부분을 폴더 이름으로 사용할 거야.
            # 예: 'khu_2023_1.pdf' -> 'khu_2023_1'
            base_filename = os.path.splitext(filename)[0]
            
            # 각 PDF 페이지 이미지를 저장할 개별 폴더를 만들어.
            # 예: 'static/images/pdf_pages/khu_2023_1/'
            output_folder_path = os.path.join(IMAGE_OUTPUT_DIR, base_filename)
            os.makedirs(output_folder_path, exist_ok=True)

            print(f"'{filename}' 파일을 처리 중...")

            # fitz를 사용해서 PDF 파일을 열어.
            doc = fitz.open(pdf_path)

            # PDF의 각 페이지를 순회하면서 이미지로 변환해.
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)  # 페이지를 불러와.
                pix = page.get_pixmap(dpi=300)  # 페이지를 픽셀맵(이미지)으로 변환해.
                
                # 저장할 이미지 파일 경로를 만들어.
                # 예: '.../khu_2023_1/page_1.png'
                output_image_path = os.path.join(output_folder_path, f"page_{page_num + 1}.png")
                
                # 이미지를 PNG 파일로 저장해.
                pix.save(output_image_path)
            
            print(f"  -> {len(doc)}개의 페이지를 이미지로 변환하여 '{output_folder_path}'에 저장했습니다.")
            doc.close()

    print("\n✅ 모든 PDF 변환 작업이 완료되었습니다!")
    print(f"이제 'python generate_config.py' 스크립트를 실행하여 'app/config.py' 파일을 업데이트하세요.")


if __name__ == "__main__":
    convert_all_pdfs()