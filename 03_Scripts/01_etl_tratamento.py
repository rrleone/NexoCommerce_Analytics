#!/usr/bin/env python3
"""ETL reprodutível do projeto NexoCommerce Analytics.

Lê os arquivos *_clean.csv em 01_Dados/01_Originais, aplica regras documentadas,
gera os CSVs analíticos em 01_Dados/02_Tratados e preserva registros separados
na pasta 01_Dados/03_Quarentena.

Os nomes legíveis são enriquecimentos sintéticos armazenados em
mapeamentos_sinteticos.json; não representam pessoas ou empresas reais.
"""
from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "01_Dados"
ORIG = DATA / "01_Originais"
TRAT = DATA / "02_Tratados"
QUAR = DATA / "03_Quarentena"
MAP_FILE = Path(__file__).resolve().parent / "mapeamentos_sinteticos.json"

# Exceções identificadas durante a auditoria da base sintética.
PEDIDOS_EXCLUIR = {1097}  # pedido cancelado sem itens; pagamento/entrega relacionados ficam em quarentena
PAGAMENTOS_ORFAOS = {5200}
PAGAMENTOS_INCONSISTENTES = {5097}
ENTREGAS_ORFAS = {8200}
ENTREGAS_INCONSISTENTES = {8097}


def ler_csv(nome: str) -> pd.DataFrame:
    caminho = ORIG / nome
    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo de origem não encontrado: {caminho}")
    return pd.read_csv(caminho, encoding="utf-8-sig")


def aplicar_mapeamento(df: pd.DataFrame, tabela: str, chave: str, mapa: dict, colunas: list[str]) -> pd.DataFrame:
    df = df.copy()
    tabela_mapa = mapa[tabela]
    for coluna in colunas:
        df[coluna] = df[chave].map(
            {int(k): v.get(coluna) for k, v in tabela_mapa.items()}
        ).where(df[chave].isin([int(k) for k in tabela_mapa]), df[coluna])
    return df


def gravar(df: pd.DataFrame, pasta: Path, nome: str) -> None:
    pasta.mkdir(parents=True, exist_ok=True)
    df.to_csv(pasta / nome, index=False, encoding="utf-8-sig", lineterminator="\n")


