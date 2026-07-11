# AgriScan AI 🌾📸

**AgriScan AI** es un sistema inteligente orientado a la detección temprana de enfermedades en cultivos agrícolas mediante el análisis de imágenes de hojas y áreas afectadas. Utiliza modelos avanzados de Visión por Computadora y Deep Learning para procesar y diagnosticar patologías de forma automatizada con alta precisión, ayudando a optimizar el rendimiento y la sostenibilidad en el sector agrícola.

---

## 📝 Descripción General del Proyecto

El sistema está diseñado para procesar fotografías de hojas capturadas por drones o dispositivos móviles, identificando patrones visuales asociados a enfermedades específicas en plantas. A través de modelos de clasificación entrenados con miles de imágenes agrícolas, diagnostica patologías de forma automatizada y con alta precisión.

## 🚀 Problema que Resuelve

Las enfermedades en cultivos representan una de las principales causas de pérdidas agrícolas a nivel mundial, impactando negativamente la seguridad alimentaria y la economía de los agricultores. Los problemas clave que aborda esta solución son:
* **Diagnósticos Tardíos:** La detección a tiempo previene la propagación masiva de patologías en grandes campos de cultivo.
* **Dependencia de Especialistas:** Evita la demora y los altos costos asociados con inspecciones manuales y la disponibilidad limitada de agrónomos en regiones remotas.
* **Uso Ineficiente de Agroquímicos:** Al identificar con precisión la enfermedad exacta, permite aplicar tratamientos específicos en lugar de pesticidas genéricos de amplio espectro, reduciendo el impacto ambiental y los costos de producción.

---

## 🛠️ Stack Tecnológico

El proyecto está estructurado con una arquitectura desacoplada y dockerizada para facilitar su despliegue y desarrollo:

* **Frontend:**
  * **React** + **Vite** (Interfaz dinámica y de alto rendimiento).
  * **Vanilla CSS** con diseño responsivo y moderno (interfaz premium).
  * **Nginx** (Servidor web para servir la compilación estática en contenedores).
* **Backend:**
  * **FastAPI** (Framework moderno de Python, rápido y asíncrono para la API REST).
  * **Uvicorn** (Servidor ASGI de alta velocidad).
  * **TensorFlow / Keras** (Carga del modelo de Machine Learning y ejecución de predicciones).
  * **OpenCV & Pillow** (Procesamiento y manipulación digital de imágenes).
  * **NumPy** (Operaciones matriciales rápidas).
* **Infraestructura:**
  * **Docker & Docker Compose** (Orquestación del backend y frontend de manera aislada y consistente).

---

## 🧠 Arquitectura del Modelo

El modelo utiliza la técnica de *Transfer Learning* (Aprendizaje por Transferencia) usando como base (**Backbone**) la arquitectura **EfficientNetB0** preentrenada en ImageNet, soldada a un cabezal clasificador a la medida.

### Parte 1: Capas del Modelo Principal

El esqueleto general del modelo está estructurado de la siguiente manera:

* **0: `input_layer_1` (InputLayer):** Es la puerta de entrada. Recibe la imagen de la hoja redimensionada a **224x224 píxeles** con sus 3 canales de color (RGB).
* **1: `efficientnetb0` (Functional):** El **Backbone** (el experto de Google). Keras lo empaqueta como una sola capa gigante de tipo funcional, pero por dentro aloja las **238 capas originales** preentrenadas.
* **2 al 6: El Cabezal Clasificador (Especialistas):**
  * **2: `global_average_pooling2d` (GlobalAveragePooling2D):** El "resumidor" que aplasta y reduce las dimensiones tridimensionales de las características a un vector de características unidimensional.
  * **3: `dropout` (Dropout):** El primer interruptor de regularización, configurado para apagar aleatoriamente el **30%** de las conexiones durante el entrenamiento y así evitar el sobreajuste (overfitting).
  * **4: `dense` (Dense):** Capa densa intermedia con **128 neuronas** y función de activación **ReLU** para aprender patrones y combinaciones no lineales.
  * **5: `dropout_1` (Dropout):** Segundo interruptor de regularización, configurado para apagar aleatoriamente el **20%** de las conexiones.
  * **6: `dense_1` (Dense):** La capa de salida o "Juez Final" con **15 neuronas** (correspondiente a las clases/enfermedades a clasificar) y una activación **Softmax** que nos proporciona la distribución de probabilidad (porcentaje de confianza) de cada diagnóstico.

---

### Parte 2: Capas del Backbone (Últimas 10)

