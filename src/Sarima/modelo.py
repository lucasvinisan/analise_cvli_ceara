from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
import pandas as pd 
import pmdarima as pm 
import numpy as np 
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
from src.sarima import plots as grafico 
from sklearn.metrics import mean_absolute_error, mean_squared_error
from statsmodels.stats.diagnostic import acorr_ljungbox
import copy



def testar_estacionariedade(df):
    #CALCULANDO O DICKEY FULLER 

    resultado = adfuller(df['CVLI']) 
    
    print('Estatistica ADF: ', resultado[0]) 
    print('p-valor: ', resultado[1]) 

    '''
    if (resultado[1] > 0.05):
        print('Serie não é estácionaria')
    else:
        print('Série é estacionária')
    
    '''
#|-------- Modelo Sarima ------------------|
def criar_modelo(df):

    modelo = pm.auto_arima(
                            df['CVLI'],
                            start_p = 1, max_p = 6, 
                            start_q = 1, max_q = 6, 
                            d = 1, D = 1,
                            exog=df[['CRISE_2017','QUEDA_2019','ANOMALIA_2020', 'REDUCAO_2026']],
                            m = 12, 
                            stationary = False,
                            seasonal = True, 
                            trace = True, 
                            suppress_warnings = True, 
                            stepwise = True 
    )

    return modelo 

def validar_modelo_sarima(modelo, df):
    
    modelo_val = copy.deepcopy(modelo)

    train = df.loc['2014-01-01':'2023-12-01']
    test  = df['CVLI'].loc['2024-01-01':]

    exog_train = train[['CRISE_2017', 'QUEDA_2019', 'ANOMALIA_2020', 'REDUCAO_2026']]

    exog_test = pd.DataFrame({
        'CRISE_2017': [0] * len(test),
        'QUEDA_2019': [0] * len(test),
        'ANOMALIA_2020': [0] * len(test),
        'REDUCAO_2026': [0] * len(test),
    })

    modelo_val.fit(train['CVLI'], X=exog_train)

    forecast = modelo_val.predict(
        n_periods=len(test),
        X=exog_test
    ).astype(int)

    forecast = pd.DataFrame(forecast, index=test.index, columns=['CVLI'])

    return test, forecast


def  test_Ljung_Box(modelo): 

    residuos = modelo.resid()
    resultado_lb = acorr_ljungbox(residuos, lags=[10], return_df=True)

    return resultado_lb

def calculando_metricas(test, forecast):
    
    # MAE: Média de erro absoluto 
    mae = mean_absolute_error(test, forecast)
    # RMSE: Penalizaos erros maiores 
    rmse = np.sqrt(mean_squared_error(test, forecast))
    # MAPE: Erro percentual
    mape = np.mean(np.abs((test - forecast['CVLI']) / test)) * 100

    print(f"Erro Médio Absoluto (MAE): {mae:.2f} crimes")
    print(f"Raiz do Erro Quadrático Médio (RMSE): {rmse:.2f} crimes")
    print(f"Erro Percentual Médio (MAPE): {mape:.2f}%")

def transformar_DataFrame(previsao): 

    datas = pd.date_range(start='2026-04', end='2026-8', freq='MS')
    previsao = previsao.values.flatten() 

    df_cvli = pd.DataFrame({
    'MES': datas,
    'CVLI': previsao 
    })


    df_cvli['MES'] = df_cvli['MES'].dt.to_period('M') # para ficar melhor apresentavel 
    
    return df_cvli

def previsao_modelo(modelo, df):
    n = 5

    future_exog = pd.DataFrame({
        'CRISE_2017': [0] * n,
        'QUEDA_2019': [0] * n,
        'ANOMALIA_2020': [0] * n,
        'REDUCAO_2026' : [0] * n,
    })

    previsao, conf_intervalo = modelo.predict(
        n_periods=n,
        exogenous=future_exog,
        return_conf_int=True,
        alpha=0.1
    )

    indice = pd.date_range(start='2026-04-01', periods=n, freq='MS')

    
    df_2026 = pd.DataFrame({
        'CVLI' : np.round(previsao).astype(float),
        'lower': np.round(conf_intervalo[:, 0]).astype(float),
        'upper': np.round(conf_intervalo[:, 1]).astype(float),
    }, index=indice)

    df_2026[['CVLI', 'lower', 'upper']] = df_2026[['CVLI', 'lower', 'upper']].clip(lower=0)
   
    return df_2026
