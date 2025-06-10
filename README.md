# Link My City

**Link My City** es una aplicación interactiva para la gestión, visualización y análisis de datos de movilidad urbana, centrada en el uso compartido de medios de transporte como bicicletas y patinetes. A través de una única interfaz basada en un mapa interactivo, permite a operadores del sistema explorar la ciudad, gestionar fuentes de datos y generar mapas de calor para evaluar cobertura y demanda de transporte.

## Características principales

- **Interfaz única y funcional** centrada en un mapa interactivo de la ciudad.
- **Panel lateral intuitivo** para gestionar todas las funcionalidades de forma sencilla.
- **Visualización personalizada** de estaciones, bicicletas y patinetes, tanto fijos en estaciones como flotantes.
- **Gestión de datos**: carga generación aleatoria e importación de archivos.
- **Mapas de calor** configurables para visualizar cobertura y demanda.
- **Simulación de demanda** y análisis visual de equilibrio entre oferta y solicitudes.


## Tecnologías utilizadas

- Python 3.12.1
- Librerías: `numpy`, `pandas`, `tkinter`, `tkintermapview`, `requests`, `scikit-learn`, `matplotlib`, `Pillow`
- OpenStreetMap + TkinterMapView para mapas
- FontAwesome como fuente para visualizar los iconos de la aplicación

## Instalación y puesta en marcha

Sigue los siguientes pasos para descargar e iniciar la aplicación en la máquina local:

### 1. Clonar el repositorio

Primero, hay que clonar el repositorio y asegurarse de estar en la rama `main`:

```bash
git clone https://github.com/paulaariasf/APLICACION.git
cd APLICACION
git checkout main
```

Es importante estar en la rama `main`, donde se encuentra la última versión estable.

### 2. Instalar la versión de Python 3.12.1 y las dependencias

Se recomienda crear un environment para la instalación de las librerías, de manera que se mantenga en un entorno controlado y separado del resto de librerías instaladas en su equipo.

- Instala la versión de Python 3.12.1 en el siguiente [link](https://www.python.org/downloads/release/python-3121/).

- Instala las librerías necesarias ejecutando:
```bash
pip install -r requirements.txt
```

- También puedes instalar manualmente las librerías necesarias:

```bash
pip install numpy pandas scikit-learn requests tkintermapview matplotlib Pillow
```

### 3. Instalar la fuente FontAwesome
Esta fuente se ha utilizado para la correcta visualización de los iconos en la aplicación. Para ello, deberá seguir los siguientes pasos:
- Descargar FontAwesome 6 Free for Desktop en el siguiente [enlace](https://fontawesome.com/v6/download)
- Descomprimir el zip descargado
- Instalar las fuentes haciendo clic en los archivos `.otf` de la carpeta `otfs` y haciendo clic en Instalar.
- (Opcional) Revisar la instalación de la fuente en Ajustes > Panel de Control > Apariencia y Personalización > Fuentes.

### 3. Ejecutar la aplicación

Finalmente, hay que lanzar la aplicación con:
```bash
python main.py
```
Esto abrirá la interfaz gráfica de Link My City, donde podrás visualizar el mapa, gestionar datos y generar mapas de calor interactivos.


## Estructura del proyecto
```
APLICACION/
│
├── 📄 main.py            # Archivo principal para ejecutar la aplicación
├── 📄 README.md          # Manual de usuario y guía de instalación
├── 📄 requirements.txt   # Lista de librerías necesarias
├── 📁 data/              # Carpeta para archivos JSON de estaciones, bicicletas, patinetes
├── 📁 imagenes/          # Imágenes, iconos y otros recursos gráficos
├── 📁 util/              # Archivos con funciones auxiliares que apoyan a la estructura de formularios
└── 📁 formularios/       # Páginas de la aplicación donde se encuentra la estructura principal de la interfaz
```

## Notas adicionales
- La aplicación requiere conexión a Internet para cargar los mapas de OpenStreetMap.

- Se pueden importar datos históricos o trabajar con datos simulados. Hay que tener en cuenta que los datos deben tener el formato adecuado.

- El sistema soporta actualización de estaciones fijas en tiempo real mediante APIs como BiciMAD.
- 
- La aplicación sólo podrá ser ejecutada en equipos con sistema operativo Windows, debido a la incompatibilidad de algunas de las librerías utilizadas en MacOS.


