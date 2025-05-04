# **Project Name**: Minimart API

## Description

A **Django Rest Framework** project that serves as a backend API for managing customers, orders, and product for the **Minimart** application. This project supports **CRUD operations**.It's simple mini e-commerce project like it's name MiniMart. It use basic logic, general and simple logical implementation of e-commerce backend system. Customer will search or looks products , and order it.

---
## 📌 API Documentation

Access the full API collection and test endpoints here:

🔗 [API Documentation](https://documenter.getpostman.com/view/31743247/2sB2j68paz)  


## 🚀 **Installation**

### Requirements:

* Python 3.x
* Django 3.x+
* Django Rest Framework
* Gunicorn (for production)

### 1. **Clone the repository:**

```bash
git clone https://github.com/RahulRajeev-0/minimart-project.git
cd minimart-project
```

### 2. **Create a virtual environment:**

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

### 4. **Set up the environment variables:**

Create a `.env` file in the project root and add the necessary environment variables:

```env
DJANGO_ENVIRONMENT=development # or production
DJANGO_SECRET_KEY=<your-secret-key> 
# below for production 
DB_NAME=database-name
DB_USER=database-username
DB_PASSWORD=database-password
DB_HOST=database-url # or Endpoint (awds rds)
DB_PORT=5432
ALLOWED_HOSTS=* 
```

### 5. **Run migrations:**

```bash
python manage.py migrate
```

### 6. **Run the development server:**

```bash
python manage.py runserver
```

Now the app is running locally at `http://127.0.0.1:8000/`.

---

## 🧑‍💻 **Testing**

Use **Postman** to test the endpoints with the following steps:

1. Use the proper HTTP method (GET, POST, PUT, DELETE).
2. Check the status code, and the response body.

---

## ⚙️ **Production Setup with Nginx + Gunicorn**

1. **Install Gunicorn:**

```bash
pip install gunicorn
```

2. **Run Gunicorn:**

```bash
gunicorn --workers 3 minimart.wsgi:application
```

3. **Configure Nginx** to reverse proxy to Gunicorn (refer to your existing Nginx setup).

4. **SSL with Let's Encrypt:**

* Use **Certbot** to set up SSL for your domain.

---

## 🧰 **Tools and Libraries**

* **Django**: 3.x+
* **Django Rest Framework**: For building the RESTful API.
* **Gunicorn**: For running the app in production.
* **Nginx**: As a reverse proxy server.
* **Certbot**: For handling SSL certificates.
* **Postman**: For testing API endpoints.

---



### 🏁 **Next Steps** (Optional)

* Add additional features like user authentication.
* Write automated tests for the API endpoints.
* Improve error handling and validation.
* Set up logging.

---

