# 🧠 Technical Case: Intelligent Analysis System for Rappi Operations

This project implements a **Data Conversational Bot** and an **Automatic Insights System** based on a predefined dataset.

---

## ⚙️ Technologies and Architecture

The project was developed in **Python** and runs within a **Dockerized environment**.
Below is a summary of the system’s main components:

* **FastAPI** → Defines the main endpoints to interact with the system’s functionalities.
* **Celery** → Manages the task queue for heavy or long-running endpoints.
* **Redis** → Serves as a message broker and database for storing chat history.
* **Supabase** → Handles user authentication and registration.
* **Gemini API (free version)** → Powers the conversational bot and the automatic insight generation.

---

## 🗂️ Project Structure

The project is mainly divided into two folders:

### **app/**

Contains the system’s core logic:

* FastAPI endpoints
* Redis connections
* Celery worker
* Gemini integrations
* Asynchronous task handling and response management

### **datasets/**

Includes:

* `.csv` files with sample data
* Python modules for performing analysis and extracting metrics from the datasets

---

## 🚀 Running the Project

1. **Create the `.env` file** in the project root following the `.env.template` model.
   Make sure to fill in **all required fields** before proceeding.

2. **Ensure that Docker is installed** on your machine.

3. From the terminal, at the project root, run:

   ```bash
   docker compose up --build
   ```

   If everything is configured correctly, the project should build and launch successfully.

---

## 🧪 Testing and Usage

It is recommended to use **Postman** to interact with the available endpoints.

> ⚠️ Most endpoints require an authenticated user.
> Register and log in to obtain a valid `access_token`.

### **Bot Interaction**

**Endpoint:**

```
POST /ask_bot_custom_query
```

**Request body (JSON):**

```json
{
  "message": "Your question or request here"
}
```

The response will include a `task_id`.

---

### **Automatic Insights Generation**

**Endpoint:**

```
POST /generate_insights
```

This endpoint generates and returns **automatic insights** based on the provided datasets.
A **Bearer Token** is required for authentication.

**Authentication required:**
Include the access token in the header:

```
Authorization: Bearer <access_token>
```

**Response format (JSON):**

```json
{
  "result": {
    "title": "Automatic Insights",
    "analysis": "<content>",
    "raw_insights": "<content>",
    "orders_summary": "<content>",
    "metrics_summary": "<content>",
    "insights_file_path": "<content>",
    "generated_at": "<content>"
  }
}
```

---

### **Retrieve Task Responses**

**Endpoint:**

```
GET /task/{task_id}
```

Replace `{task_id}` with the value returned in the previous call.

---

### **Conversation History**

**Endpoint:**

```
GET /conversation/history
```

**Authentication required:**
Include the access token in the header:

```
Authorization: Bearer <access_token>
```

---

Note: For convenience, within the main folder you can find the file Rappi.postman_collection.json. This file contains the collection of requests needed to test the project’s functionality.

---

## 🧩 Summary

| Component      | Main Function                                |
| -------------- | -------------------------------------------- |
| **FastAPI**    | Handles REST endpoints                       |
| **Celery**     | Executes asynchronous tasks                  |
| **Redis**      | Message broker and chat history storage      |
| **Supabase**   | User authentication and management           |
| **Gemini API** | Insight generation and conversational engine |

---
