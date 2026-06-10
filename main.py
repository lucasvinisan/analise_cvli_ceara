from src.sarima.sarima import executar_sarima
from src.exponential_smoothing.exponential_smoothing import executar_exponential_smoothing
from src.prophet.prophet_cvli import executar_prophet
import pandas as pd 
import joblib 
import webbrowser
import os

def executar():

    # |----- Aplicando modelos estatísticos -------|

    # Modelo exponential smoothing     
    previsao_exponential_smoothing = executar_exponential_smoothing()

    #Modelo Sarima
    previsao_sarima = executar_sarima()

    #Modelo prophet
    previsao_prophet = executar_prophet()
    

def abrir_dashboard():
    caminho_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_html = os.path.join(caminho_atual, 'index.html')
    
    if os.path.exists(caminho_html):
        url = 'file://' + os.path.realpath(caminho_html)
        webbrowser.open(url)
    else:
        print(f"Erro: O arquivo {caminho_html} não foi encontrado.")
    
if __name__ == "__main__":
    #executar()
    abrir_dashboard()