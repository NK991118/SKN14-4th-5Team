import os
import fitz
import json

PDF_SOURCE_DIR = os.path.join('static', 'pdf')

IMAGE_OUTPUT_DIR = os.path.join('static', 'images', 'pdf_pages')

CONFIG_FILE_PATH = os.path.join('app', 'config.py')

def convert_all_pdfs():
    print("PDF를 이미지로 변환하는 작업을 시작합니다...")

    os.makedirs(IMAGE_OUTPUT_DIR, exist_ok=True)

    for root, _, files in os.walk(PDF_SOURCE_DIR):
        for filename in files:
            if not filename.lower().endswith('.pdf'):
                continue

            pdf_path = os.path.join(root, filename)

            base_filename = os.path.splitext(filename)[0]

            output_folder_path = os.path.join(IMAGE_OUTPUT_DIR, base_filename)
            os.makedirs(output_folder_path, exist_ok=True)

            print(f"'{filename}' 파일을 처리 중...")

            doc = fitz.open(pdf_path)

            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                pix = page.get_pixmap(dpi=300)

                output_image_path = os.path.join(output_folder_path, f"page_{page_num + 1}.png")

                pix.save(output_image_path)
            
            print(f"  -> {len(doc)}개의 페이지를 이미지로 변환하여 '{output_folder_path}'에 저장했습니다.")
            doc.close()

    print("\n✅ 모든 PDF 변환 작업이 완료되었습니다!")
    print(f"이제 'python generate_config.py' 스크립트를 실행하여 'app/config.py' 파일을 업데이트하세요.")


if __name__ == "__main__":
    convert_all_pdfs()