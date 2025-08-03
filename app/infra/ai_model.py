# app/infra/ai_model.py
from sentence_transformers import SentenceTransformer

class ModelLoader:
    _modelo = None

    @classmethod
    def get_model(cls):
        if cls._modelo is None:
            print("Carregando o modelo de IA...")
            # Você pode pegar o nome do modelo do .env se quiser
            cls._modelo = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
            print("✅ Modelo carregado.")
        return cls._modelo

# Instância única que será usada em toda a aplicação
model_loader = ModelLoader()