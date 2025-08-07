import os
import json
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

load_dotenv()

JSON_DATA_DIR = os.path.join('data', 'json')
FAISS_INDEX_DIR = os.path.join('data', 'faiss')

def create_and_save_faiss_index():
    print(f"--- '{JSON_DATA_DIR}' 폴더의 JSON 데이터로 FAISS 인덱스 생성을 시작합니다. ---")
    
    all_documents = []
    for filename in os.listdir(JSON_DATA_DIR):
        if filename.endswith(".json"):
            filepath = os.path.join(JSON_DATA_DIR, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            question_id = os.path.splitext(filename)[0]

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
    
    # OpenAI 임베딩 모델 초기화
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    
    # Document 리스트와 임베딩 모델을 사용해 FAISS 벡터 DB 생성
    faiss_db = FAISS.from_documents(all_documents, embeddings)
    
    # 생성된 인덱스를 data/faiss 폴더에 저장
    faiss_db.save_local(FAISS_INDEX_DIR)


if __name__ == "__main__":
    create_and_save_faiss_index()