from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import re

app = Flask(__name__)
app.secret_key = 'lifeconnect_secret_key_2024'

# MySQL Configuration - Update these with your MySQL Workbench credentials
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Your Password'  # Change this
app.config['MYSQL_DB'] = 'lifeconnect'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# ── Login Required Decorator ──────────────────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to continue.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

# ── Home ──────────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) as count FROM donors WHERE is_available=1")
    donors_count = cur.fetchone()['count']
    cur.execute("SELECT COUNT(*) as count FROM blood_requests WHERE status='open'")
    requests_count = cur.fetchone()['count']
    cur.execute("SELECT COUNT(*) as count FROM users")
    users_count = cur.fetchone()['count']
    cur.close()
    return render_template('index.html', donors_count=donors_count,
                           requests_count=requests_count, users_count=users_count)

# ── Register ──────────────────────────────────────────────────────────────────
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name     = request.form['name'].strip()
        email    = request.form['email'].strip()
        password = request.form['password']
        phone    = request.form['phone'].strip()

        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address.', 'danger')
            return redirect(url_for('register'))

        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM users WHERE email=%s", (email,))
        if cur.fetchone():
            flash('Email already registered.', 'danger')
            cur.close()
            return redirect(url_for('register'))

        hashed = generate_password_hash(password)
        cur.execute("INSERT INTO users (name, email, password, phone) VALUES (%s,%s,%s,%s)",
                    (name, email, hashed, phone))
        mysql.connection.commit()
        cur.close()
        flash('Account created! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

# ── Login ─────────────────────────────────────────────────────────────────────
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form['email'].strip()
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cur.fetchone()
        cur.close()
        if user and check_password_hash(user['password'], password):
            session['user_id']   = user['id']
            session['user_name'] = user['name']
            flash(f"Welcome back, {user['name']}!", 'success')
            return redirect(url_for('dashboard'))
        flash('Invalid email or password.', 'danger')
    return render_template('login.html')

# ── Logout ────────────────────────────────────────────────────────────────────
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

# ── Dashboard ─────────────────────────────────────────────────────────────────
@app.route('/dashboard')
@login_required
def dashboard():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM donors WHERE user_id=%s", (session['user_id'],))
    donor_profile = cur.fetchone()
    cur.execute("SELECT * FROM blood_requests WHERE user_id=%s ORDER BY created_at DESC LIMIT 5",
                (session['user_id'],))
    my_requests = cur.fetchall()
    cur.execute("SELECT COUNT(*) as c FROM blood_requests WHERE status='open'")
    open_req = cur.fetchone()['c']
    cur.execute("SELECT COUNT(*) as c FROM donors WHERE is_available=1")
    avail_donors = cur.fetchone()['c']
    cur.close()
    return render_template('dashboard.html', donor_profile=donor_profile,
                           my_requests=my_requests, open_req=open_req,
                           avail_donors=avail_donors)

# ── Register as Donor ─────────────────────────────────────────────────────────
@app.route('/become-donor', methods=['GET', 'POST'])
@login_required
def become_donor():
    if request.method == 'POST':
        blood_group = request.form['blood_group']
        city        = request.form['city'].strip()
        state       = request.form['state'].strip()
        age         = request.form['age']
        gender      = request.form['gender']
        last_donated = request.form.get('last_donated') or None

        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM donors WHERE user_id=%s", (session['user_id'],))
        if cur.fetchone():
            cur.execute("""UPDATE donors SET blood_group=%s, city=%s, state=%s,
                           age=%s, gender=%s, last_donated=%s, is_available=1
                           WHERE user_id=%s""",
                        (blood_group, city, state, age, gender, last_donated, session['user_id']))
            flash('Donor profile updated!', 'success')
        else:
            cur.execute("""INSERT INTO donors (user_id, blood_group, city, state, age, gender, last_donated)
                           VALUES (%s,%s,%s,%s,%s,%s,%s)""",
                        (session['user_id'], blood_group, city, state, age, gender, last_donated))
            flash('You are now registered as a donor!', 'success')
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('dashboard'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM donors WHERE user_id=%s", (session['user_id'],))
    existing = cur.fetchone()
    cur.close()
    return render_template('become_donor.html', existing=existing)

# ── Find Donors ───────────────────────────────────────────────────────────────
@app.route('/find-donors', methods=['GET', 'POST'])
def find_donors():
    donors = []
    blood_group = city = ''
    if request.method == 'POST':
        blood_group = request.form.get('blood_group', '')
        city        = request.form.get('city', '').strip()
        query = """SELECT d.*, u.name, u.phone FROM donors d
                   JOIN users u ON d.user_id = u.id
                   WHERE d.is_available = 1"""
        params = []
        if blood_group:
            query += " AND d.blood_group = %s"
            params.append(blood_group)
        if city:
            query += " AND d.city LIKE %s"
            params.append(f'%{city}%')
        query += " ORDER BY d.created_at DESC"
        cur = mysql.connection.cursor()
        cur.execute(query, params)
        donors = cur.fetchall()
        cur.close()
    return render_template('find_donors.html', donors=donors,
                           blood_group=blood_group, city=city)

# ── Blood Requests ────────────────────────────────────────────────────────────
@app.route('/blood-requests')
def blood_requests():
    cur = mysql.connection.cursor()
    cur.execute("""SELECT r.*, u.name, u.phone FROM blood_requests r
                   JOIN users u ON r.user_id = u.id
                   WHERE r.status = 'open'
                   ORDER BY r.urgency DESC, r.created_at DESC""")
    requests = cur.fetchall()
    cur.close()
    return render_template('blood_requests.html', requests=requests)

# ── Create Request ────────────────────────────────────────────────────────────
@app.route('/create-request', methods=['GET', 'POST'])
@login_required
def create_request():
    if request.method == 'POST':
        blood_group = request.form['blood_group']
        units       = request.form['units']
        hospital    = request.form['hospital'].strip()
        city        = request.form['city'].strip()
        state       = request.form['state'].strip()
        urgency     = request.form['urgency']
        notes       = request.form.get('notes', '').strip()

        cur = mysql.connection.cursor()
        cur.execute("""INSERT INTO blood_requests
                       (user_id, blood_group, units_needed, hospital, city, state, urgency, notes)
                       VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
                    (session['user_id'], blood_group, units, hospital, city, state, urgency, notes))
        mysql.connection.commit()
        cur.close()
        flash('Blood request posted successfully!', 'success')
        return redirect(url_for('blood_requests'))
    return render_template('create_request.html')

# ── Close Request ─────────────────────────────────────────────────────────────
@app.route('/close-request/<int:req_id>')
@login_required
def close_request(req_id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE blood_requests SET status='fulfilled' WHERE id=%s AND user_id=%s",
                (req_id, session['user_id']))
    mysql.connection.commit()
    cur.close()
    flash('Request marked as fulfilled.', 'success')
    return redirect(url_for('dashboard'))

# ── Toggle Donor Availability ─────────────────────────────────────────────────
@app.route('/toggle-availability')
@login_required
def toggle_availability():
    cur = mysql.connection.cursor()
    cur.execute("SELECT is_available FROM donors WHERE user_id=%s", (session['user_id'],))
    donor = cur.fetchone()
    if donor:
        new_val = 0 if donor['is_available'] else 1
        cur.execute("UPDATE donors SET is_available=%s WHERE user_id=%s",
                    (new_val, session['user_id']))
        mysql.connection.commit()
        flash('Availability updated!', 'success')
    cur.close()
    return redirect(url_for('dashboard'))

# ── About ─────────────────────────────────────────────────────────────────────
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
