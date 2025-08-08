import os
import pprint

JSON_DIR = os.path.join('data', 'json')
IMAGE_DIR = os.path.join('static', 'images', 'pdf_pages')
OUTPUT_FILE = os.path.join('app', 'config.py')
UNIVERSITY_MAP = {
    'konkuk': '건국대', 'khu': '경희대', 'dongguk': '동국대', 'sogang': '서강대',
    'skku': '성균관대', 'sookmyung': '숙명여대', 'soongsil': '숭실대', 'ajou': '아주대',
    'ewha': '이화여대', 'hufs': '한국외대', 'hongik': '홍익대',
}

def generate_config_file():
    print("--- app/config.py 파일 생성 스크립트 (디버그 모드) 시작 ---")
    
    # ★★★ 디버깅 코드 1: 현재 작업 위치 확인 ★★★
    print(f"1. 현재 스크립트 실행 위치: {os.getcwd()}")
    
    # ★★★ 디버깅 코드 2: JSON 폴더의 절대 경로 확인 ★★★
    absolute_json_dir = os.path.abspath(JSON_DIR)
    print(f"2. JSON 파일을 찾을 절대 경로: {absolute_json_dir}")

    # ★★★ 디버깅 코드 3: 해당 폴더가 진짜 있는지 확인 ★★★
    if not os.path.isdir(absolute_json_dir):
        print("3. [치명적 에러] 위 경로에 폴더가 존재하지 않습니다! 경로를 확인해주세요.")
        return # 스크립트 중단

    # ★★★ 디버깅 코드 4: 폴더 안의 모든 내용을 날것 그대로 확인 ★★★
    try:
        all_items_in_dir = os.listdir(absolute_json_dir)
        print(f"3. 폴더에서 찾은 모든 항목: {all_items_in_dir}")
    except Exception as e:
        print(f"3. [치명적 에러] 폴더를 읽는 중 오류 발생: {e}")
        return

    # ★★★ 디버깅 코드 5: .json으로 끝나는 파일만 필터링한 결과 확인 ★★★
    json_files = [f for f in all_items_in_dir if f.endswith('.json')]
    print(f"4. '.json'으로 필터링된 파일 목록: {json_files}")

    if not json_files:
        print("5. [알림] 처리할 JSON 파일이 없습니다. 스크립트를 종료합니다.")
        return

    print("5. 파일 처리를 시작합니다...")
    university_data = {}

    for filename in json_files:
        try:
            question_id = os.path.splitext(filename)[0]
            parts = question_id.split('_')
            if len(parts) != 3:
                print(f"  [경고] '{filename}' 파일 이름 형식이 잘못되었습니다.")
                continue
            uni_code, year, q_num = parts
            uni_name = UNIVERSITY_MAP.get(uni_code, uni_code.upper())
            question_key = f"문항{q_num}"

            image_folder = os.path.join(IMAGE_DIR, question_id)
            if not os.path.isdir(image_folder):
                print(f"  [경고] '{question_id}'에 대한 이미지 폴더를 찾을 수 없습니다.")
                continue

            image_files = sorted(
                os.listdir(image_folder),
                key=lambda f: int(os.path.splitext(f)[0].split('_')[1])
            )
            pages = [os.path.join('pdf_pages', question_id, img_file).replace('\\', '/') for img_file in image_files]

            university_data.setdefault(uni_name, {}).setdefault(year, {})[question_key] = {
                'id': question_id,
                'pages': pages
            }
            # print(f"  - 처리 완료: {question_id}") # 이 부분은 너무 길어지니 일단 주석 처리

        except Exception as e:
            print(f"  [에러] '{filename}' 처리 중 오류 발생: {e}")

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("# 이 파일은 generate_config.py에 의해 자동으로 생성되었습니다.\n")
        f.write("# 직접 수정하지 마세요.\n\n")
        f.write(f"UNIVERSITY_DATA = {pprint.pformat(university_data, indent=4)}\n")

    print(f"\n✅ {OUTPUT_FILE} 파일 생성이 성공적으로 완료되었습니다!")

if __name__ == "__main__":
    generate_config_file()