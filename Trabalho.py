import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image
import os

aba1, aba2 = st.tabs(['Dados de Produção','Quedas de Desempenho'])

with aba1:
    st.title('Dados de Produção')

#Caminho fixo do arquivo CSV
    Dados_csv = "C:/Users/Lívia/Downloads/Aula_Livia_Tarde 2-20251014T003205Z-1-001/Aula_Livia_Tarde 2/Dados_de_Produção.csv"

#Garantir que o arquivo exista
    if not os.path.exists(Dados_csv):
       df_inicial = pd.DataFrame(columns=['Data', 'Máquina', 'Turno', 'Peças Produzidas', 'Peças Defeituosas'])
       df_inicial.to_csv(Dados_csv, index=False)

# o CSV existente
    st.session_state.df = pd.read_csv(Dados_csv)

#Carregar arquivo
    Dados = st.sidebar.file_uploader('Carregar Arquivo')
    if Dados:
#Formulário
      with st.form('Novas entradas',  clear_on_submit=True):
    
       col1, col2, col3, col4 = st.columns(4)
     
       data = col1.date_input('Data:')
       maq = st.selectbox('Máquina:',options = ('M1','M2','M3','M4','M5','M6','M7','M8','M9','M10'), index=None, key='maq') 
       tur = col2.selectbox('Turno:', options = ('Manhã','Tarde','Noite'), index=None, key='tur')
       ppr = col3.number_input('Peças Produzidas:', min_value= 0, max_value= 500)   
       pde = col4.number_input('Peças Defeituosas:', min_value= 0, max_value= 500)

       bt1 = st.form_submit_button('Enviar')
    
#Ao enviar
      if bt1:
         novo = pd.DataFrame({'Data':[data],
            'Máquina':[maq],
            'Turno':[tur],
            'Peças Produzidas':[int (ppr)],
            'Peças Defeituosas':[int (pde)]})
    

        # Adiciona o novo registro ao arquivo existente
         df_existente = pd.read_csv(Dados_csv)
         df_atualizado = pd.concat([df_existente, novo], ignore_index=True)

        # Salva imediatamente no arquivo
         df_atualizado.to_csv(Dados_csv, index=False)

        # Atualiza o dataframe mostrado
         st.session_state.df = df_atualizado
         st.success('Registro adicionado com sucesso!')
         st.sidebar.dataframe(st.session_state.df)
    else:
        st.warning('Arquivo inexistente')     
with aba2:
 if Dados:
    st.title(':chart_with_downwards_trend: Quedas de Desempenho')
    df = st.session_state.df.copy()

    if not df.empty:
       #Calcular Eficiência
       df['Eficiência (%)'] = np.where(df['Peças Produzidas'] > 0,
                                       (df['Peças Produzidas'] - df['Peças Defeituosas']) / df['Peças Produzidas'] * 100,
                                       0)

       #Média de Produção por Máquina
       mq = df.groupby('Máquina')['Peças Produzidas'].mean().reset_index()
       st.subheader(':bar_chart: Média de Produção por Máquina')
       st.dataframe(mq)

       #Tabela de Eficiência
       st.subheader(':chart_with_upwards_trend: Eficiência Diária')
       st.dataframe(df[['Data', 'Máquina', 'Turno', 'Peças Produzidas', 'Peças Defeituosas', 'Eficiência (%)']])
       st.line_chart(df, x='Data', y='Eficiência (%)')

       #Alertas Automáticos
       st.subheader(':rotating_light: Alertas Automáticos')
       alertas = []

       for i, linha in df.iterrows(): #Percorre cada linha do DataFrame
           if linha['Eficiência (%)'] < 90:
               alertas.append(f":warning: Eficiência abaixo de 90% na {linha['Máquina']} em {linha['Data']} ({linha['Eficiência (%)']:.1f}%)")
           if linha['Peças Produzidas'] < 80:
               alertas.append(f":warning: Produção baixa na {linha['Máquina']} em {linha['Data']} ({linha['Peças Produzidas']} peças)")

       if alertas:
           for a in alertas:
               st.error(a)
       else:
           st.success(":white_check_mark: Nenhum alerta encontrado — produção estável.")
    else:
       st.info("Ainda não há dados para análise.")
 else:st.warning('Arquivo inexistente')