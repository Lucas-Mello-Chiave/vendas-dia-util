# 📊 Monitoramento de Vendas Diárias por Dia Útil

Este projeto tem como objetivo gerar visualizações automáticas para análise diária de vendas ao longo do mês, considerando **apenas dias úteis**, com base em dados extraídos do sistema de vendas da empresa.

## 🗂 Estrutura do Projeto

```
├── main.py
├── src/
│   ├── preprocessa.py
│   ├── comparacao.py
│   └── grafico.py
├── data/
│   ├── raw/               # CSV bruto exportado do sistema
│   └── processed/         # Arquivos intermediários (limpos e com datas úteis)
├── outputs/               # Gráficos gerados
└── assets/
    └── logo.png           # (opcional) Logo da empresa usada no gráfico
```

---

## 🔄 Funcionamento Geral

1. **Pré-processamento (`preprocessa.py`)**

   * Lê o CSV original exportado do sistema.
   * Remove somatórios finais e converte os valores de vendas para float.
   * Separa as vendas do **mês atual** em um arquivo dedicado.

2. **Geração do histórico com dias úteis (`comparacao.py`)**

   * Cria uma sequência contínua de dias úteis com base no calendário brasileiro.
   * Preenche com `Venda=0` os dias úteis sem dados.
   * Adiciona colunas auxiliares (Ano, Mês, Dia Útil).

3. **Plotagem do gráfico (`grafico.py`)**

   * Compara as vendas do mês atual com a **média histórica diária**.
   * Projeta o valor total esperado até o fim do mês, com base na performance atual.
   * Gera um gráfico estético em fundo escuro, com variação percentual e comparativos visuais.

4. **Execução central (`main.py`)**

   * Orquestra todas as etapas anteriores.
   * Define os caminhos e organiza os diretórios.
   * Salva o gráfico final em `outputs/grafico_vendas.png`.

---

## 📥 Obtenção dos Dados

Para obter os dados de entrada, extraia o relatório do sistema da seguinte forma:

> **Movimento → Relatórios → Análise de Vendas → Acompanhamento de Vendas**
> ⚙️ **Filtro**: Ativar a opção **"Usar custo no momento da venda"**

Salve o arquivo em `.csv` e coloque-o em `data/raw/total.csv` antes de rodar o script.

---

## ▶️ Como Executar

Certifique-se de estar em um ambiente com Python 3.x e instale as dependências:

```bash
pip install pandas matplotlib workalendar
```

Em seguida, execute:

```bash
python main.py
```

O gráfico final estará disponível em: `outputs/grafico_vendas.png`

---

## 🧠 Observações Técnicas

* O projeto utiliza o calendário nacional brasileiro (via `workalendar`) para definir os dias úteis.
* O desempenho do mês é ajustado automaticamente com base na performance atual em relação à média histórica.
* O gráfico inclui uma projeção até o fim do mês, com anotações e variação percentual.
* Se o arquivo `assets/logo.png` estiver presente, a logo será inserida no canto superior do gráfico.

---

## 🔒 Uso Interno

Este repositório é de uso **exclusivamente interno**.
Não deve ser distribuído ou publicado fora dos ambientes autorizados pela empresa.

---
