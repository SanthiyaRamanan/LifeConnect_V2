# 🩸 LifeConnect — Blood Donation Application

A full-stack blood donation platform connecting donors with recipients.
Built with **Python Flask**, **MySQL**, **HTML/CSS/JS**.

---

## 🛠 Tech Stack
| Layer      | Technology        |
|------------|-------------------|
| Frontend   | HTML5, CSS3, Vanilla JavaScript |
| Backend    | Python 3, Flask   |
| Database   | MySQL (MySQL Workbench) |
| Auth       | Werkzeug password hashing |

---

## ⚡ Setup Instructions

### 1. Clone / Extract the project
```
cd LifeConnect
```

### 2. Create a virtual environment
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

> **Note:** On some systems you may also need: `pip install mysqlclient`
> Windows users: download mysqlclient wheel from https://www.lfd.uci.edu/~gohlke/pythonlibs/

### 4. Setup MySQL Database
1. Open **MySQL Workbench**
2. Connect to your local MySQL server
3. Open and run `schema.sql`  
   *(File → Open SQL Script → select schema.sql → Execute ⚡)*

### 5. Configure Database Credentials
Open `app.py` and update:
```python
app.config['MYSQL_HOST']     = 'localhost'
app.config['MYSQL_USER']     = 'root'
app.config['MYSQL_PASSWORD'] = 'your_password'   # ← Change this
app.config['MYSQL_DB']       = 'lifeconnect'
```

### 6. Run the Application
```bash
python app.py
```
Open your browser at: **http://127.0.0.1:5000**

---

## 📋 Features
- ✅ User registration & secure login (hashed passwords)
- ✅ Register as a blood donor with blood group & location
- ✅ Search donors by blood group and city
- ✅ Post urgent blood requests (Normal / Urgent / Critical)
- ✅ Dashboard to manage profile and requests
- ✅ Toggle donor availability on/off
- ✅ Mark requests as fulfilled
- ✅ Responsive design (mobile-friendly)

## 📁 Project Structure
```
LifeConnect/
├── app.py              # Flask backend (routes, logic)
├── schema.sql          # MySQL database schema
├── requirements.txt    # Python dependencies
├── templates/          # Jinja2 HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── become_donor.html
│   ├── find_donors.html
│   ├── blood_requests.html
│   ├── create_request.html
│   └── about.html
└── static/
    ├── css/style.css   # All styles
    └── js/main.js      # Frontend JS
```

---

## 🔑 Resume Points
- Developed a full-stack blood donation web app using **Flask** and **MySQL**
- Implemented user authentication with **Werkzeug** password hashing
- Designed a relational database schema with 3 normalized tables
- Built responsive UI with HTML5/CSS3 and Vanilla JS animations
- Features include donor search, request management, and real-time dashboard
