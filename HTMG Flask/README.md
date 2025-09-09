# 🏨 Hotel Management API

[![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-v2.3+-green.svg)](https://flask.palletsprojects.com/)
[![API Docs](https://img.shields.io/badge/API-Swagger-orange.svg)](http://localhost:5001/)

> Professional REST API for hotel management with smart booking system, built with Flask and SQLAlchemy.

## 🚀 Quick Start

```bash
# Clone the repository
git clone <your-repo-url>
cd "HTMG Flask"

# Setup environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
py app.py

# Access API
# Base URL: http://localhost:5001/api
# Documentation: http://localhost:5001/api/docs
```

## 📡 API Overview

### **Core Endpoints**

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/guests/guests` | Create new guest |
| `GET` | `/api/guests/guests` | List all guests |
| `POST` | `/api/rooms/rooms` | Create new room |
| `GET` | `/api/rooms/rooms?status=available` | List rooms (with filter) |
| `POST` | `/api/staff/staff` | Create staff member |
| `GET` | `/api/staff/staff?department=housekeeping` | List staff (with filter) |
| `POST` | `/api/reservations/reservations` | Book a room |
| `GET` | `/api/reservations/reservations` | List all reservations |
| `GET` | `/api/reservations/guest/{id}` | Get guest reservations |

### **Response Format**
```json
{
  "message": "Operation result",
  "status_code": 1,  // 1=Success, 2=Error
  "data": { ... }    // Response data
}
```

## ✨ Key Features

- 🏠 **Smart Room Management** - Availability checking with conflict prevention
- 👥 **Guest Management** - Email validation and unique constraints
- 👨‍💼 **Staff Organization** - Department-based filtering (housekeeping, front_desk, maintenance)
- 🏨 **Intelligent Booking** - Automatic date validation and overlap detection
- 📝 **Auto Documentation** - Interactive Swagger UI
- 🛡️ **Professional Validation** - Comprehensive error handling


## 🏗️ Architecture

### **Database Models**
- **Guest** - `id, name, email, created_at`
- **Room** - `id, room_number, room_type, status, created_at`
- **Staff** - `id, name, email, department, position, created_at`
- **Reservation** - `id, guest_id, room_id, check_in, check_out, status, created_at`

### **Project Structure**
```
HTMG Flask/
├── app.py                 # Application entry point
├── api_server.py          # Flask app configuration
├── config.py              # Configuration settings
├── requirements.txt       # Dependencies
├── models/                # Database models
│   ├── guests.py         # Guest model & logic
│   ├── rooms.py          # Room model with availability
│   ├── staff.py          # Staff model
│   └── reservations.py   # Smart booking logic
└── apis/                  # API routes
    ├── guest_routes.py   # Guest endpoints
    ├── room_routes.py    # Room endpoints
    ├── staff_routes.py   # Staff endpoints
    └── reservation_routes.py # Reservation endpoints
```

## 🧠 Smart Business Logic

### **Conflict Prevention**
- ✅ Prevents double-booking of rooms
- ✅ Validates date ranges (no past dates)
- ✅ Checks room availability in real-time
- ✅ Handles overlapping reservation detection

### **Data Validation**
- ✅ Email format validation
- ✅ Unique constraints (email, room numbers)
- ✅ Enum validation (room types, departments)
- ✅ Foreign key relationship validation

## 🛠️ Technology Stack

- **Flask + Flask-RESTX** - REST API with auto-documentation
- **SQLAlchemy** - ORM with relationship management
- **SQLite** - Database (production-ready for PostgreSQL)
- **Python 3.8+** - Backend language

## 📋 Requirements

- Python 3.8+
- pip (package manager)
- Virtual environment (recommended)

## 🎯 Features Highlights

✅ **Professional API Design** - RESTful endpoints with consistent responses  
✅ **Smart Booking System** - Automatic conflict detection and prevention  
✅ **Clean Architecture** - Separated models, routes, and business logic  
✅ **Interactive Documentation** - Auto-generated Swagger UI  
✅ **Production Ready** - Error handling, validation, and logging  
✅ **Extensible Design** - Easy to add new features and integrations  

---

**Perfect for demonstrating modern API development skills!** 🚀
