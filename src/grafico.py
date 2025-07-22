import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from pandas.tseries.offsets import CustomBusinessDay
from workalendar.america import Brazil

# Cores
cor_fundo      = '#222222'
cor_texto      = '#FFFFFF'
cor_atual      = '#E67E22'
cor_projecao   = "#FFFFFF"
cor_media_hist = '#AAAAAA'
cor_corte      = '#E74C3C'
cor_annot      = '#F0F0F0'

def plotar_vendas(historico_csv: str, mes_atual_csv: str, saida_png: str) -> None:
    # --- Carregamento e preparação de dados ---
    df_historico = pd.read_csv(historico_csv, sep=';', decimal='.')
    df_atual     = pd.read_csv(mes_atual_csv, sep=';', decimal='.')
    df_historico['Data'] = pd.to_datetime(df_historico['Data'], format='%Y-%m-%d')
    df_historico['Ano']  = df_historico['Data'].dt.year
    df_historico['Mes']  = df_historico['Data'].dt.month
    df_historico = df_historico.sort_values('Data')
    df_historico['DiaUtil']   = df_historico.groupby(['Ano','Mes']).cumcount() + 1
    df_historico['Acumulado'] = df_historico.groupby(['Ano','Mes'])['Venda'].cumsum()

    df_atual['Data'] = pd.to_datetime(df_atual['Data'], format='%Y-%m-%d')
    df_atual['Ano']  = df_atual['Data'].dt.year
    df_atual['Mes']  = df_atual['Data'].dt.month
    df_atual = df_atual.sort_values('Data')
    df_atual['DiaUtil'] = df_atual.groupby(['Ano','Mes']).cumcount() + 1

    ultimo_dia_util = 22
    media_historica = (
        df_historico.groupby('DiaUtil')['Venda']
                    .mean()
                    .reset_index(name='Media_Historica')
    )
    media_historica = media_historica[media_historica['DiaUtil'] <= ultimo_dia_util]

    df_cmp = pd.merge(
        df_atual[['Data','DiaUtil','Venda']],
        media_historica, on='DiaUtil', how='left'
    )
    df_cmp['Acumulado'] = df_cmp['Venda'].cumsum()
    fator_perf = df_cmp['Venda'].sum() / df_cmp['Media_Historica'].sum()

    dias_futuros = list(range(df_cmp['DiaUtil'].max() + 1, ultimo_dia_util + 1))
    df_futuro = pd.DataFrame({'DiaUtil': dias_futuros}).merge(
        media_historica, on='DiaUtil', how='left'
    )
    df_futuro['Projecao_Ajustada']   = df_futuro['Media_Historica'] * fator_perf
    df_futuro['Acumulado_Projetado'] = df_cmp['Acumulado'].iloc[-1] + df_futuro['Projecao_Ajustada'].cumsum()

    # --- Criação do gráfico ---
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(14, 8))
    fig.patch.set_edgecolor('none')
    fig.patch.set_facecolor(cor_fundo)
    ax.set_facecolor(cor_fundo)
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Média Histórica
    ax.plot(media_historica['DiaUtil'],
            media_historica['Media_Historica'],
            'o-', color=cor_media_hist, alpha=0.6,
            linewidth=2, markersize=5, label='Média Diária Histórica'
    )

    # Vendas do mês atual
    mes_label = df_atual['Data'].dt.strftime('%b/%Y').iloc[0]
    ax.plot(df_cmp['DiaUtil'], df_cmp['Venda'],
            's-', color=cor_atual, linewidth=3, markersize=7,
            label=f'Vendas Diárias ({mes_label})'
    )

    # Projeção futura
    if dias_futuros:
        ultimo_real = df_cmp['DiaUtil'].max()
        proj_x = [ultimo_real] + dias_futuros
        proj_y = [df_cmp['Venda'].iloc[-1]] + df_futuro['Projecao_Ajustada'].tolist()
        ax.plot(proj_x, proj_y, '--',
                color=cor_projecao, linewidth=2.5, alpha=0.9,
                label=f'Projeção Diária ({fator_perf:.1%})'
        )

    # Estética dos eixos
    ax.get_yaxis().set_visible(False)
    ax.tick_params(axis='y', which='both', left=False, right=False, labelleft=False)
    ax.grid(False)
    ax.set_xticks(range(1, ultimo_dia_util + 1))
    ax.set_xlabel('Dia Útil do Mês', fontsize=12, color=cor_texto)
    ax.set_title('Vendas por Dia Útil',
                 fontsize=16, pad=20, color=cor_texto)

    # Linha de corte e anotação
    dia_atual = df_cmp['DiaUtil'].max()
    ax.axvline(x=dia_atual + 0.5, color=cor_corte, linestyle=':', alpha=0.7)
    ax.annotate(f'Dia atual: {dia_atual}',
                (dia_atual + 0.5, df_cmp['Venda'].max() * 1.05),
                ha='left', color=cor_corte, fontsize=10)

    # Anotações de valores
    for _, row in df_cmp.iterrows():
        ax.annotate(f'{row["Venda"]/1000:.0f}k',
                    (row['DiaUtil'], row['Venda']),
                    textcoords="offset points", xytext=(0, 10),
                    ha='center', fontsize=9, fontweight='bold', color=cor_annot)
    for _, row in df_futuro.iterrows():
        ax.annotate(f'{row["Projecao_Ajustada"]/1000:.0f}k',
                    (row['DiaUtil'], row['Projecao_Ajustada']),
                    textcoords="offset points", xytext=(0, 10),
                    ha='center', fontsize=9, fontweight='bold', color=cor_projecao)

    # --- Inserção da logo alinhada ao título (coordenadas da FIGURA) ---
    caminho_logo = 'assets/logo.png'
    if os.path.exists(caminho_logo):
        logo = mpimg.imread(caminho_logo)
        x0, y0 = 0.03, 0.87
        width = height = 0.14
        logo_ax = fig.add_axes([x0, y0, width, height],
                               transform=fig.transFigure,
                               zorder=10)
        logo_ax.imshow(logo)
        logo_ax.axis('off')

    # Legenda reposicionada
    ax.legend(loc='upper left',
              bbox_to_anchor=(0.01, 0.80),
              fontsize=10,
              frameon=False)

    # --- Quadro informativo com variação percentual ---
    media_total_hist = media_historica['Media_Historica'].sum()
    total_projetado = df_futuro['Acumulado_Projetado'].iloc[-1] if not df_futuro.empty else df_cmp['Acumulado'].iloc[-1]
    variacao_pct = (total_projetado / media_total_hist) * 100
    cor_diferenca = '#2ECC71' if variacao_pct >= 100 else '#E74C3C'

    texto_info = (
        f"Média histórica do mês: R$ {media_total_hist:,.0f}\n"
        f"Total projetado no mês: R$ {total_projetado:,.0f}\n"
        f"Variação: {variacao_pct:.1f}%"
    )
    props = dict(boxstyle='round,pad=0.5', facecolor=cor_fundo, edgecolor=cor_diferenca, linewidth=2)

    ax.text(0.97, 0.03, texto_info, transform=ax.transAxes,
            fontsize=10, verticalalignment='bottom', horizontalalignment='right',
            color=cor_texto, bbox=props)

    # Salvamento e exibição
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.12)
    plt.savefig(saida_png, dpi=300, facecolor=cor_fundo)
    plt.show()
