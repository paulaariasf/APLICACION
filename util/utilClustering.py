from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans
from sklearn.metrics import calinski_harabasz_score
from sklearn.metrics import silhouette_score
import numpy as np
import matplotlib.pyplot as plt

def clusters_dbscan(eps, coordenadas):
    # Aplicar el algoritmo de clustering DBSCAN
    dbscan = DBSCAN(eps=eps, min_samples=50)
    return dbscan.fit_predict(coordenadas)

def clusters_kmeans(coordenadas):
    optimal_k = indices_combinados(coordenadas)
    kmeans = KMeans(n_clusters=optimal_k, init='k-means++',random_state=42)
    clusters = kmeans.fit_predict(coordenadas)
    centroides = kmeans.cluster_centers_
    return clusters, centroides

def calinski_harabasz(coordenadas):
    scores = []

    #Primera pasada
    k_values = range(500, 700, 10)

    for k in k_values:
        kmeans = KMeans(n_clusters=k, init='k-means++', random_state=42)
        clusters = kmeans.fit_predict(coordenadas)
        score = calinski_harabasz_score(coordenadas, clusters)
        scores.append(score)

    optimal_k = k_values[np.argmax(scores)]
    print(f"El número óptimo de clusters es: {optimal_k}, con un calinksi-harabasz score de {max(scores)}")

    #Segunda pasada
    scores = []
    k_values = range(optimal_k - 30, optimal_k + 30)

    for k in k_values:
        kmeans = KMeans(n_clusters=k,init='k-means++', random_state=42)
        clusters = kmeans.fit_predict(coordenadas)
        score = calinski_harabasz_score(coordenadas, clusters)
        scores.append(score)

    # Obtener el valor óptimo de k
    optimal_k = k_values[np.argmax(scores)]
    print(f"El número óptimo de clusters es: {optimal_k}, con un calinksi-harabasz score de {max(scores)}")
    return optimal_k

def silhouette(coordenadas):
    scores = []
    
    #Primera pasada
    k_values = range(500, 700, 10)

    for k in k_values:
        kmeans = KMeans(n_clusters=k, random_state=42)
        clusters = kmeans.fit_predict(coordenadas)
        score = silhouette_score(coordenadas, clusters)
        scores.append(score)

    optimal_k = k_values[np.argmax(scores)]
    print(f"El número óptimo de clusters es: {optimal_k}, con un silhouette score de {max(scores)}")

    #Segunda pasada
    scores = []
    k_values = range(optimal_k - 30, optimal_k + 30)

    for k in k_values:
        kmeans = KMeans(n_clusters=k, random_state=42)
        clusters = kmeans.fit_predict(coordenadas)
        score = silhouette_score(coordenadas, clusters)
        scores.append(score)

    # Obtener el valor óptimo de k
    optimal_k = k_values[np.argmax(scores)]
    print(f"El número óptimo de clusters es: {optimal_k}, con un silhouette score de {max(scores)}")

    return optimal_k

def indices_combinados(coordenadas):
    silhouette_scores = []
    calinski_scores = []
    
    k_values = range(500, 700)

    for k in k_values:
        kmeans = KMeans(n_clusters=k, random_state=42)
        clusters = kmeans.fit_predict(coordenadas)
        
        silhouette = silhouette_score(coordenadas, clusters)
        silhouette_scores.append(silhouette)
        
        calinski_score = calinski_harabasz_score(coordenadas, clusters)
        calinski_scores.append(calinski_score)

    silhouette_normalized = 10 * (np.array(silhouette_scores) - np.min(silhouette_scores)) / (np.max(silhouette_scores) - np.min(silhouette_scores))
    calinski_normalized = 10 * (np.array(calinski_scores) - np.min(calinski_scores)) / (np.max(calinski_scores) - np.min(calinski_scores))
    combined_scores = (0.5*silhouette_normalized + 0.5*calinski_normalized)

    """
    fig, ax1 = plt.subplots(figsize=(10, 6))

    ax1.plot(k_values, silhouette_normalized, marker='o', color='b', label='Silhouette Score', linestyle='-')
    ax1.set_xlabel('Número de Clusters')
    ax1.set_ylabel('Silhouette Score', color='b')
    ax1.tick_params(axis='y', labelcolor='b')

    ax2 = ax1.twinx()  # Crear el segundo eje Y
    ax2.plot(k_values, calinski_normalized, marker='o', color='r', label='Calinski-Harabasz Score', linestyle='-')
    ax2.set_ylabel('Calinski-Harabasz Score', color='r')
    ax2.tick_params(axis='y', labelcolor='r')

    ax1.plot(k_values, combined_scores, marker='o', color='g', label='Combined Score', linestyle='-')

    # Títulos y leyenda
    plt.title('Comparativa de Silhouette, Calinski-Harabasz y Combined Scores')
    fig.tight_layout()  # Ajustar el layout para evitar superposición
    plt.legend(loc='upper left')

    plt.show()"""

    optimal_k = k_values[np.argmax(combined_scores)]
    print(optimal_k)
    return optimal_k