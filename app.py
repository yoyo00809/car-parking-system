from flask import Flask, render_template, request, redirect, session
import sqlite3
from datetime import datetime
import re

app = Flask(__name__)
app.secret_key = 'secret123'

TOTAL_SLOTS = 11

# 💰 PRICING CONFIG (EDIT HERE ANYTIME)
PRICE_2W = 20
PRICE_4W = 40

# 🔥 INIT DB
def init_db():
    conn = sqlite3.connect('parking.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS parking (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vehicle_no TEXT,
        vehicle_type TEXT,
        entry_time TEXT,
        exit_time TEXT,
        status TEXT,
        slot_no INTEGER
    )''')
    conn.commit()
    conn.close()

init_db()

# 🔐 LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect('/')

    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == '1234':
            session['user'] = 'admin'
            return redirect('/')
        else:
            return render_template('message.html', message="Invalid Login!")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# 🏠 DASHBOARD
@app.route('/')
def index():
    if 'user' not in session:
        return redirect('/login')

    conn = sqlite3.connect('parking.db')
    c = conn.cursor()

    c.execute("SELECT slot_no FROM parking WHERE status='IN'")
    occupied_slots = [row[0] for row in c.fetchall()]

    conn.close()

    return render_template(
        'index.html',
        total=TOTAL_SLOTS,
        available=TOTAL_SLOTS - len(occupied_slots),
        occupied=len(occupied_slots),
        occupied_slots=occupied_slots
    )

# 🚘 ENTRY
@app.route('/entry', methods=['GET', 'POST'])
def entry():
    if 'user' not in session:
        return redirect('/login')

    if request.method == 'POST':
        vehicle = request.form['vehicle_no'].upper()
        v_type = request.form['vehicle_type']
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        pattern = r'^[A-Z]{2}[0-9]{2}[A-Z]{2}[0-9]{4}$'
        if not re.match(pattern, vehicle):
            return render_template('message.html', message="Invalid Vehicle Number!")

        conn = sqlite3.connect('parking.db')
        c = conn.cursor()

        c.execute("SELECT * FROM parking WHERE vehicle_no=? AND status='IN'", (vehicle,))
        if c.fetchone():
            conn.close()
            return render_template('message.html', message="Vehicle already inside!")

        c.execute("SELECT COUNT(*) FROM parking WHERE status='IN'")
        slot_no = c.fetchone()[0] + 1

        if slot_no > TOTAL_SLOTS:
            conn.close()
            return render_template('message.html', message="Parking Full!")

        c.execute("""
            INSERT INTO parking (vehicle_no, vehicle_type, entry_time, status, slot_no)
            VALUES (?, ?, ?, ?, ?)
        """, (vehicle, v_type, time, 'IN', slot_no))

        conn.commit()
        conn.close()

        return render_template('message.html', message=f"Vehicle Parked at Slot {slot_no}")

    return render_template('entry.html')

# 🚪 EXIT
@app.route('/exit', methods=['GET', 'POST'])
def exit_vehicle():
    if 'user' not in session:
        return redirect('/login')

    if request.method == 'POST':
        vehicle = request.form['vehicle_no'].upper()
        exit_time = datetime.now()

        conn = sqlite3.connect('parking.db')
        c = conn.cursor()

        c.execute("""
            SELECT id, entry_time, vehicle_type FROM parking
            WHERE vehicle_no=? AND status='IN'
            ORDER BY id DESC LIMIT 1
        """, (vehicle,))
        data = c.fetchone()

        if data:
            record_id = data[0]
            entry_time = datetime.strptime(data[1], "%Y-%m-%d %H:%M:%S")
            v_type = data[2]

            hours = (exit_time - entry_time).seconds // 3600 + 1

            # 💰 DIFFERENT PRICING
            if v_type == '2':
                rate = PRICE_2W
            else:
                rate = PRICE_4W

            bill = hours * rate

            c.execute("""
                UPDATE parking
                SET exit_time=?, status='OUT'
                WHERE id=?
            """, (exit_time.strftime("%Y-%m-%d %H:%M:%S"), record_id))

            conn.commit()
            conn.close()

            return render_template(
                'receipt.html',
                vehicle=vehicle,
                entry=entry_time.strftime("%Y-%m-%d %H:%M:%S"),
                exit=exit_time.strftime("%Y-%m-%d %H:%M:%S"),
                hours=hours,
                bill=bill,
                vehicle_type=v_type
            )

        else:
            conn.close()
            return render_template('message.html', message="Vehicle not found!")

    return render_template('exit.html')

# 📊 VIEW
@app.route('/view')
def view():
    if 'user' not in session:
        return redirect('/login')

    conn = sqlite3.connect('parking.db')
    c = conn.cursor()
    c.execute("SELECT * FROM parking")
    data = c.fetchall()
    conn.close()

    return render_template('view.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)