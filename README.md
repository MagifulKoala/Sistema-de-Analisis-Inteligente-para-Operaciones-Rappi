# 🧠 Caso Técnico: Sistema de Análisis Inteligente para Operaciones Rappi

Este proyecto implementa un **Bot Conversacional de Datos** y un **Sistema de Insights Automáticos** basados en un conjunto de datos predeterminado.

---

## ⚙️ Tecnologías y Arquitectura

El proyecto fue desarrollado en **Python** y se ejecuta dentro de un entorno **Dockerizado**.
A continuación se resumen los principales componentes del sistema:

* **FastAPI** → Define los endpoints principales para interactuar con las funcionalidades del sistema.
* **Celery** → Administra la cola de tareas para los endpoints más pesados.
* **Redis** → Funciona como broker de mensajes y base de datos para almacenar el historial de chats.
* **Supabase** → Gestiona la autenticación y el registro de usuarios.
* **Gemini API (versión gratuita)** → Alimenta el bot conversacional y la generación automática de insights.

---

## 🗂️ Estructura del Proyecto

El proyecto se divide principalmente en dos carpetas:

### **app/**

Contiene toda la lógica central del sistema:

* Endpoints de FastAPI
* Conexiones con Redis
* Worker de Celery
* Integraciones con Gemini
* Manejo de tareas asíncronas y respuestas

### **datasets/**

Incluye:

* Archivos `.csv` con la información de prueba
* Módulos de análisis y extracción de métricas sobre los datos

---

## 🚀 Ejecución del Proyecto

1. **Crear el archivo `.env`** en la raíz del proyecto siguiendo el modelo de `.env.template`.
   Asegúrate de completar **todos los campos requeridos** antes de continuar.

2. **Verifica que Docker esté instalado** en tu máquina.

3. Desde la terminal, en la carpeta base del proyecto, ejecuta:

   ```bash
   docker compose up --build
   ```

   Si todo está configurado correctamente, el proyecto se construirá y desplegará exitosamente.

---

## 🧪 Pruebas y Uso

Se recomienda usar **Postman** para interactuar con los endpoints disponibles.

> ⚠️ La mayoría de los endpoints requieren un usuario autenticado.
> Regístrate e inicia sesión para obtener un `access_token` válido.

### **Interacción con el bot**

**Endpoint:**

```
POST /ask_bot_custom_query
```

**Cuerpo del request (JSON):**

```json
{
  "message": "Tu pregunta o solicitud aquí"
}
```

La respuesta incluirá un `task_id`.

#### **Generación de insights automáticos**

Endpoint:

```
POST /generate_insights
```

Este endpoint genera y retorna insights automáticos sobre los conjuntos de datos proporcionados.
Requiere un Bearer Token para autenticación.

Requiere autenticación:
Incluye el token de acceso en el encabezado:

Authorization: Bearer <access_token>


Formato de respuesta (JSON):

```JSON
{
  "result": {
    "title": "Automatic Insights",
    "analysis": "<contenido>",
    "raw_insights": "<contenido>",
    "orders_summary": "<contenido>",
    "metrics_summary": "<contenido>",
    "insights_file_path": "<contenido>",
    "generated_at": "<contenido>"
  }
}
```

### **Consultar la respuestas de tareas**

**Endpoint:**

```
GET /task/{task_id}
```

Reemplaza `{task_id}` con el valor retornado en la llamada anterior.

---

### **Historial de conversación**

**Endpoint:**

```
GET /conversation/history
```

**Requiere autenticación:**
Incluye el token de acceso en el encabezado:

```
Authorization: Bearer <access_token>
```
---

Nota: Para mayor conveniencia dentro de la carpeta principal se puede encontrar el archivo **Rappi.postman_collection.json**. Este contiene la colección de peticiones necesarias para probar la funcionalidad del proyecto.

---

## 🧩 Resumen

| Componente     | Función Principal                            |
| -------------- | -------------------------------------------- |
| **FastAPI**    | Manejo de endpoints REST                     |
| **Celery**     | Ejecución de tareas asíncronas               |
| **Redis**      | Broker y almacenamiento de historial         |
| **Supabase**   | Autenticación de usuarios                    |
| **Gemini API** | Motor de generación de insights y respuestas |

---
