import pandas as pd
import numpy as np
import matplotlib.pyplot as  plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.api import ExponentialSmoothing
from statsmodels.tsa.api import SimpleExpSmoothing, Holt 

from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.stats.diagnostic import acorr_ljungbox
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error
from statsmodels.stats.diagnostic import acorr_ljungbox
import copy 

def modelo(df):

    modelo_suavizacao_exponencial = ExponentialSmoothing(
        df['CVLI'], 
        trend='add',
        seasonal='add',
        seasonal_periods=12
    )

    return modelo_suavizacao_exponencial 

def validacao_modelo(df): 

    train = df['2014-01-01' : '2023-12-01']
    test = df['2024-01-01': ]

    
    modelo_treino = ExponentialSmoothing(
        train['CVLI'],
        trend='add',
        seasonal='add',
        seasonal_periods=12
    )


    #Treinando o modelo
    Modelo_Treinado_validacao = modelo_treino.fit()

    #Fazendo as previsões  
    previsao = Modelo_Treinado_validacao.forecast(len(test)).astype(int)

    
    return test, previsao



def calculando_metricas(test, forecast):
    
    # MAE: Média de erro absoluto 
    mae = mean_absolute_error(test, forecast)

    # RMSE: Penaliza erros maiores 
    rmse = np.sqrt(mean_squared_error(test, forecast))

    # MAPE: Erro percentual
    mape = np.mean(np.abs((test - forecast['CVLI']) / test)) * 100

    print(f"Erro Médio Absoluto (MAE): {mae:.2f} crimes")
    print(f"Raiz do Erro Quadrático Médio (RMSE): {rmse:.2f} crimes")
    print(f"Erro Percentual Médio (MAPE): {mape:.2f}%")


def  test_Ljung_Box(modelo_ajustado): 

    residuos = modelo_ajustado.resid

    resultado_lb = acorr_ljungbox(residuos, lags=[10], return_df=True)

    return resultado_lb


def previsao_intervalo_confianca(modelo_ajustado):

    periodos = 5

    previsao_df = modelo_ajustado.forecast(5)

    simulacoes = modelo_ajustado.simulate(
        nsimulations=periodos,
        repetitions=1000,
        error='add'
    )

    indice_2026 = pd.date_range(start='2026-04-01', periods=periodos, freq='MS')

    df_2026 = pd.DataFrame({
        'CVLI'  : previsao_df.values.astype(int),
        'lower' : np.percentile(simulacoes, 5.0,  axis=1).astype(int),
        'upper' : np.percentile(simulacoes, 95.0, axis=1).astype(int),
    }, index=indice_2026)

    df_2026.index = df_2026.index.to_period('M')

    return df_2026


def transformar_DataFrame(previsao):
    previsao.index = previsao.index.to_period('M')
    return previsao