Al extraer el Backbone (`modelo.get_layer('efficientnetb0')`), se exponen las últimas 10 capas de EfficientNetB0. Estas capas son críticas durante la fase de **Fine-tuning** (ajuste fino), ya que fueron descongeladas para adaptarse y especializarse en los detalles finos y texturas de las hojas.

Se dividen en dos grupos lógicos principales:

#### 1. El Bloque de Atención Visual (`block7a_se_...`)
El término **SE** hace referencia a **Squeeze-and-Excitation** (Compresión y Excitación), un mecanismo de atención que obliga al modelo a resaltar características útiles (como manchas y coloraciones anormales de enfermedades) e ignorar el fondo inútil de la foto (cielo, tierra, manos).

* **`block7a_se_squeeze` (GlobalAveragePooling2D):** Comprime las características espaciales en un único descriptor de canal para obtener el panorama general del contexto de la imagen.
* **`block7a_se_reshape` (Reshape):** Redimensiona el vector para que pueda ser procesado por capas de convolución.
* **`block7a_se_reduce` (Conv2D):** Una convolución que actúa como un cuello de botella, reduciendo el número de canales para extraer las relaciones más importantes y eficientes entre ellos.
* **`block7a_se_expand` (Conv2D):** Expande de nuevo los canales a la dimensión original, recreando los pesos que determinan la importancia de cada característica.
* **`block7a_se_excite` (Multiply):** Multiplica los pesos de importancia obtenidos por el mapa de características original. Esta capa "enciende" o "excita" los píxeles de las manchas clave de las enfermedades en la hoja.

#### 2. La Pulida Final (`top_...` y proyección)
Son la última parada de los datos dentro del Backbone antes de ser entregados al cabezal clasificador.

* **`block7a_project_conv` (Conv2D):** Proyecta la información del bloque final a un nuevo espacio de características.
* **`block7a_project_bn` (BatchNormalization):** Normaliza y estabiliza las salidas del bloque.
* **`top_conv` (Conv2D):** Capa convolucional final que extrae patrones hiper-complejos como la geometría exacta de las lesiones por hongos, bacterias o virus.
* **`top_bn` (BatchNormalization):** Normaliza las salidas matemáticas de `top_conv` para estabilizar el flujo de gradientes, asegurando que los valores no colapsen o exploten en magnitudes dispares y el entrenamiento sea óptimo.
* **`top_activation` (Activation):** Utiliza la función de activación **Swish** (una variante de ReLU adaptada por Google). Filtra las salidas dejando pasar únicamente las señales más intensas indicadoras de presencia patológica.

---

## 💻 Instrucciones para Ejecución Local

Puedes ejecutar la aplicación de dos formas: usando contenedores Docker (recomendado) o instalando y corriendo el Frontend y Backend localmente de forma manual.

### Opción 1: Ejecución con Docker Compose (Recomendada)

Asegúrate de tener instalados **Docker** y **Docker Compose**. Luego, sitúate en la raíz del proyecto (`agriscan-ai`) y ejecuta:

```bash
# Construir y levantar ambos servicios (Backend en puerto 8000, Frontend en puerto 3000)
docker compose up --build
```

Una vez levantado:
* **Frontend:** Accede a [http://localhost:3000](http://localhost:3000)
* **Backend API (Docs):** Accede a [http://localhost:8000/docs](http://localhost:8000/docs) para probar la API directamente.

---

### Opción 2: Ejecución Manual (Servidores Locales)

Si prefieres levantar los servicios de forma nativa sin contenedores, sigue estos pasos:

#### 1. Iniciar el Backend (FastAPI)

1. Abre una terminal y navega hasta el directorio del backend:
   ```bash
   cd backend
   ```
2. Crea un entorno virtual e instálalo (opcional pero recomendado):
   ```bash
   python -m venv venv
   # En Windows:
   .\venv\Scripts\activate
   # En macOS/Linux:
   source venv/bin/activate
   ```
3. Instala las dependencias requeridas:
   ```bash
   pip install -r requirements.txt
   ```
4. Inicia el servidor de desarrollo Uvicorn:
   ```bash
   uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
   ```
   *El backend estará disponible en `http://127.0.0.1:8000`.*

#### 2. Iniciar el Frontend (React + Vite)

1. Abre otra terminal y navega al directorio del frontend:
   ```bash
   cd frontend
   ```
2. Instala los paquetes de Node.js:
   ```bash
   npm install
   ```
3. Inicia el servidor de desarrollo de Vite:
   ```bash
   npm run dev
   ```
   *El frontend estará listo en el puerto que te indique la terminal (típicamente `http://localhost:5173` o el configurado).*
