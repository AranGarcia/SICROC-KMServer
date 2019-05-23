"""
Módulo de cálculos de agrupaciones de coordenadas. El método principal es calcular_centros,
el cual utiliza el algoritmo K-Means para agrupar las denuncias en eventos que indican
robo de combustible.
"""

import math
import numpy as np

from sklearn.cluster import KMeans


def iter_coordenadas():
    """
    Función generadora que obtiene las coordenadas de la fuente de datos
    """
    # TODO: Esta función tomará las coordenadas de las fuentes de datos.
    with open('coords.txt') as f:
        lineas = f.readlines()

    for l in lineas:
        x, y = l.split(',')
        yield (float(x.strip()), float(y.strip()))


def calcular_centros(coords, cant_ini=1, radio_lim=30):
    coordenadas = np.array(coords)
    cant_agrup = cant_ini
    print('Iniciando KMeans con', cant_agrup, 'centros y', len(coordenadas), 'coordenadas.')
    while True:
        if cant_agrup > len(coordenadas):
            return []
        km = KMeans(
            init='k-means++',
            n_clusters=cant_agrup,
            random_state=0).fit(coordenadas)

        if _validar_modelo(km, coordenadas, radio_lim):
            # Stop iterating the number of clusters and
            # build the centers with their radiuses
            print('Cantida de clusters:', cant_agrup)
            break
        cant_agrup += 1

    print('Separando grupos')
    clusters = [[] for i in range(len(km.cluster_centers_))]
    # First separate instances by clusters
    for i,l in enumerate(km.labels_):
        clusters[l].append(coordenadas[i])
    # Then calculate minimum radius
    print('Calculando radios')
    centers = []
    for i, c in enumerate(clusters):
        maxdis = 0
        for coord in c:
            cordist = _dist(coord, km.cluster_centers_[i])
            maxdis = cordist if cordist > maxdis else maxdis
        centers.append([list(km.cluster_centers_[i]), maxdis])

    print('Algoritmo finalizado. Devolviendo centros.')
    return centers


def _validar_modelo(modelo, coord, radio_lim):
    centros = modelo.cluster_centers_
    for index_coord, index_centro in enumerate(modelo.predict(coord)):
        if _dist(coord[index_coord], centros[index_centro]) > radio_lim:
            return False

    return True


def _dist(p1, p2):
    return math.sqrt(((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2))


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    print("Probando kmeans...")

    coordenadas = np.array([c for c in iter_coordenadas()])
    centros = calcular_centros(coordenadas)
    print('KMeans listo')

    print(centros)
    cd_x = [c[0] for c in coordenadas]
    cd_y = [c[1] for c in coordenadas]

    ax = plt.gca()
    for c in centros:
        circle = plt.Circle(c[0], radius=c[1], color='r', alpha=0.5)
        ax.add_patch(circle)
    plt.plot(cd_x, cd_y, 'bo')
    plt.show()
