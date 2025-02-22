from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans
from sklearn.metrics import calinski_harabasz_score
from sklearn.metrics import silhouette_score
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk
from collections import Counter

def clusters_dbscan(eps, coordenadas):
    # Aplicar el algoritmo de clustering DBSCAN
    dbscan = DBSCAN(eps=eps, min_samples=50)
    return dbscan.fit_predict(coordenadas)

def clusters_kmeans(coordenadas):
    #optimal_k = indices_combinados(coordenadas)
    kmeans = KMeans(n_clusters=670, init='k-means++',random_state=42)
    clusters = kmeans.fit_predict(coordenadas)
    centroides = kmeans.cluster_centers_
    sil_score = silhouette_score(coordenadas, clusters)
    cal_score = calinski_harabasz_score(coordenadas, clusters)
    #print(f'Nº de clusters: 670\nSilhouette score: {sil_score}\nCalinski Score: {cal_score}')
    if sil_score < 0 or cal_score < 5000:
        optimal_k = indices_combinados(coordenadas)
        kmeans = KMeans(n_clusters=optimal_k, init='k-means++',random_state=42)
        clusters = kmeans.fit_predict(coordenadas)
        centroides = kmeans.cluster_centers_
        print(f'Nº de clusters: {optimal_k}\nSilhouette score: {sil_score}\nCalinski Score: {cal_score}')
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

    #graficar_resultados(k_values, silhouette_normalized, calinski_normalized, combined_scores)

    optimal_k = k_values[np.argmax(combined_scores)]
    print(optimal_k)
    return optimal_k

def graficar_resultados(k_values, silhouette_normalized, calinski_normalized, combined_scores):
    # Primero, grafiquemos los Silhouette y Calinski-Harabasz Scores en un gráfico
    fig1, ax1 = plt.subplots(figsize=(10, 6))

    # Graficar Silhouette Score
    ax1.plot(k_values, silhouette_normalized, marker='o', color='b', label='Silhouette Score', linestyle='-')
    ax1.set_xlabel('Número de Clusters')
    ax1.set_ylabel('Silhouette Score', color='b')
    ax1.tick_params(axis='y', labelcolor='b')

    # Crear el segundo eje Y para el Calinski-Harabasz Score
    ax2 = ax1.twinx()  # Crear el segundo eje Y
    ax2.plot(k_values, calinski_normalized, marker='o', color='r', label='Calinski-Harabasz Score', linestyle='-')
    ax2.set_ylabel('Calinski-Harabasz Score', color='r')
    ax2.tick_params(axis='y', labelcolor='r')

    # Títulos y leyenda
    ax1.set_title('Comparativa de Silhouette y Calinski-Harabasz Scores')
    fig1.tight_layout()  # Ajustar el layout para evitar superposición

    # Mostrar el gráfico
    plt.show()

    # Ahora, graficamos los Combined Scores en otro gráfico
    fig2, ax3 = plt.subplots(figsize=(10, 6))

    # Graficar Combined Scores
    ax3.plot(k_values, combined_scores, marker='o', color='g', label='Combined Score', linestyle='-')
    ax3.set_xlabel('Número de Clusters')
    ax3.set_ylabel('Combined Score', color='g')
    ax3.tick_params(axis='y', labelcolor='g')

    # Títulos y leyenda
    ax3.set_title('Comparativa de Combined Scores')
    fig2.tight_layout()  # Ajustar el layout para evitar superposición
    #ax3.legend(loc='upper left')

    # Mostrar el gráfico
    plt.show()
    print(k_values[np.argmax(silhouette_normalized)])
    print(k_values[np.argmax(calinski_normalized)])

"""
def recalcular_clusters(n_clusters, coordenadas):
    kmeans = KMeans(n_clusters=n_clusters.get(), init='k-means++',random_state=42)
    clusters = kmeans.fit_predict(coordenadas)
    centroides = kmeans.cluster_centers_
    return 

def indices_combinados(coordenadas, progress_bar=None, label=None, ventana=None):

    silhouette_scores = []
    calinski_scores = []
    
    k_values = range(500, 701)
    total_iteraciones = 200

    for i, k in enumerate(k_values):
        kmeans = KMeans(n_clusters=k, random_state=42)
        clusters = kmeans.fit_predict(coordenadas)
        
        silhouette = silhouette_score(coordenadas, clusters)
        silhouette_scores.append(silhouette)
        
        calinski_score = calinski_harabasz_score(coordenadas, clusters)
        calinski_scores.append(calinski_score)

        progreso = int(((i + 1) / total_iteraciones) * 100)
        progress_bar["value"] = progreso
        label.config(text=f"Progreso: {progreso}%")
        ventana.update_idletasks()

    silhouette_normalized = 10 * (np.array(silhouette_scores) - np.min(silhouette_scores)) / (np.max(silhouette_scores) - np.min(silhouette_scores))
    calinski_normalized = 10 * (np.array(calinski_scores) - np.min(calinski_scores)) / (np.max(calinski_scores) - np.min(calinski_scores))
    combined_scores = (0.5*silhouette_normalized + 0.5*calinski_normalized)

    #graficar_resultados(k_values, silhouette_normalized, calinski_normalized, combined_scores)

    optimal_k = k_values[np.argmax(combined_scores)]
    print(optimal_k)
    n_clusters.set(optimal_k)
    return optimal_k

def recalcular_n_clusters(coordenadas):
    ventana = Toplevel()
    ventana.title("Proceso en ejecución")
    ventana.geometry("300x150")
    ventana.resizable(False, False)
    ventana.protocol("WM_DELETE_WINDOW", lambda: None)

    label = Label(ventana, text="Iniciando proceso...", font=("Arial", 12))
    label.pack(pady=10)

    progress_bar = ttk.Progressbar(ventana, length=250, mode="determinate")
    progress_bar.pack(pady=10)
    
    # Ejecutar el proceso en segundo plano
    ventana.after(100, lambda: indices_combinados(coordenadas, progress_bar, label, ventana))"""