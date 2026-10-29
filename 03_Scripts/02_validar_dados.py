#!/usr/bin/env python3
"""Valida integridade básica dos CSVs tratados do NexoCommerce Analytics."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "01_Dados"
TRAT = DATA / "02_Tratados"
DOC = ROOT / "04_Documentacao"
DOC.mkdir(parents=True, exist_ok=True)

TABELAS = {
    "clientes.csv": ["id_cliente"],
    "entregas.csv": ["id_entrega"],
    "itens_pedido.csv": ["id_item"],
    "pagamentos.csv": ["id_pagamento"],
    "pedidos.csv": ["id_pedido"],
    "produtos.csv": ["id_produto"],
    "vendedores.csv": ["id_vendedor"],
}

def linha(verificacao, resultado, detalhes):
    return {"verificacao": verificacao, "resultado": resultado, "detalhes": str(detalhes)}

def main():
    dados = {}
    relatorio = []
    for arquivo, chaves in TABELAS.items():
        caminho = TRAT / arquivo
        if not caminho.exists():
            relatorio.append(linha(f"{arquivo}: arquivo", "ERRO", "arquivo ausente"))
            continue
        df = pd.read_csv(caminho, encoding="utf-8-sig")
        dados[arquivo] = df
        relatorio.append(linha(f"{arquivo}: registros", "OK", len(df)))
        duplicadas = int(df.duplicated().sum())
        relatorio.append(linha(f"{arquivo}: linhas duplicadas", "OK" if duplicadas == 0 else "ERRO", duplicadas))
        nulos = int(df.isna().sum().sum())
        relatorio.append(linha(f"{arquivo}: células nulas", "OK" if nulos == 0 else "ATENÇÃO", nulos))
        for chave in chaves:
            if chave in df:
                n = int(df[chave].duplicated().sum())
                relatorio.append(linha(f"{arquivo}: chave {chave} única", "OK" if n == 0 else "ERRO", f"duplicados: {n}"))

    def checar_relacao(nome, df_filho, col_filho, df_pai, col_pai):
        orfaos = set(df_filho[col_filho].dropna()) - set(df_pai[col_pai].dropna())
        relatorio.append(linha(nome, "OK" if not orfaos else "ERRO", f"órfãos: {len(orfaos)}"))

    if all(n in dados for n in ["itens_pedido.csv", "pedidos.csv", "produtos.csv", "clientes.csv", "vendedores.csv", "pagamentos.csv", "entregas.csv"]):
        checar_relacao("Chaves de pedidos em itens", dados["itens_pedido.csv"], "id_pedido", dados["pedidos.csv"], "id_pedido")
        checar_relacao("Chaves de produtos em itens", dados["itens_pedido.csv"], "id_produto", dados["produtos.csv"], "id_produto")
        checar_relacao("Chaves de clientes em pedidos", dados["pedidos.csv"], "id_cliente", dados["clientes.csv"], "id_cliente")
        checar_relacao("Chaves de vendedores em pedidos", dados["pedidos.csv"], "id_vendedor", dados["vendedores.csv"], "id_vendedor")
        checar_relacao("Chaves de pedidos em pagamentos", dados["pagamentos.csv"], "id_pedido", dados["pedidos.csv"], "id_pedido")
        checar_relacao("Chaves de pedidos em entregas", dados["entregas.csv"], "id_pedido", dados["pedidos.csv"], "id_pedido")
        itens=dados["itens_pedido.csv"]
        calc=(itens["quantidade"]*itens["preco_unitario"]*(1-itens["desconto"])).round(2)
        dif=(calc-itens["valor_item"].round(2)).abs()
        relatorio.append(linha("Valor dos itens", "OK" if (dif<0.011).all() else "ERRO", f"divergências: {int((dif>=0.011).sum())}"))
        desc=itens["desconto"]
        relatorio.append(linha("Descontos entre 0 e 1", "OK" if desc.between(0,1).all() else "ERRO", f"mínimo {desc.min()}, máximo {desc.max()}"))
        pos=(itens["quantidade"].gt(0)&itens["preco_unitario"].gt(0)&itens["valor_item"].gt(0)).all()
        relatorio.append(linha("Quantidade e valores positivos", "OK" if pos else "ERRO", "quantidade, preço unitário e valor do item"))
        entregas=dados["entregas.csv"].copy()
        envio=pd.to_datetime(entregas["data_envio"],errors="coerce")
        prevista=pd.to_datetime(entregas["data_prevista"],errors="coerce")
        ruins=int((prevista<envio).sum())
        relatorio.append(linha("Data prevista não anterior ao envio", "OK" if ruins==0 else "ERRO", f"casos restantes: {ruins}"))
        produtos=dados["produtos.csv"]
        margem=int((produtos["preco_unitario"]<produtos["custo_unitario"]).sum())
        relatorio.append(linha("Preço de venda maior ou igual ao custo", "OK" if margem==0 else "ATENÇÃO", f"casos: {margem}"))
        # Validar reconciliação dos pagamentos com os itens da base sintética.
        total=itens.groupby("id_pedido")["valor_item"].sum()
        pagos=dados["pagamentos.csv"].set_index("id_pedido")["valor_pago"]
        comum=total.index.intersection(pagos.index)
        delta=(total.loc[comum]-pagos.loc[comum]).abs()
        relatorio.append(linha("Pagamento reconciliado com itens (regra sintética)", "OK" if (delta<0.011).all() else "ATENÇÃO", f"divergências: {int((delta>=0.011).sum())}"))

    df_rel=pd.DataFrame(relatorio)
    out=DOC/"relatorio_validacao.csv"
    df_rel.to_csv(out,index=False,encoding="utf-8-sig",lineterminator="\n")
    print(df_rel.to_string(index=False))
    print(f"\nRelatório salvo em: {out}")
    if (df_rel["resultado"]=="ERRO").any():
        raise SystemExit("Validação encontrou erros. Revise o relatório.")

if __name__ == "__main__":
    main()
