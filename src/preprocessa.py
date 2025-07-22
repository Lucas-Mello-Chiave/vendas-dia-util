import pandas as pd

def carregar_e_limpar(caminho_entrada: str, caminho_saida: str, caminho_mes_atual: str) -> None:
    """
    Lê o CSV original, remove a última linha, mantém colunas Data, Dia, Venda,
    converte valores, separa vendas do mês atual e salva arquivos reduzidos.
    """
    # Carregar e remover última linha (sumário ou total)
    df = pd.read_csv(caminho_entrada, sep=';', header=None)
    df = df.iloc[:-1, :3]  # descarta última linha, mantém primeiras 3 colunas
    df.columns = ['Data', 'Dia', 'Venda']

    # Normalizar coluna Venda
    df['Venda'] = df['Venda'].str.replace('.', '', regex=False)
    df['Venda'] = df['Venda'].str.replace(',', '.', regex=False)
    df['Venda'] = df['Venda'].astype(float)

    # Determinar mês atual como último mês presente no arquivo
    df['Data'] = pd.to_datetime(df['Data'], dayfirst=True)
    ultimo_mes = df['Data'].dt.to_period('M').max()

    # Separar vendas do mês atual
    df_mes_atual = df[df['Data'].dt.to_period('M') == ultimo_mes]
    df_reduzido = df[df['Data'].dt.to_period('M') != ultimo_mes]

    # Salvar arquivos
    df_reduzido.to_csv(caminho_saida, sep=';', index=False)
    df_mes_atual.to_csv(caminho_mes_atual, sep=';', index=False)
    print(f"[OK] Arquivo reduzido salvo em: {caminho_saida}")
    print(f"[OK] Vendas do mês atual salvo em: {caminho_mes_atual}")