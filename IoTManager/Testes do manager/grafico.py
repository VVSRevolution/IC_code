import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
from statistics import mode, median, mean


# Dicionário para armazenar os valores numéricos agrupados por número de barras
valores_agrupados = defaultdict(list)
valor_medio = defaultdict(list)

# Dicionário para armazenar os totais e contagens dos valores por caminho
totais_por_caminho = defaultdict(float)
contagens_por_caminho = defaultdict(int)

# Abrir o arquivo de texto em modo de leitura
with open('tempo2.txt', 'r') as arquivo:
    for linha in arquivo:
        linha = linha.strip()
        caminho, valor_str = linha.split(':')
        valor_numerico = float(valor_str)
        
        # Contar o número de barras no caminho
        numero_barras = caminho.count('/')
        
        # Adicionar o valor numérico ao grupo correto no dicionário
        valores_agrupados[numero_barras].append(valor_numerico)
        
        # Fazer a agregação dos valores por caminho
        totais_por_caminho[caminho] += valor_numerico
        contagens_por_caminho[caminho] += 1
#print(totais_por_caminho)
for caminho in totais_por_caminho:
    numero_barras = caminho.count('/')
    valor_medio[numero_barras].append(totais_por_caminho[caminho] / contagens_por_caminho[caminho])
print(valor_medio)

# Calcular os limites inferior e superior para cada grupo
limites_inferiores = []
limites_superiores = []
num_barras_lista = []
for num_barras, valores in valor_medio.items():
    limites_inferiores.append(np.min(valores))
    limites_superiores.append(np.max(valores))
    num_barras_lista.append(num_barras)

# Calcular a média, moda e mediana para cada grupo, considerando os valores agregados por caminho
medias = [mean(valores) for valores in valor_medio.values()]
modas = [mode(valores) if valores.count(mode(valores)) == 1 else None for valores in valor_medio.values()]
medianas = [median(valores) for valores in valor_medio.values()]



# Criar uma figura maior
plt.figure(figsize=(10, 10))
ax = plt.gca()

major_ticks = np.arange(0, 999, 10)
minor_ticks = np.arange(0, 999, 5)
ax.set_xticks(major_ticks)
ax.set_xticks(minor_ticks, minor=True)
ax.set_yticks(major_ticks)
ax.set_yticks(minor_ticks, minor=True)


# Criar o gráfico de preenchimento entre curvas
plt.fill_between(num_barras_lista, limites_inferiores, medias, color='blue', alpha=0.3)
plt.fill_between(num_barras_lista, medias, limites_superiores, color='blue', alpha=0.3)

# Adicionar a reta média
plt.plot(num_barras_lista, medias, color='blue', label='Reta Média')
#plt.plot(num_barras_lista, modas, color='green', label='Reta Moda')
plt.plot(num_barras_lista, medianas, color='red', label='Reta Mediana')


# Adicionar os pontos em todos os dados coletados com marcador "x"
for num_barras, valores in valor_medio.items():
    plt.scatter([num_barras] * len(valores), valores, color='black', marker='x', s=40)

# Definir graduações mais espaçadas no eixo x e y
plt.xticks(np.arange(min(num_barras_lista), max(num_barras_lista) + 1, 1))


# Ajustar o grid para ser menos chamativo
ax.grid(which='both', linestyle='-', linewidth=0.5, alpha=0.3)
ax.grid(which='minor', alpha=0.2)
ax.grid(which='major', alpha=0.5)

# Ajustar o tamanho da fonte para os rótulos dos ticks dos eixos
plt.xticks(fontsize=14) # Aumente o valor de fontsize conforme necessário
plt.yticks(fontsize=14) # Aumente o valor de fontsize conforme necessário

# Legendas e títulos
plt.xlabel('Altura da árvore',fontsize=14)
plt.ylabel('Tempo de resposta (ms)',fontsize=14)
#plt.title('Intervalo de Tempo de Resposta por Altura de uma Árvore Binaria',)
plt.legend(fontsize=14)
# Salvar o gráfico como imagem
plt.tight_layout()
plt.savefig('grafico.svg')

# Mostrar o gráfico na interface
plt.show()
