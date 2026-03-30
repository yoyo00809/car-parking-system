# 🚗 Car Parking System

A web-based **Car Parking Management System** built using **Flask (Python)**.  
This system helps manage vehicle entry, exit, parking slots, and billing efficiently.

---

## 📌 Features

- 🔐 Admin Login System
- 🚘 Vehicle Entry & Exit
- 🅿️ Parking Slot Management (Limited Slots)
- 💰 Automatic Bill Calculation
- 🧾 Receipt Generation
- 📊 View Parking Records
- 🚫 Prevent Duplicate Active Entries
- 🎨 Clean and Modern UI

---

## 🛠️ Tech Stack

- **Frontend:** HTML, CSS  
- **Backend:** Python (Flask)  
- **Database:** SQLite  
- **Version Control:** Git & GitHub  

---

## 📂 Project Structure
Perfect 👌 — everything looks great, only one small mistake in README formatting

🚨 WHY PROJECT STRUCTURE IS NOT SHOWING

👉 Problem: You used this:

``` id="something"

👉 GitHub does NOT support id="" inside code blocks ❌
That breaks formatting

✅ FIX (VERY SIMPLE)

👉 Replace your project structure section with this:

## 📂 Project Structure


car_parking_system/
│
├── app.py
├── parking.db
├── templates/
│ ├── index.html
│ ├── entry.html
│ ├── exit.html
│ ├── view.html
│ ├── login.html
│ ├── message.html
│ ├── receipt.html
│
├── static/
│ └── style.css
│
├── .gitignore
└── README.md