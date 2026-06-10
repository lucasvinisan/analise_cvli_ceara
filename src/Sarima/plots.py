import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.metrics import mean_absolute_error, mean_squared_error
import matplotlib.dates as mdates


#Definindo globalmente o style dos plots 
plt.style.use('grayscale') 

# |------------ Visualização do modelo sarima.py --------------------------|
def plotar_graficos_serie (df):
    
    #Criando uma figura com três linhas e uma coluna para plotar os três graficos em um só 
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12,8))

    #PLotando o gráfico com base no gênero 
    df[['F', 'M', 'CVLI']].plot(kind='line', ax=ax1)
    ax1.set_title('Quantidade')  
    ax1.set_xlabel(None)
    ax1.set_ylabel('Número de Casos')

    #PLotando o gráfico das valores observados na série
    df_cvli = df['CVLI'].plot(kind='line', ax=ax2)
    ax2.set_title('Homicidios no Estado do Ceará')
    ax2.set_xlabel(None)
    ax2.set_ylabel('Meses')

    #Ajustando lyout
    plt.tight_layout()
    plt.show()

# |------------ Visualização do modelo sarima.py --------------------------|
def plotar_validacao(test, forecast, df):
   
    fig, ax1 = plt.subplots(figsize=(12, 5))


    train = df['2014-01-01':'2024-12-01']['CVLI']
    
    train.plot(
        ax=ax1, color='black', style='-', linewidth=1, label="Histórico (CVLI)"
    )

    test.plot(
        ax=ax1, color='black', style='-', marker='o', linewidth=1, label="_nolegend_"
    )   

    forecast.plot(
        ax=ax1, color='red', style='--', marker='x', linewidth=1, label="Previsão"
    )

    ax1.axvline(pd.Timestamp('2024-01-01'), linestyle=':', linewidth=1.5, label='Início do Teste')
    
    # MAE: Média de erro absoluto 
    mae = mean_absolute_error(test, forecast)

    # RMSE: Penaliza erros maiores 
    rmse = np.sqrt(mean_squared_error(test, forecast))

    # MAPE: Erro percentual
    mape = np.mean(np.abs((test - forecast['CVLI']) / test)) * 100

    ax1.set_title(f'Sarima — Teste vs Previsão\nMAE: {mae:.1f}  |  MAPE: {mape:.1f}% | RMSE: {rmse:.1f}', fontsize=14, fontweight='bold')

    
    ax1.set_ylabel('CVLI')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    plt.tight_layout()
    plt.show()


def modelo_diagnostico(modelo): 
    modelo.plot_diagnostics(figsize=(10,8))
    plt.tight_layout()
    plt.show()

# |------------ Decompondo a Série a Temporal (ADITIVA) --------------------------|
def decomposicao_aditivo(df):

    decomposicao_serie = seasonal_decompose(df['CVLI'], model='additive', period=12)
    figure = decomposicao_serie.plot()
    figure.set_size_inches((12, 12))
    plt.tight_layout()
    plt.show()

# |------------ Decompondo a Série a Temporal (MULTIPLICATIVA) --------------------------|
def decomposicao_multplicativo(df):
    
    decomposicao_serie = seasonal_decompose(df['CVLI'], model='multiplicative', period=12)
    figure = decomposicao_serie.plot()
    figure.set_size_inches((12, 8))
    plt.tight_layout()
    plt.show()

# |------------ Comparação --------------------------|
def tabela_comparacao(test, forecast):
    comparativo = test.to_frame()
    comparativo['Previsao'] = forecast['CVLI']
    comparativo['Erro_Absoluto'] = (comparativo['CVLI'] - comparativo['Previsao']).abs()
    comparativo['Acerto_%'] = 100 - (comparativo['Erro_Absoluto'] / comparativo['CVLI'] * 100)
    print(comparativo)




def plotar_previsao_2026(df_2026):
    df_2026 = df_2026['2026-04-01':'2026-08-01']
    fig, ax = plt.subplots(figsize=(12, 5))

    datas = df_2026.index

    ax.plot(datas, df_2026['CVLI'], color='blue', marker='o', linewidth=1.5, label='Previsão')

    ax.fill_between(
        datas,
        df_2026['lower'],
        df_2026['upper'],
        alpha=0.1,
        color='blue',
        label='IC 90%'
    )

    for i, (_, row) in enumerate(df_2026.iterrows()):
        ax.annotate(
            f"{row['CVLI']}\n[{row['lower']}–{row['upper']}]",
            xy=(datas[i], row['CVLI']),
            xytext=(0, 14),
            textcoords='offset points',
            ha='center',
            fontsize=7,
            color='black',
            clip_on=False 
    )

    ax.set_ylim(bottom=0, top=df_2026['upper'].max() * 1.3)

    ax.set_title('Previsão CVLI (Sarima)', fontsize=14, fontweight='bold')
    ax.set_ylabel('CVLI')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b/%Y'))
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()



