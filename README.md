# Melodiam

Melodiam es una aplicación de código abierto para separar pistas de audio y generar partituras y tablaturas a partir de ellas, utilizando inteligencia artificial. El proyecto incluye:

- **Backend:** Desarrollado con Django, Django REST Framework y djangorestframework-simplejwt para autenticación JWT. Incluye medidas avanzadas de seguridad (HTTPS, django-axes, django-csp, etc.).
- **Frontend:** Aplicación web construida con React, Vite y TypeScript.
- **App Móvil:** Aplicación móvil desarrollada con React Native, Expo y TypeScript.
- **Procesamiento de Audio:** Utiliza Demucs y Torch para la separación de pistas, y Music21 para la generación de notación musical.

## Características

- **Deconstrucción de audio:** Separa automáticamente la pista de audio en componentes individuales.
- **Generación de partituras y tablaturas:** Convierte la información de audio procesada en notación musical.
- **Gestión de usuarios:** Registro, autenticación y administración de cuentas mediante JWT.
- **Medidas de seguridad:** HTTPS forzado, protección contra ataques de fuerza bruta con django-axes, Content Security Policy (CSP) y más.
