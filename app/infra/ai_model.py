# app/infra/ai_model.py
from sentence_transformers import SentenceTransformer

class ModelLoader:
    _modelo = None

    @classmethod
    def get_model(cls):
        if cls._modelo is None:
            print("Carregando o modelo de IA...")
            cls._modelo = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
            print("✅ Modelo carregado.")
        return cls._modelo

model_loader = ModelLoader()