# 🧠 Technical Case: Intelligent Analysis System for Rappi Operations

This project implements a **Data Conversational Bot** and an **Automatic Insights System** based on a predefined dataset.

---

## ⚙️ Technologies and Architecture

The project was developed in **Python** and runs within a **Dockerized environment**.
Below is a summary of the main components:

* **FastAPI** → Defines the main endpoints to interact with the system's functionalities.
* **Celery** → Manages the task queue for heavy endpoints.
* **Redis** → Serves as a message broker and database for storing chat history.
* **Supabase** → Handles user authentication and registration.
* **Gemini API (free version)** → Powers the conversational bot and automatic insights generation.

---

## 🗂️ Project Structure

The project is mainly divided into two folders:

### **app/**

Contains the system’s core logic:

* FastAPI endpoints
* Redis connections
* Celery worker
* Gemini integrations
* Asynchronous task management and responses

### **datasets/**

Includes:

* `.csv` files with test data
* Python modules for performing analysis and extracting metrics from the datasets

---

## 🚀 Running the Project

1. **Create the `.env` file** in the project root following the `.env.template` model.
   Make sure to fill out **all required fields** before proceeding.

2. **Verify that Docker is installed** on your machine.

3. From the terminal, in the project root directory, run:

   ```bash
   docker compose up --build
   ```

   If everything is set up correctly, the project should build and launch successfully.

---

## 🧪 Testing and Usage

It is recommended to use **Postman** to interact with the available endpoints.

> ⚠️ Most endpoints require an authenticated user.
> Register and log in to obtain a valid `access_token`.

### **Interacting with the Bot**

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

### **Retrieve the Bot’s Response**

**Endpoint:**

```
GET /task/{task_id}
```

Replace `{task_id}` with the value returned in the previous request.

---

### **Conversation History**

**Endpoint:**

```
GET /conversation/history
```

**Requires authentication:**
Include the access token in the request header:

```
Authorization: Bearer <access_token>
```

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