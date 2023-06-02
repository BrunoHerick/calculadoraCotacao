# coding: utf-8 -*-
"""
    Fracionado -> entrega para vários clientes de uma só vez
    Dedicado -> entrega apenas para um cliente
"""
import numpy as np
import pandas as pd
import openpyxl as op
import streamlit as st

st.set_option('deprecation.showPyplotGlobalUse', False)
st.markdown(
    """
    <style>
        *, div, p, input, span, table, td, button, select, tr, .value {
            font-size: 25px;
            color: black;
        }
    </style>
    """,
    unsafe_allow_html=True
)
arquivo = pd.read_excel(
    "modelo_cotacao_calculo.xlsx",
    sheet_name="tabelaVeiculoCidade"
)
listaVeiculos = [x for x in arquivo["VEICULO"].drop_duplicates()]
listaCidadesDestino = [x for x in arquivo["CIDADE_DESTINO"].drop_duplicates()]

st.write("Calculadora de cotação")
auxiliar = arquivo
veiculoSelecionado = st.selectbox(
    label="Selecione o veículo: ",
    options=listaVeiculos
)
cidadeSelecionada = st.selectbox(
    label="Selecione a cidade de destino: ",
    options=listaCidadesDestino
)

auxiliar = auxiliar[
    auxiliar["VEICULO"] == veiculoSelecionado
]
auxiliar = auxiliar[
    auxiliar["CIDADE_DESTINO"] == cidadeSelecionada
]

distanciaPercorrer = st.number_input(
    label="Digite a distância a ser percorrida: ",
    min_value=0.0,
    step=1.0
)
nfValor = st.number_input(
    label="Digite o valor da nota fiscal: ",
    min_value=0.0,
    step=1.0
)
pesoCarga = st.number_input(
    label="Digite o peso da carga: ",
    min_value=0.0,
    step=1.0
)
st.write("==================== OPCIONAIS ====================")
valorAgregado = st.number_input(
    label="Digite o valor agregado (se não houver): ",
    value=arquivo.iloc[0]["VALOR"]*1.0,
    min_value=0.0,
    step=1.0
)
valorExcedente = st.number_input(
    label="Digite o valor do excedente (>100km): ",
    value=arquivo.iloc[0]["EXCEDENTE_100_KM"]*1.0,
    min_value=0.0,
    step=1.0
)
valorAjudante = st.number_input(
    label="Digite o valor do ajudante: ",
    value=arquivo.iloc[0]["AJUDANTE"]*1.0,
    min_value=0.0,
    step=1.0
)

valorPedagio = st.number_input(
    label="Digite o valor para o pedágio: ",
    value=0.0,
    min_value=0.0,
    step=1.0
)
valorPernoite = st.number_input(
    label="Digite o pernoite: ",
    value=arquivo.iloc[0]["PERNOITE"],
    min_value=0.0,
    step=1.0
)
st.write("===================================================")
valorMargem = st.number_input(
    label="Digite o valor da margem: ",
    value=1.35,
    min_value=1.0,
    step=0.05
)

botaoCalcular = st.button(
    label="Calcular"
)
st.write("======================= CUSTO =======================")

if botaoCalcular:
    valorExcedente = arquivo.iloc[0]["EXCEDENTE_100_KM"]
    valorFrete = ((distanciaPercorrer-100.0)*valorExcedente)+valorAgregado
    valorTotal = valorFrete + valorAjudante + valorPernoite + valorPedagio
    st.write("Valor do frete: R$ {:.2f}".format(valorFrete))
    st.write("Valor do ajudante: R$ {:.2f}".format(valorAjudante))
    st.write("Valor do pedágio: R$ {:.2f}".format(valorPedagio))
    st.write("Valor pernoite: R$ {:.2f}".format(valorPernoite))
    st.write("Valor Total: R$ {:.2f}".format(valorTotal))
    st.write("====================== RECEITA ======================")
    valorFreteReceita = (valorFrete*valorMargem)/0.9075
    valorAjudanteReceita = (valorAjudante*valorMargem)/0.9075
    valorPernoiteReceita = (valorPernoite*valorMargem)/0.9075
    seguro = nfValor * 0.0008
    valorTotalReceita = valorFreteReceita + valorAjudanteReceita + valorPedagio + valorPernoiteReceita + seguro
    st.write("Valor do frete: R$ {:.2f}".format(valorFreteReceita))
    st.write("Valor do ajudante: R$ {:.2f}".format(valorAjudanteReceita))
    st.write("Valor do pedágio: R$ {:.2f}".format(valorPedagio))
    st.write("Valor pernoite: R$ {:.2f}".format(valorPernoiteReceita))
    st.write("Seguro: R$ {:.2f}".format(seguro))
    st.write("Valor Total: R$ {:.2f}".format(valorTotalReceita))  
    st.write("=====================================================")
    margemPrincipal = (1 - (valorTotal/valorTotalReceita))*100
    margemCliente = (valorTotalReceita/nfValor)*100
    st.write("Margem: {:.2f} por cento".format(margemPrincipal))
    st.write("Margem do cliente: {:.2f} por cento".format(margemCliente))