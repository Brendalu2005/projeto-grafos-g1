import math

# Bellman-Ford (Vinícius)
def belman_ford(grafo, origem):

    distancia = {}

    for vertice in grafo:
        if (vertice.value == origem):
            distancia[vertice.value] == 0
        else:
            distancia[vertice.value] = math.inf

    num_vertices = 6 # ex 

    for i in range (num_vertices - 1):
        #ex
        vertice_inicial = origem