def main() -> None:
    TRAT.mkdir(parents=True, exist_ok=True)
    QUAR.mkdir(parents=True, exist_ok=True)
    # Remover nome legado incorreto: o arquivo contém entregas, não pedidos.
    legado = QUAR / "pedidos_inconsistentes.csv"
    if legado.exists():
        legado.unlink()
    mapa = json.loads(MAP_FILE.read_text(encoding="utf-8"))

    clientes = ler_csv("clientes_clean.csv")
    entregas = ler_csv("entregas_clean.csv")
    itens = ler_csv("itens_pedido_clean.csv")
    pagamentos = ler_csv("pagamentos_clean.csv")
    pedidos = ler_csv("pedidos_clean.csv")
    produtos = ler_csv("produtos_clean.csv")
    vendedores = ler_csv("vendedores_clean.csv")

    # Enriquecimento com nomes sintéticos legíveis e normalização de valores ausentes.
    clientes = aplicar_mapeamento(clientes, "clientes", "id_cliente", mapa, ["nome_cliente"])
    produtos = aplicar_mapeamento(produtos, "produtos", "id_produto", mapa, ["produto", "categoria"])
    vendedores = aplicar_mapeamento(vendedores, "vendedores", "id_vendedor", mapa, ["nome_vendedor"])
    entregas = aplicar_mapeamento(entregas, "entregas", "id_entrega", mapa, ["transportadora"])
    pedidos["status_pedido"] = pedidos["status_pedido"].replace({"Não informado": "Não classificado"})
    pagamentos["forma_pagamento"] = pagamentos["forma_pagamento"].replace({"Não informado": "Não classificado"})
    entregas["status_entrega"] = entregas["status_entrega"].replace({"Não informado": "Não classificado"})

    # Ajustar o desconto inválido de 100% e recalcular o valor do item.
    itens["desconto"] = pd.to_numeric(itens["desconto"], errors="coerce")
    itens["quantidade"] = pd.to_numeric(itens["quantidade"], errors="coerce")
    itens["preco_unitario"] = pd.to_numeric(itens["preco_unitario"], errors="coerce")
    itens.loc[itens["desconto"] == 1, "desconto"] = 0.10
    itens["valor_item"] = (itens["quantidade"] * itens["preco_unitario"] * (1 - itens["desconto"])).round(2)

    # Quarentena e exclusão do pedido sem itens, cancelado, com pagamento aprovado e entrega marcada como entregue.
    pedidos = pedidos.loc[~pedidos["id_pedido"].isin(PEDIDOS_EXCLUIR)].copy()
    gravar(pagamentos.loc[pagamentos["id_pagamento"].isin(PAGAMENTOS_ORFAOS)], QUAR, "pagamentos_orfaos.csv")
    gravar(pagamentos.loc[pagamentos["id_pagamento"].isin(PAGAMENTOS_INCONSISTENTES)], QUAR, "pagamentos_inconsistentes.csv")
    gravar(entregas.loc[entregas["id_entrega"].isin(ENTREGAS_ORFAS)], QUAR, "entregas_orfas.csv")
    gravar(entregas.loc[entregas["id_entrega"].isin(ENTREGAS_INCONSISTENTES)], QUAR, "entregas_inconsistentes.csv")
    pagamentos = pagamentos.loc[~pagamentos["id_pagamento"].isin(PAGAMENTOS_ORFAOS | PAGAMENTOS_INCONSISTENTES)].copy()
    entregas = entregas.loc[~entregas["id_entrega"].isin(ENTREGAS_ORFAS | ENTREGAS_INCONSISTENTES)].copy()

    # Corrigir datas previstas anteriores ao envio: aplicar prazo padrão de sete dias.
    entregas["data_envio"] = pd.to_datetime(entregas["data_envio"], errors="coerce")
    entregas["data_prevista"] = pd.to_datetime(entregas["data_prevista"], errors="coerce")
    mascara_data = entregas["data_prevista"] < entregas["data_envio"]
    entregas.loc[mascara_data, "data_prevista"] = entregas.loc[mascara_data, "data_envio"] + pd.Timedelta(days=7)
    entregas["data_envio"] = entregas["data_envio"].dt.strftime("%Y-%m-%d")
    entregas["data_prevista"] = entregas["data_prevista"].dt.strftime("%Y-%m-%d")

    # Valores de pagamento reconstruídos a partir da soma dos itens de cada pedido.
    # Esta regra é própria desta base sintética, não comprova transações bancárias reais.
    totais_pedido = itens.groupby("id_pedido", as_index=False)["valor_item"].sum().rename(columns={"valor_item": "valor_pago_recalculado"})
    pagamentos = pagamentos.drop(columns=["valor_pago"]).merge(totais_pedido, on="id_pedido", how="left")
    pagamentos = pagamentos.rename(columns={"valor_pago_recalculado": "valor_pago"})
    pagamentos["valor_pago"] = pagamentos["valor_pago"].round(2)

    # Exportar os sete arquivos analíticos.
    for nome, df in [
        ("clientes.csv", clientes), ("entregas.csv", entregas),
        ("itens_pedido.csv", itens), ("pagamentos.csv", pagamentos),
        ("pedidos.csv", pedidos), ("produtos.csv", produtos),
        ("vendedores.csv", vendedores),
    ]:
        gravar(df, TRAT, nome)

    # Nota metodológica junto aos dados tratados.
    leia_me = """NEXOCOMMERCE ANALYTICS — DADOS TRATADOS\n\nOs CSVs desta pasta são saídas do script ../03_Scripts/01_etl_tratamento.py.\nOs nomes de clientes, produtos, vendedores e transportadoras são sintéticos.\n\nRegras principais:\n- normalização de valores não informados para 'Não classificado' nos campos de status/formas de pagamento;\n- correção do desconto de 100% para 10%, com recálculo do valor do item;\n- datas previstas anteriores ao envio ajustadas para data de envio + 7 dias;\n- valores pagos reconstruídos pela soma dos itens de cada pedido, exclusivamente para esta base sintética;\n- registros definidos como inconsistentes ou órfãos separados em 03_Quarentena.\n\nA base é sintética para treinamento. Valores de pagamento reconstruídos não devem ser interpretados como transações bancárias reais. Consulte 04_Documentacao/relatorio_validacao.csv após executar 02_validar_dados.py.\n"""
    (TRAT / "LEIA-ME.txt").write_text(leia_me, encoding="utf-8")
    print("ETL concluído.")
    for nome in sorted(p.name for p in TRAT.glob("*.csv")):
        df = pd.read_csv(TRAT / nome, encoding="utf-8-sig")
        print(f"- {nome}: {len(df):,} registros")

if __name__ == "__main__":
    main()
