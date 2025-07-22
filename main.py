import os
from src.preprocessa import carregar_e_limpar
from src.comparacao import gerar_historico_dias_uteis
from src.grafico import plotar_vendas

def main():
    # Cria pastas de dados e saídas
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)
    os.makedirs('outputs', exist_ok=True)

    # Definição de caminhos
    raw = 'data/raw/total.csv'
    reduzido = 'data/processed/arquivo_reduzido.csv'
    mes_atual = 'data/processed/mes_atual.csv'
    historico = 'data/processed/historico_com_dias_uteis.csv'
    grafico = 'outputs/grafico_vendas.png'

    # Correção: agora passamos 3 argumentos para carregar_e_limpar
    carregar_e_limpar(raw, reduzido, mes_atual)

    gerar_historico_dias_uteis(reduzido, historico)
    plotar_vendas(historico, mes_atual, grafico)

if __name__ == '__main__':
    main()
