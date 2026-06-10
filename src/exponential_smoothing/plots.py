import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.api import ExponentialSmoothing
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, mean_squared_error
import matplotlib.dates as mdates


#Definindo globalmente o style dos plots 
plt.style.use('grayscale') 

def plotar_validacao(df, test, forecast): 


    fig, ax1 = plt.subplots(figsize=(12, 5))

    # Série histórica completa (treino)
    train = df['2014-01-01':'2023-12-01']
    test_series = test['CVLI']

    
    ax1.plot(train.index, train['CVLI'], label='Treino', linewidth=1)

    # Valores reais do período de teste
    ax1.plot(test_series.index, test_series, label='Real (Teste)', color='black', linewidth=1, marker='o', markersize=4)

    # Previsão
    ax1.plot(test_series.index, forecast, label='Previsão', linewidth=1, linestyle='--',  color='red', marker='x', markersize=4)

    # Linha divisória treino/teste
    ax1.axvline(pd.Timestamp('2024-01-01'), linestyle=':', linewidth=1.5, label='Início do Teste')
    
    
    # MAE: Média de erro absoluto 
    mae = mean_absolute_error(test_series, forecast)

    # RMSE: Penaliza erros maiores 
    rmse = np.sqrt(mean_squared_error(test_series, forecast))

    # MAPE: Erro percentual
    mape = np.mean(np.abs((test_series - forecast) / test_series)) * 100

    ax1.set_title(f'Exponential Smoothing — Teste vs Previsão\nMAE: {mae:.1f}  |  MAPE: {mape:.1f}% | RMSE: {rmse:.1f}%', fontsize=14, fontweight='bold')

    ax1.set_ylabel('Ocorrências CVLI')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def plotar_previsao_2026(previsao):
    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(previsao.index.to_timestamp(), previsao['CVLI'],
            color='blue', marker='o', linewidth=1.5, label='Previsão')

    ax.fill_between(
        previsao.index.to_timestamp(),
        previsao['lower'],
        previsao['upper'],
        alpha=0.1,
        color='blue',
        label='IC 90%'
    )

    for idx, row in previsao.iterrows():
        ax.annotate(
            f"{row['CVLI']}\n[{row['lower']}–{row['upper']}]",
            xy=(idx.to_timestamp(), row['CVLI']),
            xytext=(0, 12),
            textcoords='offset points',
            ha='center',
            fontsize=8
        )


    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax.set_title('Previsão CVLI (Exponential Smoothing)', fontsize=14, fontweight='bold')

    ax.set_ylabel('CVLI')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()