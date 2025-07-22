import pandas as pd
from pandas.tseries.offsets import CustomBusinessDay
from workalendar.america import Brazil

def gerar_historico_dias_uteis(arquivo_reduzido: str, historico_saida: str) -> None:
    """
    Lê o CSV reduzido, converte datas de forma unificada, gera sequência
    de dias úteis, preenche valores faltantes com Venda=0 e salva o histórico.

    - Detecta datas em ISO (YYYY-MM-DD) ou DD/MM/YYYY.
    - Salva saída em CSV com datas no formato YYYY-MM-DD.
    """
    # 1) Leitura sem parse automático
    df = pd.read_csv(arquivo_reduzido, sep=';')

    # 2) Conversão de 'Data' tentando ISO primeiro, depois dia/mês/ano
    def parse_date(s):
        for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
            try:
                return pd.to_datetime(s, format=fmt)
            except (ValueError, TypeError):
                continue
        # Se nenhum dos formatos bateu, levanta erro explícito
        raise ValueError(f"Formato de data não reconhecido: {s}")

    # Aplica a função linha a linha
    df['Data'] = df['Data'].apply(parse_date)

    # 3) Configura calendário de dias úteis para o Brasil
    cal = Brazil()
    cbd = CustomBusinessDay(calendar=cal)

    # 4) Determina o intervalo completo
    min_date = df['Data'].min()
    start = pd.Timestamp(year=min_date.year, month=min_date.month, day=1)
    max_date = df['Data'].max()
    end = pd.Timestamp(year=max_date.year, month=max_date.month, day=1) + pd.offsets.MonthEnd(0)

    # 5) Gera todas as datas úteis no intervalo
    all_dates = pd.date_range(start=start, end=end, freq=cbd)

    # 6) Preenche datas faltantes com Venda=0
    df_full = pd.DataFrame({'Data': all_dates})
    df = pd.merge(df_full, df, on='Data', how='left').fillna({'Venda': 0})

    # 7) Calcula colunas auxiliares
    df['Ano']     = df['Data'].dt.year
    df['Mes']     = df['Data'].dt.month
    df['DiaUtil'] = df.groupby(['Ano', 'Mes']).cumcount() + 1

    # 8) Salva em CSV com formato unificado ISO (YYYY-MM-DD)
    df.to_csv(historico_saida,
              sep=';',
              index=False,
              date_format='%Y-%m-%d')
    print(f"[OK] Histórico com dias úteis salvo em: {historico_saida}")
