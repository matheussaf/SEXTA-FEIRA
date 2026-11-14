import requests
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="Sexta-Feira AI",
    description="Backend da assistente virtual pessoal do Matheus.",
    version="1.2.0"
)

class MensagemRequest(BaseModel):
    texto: str

# --- FUNÇÃO DE CLIMA REAL (Santos, SP) ---
def obter_clima_atual():
    url = "https://api.open-meteo.com/v1/forecast?latitude=-23.9608&longitude=-46.3336&current_weather=true"
    resposta = requests.get(url).json()
    temp = resposta["current_weather"]["temperature"]
    vento = resposta["current_weather"]["windspeed"]
    return f"Agora fazem {temp}°C em Santos, com ventos de {vento} km/h."

@app.get("/")
def home():
    return {
        "status": "online",
        "mensagem": "Olá, Matheus. A Sexta-Feira está operando."
    }

@app.post("/chat")
def processar_comando(requisicao: MensagemRequest):
    comando = requisicao.texto.lower()

    # Comandos de Clima
    if "clima" in comando or "tempo" in comando or "temperatura" in comando:
        clima = obter_clima_atual()
        return {"resposta_sexta_feira": clima}

    # Resposta padrão para outros comandos
    return {
        "resposta_sexta_feira": f"Comando recebido: '{requisicao.texto}'. Sistema operacional estável."
    }