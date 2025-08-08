from django.apps import AppConfig
import threading
from .ocr import get_ocr_model
from .grader import get_essay_grader


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        # 백그라운드에서 모델 초기화
        threading.Thread(target=self.initialize_models).start()

    def initialize_models(self):
        get_ocr_model()
        get_essay_grader()
        print("✅ 모든 모델 초기화 완료!")
