🎫 AI-Powered Customer Support Ticket Management System

> An intelligent customer support platform that automates ticket categorization, priority prediction, and agent assignment using Machine Learning.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Framework-black?logo=flask)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-ML-orange?logo=scikitlearn)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite)
![Render](https://img.shields.io/badge/Render-Deployed-46E3B7?logo=render)

---

## 📌 Project Overview

Customer support teams often receive hundreds of tickets every day. Manually categorizing, prioritizing, and assigning these tickets increases response time and operational cost.

This project automates the ticket management process using Machine Learning by:

- Predicting ticket category
- Predicting ticket priority
- Automatically assigning tickets
- Tracking ticket status
- Providing dashboard analytics for administrators

The result is a faster, more organized, and scalable support workflow.

---

## 🚀 Live Demo

**Live Application**

> https://ticket-routing-system.onrender.com/

---

## ✨ Features

### 👤 User Module

- User Registration
- Secure Login
- Raise Support Ticket
- View Submitted Tickets
- Track Ticket Status

---

### 🛠 Admin Module

- Dashboard Analytics
- View All Tickets
- Update Ticket Status
- Manage Ticket Lifecycle
- Monitor Ticket History

---

### 🤖 AI Features

- Automatic Ticket Categorization
- Priority Prediction
- Intelligent Agent Assignment
- Real-time ML Prediction
- Text Classification using NLP

---

## 🧠 Machine Learning Pipeline

Customer Ticket

↓

Text Preprocessing

↓

TF-IDF Vectorization

↓

Logistic Regression Model

↓

Predict Category

↓

Predict Priority

↓

Assign Agent

↓

Store in Database

---

## 🏗 System Architecture

```text
                   Customer

                       │

                       ▼

              HTML / CSS / JavaScript

                       │

                 HTTP Request

                       │

                       ▼

                Flask Backend APIs

          ┌──────────┴───────────┐

          ▼                      ▼

Machine Learning Model      SQLite Database

          │                      │

          └──────────┬───────────┘

                     ▼

             JSON Response

                     │

                     ▼

              User Dashboard
```

---

## 🛠 Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Core Programming Language |
| Flask | Backend Framework |
| HTML | User Interface |
| CSS | Styling |
| JavaScript | Client-side Interaction |
| SQLite | Database |
| Pandas | Data Processing |
| NumPy | Numerical Operations |
| Scikit-Learn | Machine Learning |
| TF-IDF | Feature Extraction |
| Logistic Regression | Classification Model |
| Joblib | Model Serialization |
| Render | Deployment |

---

## 📂 Project Structure

```
AI-Ticket-System/

│

├── app.py

├── database.py

├── model/

│ ├── category_model.pkl

│ ├── priority_model.pkl

│ ├── vectorizer.pkl

│

├── templates/

├── static/

├── dataset/

├── requirements.txt

├── README.md

└── ...
```

---

## 🗄 Database Schema

### Users

| Field |
|------|
| id |
| username |
| email |
| password |
| role |

---

### Tickets

| Field |
|------|
| id |
| name |
| email |
| subject |
| description |
| category |
| priority |
| status |
| agent_assigned |
| created_at |
| resolved_at |

---

### Ticket History

| Field |
|------|
| id |
| ticket_id |
| status |
| timestamp |

---

## 🔄 Application Workflow

1. User logs into the system.
2. User submits a support ticket.
3. Ticket is sent to the Flask backend.
4. Machine Learning model preprocesses the text.
5. TF-IDF converts text into numerical vectors.
6. Logistic Regression predicts ticket category.
7. Priority is predicted.
8. Ticket is assigned to the appropriate agent.
9. Ticket details are stored in SQLite.
10. Admin manages ticket lifecycle.
11. User tracks ticket status.

---

## 📊 Machine Learning Details

### Algorithm Used

- Logistic Regression

### Feature Extraction

- TF-IDF Vectorizer

### NLP Techniques

- Text Cleaning
- Tokenization
- TF-IDF Transformation

---

## 🔌 APIs

| Method | Endpoint | Purpose |
|---------|----------|----------|
| POST | /login | User Login |
| POST | /signup | Register User |
| POST | /submit_ticket | Raise Ticket |
| GET | /tickets | Fetch Tickets |
| PUT | /update_ticket | Update Status |
| GET | /dashboard | Dashboard Analytics |

---

## 📈 Future Improvements

- Email OTP Verification
- Password Hashing
- JWT Authentication
- MySQL/PostgreSQL Integration
- AI Chatbot Support
- BERT-based NLP Model
- Multi-language Ticket Classification
- Email Notifications
- Cloud Database
- Redis Caching
- Docker Deployment

---

## ⚠ Current Limitations

- SQLite is suitable only for small-scale deployment.
- OTP verification is currently hardcoded.
- Password hashing is not implemented.
- ML model performance depends on training data quality.
- Uses Logistic Regression instead of transformer-based NLP models.

---

## 📸 Screenshots

- Login Page

<img width="1903" height="907" alt="image" src="https://github.com/user-attachments/assets/f8fde566-6b74-4b63-94ca-b5be66c19324" />

- User Dashboard

  <img width="1893" height="902" alt="image" src="https://github.com/user-attachments/assets/77153258-b9bf-43b1-b33b-07e7fd369c11" />

- Ticket Submission

  <img width="1867" height="910" alt="image" src="https://github.com/user-attachments/assets/a08b6715-b895-464a-88a3-6e2ca50c0c72" />

- Admin Dashboard

  <img width="1872" height="877" alt="image" src="https://github.com/user-attachments/assets/5d9eb076-009b-41d1-b55c-089d6b29427d" />


- Analytics Dashboard

  <img width="1857" height="912" alt="image" src="https://github.com/user-attachments/assets/d5a8138d-ac9d-4811-b890-4888ee4433af" />


## 💡 Learning Outcomes

Through this project I gained practical experience in:

- Machine Learning Model Development
- Natural Language Processing
- Flask Backend Development
- REST API Design
- SQLite Database Design
- CRUD Operations
- Model Deployment
- Debugging
- End-to-End Project Integration
- Deployment using Render

---

## 🎯 Why This Project?

The project demonstrates how Machine Learning can automate customer support operations by reducing manual effort, improving ticket routing, and enabling faster issue resolution.
