import pandas as pd 
from prophet import Prophet
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error

from src.prophet import modelo as md
from src.prophet import plots as grafico


def executar_prophet():
    
    df = pd.read_csv("dados/dados_previsoes_tratados_media.csv", index_col=0, parse_dates=True)

    df_prophet = df.reset_index().rename(columns={'MES': 'ds', 'CVLI': 'y'})
    
    #Criando o modelo a ser implmentado 
    modelo = md.criar_modelo(df_prophet)

    #Realizando a validação s
    previsao, test = md.validacao_modelo(modelo, df_prophet)

    grafico.plotar_validacao(df_prophet, previsao, test)

    modelo_final = modelo.fit(df_prophet)

    previsao = md.previsao_2026(modelo_final)

    grafico.plotar_previsao_2026(previsao)


'''

Verificar varios modelos

    from prophet.diagnostics import cross_validation, performance_metrics

    for cps in [0.10, 0.15, 0.20, 0.25, 0.30]:
        m = Prophet(
            seasonality_mode='multiplicative',
           interval_width=0.95,
           changepoint_prior_scale=cps,
            weekly_seasonality=False,
            daily_seasonality=False
        )
        m.fit(new_df)  # usa o dataframe completo
        df_cv = cross_validation(m, initial='1095 days', period='180 days', horizon='48 days')
       df_p = performance_metrics(df_cv)
       print(f"cps={cps:.2f} | MAPE={df_p['mape'].mean():.4f} | Coverage={df_p['coverage'].mean():.3f}")
    
  '''