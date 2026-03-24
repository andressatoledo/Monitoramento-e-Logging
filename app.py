import logging
import json
import time
import random
from flask import Flask
from prometheus_client import start_http_server, Summary, generate_latest

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "service": "API-Pagamentos"
        }
        return json.dumps(log_entry)

logger = logging.getLogger("app_logger")
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)

REQUEST_TIME = Summary('request_processing_seconds', 'Tempo de processamento de requisição')

app = Flask(__name__)

@app.route('/')
@REQUEST_TIME.time()
def index():
    logger.info("Processando requisição na rota principal")
    time.sleep(random.uniform(0.1, 0.5)) 
    return "Aplicação Online!"

@app.route('/error')
def error():
    logger.error("Erro crítico detectado na rota de teste!")
    return "Erro simulado", 500

@app.route('/sobrecarga')
@REQUEST_TIME.time()
def sobrecarga():
    logger.warning("ALERTA: Processamento lento detectado na rota de sobrecarga")
    time.sleep(2.0) 
    return "Simulação de lentidão concluída", 200

if __name__ == '__main__':
    start_http_server(8000) 
    logger.info("Iniciando aplicação na porta 5000 e métricas na 8000...")
    app.run(port=5000)
