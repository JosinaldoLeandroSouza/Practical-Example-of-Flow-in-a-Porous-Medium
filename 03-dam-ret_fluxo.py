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
t = 10              # espessura 
gama_agua = 9810 # peso especifico da agua N/m3

# tensor de permeabilidades
D = np.array([[Kx, 0], [0, Ky]])

# Indicacao da malha CST

# Carregar os dados de cada aba do arquivo Excel
arquivo_excel = 'D:/Python/01 - Script/Mecanic 2D/03-dam-ret.xlsx'
nome_aba = ['coord','conec']

# Coordenadas
coord = pd.read_excel(arquivo_excel,sheet_name=nome_aba[0],usecols=[0,1,2], skiprows=0,nrows=6352,names=['NO','X','Y'])

# Conectividade
conec =pd.read_excel(arquivo_excel,sheet_name=nome_aba[1],usecols=[0,1,2,3], skiprows=0,nrows=12325,names=['Elem','V1','V2','V3'])

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
restric = np.array([4036,4091,4137,4188,4239,4291,4345,4397,4451,4502,4559,4612,
                    4670,4725,4783,4837,4896,4954,5013,5072,5131,5187,5242,5298,
                    5354,5407,5459,5511,5563,5612,5661,5708,5752,5797,5842,5883,
                    5921,5960,6001,6041,6080,4119,4204,4283,4370,4453,4531,4614,
                    4693,4774,4858,4938,5021,5100,5173,5251,5326,5394,5466,5530,
                    5598,5660,5719,5774,5830,5884,5935,5984,6030,6074,6120,6164,
                    6208,6249,6277,6300,6319,6331,6341,6348,6351,6216,6218,6219,
                    6220,6223,6226,6229,6231,6235,6239,6243,6246,6250,6253,6259,
                    6262,6268,6272,6275,6282,6286,6290,6295,6299,6304,6310,6313,
                    6317,6320,6326,6329,6332,6335,6339,6340,6344,6346,6347,6349,
                    6350,6351,1448,1451,1457,1462,1467,1474,1485,1498,1504,1524,
                    1536,1550,1567,1591,1608,1629,1652,1671,1701,1721,1750,1773,
                    1806,1833,1861,1893,1918,1952,1982,2011,2047,2081,2109,2146,
                    2181,2219,2249,2286,2326,2362,2398,2431,2472,2515,2558,2601,
                    2643,2691,2733,2786,2839,2891,2946,3004,3061,3121,3182,3242,
                    3307,3372,3441,3507,3579,3649,3721,3796,3876,3957,4037,4118,
                    4203,4284,4369,4454,4530,4613,4694,4773,4857,4939,5022 ]) 
restric.sort()  # Ordenando o vetor restric

# nos com pressoes conhecidas a montante)
pm = np.array([4036,4091,4137,4188,4239,4291,4345,4397,4451,4502,4559,4612,4670,
               4725,4783,4837,4896,4954,5013,5072,5131,5187,5242,5298,5354,5407,
               5459,5511,5563,5612,5661,5708,5752,5797,5842,5883,5921,5960,6001,
               6041,6080,4119,4204,4283,4370,4453,4531,4614,4693,4774,4858,4938,
               5021,5100,5173,5251,5326,5394,5466,5530,5598,5660,5719,5774,5830,
               5884,5935,5984,6030,6074,6120,6164,6208,6249,6277,6300,6319,6331,
               6341,6348,6351 ]) # Acao do empuxo de agua a montante
pm.sort() # Ordenando o vetor 
# Acao da pressao da lamina de agua a montante
pm2 = np.array([6216,6218,6219,6220,6223,6226,6229,6231,6235,6239,6243,6246,6250,
                6253,6259,6262,6268,6272,6275,6282,6286,6290,6295,6299,6304,6310,
                6313,6317,6320,6326,6329,6332,6335,6339,6340,6344,6346,6347,6349,
                6350,6351 ])
pm2.sort() # Ordenando o vetor

# nos com pressoes conhecidas no valor 0m (valores a jusante)
pj = np.array([1448,1451,1457,1462,1467,1474,1485,1498,1504,1524,1536,1550,1567,
               1591,1608,1629,1652,1671,1701,1721,1750,1773,1806,1833,1861,1893,
               1918,1952,1982,2011,2047,2081,2109,2146,2181,2219,2249,2286,2326,
               2362,2398,2431,2472,2515,2558,2601,2643,2691,2733,2786,2839,2891,
               2946,3004,3061,3121,3182,3242,3307,3372,3441,3507,3579,3649,3721,
               3796,3876,3957,4037,4118,4203,4284,4369,4454,4530,4613,4694,4773,
               4857,4939,5022 ]) # Acao de agua a jusante
pj.sort() # Ordenando o vetor 

## Encontrar a maior coordenada em Y dos pontos com pressao conhecida
ponto = np.zeros((pm.shape[0], 2))

