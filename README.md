# CRM System - Django

## 🚀 Setup Instructions

### 1. Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Migrations
```bash
python manage.py migrate
```

### 4. Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

### 5. Run Server
```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000

---

## 📁 Project Structure (Step by Step)
```
crm_project/
├── crm_project/        ← Django config (settings, urls)
├── accounts/           ← Login, User Roles (Step 1)
├── customers/          ← Customer Management (Step 2)
├── leads/              ← Lead Management (Step 3)
├── sales/              ← Sales Pipeline (Step 4)
├── interactions/       ← Interaction History (Step 5)
├── tasks/              ← Task & Follow-up (Step 6)
├── support/            ← Support & Complaints (Step 7)
├── reports/            ← Dashboard & Reports (Step 8)
├── templates/          ← HTML Templates
├── static/             ← CSS, JS, Images
├── manage.py
└── requirements.txt
```

## 👥 User Roles
- **Admin** - Full access
- **Sales Staff** - Leads, Opportunities, Interactions, Tasks
- **Customer Service** - Support tickets, Complaints
