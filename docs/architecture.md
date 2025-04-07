# Arquitectura del Proyecto Melodiam

Este documento describe la arquitectura del proyecto **Melodiam**, una aplicación para separar pistas de audio y generar partituras y tablaturas utilizando inteligencia artificial. El sistema se compone de varios módulos que interactúan para ofrecer funcionalidades tanto en la web como en dispositivos móviles.

---

## 1. Visión General

**Melodiam** permite a los usuarios:

- **Deconstruir canciones:** Separar pistas de audio (vocal, guitarra, bajo, etc.) mediante inteligencia artificial.
- **Generar notación musical:** Convertir los datos procesados en partituras y tablaturas.
- **Gestionar cuentas de usuario:** Registro, autenticación y almacenamiento de resultados mediante JWT.
- **Acceso Multiplataforma:** Interfaces web (React/Vite + TypeScript) y móvil (Expo/React Native + TypeScript).

---

## 2. Componentes del Sistema

### 2.1 Backend (Django)

- **Framework:** Django 4.2
- **API:** Django REST Framework, configurado con endpoints para:
  - Procesamiento de audio (público).
  - Gestión y almacenamiento de resultados (protegido, requiere autenticación).
  - Gestión de usuarios (registro y autenticación con JWT).
- **Autenticación:** djangorestframework-simplejwt.
- **Seguridad:**
  - Medidas de seguridad (HTTPS, HSTS, cabeceras seguras).
  - Protección contra ataques de fuerza bruta (django-axes).
  - Política de seguridad de contenido (CSP con django-csp).
- **Variables de entorno:** Administradas mediante python-decouple y archivo `.env`.

### 2.2 Procesamiento de Audio

- **Modelo de separación:** Demucs (compatible con Python 3.11 y Torch).
- **Conversión de Notación:** Music21 para transformar datos de audio/MIDI en partituras y tablaturas.
- **Ejecución:** Se invoca desde el backend mediante llamadas a la línea de comandos (subprocess).

### 2.3 Frontend Web

- **Framework:** React con Vite y TypeScript.
- **Funcionalidad:**
  - Interfaz para subir canciones y visualizar resultados.
  - Consumo de la API REST del backend.
  - Gestión de autenticación y token JWT.

### 2.4 Aplicación Móvil

- **Plataforma:** Expo y React Native (con TypeScript).
- **Funcionalidad:** Similar a la web, adaptada para dispositivos móviles, permitiendo el registro, subida de audio y visualización de resultados.

---

## 3. Detalles de la Arquitectura

### 3.1 Backend (Django)

- **Framework:** Django 4.2
- **API REST:** Implementada con Django REST Framework, con endpoints públicos y protegidos.
- **Autenticación:** JWT utilizando `djangorestframework-simplejwt`.
- **Seguridad:**
  - HTTPS, HSTS y cabeceras seguras configuradas en `settings.py`.
  - Protección contra ataques de fuerza bruta con django-axes.
  - Content Security Policy (CSP) mediante django-csp.
- **Variables de entorno:** Administradas con python-decouple y archivo `.env`.

### 3.2 Procesamiento de Audio

- **Herramienta de separación:** Se utiliza **Demucs** junto con PyTorch para separar las pistas de audio.
- **Conversión a Notación:** Music21 convierte datos (por ejemplo, MIDI) en partituras y tablaturas.
- **Integración:** El backend invoca a Demucs mediante el módulo `subprocess` para ejecutar la separación de pistas.

### 3.3 Gestión de Usuarios

- **Registro y Autenticación:**
  - La app de usuarios, ubicada en `apps/users/`, provee endpoints para el registro y la autenticación.
  - Se usa el modelo de usuario por defecto de Django y se crean serializadores personalizados.
- **Endpoints JWT:**
  - Los endpoints para obtener y refrescar tokens están configurados en `config/urls.py` con `djangorestframework-simplejwt`.

### 3.4 Frontend y Aplicación Móvil

- **Frontend Web:**
  - Desarrollado en React con Vite y TypeScript, consume la API del backend para subir audio y mostrar resultados.
- **Aplicación Móvil:**
  - Construida con Expo y React Native (TypeScript), ofrece funcionalidades similares al frontend adaptadas para dispositivos móviles.

---

## 4. Flujo de Datos

1. **Subida y Procesamiento de Audio (Público):**

   - Un usuario envía un archivo de audio a través del endpoint `/api/deconstruct/`.
   - El backend guarda el archivo temporalmente y llama a Demucs para separar las pistas.
   - El resultado se devuelve en formato JSON sin requerir autenticación.

2. **Almacenamiento y Gestión (Protegido):**

   - Usuarios autenticados pueden almacenar y recuperar canciones procesadas mediante `/api/songs/`.
   - La autenticación se maneja mediante JWT.

3. **Registro y Autenticación de Usuarios:**
   - La app de usuarios en `apps/users/` ofrece el registro mediante `/api/users/register/`.
   - Los tokens JWT se obtienen y refrescan a través de los endpoints dedicados.

---

## 5. Consideraciones de Despliegue y Seguridad

- **Despliegue del Backend:**  
  Se recomienda usar un servidor WSGI (por ejemplo, Gunicorn) detrás de un proxy inverso (Nginx) para gestionar HTTPS y mejorar el rendimiento.
- **Base de Datos:**  
  Aunque en desarrollo se utiliza SQLite, en producción se recomienda PostgreSQL para mayor robustez y escalabilidad.
- **Procesamiento Asíncrono:**  
  Implementar Celery con Redis para manejar tareas intensivas de procesamiento de audio.
- **Medidas de Seguridad:**
  - HTTPS forzado, HSTS y cabeceras de seguridad.
  - Protección contra fuerza bruta y políticas CSP.
  - Gestión de variables sensibles a través de `.env` y python-decouple.

---

## 6. Conclusión

La arquitectura de **Melodiam** está diseñada para ofrecer una solución escalable y segura para el procesamiento de audio y generación de notación musical, permitiendo su uso tanto en entornos web como móviles. La separación en módulos facilita la escalabilidad, el mantenimiento y la incorporación de futuras mejoras.

Este documento sirve como guía para entender la estructura y el flujo de datos del proyecto, facilitando la incorporación de nuevos colaboradores y la evolución del sistema.
