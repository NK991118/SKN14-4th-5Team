# c:/Workspaces/Personal_Anything/3rd_to_4th/fourth_project/create_faiss_index.py (새 파일)

import os
import json
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

# .env 파일에서 OPENAI_API_KEY를 불러와
load_dotenv()

# 필요한 파일 및 폴더 경로 설정
JSON_DATA_DIR = os.path.join('data', 'json')
FAISS_INDEX_DIR = os.path.join('data', 'faiss')

def create_and_save_faiss_index():
    """
    JSON 파일들을 읽어서 Document 객체로 만들고,
    OpenAI 임베딩을 사용하여 FAISS 인덱스를 생성하고 저장합니다.
    """
    print(f"--- '{JSON_DATA_DIR}' 폴더의 JSON 데이터로 FAISS 인덱스 생성을 시작합니다. ---")
    
    all_documents = []
    # data/json 폴더 안의 모든 json 파일을 순회
    for filename in os.listdir(JSON_DATA_DIR):
        if filename.endswith(".json"):
            filepath = os.path.join(JSON_DATA_DIR, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 파일명에서 question_id 추출 (예: khu_2023_1.json -> khu_2023_1)
            question_id = os.path.splitext(filename)[0]

            # 각 콘텐츠(채점기준, 모범답안)를 별개의 Document 객체로 만들어 리스트에 추가
            if data.get("grading_criteria"):
                all_documents.append(Document(
                    page_content=data["grading_criteria"],
                    metadata={"source_type": "채점기준", "question_id": question_id}
                ))
            if data.get("sample_answer"):
                all_documents.append(Document(
                    page_content=data["sample_answer"],
                    metadata={"source_type": "모범답안", "question_id": question_id}
                ))
            print(f"✅ '{filename}' 처리 완료.")

    if not all_documents:
        print("[오류] 처리할 문서가 없습니다. data/json 폴더를 확인해주세요.")
        return

    print(f"\n총 {len(all_documents)}개의 문서 조각을 임베딩하여 FAISS 인덱스를 생성합니다...")
    print("(문서 양에 따라 시간이 걸릴 수 있습니다. OpenAI API를 사용합니다.)")
    
    # OpenAI 임베딩 모델 초기화
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    
    # Document 리스트와 임베딩 모델을 사용해 FAISS 벡터 DB 생성
    faiss_db = FAISS.from_documents(all_documents, embeddings)
    
    # 생성된 인덱스를 data/faiss 폴더에 저장
    faiss_db.save_local(FAISS_INDEX_DIR)
    
    print(f"\n🎉 FAISS 인덱스 생성이 완료되었습니다!")
    print(f" -> 저장 위치: '{FAISS_INDEX_DIR}'")


if __name__ == "__main__":
    create_and_save_faiss_index()