# 🚀 DealRadar Backend

A scalable backend built with **FastAPI**, **SQLModel**, and **JWT Authentication** to manage users, sites, and orders with secure APIs.

---

## 🧠 Features

* 🔐 JWT Authentication (Login/Register)
* 👤 User Profile Management
* 📊 Dashboard (sites + orders count)
* 🌐 Add & Manage Websites
* 📦 Orders Management
* 🧱 Clean Architecture (modular structure)
* 🗄 SQLite Database (easy setup)

---

## 🏗️ Project Structure

```
app/
├── main.py
├── api/
│   ├── deps.py
│   ├── routes/
│       ├── auth.py
│       ├── dashboard.py
├── core/
│   ├── config.py
│   ├── security.py
│   ├── jwt.py
├── db/
│   ├── models.py
│   ├── session.py
├── schemas/
│   ├── user.py
│   ├── site.py
│   ├── order.py
│   ├── token.py
├── services/
│   ├── auth_service.py
```

---

## ⚙️ Tech Stack

* **FastAPI** – Web framework
* **SQLModel** – ORM
* **SQLite** – Database
* **JWT (PyJWT)** – Authentication
* **Pwdlib** – Password hashing

---

## 🔧 Setup & Installation

### 1. Clone the repo

```bash
git clone <your-repo-url>
cd dealradar-backend
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate   # (Linux/Mac)
venv\Scripts\activate      # (Windows)
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run server

```bash
uvicorn app.main:app --reload
```

---

## 🌐 API Endpoints

### 🔐 Authentication

#### Register

```
POST /register
```

**Body:**

```json
{
  "name": "John",
  "age": 21,
  "email": "john@example.com",
  "phone": "1234567890",
  "password": "password123"
}
```

---

#### Login (Get Token)

```
POST /login
```

**Form Data (x-www-form-urlencoded):**

```
username = email
password = your_password
```

**Response:**

```json
{
  "access_token": "...",
  "token_type": "bearer"
}
```

---

## 🔐 Protected Routes

👉 Add header:

```
Authorization: Bearer <your_token>
```

---

### 👤 Profile

```
GET /dashbord/profile
```

---

### 📊 Dashboard

```
GET /dashbord?page=1&limit=10
```

---

### 🌐 Sites

#### Get All Sites

```
GET /dashbord/viewsites
```

#### Add Site

```
POST /dashbord/addsites
```

**Body:**

```json
{
  "url": "https://example.com"
}
```

#### Delete Site

```
DELETE /dashbord/sites?id=1
```

---

### 📦 Orders

```
GET /dashbord/myorders
```

---

## 🔐 Authentication Flow

1. Register user
2. Login → receive JWT token
3. Store token (frontend)
4. Send token in headers for protected routes

---

## ⚠️ Common Errors

| Status Code | Meaning                     |
| ----------- | --------------------------- |
| 401         | Invalid credentials / token |
| 404         | Resource not found          |
| 409         | User already exists         |
| 422         | Validation error            |

---

## 🧠 Architecture

This project follows **Layered Architecture**:

* **Routes** → API layer
* **Core** → Security & config
* **DB** → Models & session
* **Schemas** → Validation

---

## 🚀 Future Improvements

* Refresh Tokens
* Role-Based Access Control
* PostgreSQL Integration
* Docker Support
* Rate Limiting

---

## 👨‍💻 Author

Built as a learning + production-ready backend project.

---

## ⭐ Tip

Use `/docs` to explore interactive API:

```
http://127.0.0.1:8000/docs
```
