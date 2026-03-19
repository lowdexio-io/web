# LOWDEX.io

LOWDEX.io es una plataforma experimental y minimalista que integra juegos de la plataforma itch.io. Este proyecto ha sido optimizado y reestructurado para ofrecer una mejor experiencia de usuario, código mantenible y una integración real con APIs externas.

## Características Principales

- **Arquitectura Optimizada**: Separación clara de responsabilidades (HTML, CSS, JS).
- **Integración con itch.io**: Conexión real con la API de itch.io para mostrar juegos.
- **Proxy Backend**: Servidor Flask en Python que actúa como proxy para evitar problemas de CORS y proteger la API key de itch.io.
- **Sistema de Feedback**: Formulario de contacto integrado con Gmail (vía MCP) para que los usuarios puedan enviar sus comentarios directamente al correo de la plataforma.
- **Diseño Responsivo**: Interfaz minimalista que se adapta a diferentes tamaños de pantalla.

## Estructura del Proyecto

```
web/
├── index.html          # Estructura principal de la página
├── css/
│   └── style.css       # Estilos y diseño visual
├── js/
│   └── app.js          # Lógica del frontend y llamadas a la API local
├── api/
│   ├── server.py       # Servidor backend Flask (Proxy y Feedback)
│   └── itch_client.py  # Cliente para la API de itch.io
├── data/               # Almacenamiento local (ej. feedback de respaldo)
└── README.md           # Documentación del proyecto
```

## Requisitos Previos

Para ejecutar el servidor backend, necesitas tener instalado Python 3 y las siguientes dependencias:

```bash
pip install flask flask-cors requests
```

## Configuración

1. **API Key de itch.io**: Para obtener datos reales de tu cuenta de itch.io, debes configurar la variable de entorno `ITCH_API_KEY`.
   
   ```bash
   export ITCH_API_KEY="tu_api_key_aqui"
   ```
   
   *Nota: Si no se configura la API key, la plataforma funcionará en modo "fallback" mostrando datos de ejemplo.*

2. **MCP de Gmail**: El sistema de feedback utiliza el MCP de Gmail configurado en el entorno para enviar correos a `lowdex.io@gmail.com`.

## Ejecución

Para iniciar la plataforma, ejecuta el servidor backend:

```bash
python3 api/server.py
```

El servidor se iniciará en el puerto 5000 (por defecto) y servirá tanto la API como los archivos estáticos del frontend. Puedes acceder a la plataforma abriendo `http://localhost:5000` en tu navegador.

## Licencia

Este proyecto es de código abierto y está disponible bajo la Licencia MIT.
