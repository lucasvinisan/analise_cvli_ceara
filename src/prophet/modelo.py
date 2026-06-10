import pandas as pd 
from prophet import Prophet
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error
from prophet.diagnostics import cross_validation, performance_metrics
import copy


def criar_modelo(df):

    modelo = Prophet(
        seasonality_mode='additive',
        interval_width=0.90,
        changepoint_prior_scale=0.2,      
        seasonality_prior_scale=10,       
        weekly_seasonality=False,
        daily_seasonality=False,
    )

    modelo.add_regressor('CRISE_2017')
    modelo.add_regressor('QUEDA_2019')
    modelo.add_regressor('ANOMALIA_2020')
    modelo.add_regressor('REDUCAO_2026')

    return modelo 

def validacao_modelo(modelo, df):
    
    modelo_validacao = copy.deepcopy(modelo) 

    train = df[(df['ds'] >= '2014-01-01') & (df['ds'] <= '2024-01-01')]
    test = df[(df['ds'] > '2024-01-01')]

    future_test = test.drop(columns=['y'])

   #Treinamento
    modelo_validacao.fit(train)

    #Pevisão
    forecast_test = modelo_validacao.predict(future_test)

    return forecast_test, test



def previsao_2026(modelo_final):

    periodos = 8 

    future = modelo_final.make_future_dataframe(periods=periodos, freq='MS')

    future['CRISE_2017'] = 0
    future['QUEDA_2019'] = 0
    future['ANOMALIA_2020'] = 0


    future['REDUCAO_2026'] = future['ds'].apply(lambda x: 1 if x.year == 2026 else 0)

    forecast = modelo_final.predict(future)
    
    previsao_2026 = forecast[
        (forecast['ds'] >= '2026-04-01') & 
        (forecast['ds'] <= '2026-08-01')
    ][['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    
    previsao_2026['yhat']  = previsao_2026['yhat'].astype(int)
    previsao_2026['yhat_lower'] = previsao_2026['yhat_lower'].astype(int)
    previsao_2026['yhat_upper'] = previsao_2026['yhat_upper'].astype(int)

    return previsao_2026



def metricas(test, forecast_test):

    # Métricas
    real = test['y'].values
    previsto = forecast_test.set_index('ds').loc[test['ds'], 'yhat'].values

    mae  = mean_absolute_error(real, previsto)
    rmse = np.sqrt(mean_squared_error(real, previsto))
    mape = np.mean(np.abs((real - previsto) / real)) * 100

    print(f"MAE:  {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")
    print(f"MAPE: {mape:.2f}%")


def aplicando_cross_validation(modelo_final): 

    df_cv = cross_validation(
        modelo_final,
        initial='1095 days',  
        period='182 days',    
        horizon='365 days'    
    )

    df_p = performance_metrics(df_cv, rolling_window=1)
    print(df_p[['horizon', 'mae', 'rmse', 'mape', 'coverage']].to_string(index=False))

    return df_cv, df_p