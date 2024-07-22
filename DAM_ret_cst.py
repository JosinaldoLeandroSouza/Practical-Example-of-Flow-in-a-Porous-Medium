# -*- coding: utf-8 -*-
"""
Exemplo FLUID FLOW IN POROUS MEDIA - ELEMENTO TRIANGULAR CST
@author: Josinaldo Leandro de Souza
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

## 1 - PARAMETROS INICIAS 

Kx = 1e-10         # permeabilidade x
Ky = 1e-10         # permeabilidade y
t = 1              # espessura 

# tensor de permeabilidades
D = np.array([[Kx, 0], [0, Ky]])

# Indicacao da malha CST

# Carregar os dados de cada aba do arquivo Excel
arquivo_excel = 'D:/Python/01 - Script/Fluxo 2D/DAM_ret_cst.xlsx'
nome_aba = ['coord','conec']

# Coordenadas
coord = pd.read_excel(arquivo_excel,sheet_name=nome_aba[0],usecols=[0,1,2], skiprows=0,nrows=470,names=['NO','X','Y'])

# Conectividade
conec =pd.read_excel(arquivo_excel,sheet_name=nome_aba[1],usecols=[0,1,2,3], skiprows=0,nrows=838,names=['Elem','V1','V2','V3'])

## 2 - LOOP PARA CONSTRUÇÃO DA MATRIZ DOS ELEMENTOS E MATRIZ GLOBAL

nn = coord.shape[0] # Numero de nos
nel = conec.shape[0] # numero de Elementos
ngl = nn * 1 # Numero de Graus de Liberdade
 
KG = np.zeros((ngl, ngl)) # Criacao da matriz de rigidez

for i in range(nel):
    # Nos correspondentes
    no1 = conec.iloc[i, 1]
    no2 = conec.iloc[i, 2]
    no3 = conec.iloc[i, 3]
    
    # Coordenadas dos nos
    x1, y1 = coord.iloc[(no1-1),[1,2]]
    x2, y2 = coord.iloc[(no2-1),[1,2]]
    x3, y3 = coord.iloc[(no3-1),[1,2]]
    
    xx = np.array([x1, x2, x3])
    yy = np.array([y1, y2, y3])
    
    A = 0.5 * np.abs(np.dot(xx, np.roll(yy, 1)) - np.dot(yy, np.roll(xx, 1)))
    
    B = (1 / (2 * A)) * np.array([[y2 - y3, y3 - y1, y1 - y2],
                                  [x3 - x2, x1 - x3, x2 - x1]])
    
    Ke = np.dot(np.dot(B.T, D), B) * A * t
    
    gl = [no1-1, no2-1, no3-1]
    
    for j in range(3):
        for k in range(3):
            KG[gl[j-1], gl[k]] += Ke[j, k]
            

##  3 - Aplicando as Condições de Contorno

# nos com pressões prescritas
restric = np.array([ 1,  2, 3, 4, 6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
       20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79,
       80, 81, 82, 83, 84, 85, 86, 93, 94, 95, 96, 97, 98]) 
restric.sort()  # Ordenando o vetor restric

# Valores das pressoes nos nos
Pf = np.zeros(ngl) # Criacao do vetor 

# nos com pressoes conhecidas a montante)
pm = np.array([ 1, 12, 13, 14, 15, 16, 93, 94, 95, 96, 97, 98]) # Acao do empuxo de agua a montante
pm2 = np.array([ 2, 3, 4, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34 ]) # Acao da pressao da lamina de agua a montante

# nos com pressoes conhecidas no valor 0m (valores a jusante)
pj = np.array([ 6,  7,  8,  9, 10, 11, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86]) # Acao de agua a jusante

# Valores das pressoes Montante
for i in range(pm.shape[0]): 
    
    pos1 = pm[i]-1 # posição da carga
    # Coordenadas dos nos
    xx1, yy1 = coord.iloc[pos1,[1,2]]
    Pf[pos1] = 9810 * (10 - yy1) # carga em x
    
for i in range(pm2.shape[0]): 
    
    pos1a = pm2[i]-1# posição da carga
    Pf[pos1a] = 98100 # carga em x
        
for i in range(pj.shape[0]): 
    
    pos2 = pj[i]-1 # posição da carga 
    Pf[pos2] = 0 # carga igual a 0
    
## 4 - SOLUÇÃO DO SISTEMA DE EQUAÇÕES 

# vetor de forca do problema
F = np.zeros(ngl)

# vetor forca modificado considerando condicoes nao-homogeneas do problema
Fmod = F - np.dot(KG, Pf)

# eliminar linhas e colunas com restições
KGR = np.delete(KG, restric-1, axis=0)
KGR = np.delete(KGR, restric-1, axis=1)
FGR = np.delete(Fmod, restric-1)

# Solving the system of equations
sol = np.linalg.solve(KGR, FGR)

PFF = Pf.copy()

# Reunindo as informações do vetor sol no vetor Pf nas posições não prescritas
j = 0
for i in range(ngl):
    if i + 1 not in restric:
        PFF[i] = sol[j]
        j += 1

## 5 - Salvando os resultados e realização do Pós-processamento

# Exportando o vetor Pf para um arquivo de texto formatado aceitavel pelo GID
output_file = "DAM_2_ret_cst.res"

with open(output_file, "w") as file:
    file.write("GiD Post Results File 1.0\n\n")
    file.write('Result "Pressao" "Load Analysis" 1 Scalar OnNodes "Board elements"\n')
    file.write("Values\n")
    for i, value in enumerate(PFF, 1):
        file.write(f"    {i}    {value:.2f}\n")
    file.write("End Values\n")

print(f"Arquivo '{output_file}' exportado com sucesso.")