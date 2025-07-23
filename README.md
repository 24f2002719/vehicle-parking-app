#  MAD 1 PROJECT -🚗 VEHICLE PRAKING APP


This is a **Four-Wheeler Vehicle Parking Management Web Application** built using **Flask**. It enables users to register, log in, view available parking lots, reserve parking spots, and view booking history. Admins can manage users, roles, and parking lot capacities.

It also features a **visual summary dashboard using Chart.js** to track parking statistics like available spots, reservations over time, and revenue insights.

---

## 🌟 Features


✅ User registration 
✅ Role-based access (Admin / User)  
✅ Add & manage parking lots and spots  
✅ Reserve parking spot with cost and timestamps  
✅ Visual charts using Chart.js (e.g., spots availability, booking trends)  
✅ Clean, modular Flask Blueprint structure  
✅ SQLAlchemy ORM with database relationships  

---

## 🧰 Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS,JavaScript, Jinja2, Chart.js
- **ORM**: SQLAlchemy
- **Database**: SQLite (default, can be replaced with PostgreSQL or MySQL)
- **Environment Config**: `.env` file

---

## 📊 Chart.js Dashboard

The app includes a dashboard that uses **Chart.js** to show:

- 📌 Bar graph for Parking spot count  
- 💰 Revenue generated from reservations  
- 📍 Spots Availability

Charts are dynamically rendered from real-time backend data.

---

## 🗃️ Project Structure

```bash
├── controller/
│ ├── auth_routes.py # User authentication and role logic
│ ├── config.py # Flask and DB configurations
│ ├── database.py # SQLAlchemy db instance
│ └── routes.py # Core route handlers and views
├── instance/
├── models/ # Database models (User, Role, ParkingLot, etc.)
├── static/ images for background
├── templates/ # HTML templates
├── main.py # App entry point
├── .env # Environment variables
├── .gitignore
├── README.md
└── requirements.txt
```


---


## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/vehicle-parking-app.git
cd vehicle-parking-app
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv\scripts\activate  
```

### 3.Install Dependencies
```bash
pip install -r requirements.txt
```


### 4. Configure .env
```bash
FLASK_APP=main.py
FLASK_ENV=development
SECRET_KEY=your-secret-key
SQLALCHEMY_DATABASE_URI=sqlite:///instance/parking.db
SQLALCHEMY_TRACK_MODIFICATIONS=False
```

### 5. Run command
```bash
python main.py
```
Then access at - http://127.0.0.1:5000






