import os
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from groq import Groq

# Carrega as chaves do arquivo .env na raiz do projeto
load_dotenv(dotenv_path="../.env")

api_key = os.getenv("GROQ_API_KEY") or os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Aviso: A chave da API não foi encontrada no arquivo .env!")

client = Groq(api_key=api_key)

# Descobre automaticamente um modelo de chat válido disponível na conta
def obter_modelo_disponivel():
    try:
        modelos = client.models.list().data
        for m in modelos:
            # Ignora modelos de áudio (whisper) ou guarda-chuva
            if "whisper" not in m.id.lower() and "guard" not in m.id.lower():
                return m.id
    except Exception:
        pass
    return "llama-3.1-8b-instant"

MODELO_ATIVO = obter_modelo_disponivel()

app = FastAPI(
    title="Sexta-Feira AI",
    description="Backend da assistente virtual pessoal emparelhada com Groq.",
    version="1.8.0"
)

class MensagemRequest(BaseModel):
    texto: str

def obter_clima_atual():
    try:
        url = "https://api.open-meteo.com/v1/forecast?latitude=-23.9608&longitude=-46.3336&current_weather=true"
        resposta = requests.get(url).json()
        temp = resposta["current_weather"]["temperature"]
        vento = resposta["current_weather"]["windspeed"]
        return f"Agora fazem {temp}°C em Santos, com ventos de {vento} km/h."
    except Exception:
        return "Não consegui consultar o clima de Santos no momento, chefe."

@app.get("/")
def home():
    return {
        "status": "online",
        "modelo_ativo": MODELO_ATIVO,
        "mensagem": "Sexta-Feira operando com descoberta automática de modelo."
    }

@app.post("/chat")
def processar_comando(requisicao: MensagemRequest):
    comando = requisicao.texto.lower()

    if "clima" in comando or "tempo" in comando or "temperatura" in comando:
        clima = obter_clima_atual()
        return {"resposta_sexta_feira": clima}

    try:
        chat_completion = client.chat.completions.create(   
            messages=[
                {
                    "role": "system",
                    "content": "Você é a SEXTA-FEIRA, uma assistente pessoal inteligente, direta, leal e informal criada pelo Matheus. Responda em português brasileiro."
                },
                {
                    "role": "user",
                    "content": requisicao.texto,
                }
            ],
            model=MODELO_ATIVO,
        )
        return {
            "modelo_usado": MODELO_ATIVO,
            "resposta_sexta_feira": chat_completion.choices[0].message.content
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao falar com a IA ({MODELO_ATIVO}): {str(e)}")