for i in range(pm.shape[0]):
    # Número do nó correspondente
    no1 = pm[i]
    
    # Coordenadas do nó (usando iloc para indexação por posição)
    x1 = coord.iloc[no1-1, 1]  # Coordenada X
    y1 = coord.iloc[no1-1, 2]  # Coordenada Y
    
    # Armazena as coordenadas x1 e y1 no vetor 'ponto'
    ponto[i, 0] = x1
    ponto[i, 1] = y1

# Encontre o maior valor de coordenada x e y
maior_x = max(ponto, key=lambda ponto: ponto[0])[0]
maior_y = max(ponto, key=lambda ponto: ponto[1])[1]

# Valores da força devido o Empuxo de agua a montante
Femp_m = np.zeros(ngl) # Criacao do vetor 

# Valores das pressoes Montante
for i in range(pm.shape[0]): 
    
    pos1 = pm[i]-1 # posição da carga
    # Coordenadas dos nos
    xx1, yy1 = coord.iloc[pos1,[1,2]]
    Femp_m[pos1] = gama_agua *(maior_y - yy1) # carga em x

for i in range(pm2.shape[0]): 
    
    pos1a = pm2[i]-1# posição da carga
    Femp_m[pos1a] = gama_agua *maior_y # carga em x

# Valores das pressoes Jusante        

# Valores da força devido o Empuxo de agua a montante
Femp_j = np.zeros(ngl) # Criacao do vetor 

for i in range(pj.shape[0]): 
    
    pos2 = pj[i]-1 # posição da carga 
    Femp_j[pos2] = 0 # carga igual a 0

# Vetor com a soma de todos os Valores das pressoes nos nos
Ff = Femp_m + Femp_j #Criacao do vetor 
    
## 4 - SOLUÇÃO DO SISTEMA DE EQUAÇÕES 

# vetor de forca do problema
F = np.zeros(ngl)

# vetor forca modificado considerando condicoes nao-homogeneas do problema
Fmod = F - np.dot(KG, Ff)

# eliminar linhas e colunas com restições
KGR = np.delete(KG, restric-1, axis=0)
KGR = np.delete(KGR, restric-1, axis=1)
FGR = np.delete(Fmod, restric-1)

# Solving the system of equations
sol = np.linalg.solve(KGR, FGR)

PFF = Ff.copy()

# Reunindo as informações do vetor sol no vetor Pf nas posições não prescritas
j = 0
for i in range(ngl):
    if i + 1 not in restric:
        PFF[i] = sol[j]
        j += 1

# Adiciona uma coluna com o número dos nós
output = np.column_stack((np.arange(1, nn + 1), PFF))


# Colocando o valor da Pressao Nodal em cada elemento
Pressao_elemento = np.zeros( nel)

for i in range(nel):
    # Nós correspondentes ao elemento
    no1 = conec.iloc[i, 1]
    no2 = conec.iloc[i, 2]
    no3 = conec.iloc[i, 3]
    
    # Recupera deslocamentos associados aos nós do elemento
    pos = np.array([no1-1, no2-1, no3-1])
    elemento = PFF[pos]
  
    # Tensões nos elementos (detalhada no capítulo 6 - Logan)
    Pressao_elemento[i] = np.sum(elemento) / 3
# Gera uma coluna com o número dos elementos
element_numbers = np.arange(1, nel + 1).reshape(nel, 1)

# Concatena os números dos elementos com as tensões
output2 =  np.column_stack((np.arange(1, nel + 1,dtype=int), Pressao_elemento))


## 5 - Salvando os resultados e realização do Pós-processamento

# Exportando o vetor Pf para um arquivo de texto formatado aceitavel pelo GID
output_file = "03-dam-ret_fluxo.res"

with open(output_file, "w") as file:
    file.write("GiD Post Results File 1.0\n\n")
    file.write('Result "Pressao nodal" "Load Analysis" 1 Scalar OnNodes "Board elements"\n')
    file.write("Values\n")
    
    # Escreve os valores em formato exponencial
    np.savetxt(file, output, delimiter='\t', fmt=['%d', '%.6e'])
    
    file.write("End Values\n")
    file.write("")
    
    # Escrever o cabeçalho para as prensoes nos elemento
    file.write('GaussPoints "Board elements" ElemType Triangle "board"\n')
    file.write('  Number Of Gauss Points: 1\n')
    file.write('  Natural Coordinates: internal\n')
    file.write('end gausspoints\n\n')
    file.write('Result "Pressao Elemento" "Load Analysis" 1 Scalar OnGaussPoints "Board elements"\n')
    file.write('ComponentNames "PoroPresure"\n')
    file.write('Values\n')
    
    # Escrever os valores de tensão para cada elemento
    # Escreve os valores em formato exponencial
    np.savetxt(file, output2, delimiter='\t', fmt=['%d', '%.6e'])
    
        # Escrever o rodapé
    file.write('End Values\n')

print(f"Arquivo '{output_file}' exportado com sucesso.")