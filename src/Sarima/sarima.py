import pandas as pd 
import numpy as np 
from src.sarima import plots as grafico 
from src.sarima import modelo as ms
import matplotlib.pyplot as plt


def executar_sarima():

    df = pd.read_csv("dados/dados_previsoes_tratados_media.csv", index_col=0, parse_dates=True).asfreq('MS')

    # |------------ Análise Exploratória e Decomposição da Série Temporal ---------------| 
    grafico.plotar_graficos_serie(df)

    #Remove os outliers o de 2020 é o prinicpa já que na parte de residuos ele está destoando mais 
    grafico.decomposicao_aditivo(df)

    modelo = ms.criar_modelo(df)

    grafico.modelo_diagnostico(modelo)

    #modelo.plot_diagnostics(figsize=(10, 8))    
    #plt.show()
    
    #validaçãp
    test, forecast = ms.validar_modelo_sarima(modelo, df)

    grafico.plotar_validacao(test, forecast, df)

    #Metircas (MAE, RMSE, MAPE)
    ms.calculando_metricas(test, forecast)
    
    #Teste de Ljung_Box
    resultado_teste_lb = ms.test_Ljung_Box(modelo)
    print(resultado_teste_lb) 

       
   #Realizando Previsão
    previsao_2026 = ms.previsao_modelo(modelo, df)
    print(previsao_2026)
    
    #Plotar Previsão
    grafico.plotar_previsao_2026(previsao_2026)

    '''
    
    #d = 1 e D = 1 aplico a suavisação da seie (Dois são 1 se a série for estacionária)
    # |-----------------Implementando auto-arima -------------------------------------| 

    grafico.modelo_diagnostico(modelo)

   


    # Criando a tabela de comparação
    #grafico.tabela_comparacao(test, forecast)


    # |------------------ Realizando as Previsões --------------------------------|

    
    
    #Transformando em Dataframe para passar 
    #previsao = ms.transformar_DataFrame(previsao)
    


    #return previsao
    
    '''






