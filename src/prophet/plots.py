
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np 
import matplotlib.dates as mdates
from sklearn.metrics import mean_absolute_error, mean_squared_error

#Definindo globalmente o style dos plots 
plt.style.use('grayscale') 

def plotar_previsao_2026(previsao_2026):
    fig, ax = plt.subplots(figsize=(12, 5))

    datas = pd.to_datetime(previsao_2026['ds'])

    ax.plot(datas, previsao_2026['yhat'], color='blue', marker='o', linewidth=1.5, label='Previsão')

    ax.fill_between(
        datas,
        previsao_2026['yhat_lower'],
        previsao_2026['yhat_upper'],
        alpha=0.1,
        color='blue',
        label='IC 90%'
    )

    for idx, row in previsao_2026.iterrows(): 
        ax.annotate(
            f"{row['yhat']}\n[{row['yhat_lower']}–{row['yhat_upper']}]",
            xy=(pd.to_datetime(row['ds']), row['yhat']),
            xytext=(0, 14),
            textcoords='offset points',
            ha='center',
            fontsize=8,
            color='black'
        )
    

    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

    ax.set_title('Previsão CVLI (Prophet)', fontsize=14, fontweight='bold')
    ax.set_xlabel('Mês')
    ax.set_ylabel('CVLI')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plotar_validacao(df_prophet, forecast, test):
    
    fig, ax = plt.subplots(figsize=(12, 5))
    
    ax.plot(df_prophet['ds'], df_prophet['y'], color='black', linewidth=1.5, label='Real')
    
    ax.plot(forecast['ds'], forecast['yhat'], color='red', linewidth=1.5, marker='x', label='Previsão')

    ax.axvline(pd.Timestamp('2024-01-01'), linestyle=':', linewidth=1.5, label='Início do Teste')

    # MAE: Média de erro absoluto 
    mae = mean_absolute_error(test['y'], forecast['yhat'])
    # RMSE: Penaliza erros maiores 
    rmse = np.sqrt(mean_squared_error(test['y'], forecast['yhat']))
    # MAPE: Erro percentual
    mape = np.mean(np.abs((test['y'].values - forecast['yhat'].values) / test['y'].values)) * 100

    ax.set_title(f'Prophet — Teste vs Previsão\nMAE: {mae:.1f}  |  MAPE: {mape:.1f}% | RMSE: {rmse:.1f}', fontsize=14, fontweight='bold')
    ax.set_ylabel('CVLI')
    ax.grid(True, alpha=0.3)
    ax.legend()
    plt.tight_layout()
    plt.show()